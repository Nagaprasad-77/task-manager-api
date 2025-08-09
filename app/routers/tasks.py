from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app import models, schemas, database, auth
from app.utils import email  
from app.tasks.email import send_email_task

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# Create a task
@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    # Make sure project belongs to the user
    project = db.query(models.Project).filter(
        models.Project.id == task.project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    # Send assignment email if user assigned
    if task.assigned_to:
        assigned_user = db.query(models.User).filter(models.User.id == task.assigned_to).first()
        if assigned_user:
            send_email_task.delay(
                to_email=assigned_user.email,
                subject="You've been assigned a task",
                message=f"You've been assigned to task: {task.title}"
            )

    db.refresh(new_task)

    # Stub: send email when task assigned
    if new_task.assigned_user_id:
        email.send_task_assigned_email(db, new_task)

    return new_task

# List tasks with filters, sorting, pagination
@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
    status: Optional[schemas.TaskStatus] = None,
    priority: Optional[schemas.TaskPriority] = None,
    due_date: Optional[str] = None,
    project_id: Optional[int] = None,
    sort_by: Optional[str] = Query(None, regex="^(priority|due_date)$"),
    limit: int = 10,
    offset: int = 0
):
    query = db.query(models.Task).join(models.Project).filter(models.Project.owner_id == current_user.id)

    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if due_date:
        query = query.filter(models.Task.due_date == due_date)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    if sort_by:
        query = query.order_by(getattr(models.Task, sort_by))

    return query.offset(offset).limit(limit).all()

# Get task by ID (with project + assigned user)
@router.get("/{id}", response_model=schemas.TaskOut)
def get_task(id: int,
             db: Session = Depends(database.get_db),
             current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).options(
        joinedload(models.Task.project),
        joinedload(models.Task.assigned_user)
    ).join(models.Project).filter(
        models.Task.id == id,
        models.Project.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update task
@router.patch("/{id}", response_model=schemas.TaskOut)
def update_task(id: int,
                task_update: schemas.TaskUpdate,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == id,
        models.Project.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    original_status = task.status
    original_user = task.assigned_user_id

    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    if "status" in task_update.dict() and task_update.status != task.status:
        if task.assigned_to:
            assigned_user = db.query(models.User).filter(models.User.id == task.assigned_to).first()
            if assigned_user:
                send_email_task.delay(
                    to_email=assigned_user.email,
                    subject="Task status updated",
                    message=f"The status of task '{task.title}' has changed to {task_update.status}."
                )

    db.refresh(task)

    # Send email if assigned or status changed
    if (task.assigned_user_id != original_user or task.status != original_status) and task.assigned_user_id:
        email.send_task_update_email(db, task)

    return task

# Delete task
@router.delete("/{id}")
def delete_task(id: int,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == id,
        models.Project.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}

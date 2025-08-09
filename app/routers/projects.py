from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, auth
from typing import List

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

# Create a new project
@router.post("/", response_model=schemas.ProjectOut)
def create_project(project: schemas.ProjectCreate,
                   db: Session = Depends(database.get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    new_project = models.Project(
        title=project.title,
        description=project.description,
        owner_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# List all projects of the current user
@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Project).filter(models.Project.owner_id == current_user.id).all()

# Get project details by ID (with tasks)
@router.get("/{id}", response_model=schemas.ProjectOut)
def get_project(id: int,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    project = db.query(models.Project).filter(
        models.Project.id == id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Update project
@router.patch("/{id}", response_model=schemas.ProjectOut)
def update_project(id: int,
                   project_update: schemas.ProjectUpdate,
                   db: Session = Depends(database.get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    project = db.query(models.Project).filter(
        models.Project.id == id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for field, value in project_update.dict(exclude_unset=True).items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project

# Delete project
@router.delete("/{id}")
def delete_project(id: int,
                   db: Session = Depends(database.get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    project = db.query(models.Project).filter(
        models.Project.id == id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"detail": "Project deleted"}

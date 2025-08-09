from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from enum import Enum

# Enums must match model enums for status & priority
class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

# ----- USER SCHEMAS -----
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# ----- TASK SCHEMAS -----
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.todo
    priority: Optional[TaskPriority] = TaskPriority.medium
    due_date: Optional[date] = None
    project_id: int
    assigned_user_id: Optional[int]

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]
    due_date: Optional[date]
    assigned_user_id: Optional[int]

class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True

# ----- PROJECT SCHEMAS -----
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    tasks: List[TaskOut] = []

    class Config:
        orm_mode = True

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.crud import task as crud_task
from app.db.database import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

# ✅ Create Task
@router.post("/", response_model=Task)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_task.create_task(db, task, current_user.id)

# ✅ Get All Tasks for Current User
@router.get("/", response_model=List[Task])
def read_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_task.get_tasks_by_user(db, current_user.id)

# ✅ Get a Single Task by ID
@router.get("/{task_id}", response_model=Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = crud_task.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# ✅ Update a Task
@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = crud_task.update_task(db, task_id, task_data, current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return updated

# ✅ Delete a Task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = crud_task.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return

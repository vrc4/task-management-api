from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.task import Task as TaskModel
from app.schemas.task import TaskCreate, TaskUpdate

def create_task(db: Session, task: TaskCreate, owner_id: int) -> TaskModel:
    db_task = TaskModel(**task.model_dump(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_user(db: Session, owner_id: int) -> List[TaskModel]:
    return db.query(TaskModel).filter(TaskModel.owner_id == owner_id).all()

def get_task(db: Session, task_id: int, owner_id: int) -> Optional[TaskModel]:
    return (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id, TaskModel.owner_id == owner_id)
        .first()
    )

def update_task(db: Session, task_id: int, task_update: TaskUpdate, owner_id: int) -> Optional[TaskModel]:
    db_task = get_task(db, task_id, owner_id)
    if not db_task:
        return None
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, owner_id: int) -> bool:
    db_task = get_task(db, task_id, owner_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True

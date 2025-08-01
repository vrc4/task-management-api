from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "Finish the report"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Details about the report"})
    completed: bool = Field(default=False)

class TaskCreate(TaskBase):
    pass  # Inherits all fields from TaskBase for creating a task

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Task(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

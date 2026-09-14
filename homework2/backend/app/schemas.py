from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TaskCategory(str, Enum):
    AI_AUTOMATION = "AI Automation"
    DATA = "Data"
    INTERNAL_OPERATIONS = "Internal Operations"
    OTHER = "Other"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskStatus(str, Enum):
    INCOMING = "incoming"
    ANALYZING = "analyzing"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=500)
    category: TaskCategory
    priority: TaskPriority
    status: TaskStatus


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    category: TaskCategory | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None

    @model_validator(mode="after")
    def require_at_least_one_value(self):
        if not self.model_fields_set:
            raise ValueError("At least one field is required.")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Task fields cannot be null.")
        return self


class Task(TaskCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class TaskDeleteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detail: str

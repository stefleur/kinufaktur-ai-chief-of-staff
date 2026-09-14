from datetime import datetime, timezone
from uuid import uuid4

from .schemas import Task, TaskCreate, TaskUpdate


class InMemoryTaskStore:
    """Small replaceable data-access layer for the prototype."""

    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def clear(self) -> None:
        self._tasks.clear()

    def list(self) -> list[Task]:
        return [task.model_copy(deep=True) for task in self._tasks.values()]

    def get(self, task_id: str) -> Task | None:
        task = self._tasks.get(task_id)
        return task.model_copy(deep=True) if task else None

    def create(self, task_input: TaskCreate) -> Task:
        timestamp = datetime.now(timezone.utc)
        task = Task(
            id=str(uuid4()),
            **task_input.model_dump(),
            created_at=timestamp,
            updated_at=timestamp,
        )
        self._tasks[task.id] = task
        return task.model_copy(deep=True)

    def update(self, task_id: str, changes: TaskUpdate) -> Task | None:
        current_task = self._tasks.get(task_id)
        if current_task is None:
            return None

        updated_task = current_task.model_copy(
            update={
                **changes.model_dump(exclude_unset=True),
                "updated_at": datetime.now(timezone.utc),
            }
        )
        self._tasks[task_id] = updated_task
        return updated_task.model_copy(deep=True)

    def delete(self, task_id: str) -> bool:
        return self._tasks.pop(task_id, None) is not None


task_store = InMemoryTaskStore()

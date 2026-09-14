from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .schemas import ErrorResponse, Task, TaskCreate, TaskDeleteResponse, TaskUpdate
from .store import InMemoryTaskStore, task_store


app = FastAPI(
    title="KinuFlow API",
    version="1.0.0",
    description="REST API for the KinuFlow Mini Kanban Board.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_request, _exception):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": "Invalid task data."},
    )


def get_task_store() -> InMemoryTaskStore:
    return task_store


TaskStoreDependency = Annotated[InMemoryTaskStore, Depends(get_task_store)]


def require_task(task_id: str, store: InMemoryTaskStore) -> Task:
    task = store.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task


@app.get("/tasks", response_model=list[Task], tags=["Tasks"], operation_id="listTasks")
def list_tasks(store: TaskStoreDependency):
    return store.list()


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    operation_id="createTask",
    responses={
        422: {"model": ErrorResponse, "description": "Invalid task data."},
    },
)
def create_task(task_input: TaskCreate, store: TaskStoreDependency):
    return store.create(task_input)


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    operation_id="getTask",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found."},
    },
)
def get_task(task_id: str, store: TaskStoreDependency):
    return require_task(task_id, store)


@app.patch(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    operation_id="updateTask",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found."},
        422: {"model": ErrorResponse, "description": "Invalid task data."},
    },
)
def update_task(task_id: str, changes: TaskUpdate, store: TaskStoreDependency):
    task = store.update(task_id, changes)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task


@app.delete(
    "/tasks/{task_id}",
    response_model=TaskDeleteResponse,
    tags=["Tasks"],
    operation_id="deleteTask",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found."},
    },
)
def delete_task(task_id: str, store: TaskStoreDependency):
    if not store.delete(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return TaskDeleteResponse(id=task_id)

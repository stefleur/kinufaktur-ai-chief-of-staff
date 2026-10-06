from contextlib import asynccontextmanager
from typing import Annotated
import os

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .database import create_tables, get_db
from .schemas import ErrorResponse, Task, TaskCreate, TaskDeleteResponse, TaskUpdate
from .store import SqlAlchemyTaskStore, TaskStore


DatabaseSession = Annotated[Session, Depends(get_db)]


def get_task_store(database: DatabaseSession) -> TaskStore:
    return SqlAlchemyTaskStore(database)


TaskStoreDependency = Annotated[TaskStore, Depends(get_task_store)]


def require_task(task_id: str, store: TaskStore) -> Task:
    task = store.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task


def create_app(*, initialize_database: bool = True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        if initialize_database:
            create_tables()
        yield

    application = FastAPI(
        title="KinuFlow API",
        version="1.0.0",
        description="REST API for the KinuFlow Mini Kanban Board.",
        lifespan=lifespan,
    )

    # Configure CORS origins via environment variable for deployment.
    # Provide a sensible default for local dev.
    cors_env = os.getenv("KINUFLOW_CORS_ORIGINS")
    if cors_env:
        # Expect a comma-separated list of allowed origins.
        allow_origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
    else:
        allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(_request, _exception):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": "Invalid task data."},
        )

    application.add_api_route(
        "/tasks",
        list_tasks,
        methods=["GET"],
        response_model=list[Task],
        tags=["Tasks"],
        operation_id="listTasks",
    )
    application.add_api_route(
        "/tasks",
        create_task,
        methods=["POST"],
        response_model=Task,
        status_code=status.HTTP_201_CREATED,
        tags=["Tasks"],
        operation_id="createTask",
        responses={
            422: {"model": ErrorResponse, "description": "Invalid task data."},
        },
    )
    application.add_api_route(
        "/tasks/{task_id}",
        get_task,
        methods=["GET"],
        response_model=Task,
        tags=["Tasks"],
        operation_id="getTask",
        responses={
            404: {"model": ErrorResponse, "description": "Task not found."},
        },
    )
    application.add_api_route(
        "/tasks/{task_id}",
        update_task,
        methods=["PATCH"],
        response_model=Task,
        tags=["Tasks"],
        operation_id="updateTask",
        responses={
            404: {"model": ErrorResponse, "description": "Task not found."},
            422: {"model": ErrorResponse, "description": "Invalid task data."},
        },
    )
    application.add_api_route(
        "/tasks/{task_id}",
        delete_task,
        methods=["DELETE"],
        response_model=TaskDeleteResponse,
        tags=["Tasks"],
        operation_id="deleteTask",
        responses={
            404: {"model": ErrorResponse, "description": "Task not found."},
        },
    )
    return application


def list_tasks(store: TaskStoreDependency):
    return store.list()


def create_task(task_input: TaskCreate, store: TaskStoreDependency):
    return store.create(task_input)


def get_task(task_id: str, store: TaskStoreDependency):
    return require_task(task_id, store)


def update_task(task_id: str, changes: TaskUpdate, store: TaskStoreDependency):
    task = store.update(task_id, changes)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task


def delete_task(task_id: str, store: TaskStoreDependency):
    if not store.delete(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return TaskDeleteResponse(id=task_id)


app = create_app()

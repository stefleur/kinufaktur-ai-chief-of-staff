# KinuFlow Specification

## Overview

KinuFlow is a lightweight Mini Kanban Board for Kinufaktur.

It helps organize incoming business and customer requests and move them through a clear workflow.

## Target User

The primary user is the founder or operator of Kinufaktur.

## Workflow

Tasks move through the following stages:

1. Incoming
2. Analyzing
3. Planned
4. In Progress
5. Done

## Core Features

### View Kanban Board

The user can see tasks grouped by their current status.

Each card displays:

- Title
- Category
- Priority
- Short description

### Create Task

The user can create a new task with:

- Title
- Description
- Category
- Priority
- Status

### Update Task

The user can edit an existing task.

### Move Task

The user can change a task's status and move it through the workflow.

### Delete Task

The user can delete a task.

## Categories

- AI Automation
- Data
- Internal Operations
- Other

## Priorities

- Low
- Medium
- High

## Data Model

Task:

- id
- title
- description
- category
- priority
- status
- created_at
- updated_at

## Frontend

The frontend should be a modern web application.

All backend calls must be centralized in one API client module.

The current frontend uses HTTP through `frontend/src/api/tasksApi.js`. The original
prototype used mock data; that development stage is complete.

## Backend

The backend uses FastAPI and Pydantic validation, following `openapi.yaml`.

It should provide REST endpoints for:

- List tasks
- Create task
- Read one task
- Update task
- Delete task

## Database

The current backend uses SQLAlchemy behind a separate data-access layer. SQLite
is available for local development and isolated tests; Docker Compose and
production use PostgreSQL. Production is hosted on Neon.

## Out of Scope

The approved lean Final Project excludes:

- Authentication
- Multiple users
- AI API calls
- Autonomous agents
- CRM integrations
- Email integrations

## Final Project boundaries and acceptance

Use synthetic/demo data only. Keep the existing task workflow; do not add
accounts, multi-tenancy, payments, migrations, workers, queues, or new cloud
services. AI assists development, not application runtime. The historical root
Django application is outside this product.

The final demo must view tasks, create a synthetic task, edit its fields, move
its status, reload to confirm persistence, delete it, and reload to confirm
removal. Production remains GitHub Pages -> FastAPI Cloud -> Neon PostgreSQL.

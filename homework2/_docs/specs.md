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

For the first prototype, the API client should use mock data.

## Backend

The backend will use FastAPI.

It should provide REST endpoints for:

- List tasks
- Create task
- Read one task
- Update task
- Delete task

## Database

The first backend version should use a mock data store.

Later it will be replaced with SQLAlchemy and a real database.

## Out of Scope

Do not implement in the first version:

- Authentication
- Multiple users
- AI API calls
- Autonomous agents
- CRM integrations
- Email integrations

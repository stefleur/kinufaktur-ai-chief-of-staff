# Kinufaktur AI Chief of Staff

Homework project for the DataTalksClub AI Dev Tools Zoomcamp 2026.

The goal is to build an AI-powered internal assistant for Kinufaktur that helps organize business requests, classify them, and turn them into actionable work.

## Current MVP

The Django application supports:

- creating business requests;
- classifying requests as AI Automation, Data / Single Source of Truth, or Other;
- adding an action plan;
- moving requests through New, Reviewed, Planned, and Done;
- viewing all requests and individual request details.

## Local development

Install the locked dependencies:

```bash
uv sync
```

Apply database migrations:

```bash
uv run python manage.py migrate
```

Start the development server:

```bash
uv run python manage.py runserver
```

Run the test suite:

```bash
uv run python manage.py test
```

# Kinufaktur AI Chief of Staff

## Vision

Kinufaktur helps businesses automate processes with AI and turn fragmented data into a usable single source of truth.

The goal of this project is to build an AI Chief of Staff that acts as Kinufaktur's first internal digital employee.

The assistant should help organize incoming business requests and turn them into actionable work.

## Target User

The initial user is the founder/operator of Kinufaktur.

## Core Features

### 1. Request Intake

Users can create a new business request with a title and description.

Examples:
- Automate invoice processing
- Consolidate customer data
- Build an AI support workflow

### 2. Request Classification

Each request can be classified into one of the following categories:

- AI Automation
- Data / Single Source of Truth
- Other

### 3. Action Plan

Each request can contain an action plan with concrete next steps.

The first version does not require an external LLM API. Action plans can initially be entered and stored manually.

### 4. Status Tracking

Requests have a status:

- New
- Reviewed
- Planned
- Done

## MVP

The first version will be a Django web application.

Users should be able to:

- View all requests
- Create a request
- View request details
- Assign a category
- Add an action plan
- Change the request status

## Out of Scope for Version 1

- Autonomous agents
- RAG
- Vector databases
- Email integration
- CRM integration
- External LLM API calls
- User authentication
- Multi-user permissions

These can be added later after the basic workflow works.

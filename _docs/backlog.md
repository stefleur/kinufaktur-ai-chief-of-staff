# Kinufaktur AI Chief of Staff — MVP Backlog

## Task 1: Create the business request data model

Create a `BusinessRequest` model with a title, description, category, action plan,
status, and timestamps. Add the app to `INSTALLED_APPS`, create the initial
migration, and register the model in Django admin.

## Task 2: Add request intake

Create a validated Django form and a page where the operator can submit a new
business request. Redirect to the new request's detail page after saving it.

## Task 3: Add request list and detail pages

Create a home page that lists all requests and a detail page that displays a
request's classification, action plan, and current status.

## Task 4: Add workflow editing

Allow the operator to update a request's category, action plan, and status from
the detail page.

## Task 5: Cover the core workflow with tests

Test model defaults and choices, successful and invalid request intake, list and
detail rendering, missing requests, and workflow updates.

## Task 6: Polish documentation and interface

Document setup, migrations, server, and test commands in the README. Add simple
styling and verify the complete workflow manually.

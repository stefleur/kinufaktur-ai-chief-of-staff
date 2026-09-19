# Release process

Production and staging are not currently separate environments. Changes merged into `main` are released to the production services.

## Release steps

1. Develop and test the change locally.
2. Push the change to GitHub.
3. Confirm that GitHub CI in `.github/workflows/ci.yml` passes.
4. When the change reaches `main`, `.github/workflows/deploy.yml` automatically deploys the frontend to GitHub Pages.
5. FastAPI Cloud's GitHub integration automatically redeploys backend changes from GitHub.
6. After deployment, verify the production frontend and backend. Check `GET /tasks`, create a task in the frontend, reload the page, and confirm that the task persists.

## Rollback

If a release causes a problem, revert the problematic Git commit and push the revert. The normal deployment integrations will deploy the reverted state. Verify both the frontend and backend after the rollback completes.

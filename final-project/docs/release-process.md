# KinuFlow release process

The foundation was merged through [PR #4](https://github.com/stefleur/kinufaktur-ai-chief-of-staff/pull/4).
Use the normal flow: feature branch -> pull request -> CI -> review -> merge to
main -> deployment. There is one production environment, with synthetic data.

## Release steps

1. Implement and verify on a feature branch; review the diff and configuration.
2. Push/open a PR only when authorized. PR CI runs backend tests and frontend
   tests/build; require passing checks and human review before merging.
3. After an authorized merge to main, the Pages workflow calls CI and publishes
   the frontend only if those checks pass. It retains the existing site/variables.
4. FastAPI Cloud independently deploys from its GitHub integration. Its settings
   are external; backend deployment is not yet fully gated by repository CI.
   A prepared Actions job requires CI and owner opt-in but defaults to disabled. See the
   [remaining provider step](deployment.md#external-fastapi-cloud-deployment-and-remaining-manual-step).
5. Check deployed URLs and complete the synthetic CRUD/persistence smoke test
   described in [deployment.md](deployment.md).

Batch 3 changes remain uncommitted for review. No commit, push, PR, merge, or
production deployment was performed by this batch. The revised Pages gate needs
an actual GitHub run after delivery; static inspection is not deployment proof.

## Rollback

After review/authorization, revert the problematic commit through a PR. Passing
checks and merge trigger the normal Pages deployment; FastAPI Cloud follows its
external trigger until the documented owner cutover; afterward the enabled
backend Actions job requires passing CI. Verify both services afterward. No database schema changes are
part of this batch; reverting application code is not a database restore.

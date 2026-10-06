# Task API Change Workflow

Use this workflow for bounded changes to the KinuFlow task API.

1. **Spec:** Read `product-spec.md`, `openapi.yaml`, and `AGENTS.md`. State the requested behavior, affected contract, and explicit out-of-scope areas.
2. **Bounded implementation:** Change only the authorized API surface and its directly related tests. Preserve existing behavior outside the approved scope; do not alter deployment, credentials, production settings, or unrelated application layers.
3. **Tests:** Add or update focused tests, run them, then run any broader verification required by the change. Report the commands and actual results.
4. **Specialist review:** Ask `api-test-reviewer` to review the diff and test evidence. Resolve or explicitly report each finding; the specialist does not approve or apply changes.
5. **Human approval:** Present the scope, diff summary, checks, and unresolved findings to a human. Stop for approval before any commit, push, merge, or deployment.
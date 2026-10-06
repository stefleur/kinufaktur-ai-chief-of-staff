# Agent Extension Pack

The KinuFlow extension pack supports bounded task API development. It does not add AI features to the running application.

- `AGENTS.md` provides the existing project-wide instructions and boundaries.
- `agent-capabilities/task-api-change.md` defines the spec -> bounded implementation -> tests -> specialist review -> human approval workflow.
- `custom-agent/api-test-reviewer.md` is a read-only API and test review specialist.
- `mcp-server/server.py` exposes one read-only MCP tool for the fixed specification, API contract, or project instructions.
- `agent-hooks/check_protected_files.py` checks staged paths for obvious secret and credential filenames.
- `docs/permissions.md` records access boundaries and limitations.

## MCP setup and smoke test

From the repository root:

```bash
uv sync --project final-project/mcp-server --locked --group dev
uv run --project final-project/mcp-server --locked pytest -q final-project/mcp-server/tests final-project/agent-hooks/tests
```

Configure an MCP client to launch `uv run --project <repository>/final-project/mcp-server --locked python <repository>/final-project/mcp-server/server.py` over stdio. The server exposes only `get_project_context(section)`; see `docs/permissions.md` for its fixed sections and file mapping.

Run the staged-path guardrail from the repository root:

```bash
python3 final-project/agent-hooks/check_protected_files.py
```

The guardrail is advisory filename screening, not secret detection or a substitute for repository and platform controls.
# Agent Extension Security Review

- The MCP tool accepts only `spec`, `api_contract`, or `instructions` and maps those labels to `product-spec.md`, `openapi.yaml`, or `AGENTS.md` beneath `final-project/`.
- It accepts no arbitrary path parameter and has no shell, SQL, URL, write, credential, or production access. It performs no network requests.
- The API/test specialist is review-only and has read/search tools; it has no editing, command, deployment, credential, production, commit, push, or approval authority.
- The staged-file guardrail reads Git's staged path names only. It detects common environment, credential, secret, service-account, and private-key filenames; it neither reads file contents nor changes the index. It is heuristic and can miss secrets under innocuous names or detect harmless matching names.
- Human approval remains required for commits, pushes, merges, deployment, and work beyond the authorized scope. Agent review is not human approval.

## Review Finding and Limitation

The local Extension Pack audit found that Python `read_text()` followed symlinks at one of the fixed mapped filenames. The MCP reader now rejects a symlink, resolves the selected fixed file, verifies the resolved target is beneath the resolved `final-project/` root, and requires a regular file before reading. A regression test points the allowlisted `product-spec.md` filename at an outside file and verifies rejection; the existing protocol test still verifies all normal allowed reads, exactly one tool, and invalid-section rejection. The focused MCP tests passed.

This closes the reported symlink case for the current implementation and tested threat model. The MCP reads local project files and assumes the checkout is not concurrently mutated by an attacker between validation and file open; it is not a general hostile-filesystem sandbox.

The review is a local checkpoint audit, not a final PR audit or a security certification. See `pr-audits/extension-pack-local-diff-audit.md`.
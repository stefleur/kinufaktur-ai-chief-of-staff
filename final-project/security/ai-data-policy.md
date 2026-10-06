# AI Tool and Data Policy

- Use synthetic/demo data only in prompts, tests, logs, and examples.
- Never place secrets in prompts; credentials must not enter logs or reports.
- Human-review AI-generated code before accepting it.
- Verify changes with relevant tests and builds.
- Production changes require a pull request, passing CI, and human review.
- AI tools have no autonomous production authority; deployment requires explicit human authorization.
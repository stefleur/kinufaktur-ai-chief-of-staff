# Security Scan Evidence

## Run identity

- Source revision: `34cb0d9460ba831b29b87f6eb867844bf73daea5` plus the non-ignored Final Project worktree files present when the final audit scan ran. The tracked documentation changes were local and uncommitted; generated JSON reports are excluded from the scan input.
- Gitleaks: `8.30.1`
- Bandit: `1.9.4`
- Command: `bash final-project/security/run-scans.sh`
- Date: 2026-10-06

## Scope and commands

The runner snapshots tracked and non-ignored worktree files under `final-project/`. It excludes only generated `security/scans/*.json` reports from Gitleaks input; Git-ignored local environments and build outputs are not included. Gitleaks scans the snapshot directory with 100% secret redaction. Bandit recursively analyzes Python files in the snapshot, excluding virtualenv, node_modules, and dist paths. This is a current-source scan, not a Git-history scan.

Equivalent scanner invocations are defined in `../run-scans.sh`. The script requires the recorded exact tool versions and writes JSON reports here.

## Findings

- Gitleaks: zero findings. `gitleaks.json` is an empty findings array.
- Bandit: 58 low-severity, high-confidence findings; zero medium/high findings; 659 lines analyzed. Breakdown: 54 B101 assertion-use findings in tests, two B404 subprocess-import findings, one B603 subprocess-call finding, and one B607 partial executable path finding. The subprocess findings are in the staged-path guardrail and its tests; it uses a fixed `git diff --cached --name-only -z` argument vector, `shell=False`, and a fixed repository working directory. Test assertions are intentional test checks.

## Disposition

No finding was hidden, baseline-suppressed, or waived by the runner. Dispositions below apply to the current local developer guardrail, not deployment or use with an untrusted environment:

| Rule | Count | Severity | Why it exists | Disposition and reasoning |
| --- | ---: | --- | --- | --- |
| B101 | 54 | Low, high confidence | Pytest files use assertions to express test expectations. | **Accepted.** These are test checks, not production authorization or input validation. Removing assertions would weaken tests; Bandit reports their use in tests by default. |
| B404 | 2 | Low, high confidence | The guardrail and its test import Python's subprocess module. | **Accepted.** The guardrail needs to query staged filenames from Git; the test mocks that call. Import alone executes no command. |
| B603 | 1 | Low, high confidence | The guardrail calls `subprocess.run`. | **Accepted for this local tool.** It passes a fixed Git argument list and fixed repository cwd, captures output, and does not enable a shell or interpolate staged values into the command. This does not make arbitrary subprocess use safe. |
| B607 | 1 | Low, high confidence | The executable name `git` is resolved through `PATH`. | **Accepted with an environment limitation.** This advisory developer-run guardrail assumes the caller's normal trusted local `PATH`; it is not an enforcement boundary against an attacker who controls that environment. If run in a privileged or untrusted-PATH context, executable resolution requires remediation before use. |

These are the disposition for this scan, not a claim that a human independently approved them. No finding is suppressed or claimed fixed. The JSON reports contain no discovered secret values; Gitleaks redaction is enabled for future findings as well.
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
REPORT_DIR="$SCRIPT_DIR/scans"
EXPECTED_GITLEAKS_VERSION="8.30.1"
EXPECTED_BANDIT_VERSION="1.9.4"

command -v gitleaks >/dev/null || {
  printf 'gitleaks is required (expected %s).\n' "$EXPECTED_GITLEAKS_VERSION" >&2
  exit 2
}
command -v bandit >/dev/null || {
  printf 'bandit is required (expected %s).\n' "$EXPECTED_BANDIT_VERSION" >&2
  exit 2
}

GITLEAKS_VERSION="$(gitleaks version)"
BANDIT_VERSION="$(bandit --version | awk 'NR == 1 { print $2 }')"
if [[ "$GITLEAKS_VERSION" != "$EXPECTED_GITLEAKS_VERSION" ]]; then
  printf 'Expected Gitleaks %s, found %s.\n' "$EXPECTED_GITLEAKS_VERSION" "$GITLEAKS_VERSION" >&2
  exit 2
fi
if [[ "$BANDIT_VERSION" != "$EXPECTED_BANDIT_VERSION" ]]; then
  printf 'Expected Bandit %s, found %s.\n' "$EXPECTED_BANDIT_VERSION" "$BANDIT_VERSION" >&2
  exit 2
fi

mkdir -p "$REPORT_DIR"
TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/kinuflow-security-scan.XXXXXX")"
trap 'rm -rf "$TEMP_DIR"' EXIT
SNAPSHOT_ROOT="$TEMP_DIR/source"
FILE_LIST="$TEMP_DIR/files"
mkdir -p "$SNAPSHOT_ROOT"

git -C "$REPO_ROOT" ls-files -z --cached --others --exclude-standard -- final-project > "$FILE_LIST"
while IFS= read -r -d '' relative_path; do
  case "$relative_path" in
    final-project/security/scans/*.json) continue ;;
  esac
  destination="$SNAPSHOT_ROOT/$relative_path"
  mkdir -p "$(dirname "$destination")"
  cp "$REPO_ROOT/$relative_path" "$destination"
done < "$FILE_LIST"

SOURCE_REVISION="$(git -C "$REPO_ROOT" rev-parse HEAD)"
printf 'Scanning Final Project source at commit %s plus non-ignored worktree files.\n' "$SOURCE_REVISION"
printf 'Gitleaks %s; Bandit %s.\n' "$GITLEAKS_VERSION" "$BANDIT_VERSION"

cd "$SNAPSHOT_ROOT"
gitleaks dir \
  --redact=100 \
  --exit-code 0 \
  --no-banner \
  --report-format json \
  --report-path "$REPORT_DIR/gitleaks.json" \
  final-project

bandit -r final-project \
  -x '*/.venv/*,*/node_modules/*,*/dist/*' \
  --format json \
  --output "$REPORT_DIR/bandit.json" \
  --exit-zero

printf 'Reports written to %s. Review findings and record human disposition in scans/README.md.\n' "$REPORT_DIR"
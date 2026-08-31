#!/usr/bin/env bash
# Rematerialize the exam catalog on a running API (after deploying new templates).
#
# Usage:
#   API_URL=https://erettsegi-api-xxx.run.app CLEANUP_TOKEN=secret \
#     ./scripts/seed-exams.sh

set -euo pipefail

API_URL="${API_URL:?Set API_URL to the backend origin (no trailing slash)}"
CLEANUP_TOKEN="${CLEANUP_TOKEN:?Set CLEANUP_TOKEN to match the API env var}"

resp="$(curl -sS -X POST "${API_URL}/internal/seed-exams" \
  -H "X-Cleanup-Token: ${CLEANUP_TOKEN}" \
  -H "Content-Type: application/json" \
  -w "\n%{http_code}")"

body="${resp%$'\n'*}"
code="${resp##*$'\n'}"

echo "${body}"
if [[ "${code}" != "200" ]]; then
  echo "seed failed: HTTP ${code}" >&2
  exit 1
fi

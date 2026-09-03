#!/usr/bin/env bash
# Rematerialize the exam catalog on a running API (after deploying new templates).
#
# Usage:
#   API_URL=https://erettsegi-api-xxx.run.app CLEANUP_TOKEN=secret \
#     ./scripts/seed-exams.sh

set -euo pipefail

API_URL="${API_URL:?Set API_URL to the backend origin (no trailing slash)}"
CLEANUP_TOKEN="${CLEANUP_TOKEN:?Set CLEANUP_TOKEN to match the API env var}"

# Must exceed Cloud Run --timeout (deploy default 300s) so curl waits for the real status.
SEED_TIMEOUT="${SEED_TIMEOUT:-320}"

resp="$(curl -sS --max-time "${SEED_TIMEOUT}" -X POST "${API_URL}/internal/seed-exams" \
  -H "X-Cleanup-Token: ${CLEANUP_TOKEN}" \
  -H "Content-Type: application/json" \
  -w "\n%{http_code}")"

body="${resp%$'\n'*}"
code="${resp##*$'\n'}"

echo "${body}"
if [[ "${code}" != "200" ]]; then
  echo "seed failed: HTTP ${code}" >&2
  if [[ "${code}" == "504" ]]; then
    echo "Cloud Run timed out mid-catalog. Raise the service timeout (no rebuild):" >&2
    echo "  gcloud run services update erettsegi-api --project project-3809701b-6b98-4468-890 --region europe-west1 --timeout 300" >&2
    echo "Then retry this script." >&2
  fi
  exit 1
fi

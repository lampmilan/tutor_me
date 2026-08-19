#!/usr/bin/env bash
# Deploy the FastAPI backend to Cloud Run from Cloud Shell (or any logged-in gcloud).
# JSON service-account keys are blocked on this GCP org — deploy as your user instead.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="${GCP_PROJECT:-project-3809701b-6b98-4468-890}"
REGION="${GCP_REGION:-europe-west1}"
SERVICE="${CLOUD_RUN_SERVICE:-erettsegi-api}"
DATABASE_SECRET="${DATABASE_SECRET:-DATABASE_URL}"
CORS_ORIGINS="${CORS_ORIGINS:-}"
ALLOW_OPEN_CORS="${ALLOW_OPEN_CORS:-0}"
MEMORY="${CLOUD_RUN_MEMORY:-512Mi}"
WORKSPACE_TTL_DAYS="${WORKSPACE_TTL_DAYS:-7}"
RATE_LIMIT_EXECUTE_PER_MINUTE="${RATE_LIMIT_EXECUTE_PER_MINUTE:-30}"
RATE_LIMIT_JUDGE_PER_MINUTE="${RATE_LIMIT_JUDGE_PER_MINUTE:-12}"
CLEANUP_TOKEN="${CLEANUP_TOKEN:-}"
CORS_ORIGIN_REGEX="${CORS_ORIGIN_REGEX:-}"

if [[ -z "${CORS_ORIGINS}" || "${CORS_ORIGINS}" == "*" ]]; then
  if [[ "${ALLOW_OPEN_CORS}" != "1" ]]; then
    echo "CORS_ORIGINS must be the Vercel production origin (not *)." >&2
    echo "  export CORS_ORIGINS='https://YOUR-APP.vercel.app'" >&2
    echo "Emergency escape hatch: ALLOW_OPEN_CORS=1 (do not use for public beta)." >&2
    exit 1
  fi
  CORS_ORIGINS="*"
fi

echo "Enabling required APIs on ${PROJECT}..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  --project "${PROJECT}"

if ! gcloud secrets describe "${DATABASE_SECRET}" --project "${PROJECT}" >/dev/null 2>&1; then
  echo "Secret ${DATABASE_SECRET} not found in ${PROJECT}." >&2
  echo "Create it once (pooled Neon URL, no trailing newline):" >&2
  echo "  echo -n 'postgresql://USER:PASSWORD@...-pooler...neon.tech/neondb?sslmode=require' \\" >&2
  echo "    | gcloud secrets create ${DATABASE_SECRET} --data-file=- --project ${PROJECT}" >&2
  exit 1
fi

PROJECT_NUMBER="$(gcloud projects describe "${PROJECT}" --format='value(projectNumber)')"
RUNTIME_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
echo "Granting ${RUNTIME_SA} access to ${DATABASE_SECRET}..."
gcloud secrets add-iam-policy-binding "${DATABASE_SECRET}" \
  --project "${PROJECT}" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/secretmanager.secretAccessor" \
  --quiet >/dev/null

# If DATABASE_URL was previously a plaintext env var, drop it so it can be a secret.
if gcloud run services describe "${SERVICE}" --project "${PROJECT}" --region "${REGION}" >/dev/null 2>&1; then
  gcloud run services update "${SERVICE}" \
    --project "${PROJECT}" \
    --region "${REGION}" \
    --remove-env-vars DATABASE_URL \
    --quiet >/dev/null 2>&1 || true
fi

echo "Deploying ${SERVICE} to Cloud Run (${REGION})..."
# Custom delimiter ^@^ so CORS_ORIGINS commas are safe.
# --update-env-vars keeps the DATABASE_URL secret; --set-env-vars would wipe it.
gcloud run deploy "${SERVICE}" \
  --source "${ROOT}/backend" \
  --project "${PROJECT}" \
  --region "${REGION}" \
  --allow-unauthenticated \
  --timeout 60 \
  --memory "${MEMORY}" \
  --cpu 1 \
  --update-env-vars "^@^EXECUTION_BACKEND=subprocess@WORKSPACES_ROOT=/tmp/erettsegi-workspaces@CORS_ORIGINS=${CORS_ORIGINS}@CORS_ORIGIN_REGEX=${CORS_ORIGIN_REGEX}@AI_GENERATION_ENABLED=false@WORKSPACE_TTL_DAYS=${WORKSPACE_TTL_DAYS}@RATE_LIMIT_EXECUTE_PER_MINUTE=${RATE_LIMIT_EXECUTE_PER_MINUTE}@RATE_LIMIT_JUDGE_PER_MINUTE=${RATE_LIMIT_JUDGE_PER_MINUTE}@CLEANUP_TOKEN=${CLEANUP_TOKEN}" \
  --set-secrets "DATABASE_URL=${DATABASE_SECRET}:latest"

URL="$(gcloud run services describe "${SERVICE}" --project "${PROJECT}" --region "${REGION}" --format='value(status.url)')"
echo
echo "Backend URL: ${URL}"
echo "Set these on the Vercel project (Root Directory = frontend):"
echo "  API_URL=${URL}"
echo "  BACKEND_URL=${URL}"
echo
echo "Health: ${URL}/health"
echo
echo "Workspace cleanup (Cloud Scheduler daily POST):"
echo "  curl -X POST ${URL}/internal/cleanup-workspaces -H \"X-Cleanup-Token: \$CLEANUP_TOKEN\""

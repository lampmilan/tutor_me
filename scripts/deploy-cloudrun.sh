#!/usr/bin/env bash
# Deploy the FastAPI backend to Cloud Run from Cloud Shell (or any logged-in gcloud).
# JSON service-account keys are blocked on this GCP org — deploy as your user instead.
#
# DATABASE_URL is read from Secret Manager (neon-database-url), not the shell.
# Create the secret once, then deploy:
#
#   echo -n 'postgresql://USER:PASSWORD@...-pooler...neon.tech/neondb?sslmode=require' \
#     | gcloud secrets create neon-database-url --data-file=-
#   export CORS_ORIGINS='*'
#   ./scripts/deploy-cloudrun.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="${GCP_PROJECT:-project-3809701b-6b98-4468-890}"
REGION="${GCP_REGION:-europe-west1}"
SERVICE="${CLOUD_RUN_SERVICE:-erettsegi-api}"
DATABASE_SECRET="${DATABASE_SECRET:-neon-database-url}"
CORS_ORIGINS="${CORS_ORIGINS:-*}"
MEMORY="${CLOUD_RUN_MEMORY:-512Mi}"

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
  --update-env-vars "^@^EXECUTION_BACKEND=subprocess@WORKSPACES_ROOT=/tmp/erettsegi-workspaces@CORS_ORIGINS=${CORS_ORIGINS}" \
  --set-secrets "DATABASE_URL=${DATABASE_SECRET}:latest"

URL="$(gcloud run services describe "${SERVICE}" --project "${PROJECT}" --region "${REGION}" --format='value(status.url)')"
echo
echo "Backend URL: ${URL}"
echo "Set these on the Vercel project (Root Directory = frontend):"
echo "  API_URL=${URL}"
echo "  BACKEND_URL=${URL}"
echo
echo "Health: ${URL}/health"

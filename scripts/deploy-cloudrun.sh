#!/usr/bin/env bash
# Deploy the FastAPI backend to Cloud Run from Cloud Shell (or any logged-in gcloud).
# JSON service-account keys are blocked on this GCP org — deploy as your user instead.
#
#   export DATABASE_URL='postgresql://...@...neon.tech/neondb?sslmode=require'
#   export CORS_ORIGINS='*'
#   ./scripts/deploy-cloudrun.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="${GCP_PROJECT:-project-3809701b-6b98-4468-890}"
REGION="${GCP_REGION:-europe-west1}"
SERVICE="${CLOUD_RUN_SERVICE:-erettsegi-api}"
DATABASE_URL="${DATABASE_URL:?Set DATABASE_URL to the Neon pooled connection string}"
CORS_ORIGINS="${CORS_ORIGINS:-*}"
MEMORY="${CLOUD_RUN_MEMORY:-512Mi}"

echo "Enabling required APIs on ${PROJECT}..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  --project "${PROJECT}"

echo "Deploying ${SERVICE} to Cloud Run (${REGION})..."
# Custom delimiter ^@^ so DATABASE_URL commas/query strings are safe.
gcloud run deploy "${SERVICE}" \
  --source "${ROOT}/backend" \
  --project "${PROJECT}" \
  --region "${REGION}" \
  --allow-unauthenticated \
  --timeout 60 \
  --memory "${MEMORY}" \
  --cpu 1 \
  --set-env-vars "^@^EXECUTION_BACKEND=subprocess@WORKSPACES_ROOT=/tmp/erettsegi-workspaces@CORS_ORIGINS=${CORS_ORIGINS}@DATABASE_URL=${DATABASE_URL}"

URL="$(gcloud run services describe "${SERVICE}" --project "${PROJECT}" --region "${REGION}" --format='value(status.url)')"
echo
echo "Backend URL: ${URL}"
echo "Set these on the Vercel project (Root Directory = frontend):"
echo "  API_URL=${URL}"
echo "  BACKEND_URL=${URL}"
echo
echo "Health: ${URL}/health"

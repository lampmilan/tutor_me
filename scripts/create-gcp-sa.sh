#!/usr/bin/env bash
# Create a deployer service account and JSON key for GitHub Actions → Cloud Run.
# Run this in Google Cloud Shell (or any machine already logged into gcloud).
#
#   ./scripts/create-gcp-sa.sh
#
# Then paste the printed JSON into GitHub → Settings → Secrets → Actions → GCP_SA_KEY
# and delete the local key file.

set -euo pipefail

PROJECT="${GCP_PROJECT:-project-3809701b-6b98-4468-890}"
SA_NAME="${GCP_SA_NAME:-github-cloudrun}"
SA_EMAIL="${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
KEY_FILE="${GCP_SA_KEY_FILE:-$PWD/gcp-sa-key.json}"

if ! command -v gcloud >/dev/null 2>&1; then
  echo "gcloud is not installed. Open Cloud Shell:"
  echo "  https://console.cloud.google.com/cloudshell?project=${PROJECT}"
  exit 1
fi

ACCOUNT="$(gcloud auth list --filter=status:ACTIVE --format='value(account)' 2>/dev/null | head -n1 || true)"
if [ -z "$ACCOUNT" ]; then
  echo "No active gcloud account. Run: gcloud auth login"
  exit 1
fi

echo "Using GCP project ${PROJECT} as ${ACCOUNT}"
gcloud config set project "${PROJECT}"

echo "Enabling APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  iam.googleapis.com \
  --project "${PROJECT}"

if gcloud iam service-accounts describe "${SA_EMAIL}" --project "${PROJECT}" >/dev/null 2>&1; then
  echo "Service account ${SA_EMAIL} already exists."
else
  echo "Creating service account ${SA_EMAIL}..."
  gcloud iam service-accounts create "${SA_NAME}" \
    --project "${PROJECT}" \
    --display-name "GitHub Cloud Run deployer"
fi

# Source deploys need Run + Cloud Build + the buckets/AR Cloud Build writes to.
for role in \
  roles/run.admin \
  roles/iam.serviceAccountUser \
  roles/cloudbuild.builds.editor \
  roles/storage.admin \
  roles/artifactregistry.admin \
  roles/serviceusage.serviceUsageConsumer
do
  echo "Granting ${role}..."
  gcloud projects add-iam-policy-binding "${PROJECT}" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="${role}" \
    --condition=None \
    --quiet >/dev/null
done

echo "Creating JSON key at ${KEY_FILE}..."
gcloud iam service-accounts keys create "${KEY_FILE}" \
  --iam-account="${SA_EMAIL}" \
  --project "${PROJECT}"

echo
echo "============================================================"
echo "Add this file's contents as GitHub Actions secret GCP_SA_KEY:"
echo "  ${KEY_FILE}"
echo
echo "GitHub → repo → Settings → Secrets and variables → Actions → New repository secret"
echo "  Name: GCP_SA_KEY"
echo "  Value: paste the entire JSON file"
echo
echo "Then delete the key file:"
echo "  rm -f '${KEY_FILE}'"
echo "============================================================"

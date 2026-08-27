#!/usr/bin/env bash
# Idempotent dev-environment bootstrap for VizsgaGO (backend + frontend).
# Runs natively (no Docker): FastAPI on SQLite + subprocess executor, Next.js dev server.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# The default image ships Python 3.12 but not the venv module.
if ! python3 -c "import ensurepip" >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo apt-get install -y -qq python3-venv
fi

# Backend: virtualenv + pinned deps (+ pytest for the test suite) + SQLite data dir.
cd "$REPO_ROOT/backend"
python3 -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
pip install --upgrade pip -q
pip install -q -r requirements.txt pytest
mkdir -p data
deactivate

# Frontend: install from lockfile.
cd "$REPO_ROOT/frontend"
npm ci

echo "install.sh: VizsgaGO dev environment ready."

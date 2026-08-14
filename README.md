# Érettségi Lab

Online coding practice platform for the Hungarian programming **érettségi**.

## Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js on **Vercel** |
| Backend | FastAPI on **Google Cloud Run** |
| Database | **Neon** Postgres |
| Execution | Subprocess on Cloud Run (Docker isolation locally) |
| Local runtime | Docker Compose |

## Quick start

```bash
# 1. Copy env
cp .env.example .env

# 2. Build the executor image (used for student code)
docker compose build executor
# or:
docker build -t erettsegi-executor:latest ./docker/executor

# 3. Start everything
docker compose up --build
```

- App: http://localhost:3000  
- API docs: http://localhost:8000/docs  

The frontend talks to the backend over the Compose network (`backend:8000`).
Browser calls go to `/api/*` on port 3000 and Next.js rewrites them to the backend.

## Deploy (Vercel + Cloud Run + Neon)

Order matters: **Neon → Cloud Run → Vercel**, so the frontend can rewrite `/api/*` to the API URL.

### 1. Neon

Create a project at [neon.tech](https://neon.tech) (or claim a temporary DB from [neon.new](https://neon.new)). Copy the **pooled** connection string:

```text
postgresql://USER:PASSWORD@ep-xxx-pooler.REGION.aws.neon.tech/neondb?sslmode=require
```

Schema + exam seed run automatically when the API starts.

### 2. Cloud Run

Project id: `project-3809701b-6b98-4468-890` (billing must be enabled).

This org blocks service-account JSON keys (`iam.disableServiceAccountKeyCreation`). Deploy from Cloud Shell as your user — no `GCP_SA_KEY`.

1. Open [Cloud Shell](https://console.cloud.google.com/cloudshell?project=project-3809701b-6b98-4468-890).
2. If the repo is not already there:

```bash
git clone https://github.com/lampmilan/tutor_me.git
cd tutor_me
```

3. Store the pooled Neon URL in Secret Manager **once** (same value as GitHub secret `NEON_DATABASE_URL`). Do not export it in Cloud Shell or commit it:

```bash
echo -n 'postgresql://USER:PASSWORD@...-pooler...neon.tech/neondb?sslmode=require' \
  | gcloud secrets create neon-database-url --data-file=-
```

4. Deploy (no `DATABASE_URL` in the shell — Cloud Run reads `neon-database-url`):

```bash
export CORS_ORIGINS='*'
./scripts/deploy-cloudrun.sh
```

The script prints `https://erettsegi-api-….run.app`. Open `/health` to confirm. If `DATABASE_URL` was previously a plaintext Cloud Run env var, the script removes it and rebinds the name as a secret.

### 3. Vercel

1. [Import the GitHub repo](https://vercel.com/new) (`lampmilan/tutor_me`).
2. Set **Root Directory** to `frontend`.
3. Environment variables (Production + Preview):
   - `API_URL` = Cloud Run URL (no trailing slash)
   - `BACKEND_URL` = same Cloud Run URL
4. Deploy.

Browser traffic stays same-origin (`/api/*`); Vercel rewrites it to Cloud Run, so Run/Submit is not limited by Vercel function timeouts.

After the first Vercel URL is known, redeploy Cloud Run with `CORS_ORIGINS` set to that origin if the browser will call the API directly.

## Core workflow

1. Open an exam (e.g. **Cities**).
2. Workspace is created with `main.py` + the exam data file (e.g. `cities.txt`).
3. Edit code in Monaco.
4. Click **Run** → executes `main.py` against the **visible** dataset (what you see in the file explorer).
5. Click **Submit** → runs the same code against **hidden** datasets. Each hidden test overwrites the data file **under the same filename** (still `cities.txt`) in a temporary sandbox — your code keeps using `open("cities.txt")`. Hidden inputs are never shown; you get a pass summary and educational hints instead.

## Project layout

```
frontend/                 Next.js app (Monaco workspace UI)
backend/app/exams/        Exam catalog (one folder per exam)
backend/app/services/     Judge, executor, materializer
docker/executor/          Slim Python image for student code
docker-compose.yml        Postgres + backend + frontend
```

## API highlights

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/exams` | List exams |
| GET | `/exams/{id}` | Exam details + tasks |
| POST | `/exams/{id}/start` | Create workspace |
| PUT | `/workspaces/{id}/files/{name}` | Save file |
| POST | `/execute` | Run `main.py` (visible dataset) |
| POST | `/judge` | Grade against sample + hidden tests |
| POST | `/exams/from-template` | Materialize exam from catalog id |

(Browser clients should use `/api/...` via the frontend proxy.)

## Per-task files and preamble (Option A)

Each feladat is a separate editable file (`feladat1.py`, `feladat2.py`, …).
**Do not** collapse an exam into one `.py`.

- **Task 1** reads the data file and stores it as a **string** (e.g. `cities = f.read()`).
- **Later tasks** set `uses_preamble: true`. On Run/Submit the platform **prepends** a
  canonical loader that re-reads the data file into that same string variable.
  Students split/convert the string themselves — the platform does not inject a parsed list.
- `input()` is real: the backend pipes `task.stdin` (shown as minta bemenet). Do not
  monkeypatch `input()`. Prompt lines that are part of the official output stay on stdout.
- Output files (e.g. `szinek.txt`) use `expected_file`; the judge captures that file
  instead of stdout.

Hidden tests still replace the data filename only (e.g. `cities.txt`).

Each exam lives under `backend/app/exams/<id>/`:

```text
cities/
  template.json
  datasets/
    visible.txt          # shown in the student workspace as data_file
    hidden/
      01.txt             # authoring names only — mounted as cities.txt at judge time
viragagyasok/
  template.json
  builders.py            # exam-specific oracle (students never see this)
  datasets/
    ...
```

`template.json` defines metadata, the workspace filename (`data_file`), task types, and hints.
**Expected outputs are not authored** — they are computed from each dataset + task type.
Generic types (`count`, `maximum`, `minimum`, `average`, `count_where`, `read`, `literal`,
`store`) live in `backend/app/exams/builders.py`. Unique exams add
`backend/app/exams/<id>/builders.py` with `parse()` and `TASK_BUILDERS`.

Converting an official érettségi from the sanitized MD corpus: see
`.cursor/skills/erettsegi-to-catalog/SKILL.md` and `reference.md`.

Example (abbreviated):

```json
{
  "id": "cities",
  "title": "Cities",
  "data_file": "cities.txt",
  "dataset_type": "cities",
  "visible": "datasets/visible.txt",
  "hidden": ["datasets/hidden/01.txt", "datasets/hidden/02.txt"],
  "tasks": [
    {
      "type": "count",
      "title": "Városok száma",
      "points": 1,
      "hints": [
        "Your solution works for the example dataset but fails on other datasets."
      ]
    }
  ]
}
```

Seeded exams: **Cities**, **Trains**, **Temperatures**, **Students**, **Virágágyások**, **MRZ kód**.

```bash
curl -X POST http://localhost:8000/exams/from-template \
  -H 'Content-Type: application/json' \
  -d '{"exam_id": "cities", "use_ai": false}'
```

## AI generation (Phase 8)

Set in `.env`:

```
AI_GENERATION_ENABLED=true
OPENAI_API_KEY=sk-...
```

The LLM may only rewrite story text.
Task types and expected outputs are always computed from the template + datasets.

## Security (code execution)

Docker runs with:

- `--network none`
- memory / CPU / PID limits
- execution timeout
- read-only root filesystem (+ small `/tmp`)
- container destroyed after each run (`--rm`)

## Example exam: Cities

Visible `cities.txt`:

```
Budapest 1780000
Szeged 160000
Pecs 140000
```

Sample solution for task 1 (count cities):

```python
with open("cities.txt", encoding="utf-8") as f:
    print(len([line for line in f if line.strip()]))
```

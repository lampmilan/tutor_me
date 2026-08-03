# Érettségi Lab

Online coding practice platform for the Hungarian programming **érettségi**.

## Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js + TypeScript + Monaco Editor |
| Backend | FastAPI + Python |
| Database | PostgreSQL |
| Execution | Isolated Docker containers |
| Local dev | Docker Compose |

## Quick start (Docker Compose)

```bash
# 1. Copy env
cp .env.example .env

# 2. Build the executor image (used for student code)
docker compose build executor
docker compose --profile build-only build executor
# or:
docker build -t erettsegi-executor:latest ./docker/executor

# 3. Start everything
docker compose up --build
```

- Frontend: http://localhost:3000  
- Backend API: http://localhost:8000  
- API docs: http://localhost:8000/docs  

## Local development (without Compose)

Requires Python 3.12+, Node 22+, and optionally Docker for secure execution.

```bash
# Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
export $(grep -v '^#' .env | xargs)
cd backend && uvicorn app.main:app --reload --port 8000

# Frontend (another terminal)
cd frontend
npm install
npm run dev
```

If Docker is not available, set `EXECUTION_BACKEND=subprocess` in `.env`
(less isolated — for development only).

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

## Exam catalog

Each exam lives under `backend/app/exams/<id>/`:

```text
cities/
  template.json
  datasets/
    visible.txt          # shown in the student workspace as data_file
    hidden/
      01.txt             # authoring names only — mounted as cities.txt at judge time
      02.txt
      ...
```

`template.json` defines metadata, the workspace filename (`data_file`), task types, and hints.
**Expected outputs are not authored** — they are computed from each dataset + task type
(`count`, `maximum`, `minimum`, `average`, `count_where`, …).

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

Seeded exams: **Cities**, **Trains**, **Temperatures**, **Students**.

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

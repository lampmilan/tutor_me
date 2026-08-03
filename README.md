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
2. Workspace is created with `main.py` + `cities.txt`.
3. Edit code in Monaco.
4. Click **Run** → `POST /execute` → isolated Python run → stdout/stderr/runtime.
5. Click **Submit** → automatic judging against test cases → points.

## Project layout

```
frontend/          Next.js app (Monaco workspace UI)
backend/           FastAPI API, models, judge, templates
docker/executor/   Slim Python image for student code
docker-compose.yml Postgres + backend + frontend
```

## API highlights

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/exams` | List exams |
| GET | `/exams/{id}` | Exam details + tasks |
| POST | `/exams/{id}/start` | Create workspace |
| PUT | `/workspaces/{id}/files/{name}` | Save file |
| POST | `/execute` | Run `main.py` |
| POST | `/judge` | Grade against tests |
| POST | `/exams/from-template` | Generate exam from JSON template |

## Exam templates (Phase 7)

Templates define dataset type and task types. Grading logic comes from the
template — never from the LLM.

Example: `backend/app/templates/cities.json`

```json
{
  "title": "Cities",
  "dataset": { "type": "cities", "fields": ["name", "population"] },
  "tasks": [{ "type": "count" }, { "type": "maximum", "field": "population" }]
}
```

```bash
curl -X POST http://localhost:8000/exams/from-template \
  -H 'Content-Type: application/json' \
  -d '{"template": {...}, "use_ai": false, "seed": 42}'
```

## AI generation (Phase 8)

Set in `.env`:

```
AI_GENERATION_ENABLED=true
OPENAI_API_KEY=sk-...
```

The LLM may only rewrite story text and vary realistic data.
Task types and expected outputs are always computed from the template.

## Security (code execution)

Docker runs with:

- `--network none`
- memory / CPU / PID limits
- execution timeout
- read-only root filesystem (+ small `/tmp`)
- container destroyed after each run (`--rm`)

## Example exam: Cities

`cities.txt`:

```
Budapest 1780000
Szeged 160000
Pecs 140000
```

Sample solution for task 1 (count cities):

```python
with open("cities.txt") as f:
    print(len([line for line in f if line.strip()]))
```

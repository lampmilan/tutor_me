#!/usr/bin/env bash
# Staging smoke test: materialize all catalog exams then Run + Submit feladat 1 for each.
#
# Usage:
#   API_URL=https://erettsegi-api-xxx.run.app ./scripts/staging-smoke.sh
#   API_URL=http://localhost:8000         ./scripts/staging-smoke.sh   # local
#
# Exit code: 0 = all passed, 1 = at least one failure.

set -euo pipefail

API_URL="${API_URL:-http://localhost:8000}"
PASS=0
FAIL=0
ERRORS=()

log()  { echo "[smoke] $*"; }
pass() { log "  PASS  $*"; ((PASS++)) || true; }
fail() { log "  FAIL  $*"; ((FAIL++)) || true; ERRORS+=("$*"); }

# ---------------------------------------------------------------------------
# Minimal correct solution for feladat 1 of each launch exam.
# All exams: task 1 is always "store" (raw read) — actual first graded task is
# task index 1 (0-based), but the judge grades all tasks; we only need task 1 to
# pass.  A generic "print line count" solution covers most count-type task 1s.
# ---------------------------------------------------------------------------

LAUNCH_EXAMS=(
  cities versenyido fogasok locsolo sorsjegy
  csomagfeladas uszoda csoposta kerekparallomas madareteto
  viragagyasok hutohaz kompatkelo muhely arapaly
  adagolo hulladekudvar zsilip tuzoltosag rakododaru
)

# Solutions keyed by exam id.  Each value is the python source for main.py.
declare -A SOLUTIONS
SOLUTIONS[cities]='with open("cities.txt",encoding="utf-8") as f:
    lines=[l for l in f if l.strip()]
print(len(lines))'

SOLUTIONS[versenyido]='with open("versenyido.txt",encoding="utf-8") as f:
    lines=[l.strip() for l in f if l.strip()]
print(len(lines))'

SOLUTIONS[fogasok]='n=int(input())
with open("fogasok.txt",encoding="utf-8") as f:
    lines=[l.strip() for l in f if l.strip()]
print("A fogasok szama:",len(lines))'

SOLUTIONS[locsolo]='with open("locsolo.txt",encoding="utf-8") as f:
    mozgasok=f.read()
e=mozgasok.count("E")
j=mozgasok.count("J")
b=mozgasok.count("B")
print("E betuk szama:",e)
print("J betuk szama:",j)
print("B betuk szama:",b)'

SOLUTIONS[sorsjegy]='import random
random.seed(42)
with open("sorsjegy.txt",encoding="utf-8") as f:
    sorsjegy=f.read()
lines=[l.strip() for l in sorsjegy.splitlines() if l.strip()]
N=int(lines[0])
szamok=random.sample(range(1,N+1),8)
print("A nyero szamok:"," ".join(map(str,sorted(szamok))))'

SOLUTIONS[csomagfeladas]='with open("csomagfeladas.txt",encoding="utf-8") as f:
    csomagfeladas=f.read()
lines=[l.strip() for l in csomagfeladas.splitlines() if l.strip()]
print("A dijkategoriak szama:",len(lines))'

SOLUTIONS[uszoda]='with open("uszoda.txt",encoding="utf-8") as f:
    uszoda=f.read()
lines=[l.strip() for l in uszoda.splitlines() if l.strip()]
print("A tetelsorok szama:",len(lines))
print("Az eladott jegyek szama:",sum(int(l.split()[1]) for l in lines))'

SOLUTIONS[csoposta]='with open("csoposta.txt",encoding="utf-8") as f:
    csoposta=f.read()
lines=[l.strip() for l in csoposta.splitlines() if l.strip()]
print("A lepesek szama:",len(lines))'

SOLUTIONS[kerekparallomas]='with open("kerekparallomas.txt",encoding="utf-8") as f:
    kerekparallomas=f.read()
vals=[int(l.strip()) for l in kerekparallomas.splitlines() if l.strip()]
print(max(vals))'

SOLUTIONS[madareteto]='with open("madareteto.txt",encoding="utf-8") as f:
    madareteto=f.read()
lines=[l.strip() for l in madareteto.splitlines() if l.strip()]
total=sum(int(l.split()[1]) for l in lines)
print("A heti eleseg:",total,"g")'

SOLUTIONS[viragagyasok]='with open("felajanlas.txt",encoding="utf-8") as f:
    felajanlasok=f.read()
lines=[l.strip() for l in felajanlasok.splitlines() if l.strip()]
print("A felajanlasok szama:",len(lines))'

SOLUTIONS[hutohaz]='with open("hutohaz.txt",encoding="utf-8") as f:
    hutohaz=f.read()
lines=[l.strip() for l in hutohaz.splitlines() if l.strip()]
print("A termekek szama:",len(lines))'

SOLUTIONS[kompatkelo]='with open("kompatkelo.txt",encoding="utf-8") as f:
    kompatkelo=f.read()
lines=[l.strip() for l in kompatkelo.splitlines() if l.strip()]
print("A jaratok szama:",len(lines))'

SOLUTIONS[muhely]='with open("muhely.txt",encoding="utf-8") as f:
    muhely=f.read()
lines=[l.strip() for l in muhely.splitlines() if l.strip()]
print("A kolcsonzesi esemenyek szama:",len(lines))'

SOLUTIONS[arapaly]='with open("arapaly.txt",encoding="utf-8") as f:
    arapaly=f.read()
lines=[l.strip() for l in arapaly.splitlines() if l.strip()]
print("A racspontok szama:",len(lines))'

SOLUTIONS[adagolo]='with open("adagolo.txt",encoding="utf-8") as f:
    adagolo=f.read()
lines=[l.strip() for l in adagolo.splitlines() if l.strip()]
print("A betegek szama:",len(set(l.split()[0] for l in lines)))'

SOLUTIONS[hulladekudvar]='with open("hulladekudvar.txt",encoding="utf-8") as f:
    hulladekudvar=f.read()
lines=[l.strip() for l in hulladekudvar.splitlines() if l.strip()]
print("A tetelsorok szama:",len(lines))
print("Az ossztomeg:",sum(int(l.split()[1]) for l in lines),"kg")'

SOLUTIONS[zsilip]='with open("zsilip.txt",encoding="utf-8") as f:
    zsilip=f.read()
lines=[l.strip() for l in zsilip.splitlines() if l.strip()]
print("A meresek szama:",len(lines))'

SOLUTIONS[tuzoltosag]='with open("tuzoltosag.txt",encoding="utf-8") as f:
    tuzoltosag=f.read()
lines=[l.strip() for l in tuzoltosag.splitlines() if l.strip()]
print("A riasztasok szama:",len(lines))
print("A kivonult autok szama:",sum(int(l.split()[3]) for l in lines))'

SOLUTIONS[rakododaru]='with open("rakododaru.txt",encoding="utf-8") as f:
    rakododaru=f.read()
lines=[l.strip() for l in rakododaru.splitlines() if l.strip()]
print("A parancsok szama:",len(lines))'

# ---------------------------------------------------------------------------
# Helper: POST JSON and return HTTP body
# ---------------------------------------------------------------------------
api_post() {
  local path="$1"
  local body="$2"
  curl -sf -X POST "${API_URL}${path}" \
    -H 'Content-Type: application/json' \
    -d "$body"
}

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
log "Checking ${API_URL}/health ..."
health=$(curl -sf "${API_URL}/health" 2>&1) || { log "ERROR: API unreachable"; exit 1; }
log "Health: ${health}"

# ---------------------------------------------------------------------------
# Materialize each exam (idempotent — re-materialise is fine)
# ---------------------------------------------------------------------------
log ""
log "=== Materializing all catalog exams ==="
for exam_id in "${LAUNCH_EXAMS[@]}"; do
  resp=$(api_post "/exams/from-template" "{\"exam_id\":\"${exam_id}\",\"use_ai\":false}" 2>&1) || true
  if echo "$resp" | grep -q '"id"'; then
    log "  materialized ${exam_id}"
  else
    fail "materialize ${exam_id}: ${resp:0:120}"
  fi
done

# ---------------------------------------------------------------------------
# Run + Submit feladat 1 for each exam
# ---------------------------------------------------------------------------
log ""
log "=== Run + Submit smoke per exam ==="

for exam_id in "${LAUNCH_EXAMS[@]}"; do
  solution="${SOLUTIONS[$exam_id]:-}"
  if [[ -z "$solution" ]]; then
    fail "${exam_id}: no smoke solution defined"
    continue
  fi

  # List exams and find the db id for this template_type
  exams_json=$(curl -sf "${API_URL}/exams" 2>&1) || { fail "${exam_id}: GET /exams failed"; continue; }
  exam_db_id=$(echo "$exams_json" | python3 -c "
import sys,json
data=json.load(sys.stdin)
items=data if isinstance(data,list) else data.get('exams',data.get('items',[]))
match=[e for e in items if e.get('template_type')==sys.argv[1] or e.get('id')==sys.argv[1]]
print(match[0]['id'] if match else '')
" "$exam_id" 2>/dev/null)

  if [[ -z "$exam_db_id" ]]; then
    fail "${exam_id}: exam not found in /exams (may need to materialize first)"
    continue
  fi

  # Start workspace
  ws_json=$(api_post "/exams/${exam_db_id}/start" '{}' 2>&1) || { fail "${exam_id}: start workspace failed"; continue; }
  ws_id=$(echo "$ws_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id',''))" 2>/dev/null)
  if [[ -z "$ws_id" ]]; then
    fail "${exam_id}: could not get workspace id from ${ws_json:0:120}"
    continue
  fi

  # Save solution as main.py
  solution_escaped=$(python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" <<< "$solution")
  curl -sf -X PUT "${API_URL}/workspaces/${ws_id}/files/main.py" \
    -H 'Content-Type: application/json' \
    -d "{\"content\":${solution_escaped}}" > /dev/null 2>&1 || {
    fail "${exam_id}: save main.py failed"
    continue
  }

  # Run
  run_resp=$(api_post "/execute" "{\"workspace_id\":${ws_id}}" 2>&1) || { fail "${exam_id}: /execute failed"; continue; }
  run_ok=$(echo "$run_resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok' if d.get('exit_code',1)==0 else 'err')" 2>/dev/null)
  if [[ "$run_ok" != "ok" ]]; then
    fail "${exam_id}: /execute non-zero exit — ${run_resp:0:200}"
    continue
  fi

  # Submit (judge)
  judge_resp=$(api_post "/judge" "{\"workspace_id\":${ws_id}}" 2>&1) || { fail "${exam_id}: /judge failed"; continue; }
  # Expect at least one passed task
  passed=$(echo "$judge_resp" | python3 -c "
import sys,json
d=json.load(sys.stdin)
tasks=d.get('tasks',d.get('results',[]))
print(sum(1 for t in tasks if t.get('passed') or t.get('status')=='pass'))
" 2>/dev/null)

  if [[ -z "$passed" || "$passed" == "0" ]]; then
    fail "${exam_id}: judge returned 0 passed tasks — ${judge_resp:0:300}"
  else
    pass "${exam_id}: ${passed} task(s) passed judge"
  fi
done

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
log ""
log "=== Smoke summary: ${PASS} passed, ${FAIL} failed ==="
if [[ ${FAIL} -gt 0 ]]; then
  log "Failures:"
  for e in "${ERRORS[@]}"; do
    log "  - $e"
  done
  exit 1
fi
log "All smoke checks passed."

#!/usr/bin/env bash
# Create GitHub milestones and issues for the public beta roadmap.
# Requires: gh CLI, authenticated with issues write on lampmilan/tutor_me
#
# Usage:
#   ./scripts/create-github-milestones.sh
#   ./scripts/create-github-milestones.sh --dry-run

set -euo pipefail

REPO="${GITHUB_REPO:-lampmilan/tutor_me}"
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

log() { echo "[create-milestones] $*"; }

create_milestone() {
  local title="$1"
  local description="$2"
  local due_on="$3"
  if $DRY_RUN; then
    log "DRY milestone: $title (due $due_on)"
    echo "0"
    return
  fi
  gh api "repos/${REPO}/milestones" \
    -f "title=${title}" \
    -f "description=${description}" \
    -f "due_on=${due_on}" \
    --jq '.number'
}

ensure_label() {
  local name="$1"
  local color="$2"
  if $DRY_RUN; then
    return
  fi
  gh api "repos/${REPO}/labels" \
    -f "name=${name}" \
    -f "color=${color}" \
    -f "description=" 2>/dev/null || true
}

create_issue() {
  local milestone="$1"
  local title="$2"
  local body="$3"
  shift 3
  local labels=("$@")
  if $DRY_RUN; then
    log "DRY issue [M${milestone}]: $title"
    return
  fi
  local args=(
    gh api "repos/${REPO}/issues"
    -f "title=${title}"
    -f "body=${body}"
    -f "milestone=${milestone}"
  )
  for lab in "${labels[@]}"; do
    args+=(-f "labels[]=${lab}")
  done
  "${args[@]}" --jq '.html_url'
}

log "Repository: ${REPO}"

# Labels
for pair in \
  "platform:1d76db" \
  "grading:d4c5f9" \
  "emelt:5319e7" \
  "catalog:fbca04" \
  "ux:e99695" \
  "beta:0e8a16" \
  "i18n:c5def5" \
  "content:fef2c0" \
  "kozep:7057ff" \
  "existing:c2e0c6" \
  "convert:fbca04" \
  "new:1d76db" \
  "testing:0075ca" \
  "ci:0075ca" \
  "staging:006b75" \
  "production:5319e7" \
  "security:d73a4a" \
  "ops:006b75"; do
  ensure_label "${pair%%:*}" "${pair##*:}"
done

M1=$(create_milestone \
  "Platform: Sandbox edge cases" \
  "Tier B platform blockers for faithful 10+10 exam launch (stdin, random seed, function preamble, aux files). AI out of scope." \
  "2026-09-14T23:59:59Z")

M2=$(create_milestone \
  "UX: Public beta (közép)" \
  "Student-facing polish: resume workspace, Hungarian UI, discovery, grading feedback. Auth deferred." \
  "2026-09-21T23:59:59Z")

M3=$(create_milestone \
  "Catalog: 10 közép exams" \
  "Launch közép set covering sandbox edge-case matrix. Target audience for public beta." \
  "2026-10-12T23:59:59Z")

M4=$(create_milestone \
  "Catalog: 10 emelt exams" \
  "Launch emelt set covering emelt sandbox coordinates. Exclude partial-grade mrz-kod unless fully wired." \
  "2026-10-12T23:59:59Z")

M5=$(create_milestone \
  "Quality: Oracle tests & CI" \
  "Per-exam builder tests, materialize-all CI, staging Run+Submit smoke." \
  "2026-10-05T23:59:59Z")

M6=$(create_milestone \
  "Production: Beta launch" \
  "CORS, rate limits, workspace cleanup, launch sign-off. Docker executor and full auth deferred." \
  "2026-10-17T23:59:59Z")

log "Milestone numbers: M1=$M1 M2=$M2 M3=$M3 M4=$M4 M5=$M5 M6=$M6"

# --- M1 Platform ---
create_issue "$M1" "Per-test-case stdin in exam materialization" \
'## Goal
Allow different `stdin` values per test case (sample vs each hidden dataset).

## Why
Today `templates.py` copies a single `task.stdin` to every `TestCase`. This blocks Fogások, Hűtőház, and Virágágyások hidden quality.

## Acceptance criteria
- [ ] Template supports per-hidden stdin
- [ ] Judge pipes correct stdin per test case
- [ ] Unit test with two hidden cases using different stdin

## References
- `backend/app/services/templates.py`
- `.cursor/skills/erettsegi-to-catalog/reference.md`' \
  platform grading

create_issue "$M1" "Inject random.seed from exam template" \
'## Goal
Support `[random]` közép exams with deterministic grading.

## Acceptance criteria
- [ ] Optional `seed` on `template.json`
- [ ] Preamble prepends `import random` + `random.seed(N)`
- [ ] Builders compute expected output with the same seed
- [ ] Smoke test with one random közép feladat' \
  platform grading

create_issue "$M1" "Named function block in exam preamble" \
'## Goal
First-class support for emelt `Készítsen függvényt …` subtasks.

## Acceptance criteria
- [ ] Template field for function body (structured preamble)
- [ ] Hűtőház `percben` works end-to-end after conversion
- [ ] Document in erettsegi-to-catalog skill' \
  platform emelt

create_issue "$M1" "Read-only auxiliary files in template" \
'## Goal
Ship lookup tables (Palacsinta, Szólánc) without hidden-swapping.

## Acceptance criteria
- [ ] `aux_files` on template copied into workspace as read-only
- [ ] Only primary `data_file` swaps on hidden tests' \
  platform catalog

# --- M2 UX ---
create_issue "$M2" "Resume workspace across sessions" \
'## Goal
Students return to saved work instead of a new workspace every visit.

## Acceptance criteria
- [ ] Persist workspace_id per exam (localStorage or URL)
- [ ] Reload when valid; explicit reset for new workspace
- [ ] Anonymous users supported

## Ref
`frontend/src/components/ExamWorkspace.tsx`' \
  ux beta

create_issue "$M2" "Hungarian student-facing UI copy" \
'## Acceptance criteria
- [ ] Homepage and exam list in Hungarian
- [ ] Run / Submit / Save / feladat labels in Hungarian
- [ ] Loading and error states in Hungarian' \
  ux beta i18n

create_issue "$M2" "Exam discovery filters on homepage" \
'## Acceptance criteria
- [ ] Filter by level (közép / emelt)
- [ ] Filter or sort by difficulty
- [ ] Show tags on exam cards' \
  ux beta

create_issue "$M2" "Show story, constraints, and data explanation in workspace" \
'## Acceptance criteria
- [ ] Story/scenario visible in problem panel
- [ ] Constraints and data_explanation visible
- [ ] Minta stdin hint for interactive feladatok' \
  ux beta

create_issue "$M2" "Hungarian execution and grading error messages" \
'## Acceptance criteria
- [ ] Timeout and runtime errors in Hungarian
- [ ] Wrong answer vs runtime fail distinguished on Submit
- [ ] Hidden tests still hide expected/actual' \
  ux beta

# --- M3 Közép catalog ---
kozep_issue() {
  local title="$1"
  local status="$2"
  local desc="$3"
  create_issue "$M3" "[közép] ${title}" \
"## Launch slot: közép exam
**Status:** ${status}

${desc}

## Checklist
- [ ] template.json + builders.py if needed
- [ ] visible + 3 hidden datasets
- [ ] Oracle test in backend/tests/
- [ ] Run + Submit smoke" \
    content kozep "$status"
}

kozep_issue "Városok (cities) — verify launch set" existing \
  "File read + hidden swap. Keep as easy onboarding."
kozep_issue "Versenyidő — verify launch set" existing \
  "File + sum/avg/max chain."
kozep_issue "Fogások — convert from synthetic MD" convert \
  "Convert synthetic/kozep/2027_majus_fogasok.md. Requires per-test stdin."
kozep_issue "Robot — new catalog exam" new \
  "Path/command simulation (E/D/K/N)."
kozep_issue "Liftvezérlő — new catalog exam" new \
  "Random state — requires random.seed platform fix."
kozep_issue "Szólánc — new catalog exam" new \
  "Interactive loop + lookup table (aux file)."
kozep_issue "Palacsinta — new catalog exam" new \
  "Table-driven pricing with read-only price table."
kozep_issue "Létra or Szállítás — new catalog exam" new \
  "Board simulation or greedy packing."
kozep_issue "Kerékpárállomás — verify or replace" existing \
  "Threshold count + tie-breaking; replace if redundant."
kozep_issue "Befőzés or Kihívás — new catalog exam" new \
  "Series with bonus rules / exact-string branches."

# --- M4 Emelt catalog ---
emelt_issue() {
  local title="$1"
  local status="$2"
  local desc="$3"
  create_issue "$M4" "[emelt] ${title}" \
"## Launch slot: emelt exam
**Status:** ${status}

${desc}

## Checklist
- [ ] template.json + builders.py
- [ ] visible + 3 hidden datasets
- [ ] Oracle test
- [ ] Do not ship partial (see mrz-kod)" \
    content emelt "$status"
}

emelt_issue "Virágágyások — verify launch set" existing \
  "Gold reference: interval overlap, stdin, output file."
emelt_issue "Hűtőház — convert from synthetic MD" convert \
  "Convert synthetic/emelt/2027_oktober_hutohaz.md."
emelt_issue "Menetlevél / fuvar — new catalog exam" new \
  "Header + fixed records + grouping."
emelt_issue "Beléptető-style — new catalog exam" new \
  "Paired in/out event matching."
emelt_issue "Kép / rács — new catalog exam" new \
  "2-D grid parse and reasoning."
emelt_issue "Pénztár-style — new catalog exam" new \
  "Sentinel-delimited stream."
emelt_issue "Lookup join — new catalog exam" new \
  "Aux lookup table + transaction join."
emelt_issue "Ütemezés-style — new catalog exam" new \
  "Second emelt with [function] subtask."
emelt_issue "Kert / output file — new catalog exam" new \
  "Second expected_file output grading exam."
emelt_issue "Validáló lánc — new catalog exam" new \
  "Validate + simulation chain."

# --- M5 Quality ---
create_issue "$M5" "Extend builder test suite for all launch exams" \
'## Acceptance criteria
- [ ] Oracle tests for all 20 launch exams
- [ ] Visible + hidden expected outputs verified
- [ ] pytest runs on PR' \
  testing ci

create_issue "$M5" "CI: materialize all catalog exams on PR" \
'## Acceptance criteria
- [ ] GitHub Actions on PR
- [ ] All catalog folders materialize without error' \
  testing ci

create_issue "$M5" "Staging smoke: Run + Submit one feladat per exam" \
'## Acceptance criteria
- [ ] E2E script against staging API
- [ ] At least feladat 1 per exam passes judge' \
  testing staging

# --- M6 Production ---
create_issue "$M6" "Lock CORS to Vercel production origin" \
'## Acceptance criteria
- [ ] CORS_ORIGINS set to production Vercel URL
- [ ] Cloud Run redeployed' \
  production security

create_issue "$M6" "Rate limit /execute and /judge" \
'## Acceptance criteria
- [ ] Rate limit by IP or fingerprint
- [ ] 429 with Hungarian message' \
  production security

create_issue "$M6" "Workspace TTL and cleanup job" \
'## Acceptance criteria
- [ ] Delete workspaces older than N days
- [ ] Documented cron or sweep' \
  production ops

create_issue "$M6" "Beta launch checklist and smoke sign-off" \
'## Acceptance criteria
- [ ] M1 + M2 blockers closed
- [ ] 10 közép + 10 emelt in production Neon
- [ ] CI and staging smoke green
- [ ] AI_GENERATION_ENABLED=false
- [ ] Known limitations documented' \
  production beta

log "Done. See https://github.com/${REPO}/milestones"

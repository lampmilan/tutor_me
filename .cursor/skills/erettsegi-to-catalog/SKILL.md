---
name: erettsegi-to-catalog
description: >-
  Convert a named Hungarian Informatika / Digitális kultúra érettségi exam from
  a sanitized MD corpus into a tutor_me catalog exam (template.json, datasets,
  per-exam builders.py parser + task builders). Use when the user names an exam
  to convert, points at a sanitized MD file, or asks to materialize an exam
  under backend/app/exams like viragagyasok.
---

# MD exam → tutor_me catalog

Convert **one named exam** from a sanitized MD corpus into a live catalog folder.

**Never edit** the source MD files. They are read-only.

Field-level mapping, gold exam, and builder patterns: [reference.md](reference.md).

## Inputs

- **Exam name** (required): heading under `###`, e.g. `Virágágyások`, `Toronyépítés`
- **MD file** (optional): if omitted, search both corpora when those paths exist:
  - `h:\obsidian\personal\personal\Informatika and Digitális kultúra érettségi - Sanitized.md`
  - `h:\obsidian\personal\personal\Informatika and Digitális kultúra érettségi EMELT  - Sanitized.md`
  - Cloud / other machines: ask for the MD path or contents if those drives are missing
- **Output root**: `backend/app/exams/` (same as `f:\github\tutor_me\backend\app\exams\` on the author's machine)

Gold reference (read before writing): `backend/app/exams/viragagyasok/` (folder + `builders.py` + `template.json`).

## Non-negotiables

1. **One folder per exam, one `.py` per feladat.** Never one file for the whole exam. Do not concatenate previous student files.
2. **Python filenames** — never bare `monitor.py`, `beolvasas.py`, `parse.py`. Always `{exam_id}_{slug}.py` so workspace/DB files cannot collide across exams. Same `{id}` prefix for parser/builder **function names**.
3. **JSON fields** (copy, do not invent):

   `"id": "toronyepites"` ← same name as the exam, but only `a-z` and `_`
   `"title": "Toronyépítés"` ← same as the exam in the MD
   `"difficulty"` ← from the MD, integer 1–5
   `"tags"` ← copy the exam-level MD tags as-is (`IO`, `count`, …). Do **not** translate to the old live-exam vocabulary (`list`, `loops`, `counting`)
   `"story"` ← copy the Scenario section from the MD
   `"constraints"` ← copy from Constraints; also use this when generating datasets
   `"data_explanation"` ← copy the Explanation under Data
4. **Student runtime is a raw string**, not a parsed list and not a file handle.
   - Feladat 1: student `open` + `f.read()` into `shared_variable`. `uses_preamble: false`.
   - Later feladats: preamble re-reads the **mounted** `data_file` at run time into that same string. Students split/convert themselves.
   - Do **not** inject extra derived variables (`agyasok_szama`, parallel arrays).
   - Do **not** bake the visible dataset into the preamble as a Python string literal (hidden tests swap the file on disk).
5. **Expected outputs are computed**, never stored in `template.json`. Add `parse` + one builder per custom task in **this exam's** `builders.py`. Do not use `literal` when the answer depends on the dataset. Do **not** append exam-specific types to the global `backend/app/exams/builders.py`.
6. **`input()` is real.** Pipe values via `stdin`. Do not monkeypatch or silence `input()`. Official prompt lines belong in expected stdout.
7. **Do not overwrite** an existing `exams/{id}/` folder unless the user asked to replace it.
8. The LLM may rewrite story text only. Never grading rules.

## Workflow

```
Task Progress:
- [ ] Locate ### ExamTitle in the MD (read-only)
- [ ] Derive exam_id; refuse if folder exists (unless replace)
- [ ] Map JSON + tasks from MD
- [ ] Implement exams/{id}/builders.py (parse + TASK_BUILDERS)
- [ ] Generate visible.txt (Constraints + sample; builders must match MD Expected I/O)
- [ ] Generate 3 hidden datasets (edge cases from Constraints)
- [ ] Write exams/{id}/template.json
- [ ] Checklist
```

### 1. Look up

Find `### {ExamTitle}` (accent-insensitive). Read through the next `---` / `###`. If missing, list nearby titles. If two hits, ask.

### 2. `exam_id`

Lowercase; strip accents (`á→a`, `é→e`, `í→i`, `ó/ö/ő→o`, `ú/ü/ű→u`); spaces/hyphens → `_`; drop other punctuation; **only `a-z` and `_`**. Collapse repeat `_`.

`Virágágyások` → `viragagyasok`. `MRZ kód` → `mrz_kod` (new exams; do not create hyphenated ids like legacy `mrz-kod`).

Folder name **is** `id`. Loader discovers any folder with `template.json` — do not edit `loader.py`.

### 3. Catalog folder

```
backend/app/exams/{id}/
  template.json
  builders.py                 # required for custom types; skip only if every task is a generic aggregator
  datasets/visible.txt
  datasets/hidden/01.txt
  datasets/hidden/02.txt
  datasets/hidden/03.txt
```

Do **not** put solution `.py` files in this folder. Names live in `solution_file`; starters live in JSON.

### 4. `template.json` (beyond the required copies)

Schema: `backend/app/schemas/templates.py`. Details: [reference.md](reference.md).

| Field | Rule |
|---|---|
| `level` | `közép` → `kozep`, `emelt` → `emelt` |
| `description` | One Hungarian imperative line (title + data file) |
| `data_file` | First filename under **files:** (else `{id}.txt`) |
| `dataset_type` | `{id}` (this exam's `parse`; do not reuse `cities` / `temperatures`) |
| `shared_variable` | Hungarian plural of the main records (`felajanlasok`) — this is a **str** |
| `preamble` | Canonical UTF-8 **raw read** of `data_file` into `shared_variable` (see below). If the MD has a named `[function]` subtask, append a correct implementation **after** the read so later tasks can call it |
| `visible` / `hidden` | `datasets/visible.txt` and `datasets/hidden/01.txt` … `03.txt` |

Canonical preamble (always this shape; materializer also generates it if omitted):

```python
with open("felajanlas.txt", encoding="utf-8") as f:
    felajanlasok = f.read()
```

### 5. Tasks

One JSON task per numbered MD task. Nested `1.` / `2.` / `3.` under a parent stay **one** task (see Virágágyások 4).

| Field | Rule |
|---|---|
| `type` | `{id}_{slug}` unless a **generic** builder already emits the exact stdout (bare number / name). Formatted Hungarian lines → custom type in **this exam's** `TASK_BUILDERS` |
| `tags` | The `[tag]` markers on that task, same closed list |
| `title` | Short Hungarian label (`Beolvasás`, `szinek.txt`) |
| `description` | Full MD task text, including nested parts and exact strings |
| `points` | 1 = load/count; 2 = search/validate; 3 = nested / file-write / simulation |
| `solution_file` | `{id}_{slug}.py` — **always** on new exams |
| `uses_preamble` | `false` on task 1 (student loads); `true` after |
| `starter` | Hungarian comments + stub. Variable is `(str)`. No parsed tuple/list examples. Print prompts for `IO`; `open` stub for file-write |
| `stdin` | Values only from `input(…)` in Expected Input, each on its own line, trailing `\n`. Copied onto every test case (platform limit) |
| `expected_file` | Output filename if the task writes a file (stdout then ignored by judge). Do not ship that file as an editable workspace file |
| `hints` | English, dataset-general (not sample-specific numbers) |
| `field` / `label_field` / `op` / `value` | Only for generic aggregators |

Flatten nested Expected I/O into **one** builder that prints prompts + all sub-answers in order.

`[function]` task: `store`-like empty stdout; starter has the signature; working body goes in `preamble` **after** `f.read()`.

### 6. `exams/{id}/builders.py` (oracle — students never see this)

Contract the loader imports **by path**:

```python
def parse(content: str) -> list[dict]:
    ...

TASK_BUILDERS = {
    "toronyepites_monitor": _task_toronyepites_monitor,
}
```

Internally name functions `parse_{id}` (alias as `parse`) and `_task_{id}_{slug}`. Keys in `TASK_BUILDERS` are the JSON `type` strings.

Builders must:

- Include **prompt lines** in expected stdout (student `print`s them; typed values are stdin, not stdout)
- Emit **Exact strings** from the MD
- For `expected_file` tasks, return the **file body** (not screen text)
- Derive every number from `rows` + `spec["stdin"]`, never from the MD sample literals
- Put file-global facts (`n_beds`) on every row so builders can read `rows[0]`

Generic types (`store`, `count`, `sum`, `maximum`, `minimum`, `average`, `count_where`, `read`) live in `backend/app/exams/builders.py`. Reuse them **only** when stdout is exactly what they already produce. `store` = empty stdout (load-only / function-def). `literal` is last resort (missing auxiliary file, unseeded random) — never for data-dependent answers.

Do not register this exam in the global `PARSERS` / `TASK_BUILDERS` dicts.

### 7. Datasets

**Visible** must make builders reproduce the MD **Expected Output** / `output(…)` values.

- Start from the Data **Sample**
- **Also use Constraints** when generating the example file (ranges, wrap-around, counts, forbidden values)
- If the sample is truncated (`files:` says 466 lines, sample shows 5), synthesize the rest under Constraints so sample I/O still holds. Prefer a known official file if it already exists in the repo (e.g. viragagyasok `visible.txt`)
- No Data section (fully interactive): still create `data_file` (may be empty/minimal). Hidden file swaps will not change stdin-only answers — that is a platform limit; do not fake `literal` hidden tests as if they varied

**Hidden (3 files):** smaller than visible; still legal under Constraints; hit edge cases named in Constraints (empty/uncovered, wrap, ties, zero hits). Hardcoding the sample answer must fail.

### 8. Extra MD sections

- **Example:** optional; may inform starters, not JSON `story`
- **Tables:** parse into a `dict`/`list` in `preamble` **after** the raw `f.read()` (platform has one swappable `data_file`)
- **Exact strings:** already in descriptions + builders
- Extra input files (`kodok.txt`, `egytanulo.txt`): constant lookup → preamble literal after the read. Student-written → `expected_file`. Second swappable input file is **not** supported; say so if the exam needs it
- `[random]` / unseeded output: cannot exact-match grade; `store` or skip hidden; note it in the wrap-up

## Student vs oracle

| Layer | What it sees |
|---|---|
| Feladat 1 code | Must `open(data_file)` and `.read()` into `shared_variable` |
| Feladat 2+ code | Preamble already set `shared_variable` to `f.read()` of the **current** data file (visible or hidden) |
| Oracle / hidden tests | `parse(dataset)` + `TASK_BUILDERS[type](rows, spec)` |

## Checklist

- [ ] Source MD not modified
- [ ] `id` is `[a-z_]+`; `title` / `difficulty` (1–5) / `tags` / `story` / `constraints` / `data_explanation` copied
- [ ] Every `solution_file` is `{id}_*.py`; every builder/parser function is `{id}`-prefixed
- [ ] `dataset_type` == `{id}`; `parse` lives in `exams/{id}/builders.py` (not the global registry)
- [ ] Each custom task `type` is a key in that file's `TASK_BUILDERS`; no `literal` for data-dependent answers
- [ ] Preamble is runtime `f.read()` into one string; no parsed list / extra derived vars
- [ ] Starters say `(str)` and describe the **file** format, not a parsed record
- [ ] Visible builders match MD sample I/O (prompts + exact strings)
- [ ] Three hidden files obey Constraints and break hardcoded sample answers
- [ ] Task 1 `uses_preamble: false`; later file-using tasks `true`
- [ ] `stdin` / `expected_file` set when the MD has input / output files
- [ ] Separate `.py` per feladat; existing `exams/{id}/` not overwritten unless asked
- [ ] API seed rematerializes after catalog edits (preamble/starter change is detected)

## Wrap-up

Tell the user the new `exam_id`, folder path, which tasks used custom vs generic types, and any platform gaps (second input file, `[random]`, stdin identical on hidden tests). Restart the API (or wait for startup seed) so the exam is materialized.

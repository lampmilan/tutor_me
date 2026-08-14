---
name: erettsegi-to-catalog
description: Convert an official Hungarian informatika érettségi programming exam (PDF, feladatsor, mintamegoldás, adatfájl) into this repo's exam catalog under backend/app/exams/<id>/. Use when adding a new érettségi exam, importing a feladatsor, or authoring template.json / datasets / builders.py.
---

# Érettségi → catalog

Turn one official programming exam into a catalog folder. Keep the real exam hard; do not streamline student work.

## Non-negotiables

- **One folder per exam**, one **`.py` per feladat**. Never one file for the whole exam.
- **Feladat 1** reads the data file and stores it as a **string** (`f.read()`). `uses_preamble: false`.
- **Later feladats** get that same string via preamble, injected at **run time** from the mounted data file. Students split/convert/filter themselves.
- Do **not** inject a parsed list, dict, tuples, or an open file handle.
- Do **not** inject extra derived variables (`agyasok_szama`, parallel arrays). Those are the student's job.
- Do **not** bake the visible dataset into the preamble as a Python string literal (hidden tests swap the file on disk).
- **Expected outputs are never authored** in `template.json`. The oracle computes them from each dataset.
- **`input()` is real.** Put sample/hidden answers in `stdin`. Do not monkeypatch or silence `input()`. Official prompt lines belong in expected stdout.
- **Output files** (e.g. `szinek.txt`) use `expected_file`. Students write them in code; do not add them as editable workspace files.
- The LLM may rewrite story text only. Never grading rules.

## Layout

```text
backend/app/exams/<exam-id>/
  template.json
  builders.py          # only if generic task types cannot grade this exam
  datasets/
    visible.txt        # student-visible data file
    hidden/
      01.txt           # mounted as data_file at judge time
      02.txt
```

`<exam-id>` may contain hyphens (`mrz-kod`). Loaders import `builders.py` **by path**, not as a Python package.

Shared generics live in `backend/app/exams/builders.py`:
`read`, `count`, `maximum`, `minimum`, `sum`, `average`, `count_where`, `literal`, `store`.

## Workflow

1. Read the official feladatsor + mintamegoldás + sample data file.
2. Choose a slug (`viragagyasok`, `mrz-kod`). Create the folder.
3. Copy the official sample into `datasets/visible.txt` (normalize to UTF-8, trailing newline).
4. Author 3–4 **hidden** datasets in the same format. Vary sizes and edge cases the mintamegoldás cares about (empty intervals, wrapping, ties, male vs female MRZ, …).
5. Write `template.json` (schema: `backend/app/schemas/templates.py`).
6. If every feladat is a generic aggregator, stop. Otherwise add `builders.py` with `parse(content) -> list[dict]` and `TASK_BUILDERS`.
7. Starters: feladat 1 scaffolds `shared_variable = ""`. Later starters say the variable is `(str)` and describe the **file** format, not a parsed record.
8. Seed rematerializes when preamble/starters change. Restart the API (or wait for startup seed) after catalog edits.

## `template.json` fields that matter

| Field | Rule |
|---|---|
| `id` | Folder name |
| `data_file` | Workspace filename students `open()` (`felajanlas.txt`) |
| `dataset_type` | Shared parser key, or unused when `builders.py` defines `parse` |
| `shared_variable` | Name of the injected **string** (`felajanlasok`, `mrz`) |
| `preamble` | Prefer omitted — materializer generates `with open(data_file) as f: var = f.read()`. If set, it must be that raw-string form |
| `visible` / `hidden` | Paths relative to the exam folder |
| `tasks[].type` | Shared generic **or** a key in this exam's `TASK_BUILDERS` |
| `tasks[].uses_preamble` | `false` on feladat 1; `true` after |
| `tasks[].solution_file` | Separate `.py` per feladat |
| `tasks[].stdin` | Piped into the process for `input()`. Same value is copied onto every test case unless you extend hidden stdin later |
| `tasks[].expected_file` | Grade this output file instead of stdout |
| `tasks[].starter` | Comments + stub only. No worked solution. No tuple/list examples of parsed rows |

## Per-exam `builders.py` contract

Students never import this. The judge does.

```python
def parse(content: str) -> list[dict]:
    ...

TASK_BUILDERS = {
    "offer_count": lambda rows, spec: "...",
}
```

- `parse` is the **oracle** representation, not what the student receives.
- Task functions return the exact official stdout (or file body), including Hungarian punctuation.
- Put exam-specific types here (`offer_count`, `bed_query`, `gender`, `mrz_name`). Do not add them to the global registry.
- Keep using shared types (`count`, `maximum`, …) when they already match.
- `literal` is a last resort (checksum tables, missing auxiliary files). Prefer a real builder so hidden tests work.

## Student vs oracle

| Layer | What it sees |
|---|---|
| Feladat 1 code | Must `open(data_file)` and `.read()` into `shared_variable` |
| Feladat 2+ code | Preamble already set `shared_variable` to `f.read()` of the **current** data file (visible or hidden) |
| Oracle / hidden tests | `parse(dataset)` + `TASK_BUILDERS[type](rows, spec)` |

## `input()` and extra files

- Keyboard input: `stdin` on the task. Frontend Run already sends it. Judge uses each test case's `stdin`.
- Prompts: if the mintamegoldás does `print("Adja meg…")` then `input()`, that print **is** part of expected output. `input("…")` has no newline and will not match.
- Student output files: `expected_file` + oracle returns the file body. Isolation copies the workspace so writes do not pollute the editor.
- Extra **input** tables (`kodok.txt`): add them as exam files (read-only) or the feladat cannot be graded. Hidden tests only swap `data_file`.

## Checklist before merging a new exam

- [ ] Separate `.py` per feladat; no single-file exam
- [ ] Preamble is runtime `f.read()` into one string variable
- [ ] Starters never show parsed tuples/lists as the injected type
- [ ] Feladat 1 `uses_preamble: false`; later tasks `true`
- [ ] Hidden datasets exist and are not copies of visible
- [ ] Unique logic is in `exams/<id>/builders.py`, not `exams/builders.py`
- [ ] `input()` feladats have `stdin`; prompt text is in the oracle output
- [ ] File-output feladats have `expected_file`; no pre-created editable output file
- [ ] Expected strings match the mintamegoldás byte-for-byte after trailing-whitespace normalize
- [ ] API seed rematerializes (preamble/starter change is detected)

## Examples in this repo

- Generic aggregators only: `cities`, `trains`, `temperatures`, `students`
- Exam-specific oracle: `viragagyasok/builders.py`, `mrz-kod/builders.py`
- `stdin` + `expected_file`: Virágágyások feladats 4 and 6

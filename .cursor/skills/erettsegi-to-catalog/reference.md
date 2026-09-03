# Catalog conversion reference

Read this after the skill workflow. Gold exam: `backend/app/exams/viragagyasok/`.

New conversions follow this file. Legacy folders (`mrz-kod` hyphen, unprefixed `beolvasas.py`, global-ish task types like `offer_count`) are **not** the template for new exams.

## MD block (do not write into corpora)

```md
### ExamTitle
#### Meta          level, year, session, language, difficulty 1-5
#### Tags          closed list (exam-level)
#### Scenario      → story
#### Constraints   → constraints[] and dataset generation
#### Example       optional mini-example (not story)
#### Data          files / Sample / Explanation → data_file, visible, data_explanation
#### Tables        optional; bake into preamble after f.read()
#### Tasks         numbered, [tags], nested subtasks, Expected Input/Output
#### Exact strings mandatory print phrases
```

Closed tags (exam + task): `IO`, `count`, `sum`, `min_max`, `search`, `validate`, `simulation`, `group`, `string`, `path`, `table`, `lookup`, `function`, `random`, `weighted_sum`.

## `exam_id` accents

| From | To |
|---|---|
| á à â ä ã Á | a |
| é è ê ë É | e |
| í ì î ï Í | i |
| ó ò ô ö õ ő Ó Ö Ő | o |
| ú ù û ü ű Ú Ü Ű | u |
| space, hyphen | `_` |

Drop everything that is not `a-z` or `_`. Collapse repeat `_`. Folder name equals `id`.

## Platform facts

- Catalog = folder with `template.json` + datasets. Optional `builders.py` next to them. `loader.py` discovers any such folder (by path, so hyphens would load, but **new ids use only `a-z_``**).
- Seeding materializes DB rows; `solution_file` becomes an `ExamFile` and workspace file. **That is why names must be globally unique:** `{id}_{slug}.py`.
- Judge runs `preamble + student code` when `uses_preamble` is true. Hidden tests replace **only** `data_file`. `stdin` is the same string on sample and hidden.
- If `expected_file` is set, judge compares that file’s contents, not stdout.
- Student variable is the **file text** (`str`). The oracle `parse()` is independent and never shown to the student.
- Schema: `backend/app/schemas/templates.py`.
- Shared generics: `backend/app/exams/builders.py`. Exam-specific oracles: `backend/app/exams/{id}/builders.py`.

## Generic builders (reuse only if stdout matches exactly)

| `type` | stdout |
|---|---|
| `store` | `""` |
| `count` | `str(len(rows))` |
| `sum` / `average` / `maximum` / `minimum` | number or `label_field` |
| `count_where` | needs `field`, `op`, `value` |
| `read` | dumped rows |
| `literal` | **do not use** for data-dependent tasks (same expected on every hidden file) |

Érettségi tasks almost always need `{id}_{slug}` because stdout is a Hungarian sentence.

## Builder stdout vs MD Expected I/O

MD:

```
Adja meg az ágyás sorszámát! input(100)
A felajánlók száma: output(8)
```

`stdin`: `"100\n"`

Builder stdout (prompt, no typed value):

```
Adja meg az ágyás sorszámát!
A felajánlók száma: 8
```

Compute `8` from rows, do not hard-code it.

`input("prompt")` writes a prompt **without** a newline and will not match. Starters should `print` the prompt, then leave `var = ` so the student writes `input()` themselves.

## Starter pattern (new exams)

Task 1 (`uses_preamble: false`):

```python
# 1. feladat: olvassa be a felajanlas.txt tartalmát.
# Tárolja az állomány tartalmát a 'felajanlasok' változóban mint string (szöveg).

felajanlasok = ""
```

Do **not** add schema crumbs (`# op arg`, `# ora perc tipus`, `# Sorok: …`). File layout belongs in `data_explanation` and the feladat text.

Later (`uses_preamble: true`):

```python
# A felajanlas.txt tartalma a 'felajanlasok' változóban van szöveges formában.
# Elvárt kimenet: 'A felajánlások száma: x'
```

Several lines:

```python
# A felajanlas.txt tartalma a 'felajanlasok' változóban van szöveges formában.
# Elvárt kimenetek:
# 'A racspontok szama: x'
# 'A legkisebb melyseg: y cm'
```

A short domain reminder is fine when the rule is not obvious (`# 16 állomás, átrakó: 4, 9, 13 (+2 ugrás).`). Do **not** leave `# Title` leftovers or empty `print(f"…")` stubs.

Do **not** tell them it is a list of tuples, and do **not** mention `agyasok_szama` as already injected.

IO: print the prompt, then `var = ` (student writes `input()`). File-write: `with open("szinek.txt", "w", encoding="utf-8") as f: pass`. Function tasks keep the `def` stub.

Hints are Hungarian, method-level, and dataset-general (e.g. `open` + `read`, `split` / `splitlines`). Not English generics like “Derive the answer…”.

## Preamble

Always start with a runtime read (so hidden swaps work):

```python
with open("felajanlas.txt", encoding="utf-8") as f:
    felajanlasok = f.read()
```

Allowed **after** that line, not instead of it:

- `[function]` task: set `functions` on the exam template with the named function body later tasks may call (appended after the load block in the composed preamble)
- **Tables** / constant extra files (`kodok.txt`): use `aux_files: [{filename, content, read_only}]` (not swapped by hidden tests) or a literal `dict`/`list` in `functions`

Never:

- Parsed records (`felajanlasok = []` + `.append`)
- Extra derived scalars (`agyasok_szama = int(...)`)
- `open(...).read()` baked as a triple-quoted copy of `visible.txt`
- An open file handle left for `.read()` in student code

## Virágágyások mapping (gold)

MD `### Virágágyások` → folder `viragagyasok`.

| JSON | Source |
|---|---|
| `id` | `viragagyasok` |
| `title` | `Virágágyások` |
| `level` | `emelt` |
| `origin` | `official` |
| `difficulty` | `4` |
| `tags` | `["IO","count","search","validate","simulation"]` |
| `story` | full Scenario paragraph |
| `constraints` | the three MD bullets |
| `data_explanation` | paragraph after `Explanation:` |
| `data_file` | `felajanlas.txt` |
| `dataset_type` | `viragagyasok` |
| `shared_variable` | `felajanlasok` |
| `preamble` | raw `f.read()` into `felajanlasok` (or omit — platform default) |
| `functions` | optional named helpers for `[function]` tasks (e.g. `percben`) |
| `seed` | optional `random.seed(N)` injected at preamble start for `[random]` tasks |
| `aux_files` | optional read-only lookup tables (e.g. `kodok.txt`) |

**New conversions must prefix `solution_file` and custom `type`.** Legacy viragagyasok uses `beolvasas.py` and `offer_count`; a new exam named similarly would use `viragagyasok_beolvasas.py` and `viragagyasok_offer_count`.

| MD task | `type` (new style) | `solution_file` (new style) | notes |
|---|---|---|---|
| 1 IO load | `store` | `{id}_beolvasas.py` | empty expected |
| 2 count | `{id}_offer_count` | `{id}_felajanlasok_szama.py` | formatted sentence |
| 3 wrap search | `{id}_wrap_offers` | `{id}_bejart.py` | |
| 4 nested IO | `{id}_bed_query` | `{id}_egy_agyas.py` | `stdin: "100\n"`; `hidden_stdin: ["1\n", ...]` per hidden dataset |
| 5 validate | `{id}_planting_status` | `{id}_megoldhatosag.py` | exact strings |
| 6 file write | `{id}_colors_file` | `{id}_szinek.py` | `expected_file: "szinek.txt"` |

Visible = official sample (first line bed count, then offers). Hidden 01–03 = smaller legal files: wrap-around (`start > end`), full coverage vs gaps, bed 100-like queries still in range.

## `exams/{id}/builders.py` sketch

```python
from __future__ import annotations

from typing import Any, Callable

from app.exams.builders import Row, _nonempty_lines


def parse_toronyepites(content: str) -> list[Row]:
    rows: list[Row] = []
    for i, line in enumerate(_nonempty_lines(content), start=1):
        parts = line.split()
        rows.append({"index": i, "field": parts[0], ...})
    return rows


def parse(content: str) -> list[Row]:
    return parse_toronyepites(content)


def _task_toronyepites_monitor(rows: list[Row], spec: dict[str, Any]) -> str:
    ...


TASK_BUILDERS: dict[str, Callable[[list[Row], dict[str, Any]], str]] = {
    "toronyepites_monitor": _task_toronyepites_monitor,
}
```

Parser: one `Row` dict per record. Put file-global facts (`n_beds`) on every row so builders can read `rows[0]`. Skip blank lines.

Do **not** add `PARSERS["toronyepites"] = ...` to the global module.

## Dataset generation

Use **Constraints** for both visible (example) and hidden:

- Honor maxima (`Ágyások <= 3000`)
- Honor format (fields, separators, wrap rule)
- Honor suggested test keys (`ágyás 1`, `269`)
- Visible: builders(visible, stdin) == MD Expected Output
- Hidden: different answers; include at least one edge named in Constraints

Közép “hardcode the array in source”: still emit `data_file` + preamble load so hidden swaps work. Task 1 description may keep the MD wording; starter should read the file (platform adaptation). Mention that in the wrap-up.

## Points heuristic

| Shape | Points |
|---|---|
| Load / print count | 1 |
| Single search, min/max, simple validate | 2 |
| Nested 2–3 questions, simulation, output file | 3 |

Sum does not need to match a real OH paper.

## Platform fields (M1)

| Field | Where | Purpose |
|---|---|---|
| `stdin` | task | Sample / visible test stdin |
| `hidden_stdin` | task | List aligned with `hidden[]`; overrides stdin per hidden test case |
| `seed` | exam | Prepends `import random` + `random.seed(N)` to preamble; oracles use the same seed |
| `functions` | exam | Named function bodies appended after the file-load preamble |
| `aux_files` | exam | Read-only extra files copied into the workspace (not swapped on hidden tests) |

## Out of scope without extra code

- Two independently swapped input files (loader has one `data_file`)
- Unseeded `[random]` exact grading (use `seed` on the template)
- One `.py` for the whole exam (explicitly rejected)
- Injecting a parsed list or file handle to “make later tasks easier”

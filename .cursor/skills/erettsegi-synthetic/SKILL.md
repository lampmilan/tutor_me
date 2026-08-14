---
name: erettsegi-synthetic
description: >-
  Generate or revise Hungarian Informatika / Digitális kultúra érettségi
  (közép or emelt) algoritmizálás exams as sanitized MD under
  .cursor/skills/erettsegi-synthetic/synthetic/. Use when the user asks for
  synthetic érettségi, exam tasks, Digkult/Informatika MD, or official-quality
  tutoring corpora. Do not write catalog folders (that is erettsegi-to-catalog).
---

# Érettségi synthetic exam generation

Write **new sanitized MD exams** that match official OH quality. Compare against **read-only official** papers; never mix gold and generated text in one file.

Conversion to `backend/app/exams/` is **`erettsegi-to-catalog`**. This skill must not touch the catalog.

Full manifesto: [GUIDE.md](GUIDE.md).

## Layout

```text
.cursor/skills/erettsegi-synthetic/
  SKILL.md
  GUIDE.md
  official/                         # READ-ONLY gold (quality comparison)
    kozep.md
    emelt.md
    exam_as_text/                   # tone / blocklist source
  synthetic/                        # the only writable output
    kozep/{year}_{session}_{id}.md
    emelt/{year}_{session}_{id}.md
```

Local Obsidian copies (if those drives exist) are optional mirrors, **not** the SSOT in this repo:

- `h:\obsidian\personal\personal\Informatika and Digitális kultúra érettségi - Sanitized.md`
- `h:\obsidian\personal\personal\Informatika and Digitális kultúra érettségi EMELT  - Sanitized.md`

If both exist, still **write only** `synthetic/{level}/…`. Never append to `official/` or to the Obsidian gold files.

**Always read GUIDE.md + 1–2 real exams from `official/` (same level) before generating.** Prefer real papers over other synthetics for tone.

## Non-negotiables

1. **Schema** — Meta (level, year, session, language, difficulty; **`seed` if any task is `[random]`**), Tags, Scenario, Constraints, Tasks with inline **Expected Input** / **Expected Output** (Virágágyások). Optional: Example, Data, Tables, Exact strings (omit if unused). No trailing Sample I/O block.
2. **Tags** — exam-level and task-level use the **same** closed list. Multiple tags per task are valid; only these are allowed:
   `IO`, `count`, `sum`, `min_max`, `search`, `validate`, `simulation`, `group`, `string`, `path`, `table`, `lookup`, `function`, `random`, `weighted_sum`
   Match what the subtask actually asks (`IO` = file/console read-write or user prompt; `function` = named helper). Do not invent tags (`store`, `input`, `counting`, `file_read`, …). `function` is emelt-only wording — still do not invent function subtasks for közép.
3. **Tone (level-specific)** — official OH imperatives + edge cases; ban telegraphic stubs like `Hány X?`.
   - **Emelt:** scenario 60–90 words; every subtask ~3–4 sentences / ~30–40 words.
   - **Közép:** scenario 40–70 words; every subtask ~2–3 sentences / ~20–35 words (shorter papers — do not pad to emelt density).
4. **Data** — short template samples + Explanation. Do not paste full official production files. Közép may say the array is stored in source (`tárolja el a programban`); still include a Sample under Data. Catalog conversion will still emit a `data_file`.
5. **Consistency** — Expected Input/Output must match sample Data (compute it). If `[random]`, compute them **with `Meta.seed`**.
6. **Synthetics** — year ≥ 2027; one new file under `synthetic/{level}/`; **do not edit** `official/` or real exams.
7. **Function subtask (emelt only)** — roughly 1 emelt exam in 4 must include `Készítsen függvényt <név> néven, amely …`, and a *later* subtask must consume it. In an emelt batch of 4–6, at least one exam has it. **Do not** invent function subtasks for közép.
8. **Sample-output phrasing** — `a mintának megfelelően` is a *global* convention, not a per-task suffix. Use it on at most 1 subtask in 4, and only where the format is unusual.
9. **Do not write** `backend/app/exams/` or `builders.py`. Stop after the MD file exists.

## `[random]` and seed

Any exam with a `[random]` task **must** declare an integer seed in Meta:

```yaml
- seed: 2027
```

- Hand-compute Expected Output using `random.seed(seed)` (Python `random` module).
- Do **not** put the seed in the student-facing task text (platform injects it later, like `f.read()`).
- If random only draws from the data file, hidden catalog tests can still vary. If there is **no** data file, sample and hidden answers are identical — still seed it so the sample is gradeable; do not fake varying `literal` hidden tests.
- Fully interactive no-file közép: seed still belongs in Meta when `[random]` is present.

## Level patterns

| | Közép | Emelt |
|---|---|---|
| Input | Hardcoded array **or** fully interactive (rarely file) | Almost always file-first |
| Tasks | 3–5 | 5–8 chained |
| Arc | small; often store → aggregate → input/validate | store → count/search/min_max → input → simulate/validate → write file |
| Diversity | pick a **közép matrix coordinate** first (GUIDE §4a) — mix hardcoded / interactive / random / path / game / table | pick an **emelt matrix coordinate** first (GUIDE §4) — novel domain, not a real-paper re-skin |

## Inline I/O (required)

Put **Expected Input:** / **Expected Output:** under the task or nested subtask they belong to — not a separated block at the end.

```md
2. `[count]` Írja ki, hány felajánlást tartalmaz az állomány!
   **Expected Output:**
   ```
     A felajánlások száma: 465
   ```
4. `[IO]` `[count]` Kérje be a felhasználótól egy ágyás sorszámát!
   **Expected Input:**
   ```
     Adja meg az ágyás sorszámát! input(100)
   ```
	1. Írja a képernyőre, hogy hány felajánlásban szerepel ez az ágyás!
	   **Expected Output:**
   ```
	     A felajánlók száma: output(8)
   ```
```

- Prompt text on the line; typed value as `input(…)`.
- Values that depend on that input (or a chosen exact-string branch) as `output(…)`.
- File-derived constants stay literal. Nested subtasks each get their own Expected block.
- Omit a block when that task has no screen I/O (file write only, named function definition).
- **Do not** put `N. feladat` headers inside Expected blocks (gold: Virágágyások; the catalog judge exact-matches these strings).

## Task wording template

```text
[Context clause, if the rule is not self-evident.] [Imperative ask]!
[Rule, definition, or formula.]
[Edge case: ties, missing key, empty result — and exactly what to print then.]
[Output contract: screen format, or target file with fields and order.]
```

Közép may use 2–3 of these parts when the ask is simple; still avoid one-line stubs.

## Function-subtask template (emelt only)

```text
`[function]` Készítsen függvényt <nev> néven, amely <mit számol ki>!
A függvény kapja meg paraméterként <paraméterek típussal>, a visszaadott érték legyen <típus>!
[Opcionális: A függvény elkészítésekor az algoritmusban megadott változóneveket használja!]
A függvényt a későbbi feladatok megoldásánál felhasználhatja.
```

## Output file

`synthetic/{level}/{year}_{session}_{id}.md`

- `level`: `kozep` or `emelt` (folder; ASCII)
- `session`: `majus` or `oktober`
- `id`: title lowercased, accents stripped (`á→a`, `é→e`, `í→i`, `ó/ö/ő→o`, `ú/ü/ű→u`), spaces → `_`, only `a-z` and `_`
- Example: `### Hűtőház` → `synthetic/emelt/2027_oktober_hutohaz.md`
- Refuse if that path exists unless the user asked to replace it

Do **not** append under `# Synthetic Exams` in `official/*.md`.

## Before finishing

- [ ] New file only under `synthetic/{kozep|emelt}/`; `official/` untouched
- [ ] Allowed tags only (closed list above, commas between names; none invented)
- [ ] Tone matches **level** (emelt 60–90 / 3–4 sent; közép 40–70 / 2–3 sent)
- [ ] `a mintának megfelelően` on ≤ 1/4 of subtasks
- [ ] `[random]` ⇒ `Meta.seed` integer; Expected I/O computed with that seed
- [ ] Expected blocks have **no** `N. feladat` headers
- [ ] Emelt batch: ≥ 1 exam has a named function subtask consumed later
- [ ] Közép batch: ≥ 1 exam is **not** the “small list → min_max → one validate” cookie-cutter (GUIDE §4a)
- [ ] Domain not on the level’s real-paper blocklist (GUIDE §4c / §4d); compared against `official/` + existing `synthetic/`
- [ ] Constraints = domain limits (not only global rules)
- [ ] Expected Input/Output recomputed and inlined under the matching task
- [ ] Exact strings listed when mandated; proofread for typos
- [ ] Catalog paths not modified

If anything conflicts, prefer **real exam wording rhythm** from `official/` over inventing a shorter style.

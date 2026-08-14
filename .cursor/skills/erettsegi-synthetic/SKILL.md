---
name: erettsegi-synthetic
description: >-
  Generate or revise Hungarian Informatika / Digitális kultúra érettségi
  (közép or emelt) algoritmizálás exams in the sanitized corpus schema.
  Use when the user asks for synthetic érettségi, exam tasks, Digkult/Informatika
  sanitized MD, or tutoring corpora under Synthetic Exams.
---

# Érettségi synthetic exam generation

## Corpora

- Közép: `h:\obsidian\personal\personal\Informatika and Digitális kultúra érettségi - Sanitized.md`
- Emelt: `h:\obsidian\personal\personal\Informatika and Digitális kultúra érettségi EMELT  - Sanitized.md`
- Full manifesto: `h:\obsidian\personal\personal\Érettségi synthetic generation GUIDE.md`

**Always read the GUIDE + 1–2 real exams before generating.** Append under `# Synthetic Exams` only.

## Non-negotiables

1. **Schema** — Meta (level, year, session, language, difficulty), Tags, Scenario, Constraints, Tasks with inline **Expected Input** / **Expected Output** (Virágágyások). Optional: Example, Data, Tables, Exact strings (omit if unused). No trailing Sample I/O block.
2. **Tags** — exam-level and task-level use the **same** closed list. Multiple tags per task are valid; only these are allowed:
   `IO`, `count`, `sum`, `min_max`, `search`, `validate`, `simulation`, `group`, `string`, `path`, `table`, `lookup` `function` `random` `weighted_sum`
   Match what the subtask actually asks (`IO` = file/console read-write or user prompt; `function` = named helper). Do not invent tags (`store`, `input`, `counting`, `file_read`, …). `function` is emelt-only wording — still do not invent function subtasks for közép.
3. **Tone (level-specific)** — official OH imperatives + edge cases; ban telegraphic stubs like `Hány X?`.
   - **Emelt:** scenario 60–90 words; every subtask ~3–4 sentences / ~30–40 words.
   - **Közép:** scenario 40–70 words; every subtask ~2–3 sentences / ~20–35 words (shorter papers — do not pad to emelt density).
4. **Data** — short template samples + Explanation. Large files come later in production. Közép often hardcodes a small array in source (`tárolja el a programban`) instead of a file.
5. **Consistency** — Expected Input/Output must match sample Data (compute it).
6. **Synthetics** — year ≥ 2027; do not edit real exams.
7. **Function subtask (emelt only)** — roughly 1 emelt exam in 4 must include `Készítsen függvényt <név> néven, amely …`, and a *later* subtask must consume it. In an emelt batch of 4–6, at least one exam has it. **Do not** invent function subtasks for közép.
8. **Sample-output phrasing** — `a mintának megfelelően` is a *global* convention, not a per-task suffix. Use it on at most 1 subtask in 4, and only where the format is unusual.

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

## Before finishing

- [ ] Allowed tags only (closed list above; multiple OK; none invented)
- [ ] Tone matches **level** (emelt 60–90 / 3–4 sent; közép 40–70 / 2–3 sent)
- [ ] `a mintának megfelelően` on ≤ 1/4 of subtasks
- [ ] Emelt batch: ≥ 1 exam has a named function subtask consumed later
- [ ] Közép batch: ≥ 1 exam is **not** the “small list → min_max → one validate” cookie-cutter (GUIDE §4a)
- [ ] Domain not on the level’s real-paper blocklist (GUIDE §4c / §4d); differs on matrix axes from other corpus entries
- [ ] Constraints = domain limits (not only global rules)
- [ ] Expected Input/Output recomputed and inlined under the matching task
- [ ] Exact strings listed when mandated; proofread for typos
- [ ] Separated with `---`

If anything conflicts, prefer **real exam wording rhythm** from the corpora over inventing a shorter style.

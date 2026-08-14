# Érettségi synthetic generation — manifesto / guideline

Guide for agents generating **synthetic** Informatika / Digitális kultúra **algoritmizálás** exams.

**Layout (this repo is SSOT):**

```text
official/kozep.md          # READ-ONLY real közép (quality comparison)
official/emelt.md          # READ-ONLY real emelt
official/exam_as_text/     # tone / blocklist source
synthetic/kozep/           # write new files here
synthetic/emelt/
```

**Never overwrite or append to `official/`.** One new file per synthetic exam: `synthetic/{kozep|emelt}/{year}_{session}_{id}.md`.

Catalog conversion (`backend/app/exams/`) is a **different skill** (`erettsegi-to-catalog`). This guide stops at sanitized MD.

---

## 1. Purpose

Generate exams that:
1. Match the **schema** exactly (tags, sections, meta).
2. Sound like **official OH / érettségi** task wording (not telegraphic prompts).
3. Follow **level-appropriate** patterns (közép vs emelt / classic Informatika).
4. Use **short Data samples as templates** — production will swap in large files later.
5. Get **diversity from structure** (input mode + reasoning primitive), not from re-skinning familiar domains with thinner prose.

---

## 2. Hard schema rules

### Required sections (every exam)
`### Title` → `#### Meta` → `#### Tags` → `#### Scenario` → `#### Constraints` → `#### Tasks`

Place **Expected Input:** / **Expected Output:** under the task (or nested subtask) they belong to — not a trailing Sample I/O block. See Virágágyások. Omit a block when that task has no screen I/O (file write only, named function definition, store-only).

### Optional (omit if unused — no empty placeholders)
`#### Example` · `#### Data` · `#### Tables` · `#### Exact strings`

### Meta fields (all required)
```yaml
- level: közép | emelt
- year: YYYY          # synthetics: use 2027+ to stay distinct from real papers
- session: május | október
- language: hu | idegen
- difficulty: 1-5
- seed: integer       # REQUIRED if any task is tagged [random]; omit otherwise
```

### Tags — exam-level and task-level use ONLY this list
`IO`, `count`, `sum`, `min_max`, `search`, `validate`, `simulation`, `group`, `string`, `path`, `table`, `lookup`, `function`, `random`, `weighted_sum`

Same list for `#### Tags` and for each task. Multiple tags per task are valid. **Do not invent tags** (`store`, `input`, `counting`, `file_read`, `file_write`, `geometry`, `physics`, `carry`, `categorize`, `interactive`, `list`, `loops`).

Match the skill the subtask actually asks:
- `IO` — file read/write, console prompt, user input
- `count` / `sum` / `min_max` / `search` / `validate` / `simulation` / `group` / `string` / `path` / `table` / `lookup` / `random` / `weighted_sum` — the reasoning primitive
- `function` — named helper (`Készítsen függvényt …`); emelt only (§4b). Do not tag közép tasks `function`.

### Task line format
```md
1. `[IO]` Olvassa be és tárolja el a `adat.txt` tartalmát!
2. `[count]` Határozza meg, hogy hány …
   **Expected Output:**
   ```
     A felajánlások száma: 465
   ```
3. `[IO]` `[count]` Kérje be a felhasználótól …
   **Expected Input:**
   ```
     Adja meg az ágyás sorszámát! input(100)
   ```
	1. Írja a képernyőre, hogy hány …
	   **Expected Output:**
   ```
	     A felajánlók száma: output(8)
   ```
```
Tags in backticks+brackets before the sentence. Multiple tags allowed, but only from the closed list above.

**Expected Input / Output conventions** (SSOT: Virágágyások):
- Prompt text stays on the line; wrap the typed value as `input(…)`.
- Wrap values that depend on that input, or a chosen exact-string alternative, as `output(…)`.
- File-derived constants from the official sample stay literal (`A felajánlások száma: 465`).
- Do **not** put `N. feladat` headers inside Expected blocks (gold Virágágyások; catalog exact-match).
- Nested subtasks get their own Expected block.
- `[random]` values: compute with `random.seed(Meta.seed)` (Python `random`). Put `seed` in Meta; do not mention the seed in the task text.

### Data policy
- Short samples only (a few lines / a handful of records).
- Always: `**files:** \`name.txt\` (N sor)` when file-backed.
- Közép: if the array is hardcoded in source, still show a short Sample under Data and note that task 1 stores it in the program (real style: `tárolja el a program forrásában`). Catalog conversion will still emit a swappable `data_file`.
- Add **Explanation** of record layout under Data when fields need decoding.
- Do **not** paste full real datasets into MD (those live in `official/exam_as_text/` for comparison only).

### `[random]` + seed
- If any task is tagged `[random]`, Meta **must** include `seed: <int>`.
- Expected Output is whatever Python `random` produces after `random.seed(seed)`.
- No-file random exams: seed still required; hidden catalog tests will not vary — do not invent fake hidden literals.
- Do not print the seed in Scenario / Tasks (the platform injects `random.seed` in the preamble).

### Global exam conventions (assume always; do not restate as the whole Constraints block)
- Do not validate user input unless the task asks.
- Official papers often print `2. feladat` before results. **Do not put that header in Expected Output** — gold Virágágyások and this catalog judge omit it. Exact strings in Expected blocks are what conversion will grade.
- Show prompt text on input (`print` then `input()`, not `input("prompt")`).
- Accent-free output OK.
- Sample-output fidelity (`a mintának megfelelően`) is a **global** convention — do **not** repeat it on every subtask (see §3).

### Constraints content
Domain limits, formulas, encoding rules, fallbacks — **not** a copy of the global conventions above.

---

## 3. Tone manifesto (critical)

Official papers are **descriptive, complete sentences**. Synthetics must not sound like a checklist.

### Measurable targets by level

| Metric | Közép target | Emelt target |
|---|---|---|
| Scenario length | **40–70 words** | **60–90 words** |
| Words per subtask | **~20–35** | **~30–40** |
| Sentences per subtask | **2–3** (3–4 when rules are dense) | **3–4** |
| `a mintának megfelelően` / `minta szerint` | **≤ 1 subtask in 4** | **≤ 1 subtask in 4** |

Do **not** pad közép scenarios to emelt length. Real középszint papers are shorter and often interactive.

### Four-part subtask structure
Every non-trivial subtask should follow this rhythm (közép may omit a part when the ask is truly simple — still no one-line stubs):

```text
[Context clause, if the rule is not self-evident.] [Imperative ask]!
[Rule, definition, or formula.]
[Edge case: ties, missing key, empty result — and exactly what to print then.]
[Output contract: screen format, or target file with fields and order.]
```

Do **not** put `a mintának megfelelően` in part 4 by default. State the sample-output convention once in spirit (global rule), and only mention the minta on subtasks with an unusual format.

### Ban (telegraphic)
- `Hány jegyet adtak el?`
- `Kérjen be egy km-t! Hány ülés foglalt?`
- `Írja ki a max-ot!`

### Require (official register)
- Full imperatives: `Határozza meg…`, `Állapítsa meg…`, `Kérje be a felhasználótól…`, `Jelenítse meg a képernyőn…`
- Context before the ask when it helps.
- Inline definitions of rules / edge cases.
- File writes as full steps: what file, what fields, what order.

### Before → after

**Emelt** (compressed → real rhythm):

| Compressed (avoid) | Official rhythm (prefer) |
|---|---|
| `Határozza meg, hogy összesen hány helyjegyet adtak el! Az eredményt a mintának megfelelően jelenítse meg a képernyőn!` | `Adja meg a legutolsó jegyvásárló ülésének sorszámát és az általa beutazott távolságot! A kívánt adatokat a képernyőn jelenítse meg!` |

**Közép** (stub / minta-tic → real rhythm):

| Compressed (avoid) | Official rhythm (prefer) |
|---|---|
| `Határozza meg a maximumot! Az eredményt a mintának megfelelően írja ki!` | `Az üvegek űrtartalma alapján határozza meg, hogy a legnagyobb üveg hány deciliteres és hányadik a sorban! Ha több ilyen van, akkor az elsőt adja meg!` |
| `Kérje be a napot! Írja ki, atlag felett van-e a mintának megfelelően!` | `Kérje be a felhasználótól egy nap sorszámát (1–7)! Hasonlítsa össze az adott nap eladását a 2. feladatban kapott átlaggal, és írja ki, hogy az eladás \`atlag felett\`, \`atlag alatt\` vagy \`pont az atlag\` volt-e!` |

### Scenario tone
- **Emelt:** 60–90 words (roughly 4–8 sentences), like Beléptető / Fehérje.
- **Közép:** 40–70 words — short narrative + the rules the student must understand (like Befőzés / Létra), not a one-liner topic label and not a padded essay.

### Exact strings
List every mandatory quoted phrase the program must print. Keep them in Exact strings **and** mention them in the task text. **Proofread** — typos in exact strings teach the wrong answer.

### Expected Input / Output
- Must be **internally consistent** with the sample Data (compute it).
- Prefer slightly sentence-like labels (`Az eladott helyjegyek szama: 7`) over bare keys (`Jegyek: 7`), matching real output samples when possible.
- Inline under the task; never a separated `#### Sample I/O` / `**Output:**` dump at the end.

---

## 4. Közép vs emelt patterns

### Középszint
- Often **hardcoded arrays** in source (`tárolja el a program forrásában`) **or** **fully interactive** (no preloaded file). File-backed közép exists but is uncommon — do not force emelt-style `.txt` I/O.
- Typically **3–5** tasks.
- May / should use `random`, `IO`, `path`, `simulation`, `table` when the matrix coordinate calls for them.
- Smaller cognitive load; official sentences at **közép density** (2–3 sentences), not emelt padding.
- Difficulty 1–3 common; **include some 4–5** for path / simulation / interactive games (real: Robot, Liftvezérlő, Szólánc).
- **No named function subtask** — that is an emelt signature (§4b).

### Emelt (Digitális kultúra + classic Informatika)
- **File-first** almost always. Task 1 ≈ read/store the file(s). All 63 real papers are file-backed — treat no-file emelt as an anti-pattern.
- Typically **5–8** chained tasks.
- Arc: store → count/search/min_max → input query → (optional named function) → simulation/validate → write result file.
- **Diversity comes from the emelt matrix below**, not from reusing kapu / helyjegy / sebesség domain skins.
- Prefer **operational dataset processing** over pure checksum/encoding puzzles.
- Difficulty mostly 3–5; **mix** ratings in a batch (do not rate every exam 4).

### Diversity matrix (emelt)

Pick a coordinate **before** inventing a domain. Real papers hold the skeleton constant and vary the **shape of the data** and the **reasoning applied to it**.

**Axis A — record shape** (from real data files):
| Shape | Real precedent (file excerpt) |
|---|---|
| Header + fixed-field records | `113 172 71` then N rows (`eladott.txt`) |
| Paired event log (in/out matching) | `9 1 2 be` (`ajto.txt`) |
| Interval list with overlap | `2073 2107 P` (`felajanlas.txt`) |
| 1-D numeric profile (runs / transitions) | `melyseg.txt` |
| 2-D grid | RGB triples / sudoku (`kep.txt`) |
| Token or word list | `szavak.txt`, `szotar.txt` |
| Fixed-width encoded string | `mrz1.txt`, IPv6 |
| Sentinel-delimited stream | `penztar.txt` with `F` separators |
| Lookup table joined to transactions | `aminosav.txt` + sequence; `honapok.txt` + events |
| Run-length compressed form | `konyv_t.txt` |
| Free-text / mixed-type records | `fogado.txt`, exam questions |

**Axis B — reasoning primitive:**
- Whole-set aggregate
- Per-entity grouping
- Temporal state replay
- Collision / capacity check
- First-writer-wins
- Cumulative carry
- Positional decode
- Neighbour comparison

**Axis C — output artifact:**
- Per-entity report with key-derived filename (real: `X_menetlevel.txt` → `CEG304_menetlevel.txt`)
- Transformed dataset
- Filtered subset
- Reconstructed grid / image

**Novelty rule (emelt):** a new exam must differ from every corpus entry on Axis A **or** Axis B, and its domain must **not** appear in the emelt blocklist (§4c).

Do **not** obey a domain-family wishlist (kapu, pénztár, sebesség…) at the expense of novelty. Those names describe *structures*, not titles to clone.

### Optional realism notes (emelt)
- Some real papers ship multiple test datasets (`forgalom-1.txt`, `naplo-2.txt`).
- Kráterek ships decimal-separator variants (`felszin_tpont.txt` / `felszin_tvesszo.txt`).
- Older papers offer a read-failure fallback: `Ha az állományt nem tudja beolvasni, az állomány első 10 sorának adatait jegyezze be a programba` — optional flavour for classic Informatika-style synthetics.

---

## 4a. Diversity matrix (közép)

Közép variety is **not** about file record shapes. Real papers vary the **input mode** and the **interaction pattern**. The failure mode of early synthetics was repeating one cookie-cutter:

> small hardcoded list → min_max / sum → one interactive validate

(Kerékpárállomás, Telefoneladás, Házfestő, Karácsonyfa, Avokádó — too many of the same arc.)

Pick a coordinate **before** inventing a domain.

**Axis A — input / setup mode:**
| Mode | Real precedent |
|---|---|
| Hardcoded small array in source | Szállítás, Létra, Befőzés, Forgalomszámlálás, Nyomás, Palacsinta |
| Fully interactive (all data from keyboard) | Fogyókúra, Robot, Szólánc, Kitaláló |
| Random-generated state | Liftvezérlő |
| Lookup table + interactive use | Palacsinta (`arak`), Szólánc (HIBA / LÉPÉSEK tables) |
| Short command / path string | Robot (`E/D/K/N`) |

**Axis B — reasoning / interaction primitive:**
| Primitive | Real precedent |
|---|---|
| Aggregate / min_max / first-hit search | Befőzés, Nyomás, Fogyókúra |
| Greedy packing / carry simulation | Szállítás (20 kg boxes) |
| Board / rule simulation | Létra (spiral + ladder fields) |
| Interactive validation loop until fail | Szólánc, Kitaláló |
| Path simplification / net displacement | Robot |
| Random + path distance | Liftvezérlő |
| Table-driven pricing / categorization | Palacsinta, Szólánc levels |
| Weekly / series with bonus rules | Kihívás |

**Axis C — output style:**
- Console labels only (most közép)
- Exact-string branches (`Elegendo…` / `Maradt…`)
- Multi-value line (dobás mezők szóközzel)
- Category label from a table (`kezdo` / `kozepes` / `halado`)

**Novelty rule (közép):**
1. Domain must **not** appear in the közép blocklist (§4d) or as a near-re-skin of an existing synthetic.
2. Differ from every other corpus entry on Axis A **or** Axis B.
3. In a batch of 3–6 közép exams, **at most half** may use the hardcoded-list → aggregate → single-validate cookie-cutter. At least one must be interactive-loop, path, random, game-sim, or table-driven.

**Do not** re-skin: Fogyókúra → Avokádó-style threshold series; Robot → another `E/D/K/N` energy/path puzzle; Liftvezérlő → another random elevator.

---

## 4b. The named function subtask (emelt only)

Roughly **1 in 4** real emelt papers includes a named helper. **0 of the first 17 synthetics did** — that gap must not continue.

**Közép: never invent a named function subtask.** Real középszint papers do not use this signature.

### Quota (emelt)
- In a batch of 4–6 emelt exams, **at least one** must include `Készítsen függvényt <név> néven, amely …`.
- A **later** subtask must consume the function (state this in the function task text: `A függvényt a későbbi feladatok megoldásánál felhasználhatja.`).

### Template
```text
Készítsen függvényt <nev> néven, amely <mit számol ki>!
A függvény kapja meg paraméterként <paraméterek típussal>, a visszaadott érték legyen <típus>!
[Opcionális: A függvény elkészítésekor az algoritmusban megadott változóneveket használja!]
A függvényt a későbbi feladatok megoldásánál felhasználhatja.
```

Two real contract forms exist — both are valid:

**Prose contract** (Ütemezés — `sorszam`):
> Készítsen függvényt sorszam néven, amely megadja, hogy a paraméterként kapott hónap és nap a nyári szünet hányadik napja! A dátumot a függvény két egész számként kapja meg, a visszaadott érték egy egész szám legyen! A nyári szünet első napja június (6. hó) 16. A nyári szünet 77. napja augusztus (8. hó) 31. (A nyári hónapok rendre 30, 31, 31 naposak.) A későbbi feladatok megoldásánál ezt a függvényt felhasználhatja.

**Prose + reuse licence** (Jeladó — `eltelt`):
> Készítsen függvényt eltelt néven, amely megadja, hogy a paraméterként átadott két időpont között hány másodperc telik el! A két időpontot, mint paramétert tetszőleges módon átadhatja. Használhat három-három számértéket, két tömböt vagy listát, de más, a célnak megfelelő típusú változót is. Ezt a függvényt később használja fel legalább egy feladat megoldása során!

**Pseudocode header** (Szállítószalag — `tav`):
> Készítsen függvényt tav néven, amely megadja a szállítás távolságát a szalag hosszának, valamint az indulási és a célhelynek ismeretében! A függvényt használja fel a későbbi feladatok megoldása során. A függvényfejet az alábbiaknak megfelelően készítse el, megoldásában az ott szereplő változóneveket használja!  
> `Függvény tav(szalaghossz, …) : …`

Tag the task `[function]` (plus any other matching skills, e.g. `[function]` `[sum]`). Include `function` on the exam-level `#### Tags` list when the paper has a named helper.

---

## 4c. Emelt real-paper domain blocklist

Do **not** reuse these titles or near-identical domains for new **emelt** synthetics. Structures (Axis A/B) may recur; the **surface domain** must be new.

| Year | Session | Title |
|---|---|---|
| 2005 | október | Vigenère tábla |
| 2006 | május | Fehérje |
| 2006 | misc | Telefonszámla |
| 2006 | október | Zenei adók |
| 2007 | május | SMS szavak |
| 2007 | október | Foci |
| 2008 | május | SMS |
| 2008 | október | Robot |
| 2009 | május | Lift |
| 2009 | május (id) | Automata |
| 2009 | október | Útépítés |
| 2010 | május | Helyjegy |
| 2010 | május (id) | Telek |
| 2010 | október | Anagramma |
| 2011 | május | Szójáték |
| 2011 | május (id) | Rejtvény |
| 2011 | október | Pitypang |
| 2012 | május | Futár |
| 2012 | május (id) | Törtek |
| 2012 | október | Szín-kép |
| 2013 | május | Választások |
| 2013 | május (id) | Számok |
| 2013 | október | Közúti ellenőrzés |
| 2014 | május | IPv6 |
| 2014 | május (id) | Céllövészet |
| 2014 | október | Nézőtér |
| 2015 | május | Expedíció |
| 2015 | május (id) | Latin táncok |
| 2015 | október | Fej vagy írás |
| 2016 | május | Ötszáz |
| 2016 | május (id) | Zár |
| 2016 | október | Telefonos ügyfélszolgálat |
| 2017 | május | Tesztverseny |
| 2017 | május (id) | Fürdő |
| 2017 | október | Hiányzások |
| 2018 | május | Társalgó |
| 2018 | május (id) | Fogadóóra |
| 2018 | október | Kerítés |
| 2019 | május | Céges autók |
| 2019 | május (id) | Tantárgyfelosztás |
| 2019 | október | eUtazás |
| 2020 | május | Meteorológiai jelentés |
| 2020 | május (id) | Menetrend |
| 2020 | október | Sorozatok |
| 2021 | május | Gödrök |
| 2021 | május (id) | Bányató |
| 2021 | október | Sudoku |
| 2022 | május | Építményadó |
| 2022 | május (id) | Szakaszsebesség-ellenőrzés |
| 2022 | október | Jeladó |
| 2022 | október | Virágágyások |
| 2023 | május | RGB színek |
| 2023 | május (id) | Szállítószalag |
| 2023 | október | Társas |
| 2023 | október | Reklám |
| 2023 | május | Ütemezés |
| Digkult | — | ASCII-rajzok |
| Digkult | — | Autók mozgása |
| Digkult | — | Beléptető rendszer |
| Digkult | — | Kráterek |
| Digkult | — | MRZ kód |
| Digkult | — | Sebesség |
| Digkult | — | Városi autózás |

Also avoid near-duplicates of **existing emelt synthetics** (e.g. another Helyjegyek / Sebességellenőrzés / Kapuátjárás / Csomagautomata skin).

---

## 4d. Közép real-paper domain blocklist

Do **not** reuse these titles or near-identical domains for new **közép** synthetics.

| Year | Session | Title |
|---|---|---|
| 2022 | május (id) | Fogyókúra |
| 2022 | május | Robot |
| 2022 | október | Kockák |
| 2023 | május | TAJ-szám |
| 2023 | május (id) | Kitaláló |
| 2023 | október | Szállítás |
| 2024 | május (id) | Szólánc |
| 2024 | május | Létra |
| 2024 | október | Befőzés |
| 2025 | május (id) | Liftvezérlő |
| 2025 | május | Kihívás |
| 2025 | október | Forgalomszámlálás |
| 2026 | május | Palacsinta |
| 2026 | október | Nyomás |

Also avoid near-duplicates of **existing közép synthetics**: Kerékpárállomás, Jelszóellenőrző, Drónjárat, Telefoneladás, Házfestő, Karácsonyfa, Gyorsétterem, Avokádó — especially another weight/threshold series (Avokádó) or another `E/D/K/N` path (Drónjárat).

---

## 5. Task design checklist

Before finishing an exam, verify:

1. **Schema valid** — only the closed tag list in §2; Meta complete (`seed` iff `[random]`); no empty optional sections; Expected I/O inlined under tasks.
2. **Tone matches level** — emelt: scenario 60–90 / ~3–4 sent/task; közép: scenario 40–70 / ~2–3 sent/task.
3. **Sample phrasing budget** — `a mintának megfelelően` / `minta szerint` on ≤ 1/4 of subtasks.
4. **Chaining** — later tasks reuse earlier data/state.
5. **Edge cases** — ties (first / smallest id), missing keys, empty results — spelled out in the task text.
6. **Sample math** — recompute Expected Input/Output from Data (and `Meta.seed` when `[random]`); fix mismatches. No `N. feladat` in Expected blocks.
7. **Level fit** — közép: no forced file I/O, no named function; emelt: file-first.
8. **Novelty** — domain not on §4c (emelt) or §4d (közép); differs on the level’s matrix axes; don’t clone a title from `official/` or existing `synthetic/`.
9. **Function quota** — emelt batch only: ≥ 1 exam has a named function consumed later.
10. **Közép arc mix** — batch is not all “small list → min_max → one validate”.
11. **Exact strings** — listed when mandated; proofread for typos.
12. **Language** — task body in Hungarian (even if `language: idegen` for the paper track); accent-free OK in Exact strings / sample output.
13. **Difficulty mix** — do not rate every exam the same (közép: include some 4–5; emelt: not all 4).
14. **Output path** — new file under `synthetic/{kozep|emelt}/`; `official/` untouched; no catalog writes.

---

## 6. Generation workflow for agents

1. Read this guide + 1–2 **real** exams from `official/` at the target level (not only synthetics).
2. **Pick level**, then a **matrix coordinate**:
   - Emelt → §4 Axis A+B+C; domain absent from §4c.
   - Közép → §4a Axis A+B+C; domain absent from §4d.
3. Draft Meta / Tags / Scenario / Constraints / Data (short template). Scenario target by level (§3). Add `seed` if any task will be `[random]`.
4. Draft Tasks in the official rhythm with tags. Emelt: include a named function when the batch quota requires it. Közép: never invent one.
5. Hand-compute Expected Input/Output (with `random.seed` when needed) and place them under the matching task; add Exact strings if needed; proofread them.
6. Write **one new file** `synthetic/{kozep|emelt}/{year}_{session}_{id}.md`. Refuse if it exists unless the user asked to replace it.
7. Self-check against §5. Do not edit `official/` or `backend/app/exams/`.

### Batch guidance
- Prefer **3–6 exams per batch**.
- Mix difficulties, matrix coordinates, and domains.
- **Emelt:** ≥ 1/4 of the batch includes a named function subtask; prefer operational file-backed processing.
- **Közép:** ≤ half of the batch may be the hardcoded-list cookie-cutter; ≥ 1 exam must be interactive-loop, path, random, game-sim, or table-driven.

---

## 7. Anti-patterns

- Telegraphic tasks (`Hány X?`).
- Invented tags (`file_read`, `store`, `counting`, `geometry`).
- Constraints that only repeat global rules.
- Expected Input/Output that doesn’t match Data (or that ignores `Meta.seed` on `[random]`).
- `[random]` without `Meta.seed`.
- `N. feladat` lines inside Expected blocks.
- Emelt exam with **no** input file.
- Dumping huge datasets into the MD (templates stay short).
- Editing `official/` or appending under `# Synthetic Exams` in the gold files.
- Writing `backend/app/exams/` from this skill.
- Purple prose / English task bodies / emoji.
- Ending nearly every subtask with `a mintának megfelelően` (machine-written tell).
- Emelt batch with **no** named function subtask anywhere.
- **Named function on a közép exam.**
- Re-skinning a real paper’s domain (emelt: Helyjegy → Helyjegyek; közép: Robot → Drónjárat, Fogyókúra → Avokádó).
- Rating every exam the same difficulty.
- Padding közép scenarios to emelt length (≥ 80 words of fluff).
- Közép batch that is only “N numbers → max/sum → one validate ask”.
- Scenario under ~35 words (közép) / ~50 words (emelt), or subtasks that are one-line stubs.

---

## 8. Minimal skeletons

### Emelt (file-backed)

```md
### CímszerűEgySzó

#### Meta
- level: emelt
- year: 2027
- session: május
- language: hu
- difficulty: 4
# - seed: 2027   # required iff any task is [random]

#### Tags
- IO
- count
- search
- validate

#### Scenario
[60–90 szó narratíva + lényeges szabályok]

#### Constraints
- [tartományok, formátumok, kimeneti fájl]
- [döntetlen / hiányzó adat szabály]

#### Data
**files:** `adat.txt` (minta), `ki.txt` (kimenet)

Sample (`adat.txt`):
```
...
```

Explanation:
[mezők jelentése]

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `adat.txt` …
2. `[count]` Határozza meg, hogy hány …
   **Expected Output:**
   ```
     A rekordok száma: …
   ```
3. `[IO]` `[count]` Kérje be a felhasználótól …
   **Expected Input:**
   ```
     Adja meg … input(…)
   ```
   **Expected Output:**
   ```
     … output(…)
   ```
N. `[IO]` … írja a `ki.txt` állományba …

#### Exact strings
- `…`

---
```

### Közép (hardcoded array)

```md
### CímszerűEgySzó

#### Meta
- level: közép
- year: 2027
- session: május
- language: hu
- difficulty: 2
# - seed: 2027   # required iff any task is [random]

#### Tags
- IO
- count
- min_max
- validate

#### Scenario
[40–70 szó narratíva + lényeges szabályok]

#### Constraints
- [N elem; cserélhető adatokkal is működnie kell]
- [döntetlen / hiányzó adat szabály]

#### Data
Sample:
```
…
```

#### Tasks
1. `[IO]` A megadott N számot tárolja el a programban egy megfelelő adatszerkezetben!
2. …
3. `[IO]` `[validate]` Kérje be… Ha …, írja ki: `…`!
   **Expected Input:**
   ```
     … input(…)
   ```
   **Expected Output:**
   ```
     output(…)
   ```

#### Exact strings
- `…`

---
```

For fully interactive / path / random / table-driven közép exams, omit unused Data, add Example or Tables as needed, and follow a real exemplar’s arc (Szólánc, Robot, Liftvezérlő, Palacsinta) with a **new** domain.

---

## 9. Reference exemplars in-corpus

Read these from **`official/`** (real papers). Use **`synthetic/`** only to avoid cloning arcs you already generated.

**Emelt — tone / structure (real, `official/emelt.md`):** Virágágyások (inline Expected I/O + nested subtasks), Beléptető rendszer, Reklám, Fehérje, Autók mozgása, Ütemezés (function subtask).  
**Emelt — function-subtask exemplars (real):** Ütemezés (`sorszam`), Jeladó (`eltelt`), Szállítószalag (`tav`), RGB színek (`hatar`), Építményadó (`ado`) — also `official/exam_as_text/`.  
**Közép — tone / structure (real, `official/kozep.md`):** Befőzés, Létra, Szólánc, Robot, Fogyókúra, Liftvezérlő, Palacsinta.  
**Közép — live synthetics (do not clone arcs):** files under `synthetic/kozep/` plus older titles Kerékpárállomás, Jelszóellenőrző, Drónjárat, Telefoneladás, Házfestő, Karácsonyfa, Gyorsétterem, Avokádó.

When unsure, **copy the sentence rhythm** of a real exam’s Tasks block, then swap domain content — but pick the domain from a **new** matrix coordinate, not from the exemplar’s title.

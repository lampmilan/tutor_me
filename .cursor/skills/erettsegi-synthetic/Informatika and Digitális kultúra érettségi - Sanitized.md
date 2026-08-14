# Informatika and Digitális kultúra érettségi — Sanitized

Structured corpus of programming (algoritmizálás) exam tasks for synthetic generation and tutoring.

## Schema

Every exam under `# Középszintű` follows this shape. Omit a section only when it does not apply (do not leave empty placeholders).

```md
### ExamTitle

#### Meta
- level: közép
- year: YYYY
- session: május | október
- language: hu | idegen
- difficulty: 1-5

#### Tags
Exam-level skill tags (for tutoring / weak-point targeting). Use only from this list:
`IO`, `count`, `sum`, `min_max`, `search`, `validate`, `simulation`, `group`, `string`, `path`, `table`, `lookup` `function` `random` `weighted_sum`

#### Scenario
Flavor text and rules the student must understand.

#### Constraints
- Bullet list of ranges, assumptions, and limits.

#### Example
Optional worked mini-example (not the full console sample).

#### Data
Hardcoded / file snippet the program may embed. Omit if interactive-only.

#### Tables
Optional markdown tables referenced by tasks.

#### Tasks
1. `[tag]` Task text…
2. `[tag]` …
   **Expected Output:**
   ```
     …
   ```
   **Expected Input:**
   ```
     Prompt! input(value)
   ```

Allowed tags: `IO`, `count`, `sum`, `min_max`, `search`, `validate`, `simulation`, `group`, `string`, `path`, `table`, `lookup` `function` `random` `weighted_sum`

#### Exact strings
- Exact phrases the program must print (when specified).
```

**Expected I/O:** put **Expected Input:** / **Expected Output:** under the task they belong to (Virágágyások). Use `input(…)` / `output(…)` for interactive values. No trailing Sample I/O block.

---

# Real Exams

### Fogyókúra

#### Meta
- level: közép
- year: 2022
- session: május
- language: idegen
- difficulty: 2

#### Tags
- IO
- count
- search

#### Scenario
Mari néni – orvosi tanácsra – többhetes fogyókúrába kezdett. Előre elhatározta, hogy hány kilogrammra szeretne lefogyni. Minden héten kedden reggel mérlegre állt, és feljegyezte az aktuális tömegét. A feladat az így kapott adatok elemzése.

#### Constraints
- A fogyókúra egy évnél biztosan rövidebb.
- Hetek száma és céltömeg a felhasználótól érkezik. a heti értékek bekérésből.

#### Tasks
1. `[IO]` Olvassa be a mintának megfelelően, és tárolja el, hogy hány héten át tartott a fogyókúra, és Mari néni milyen célt tűzött ki maga elé!
   **Expected Input:**
   ```
     Hetek száma=input(6)
     Elérni kívánt testtömeg (kg)=input(93.5)
   ```
2. `[IO]` Olvassa be a mintának megfelelően Mari néni tömegét a fogyókúra heteiben!
   **Expected Input:**
   ```
     1. héten=input(95.5)
     2. héten=input(94.3)
     3. héten=input(94.4)
     4. héten=input(93.3)
     5. héten=input(93.8)
     6. héten=input(92.9)
   ```
3. `[search]` Elérte-e Mari néni a kitűzött célt? Ha igen, írassa ki a képernyőre az első olyan hét sorszámát, amikor Mari néni tömege már nem haladta meg a kitűzött célt! Ha egyetlen héten sem érte ezt el, akkor írassa ki: `Sajnos Mari néni nem érte el a célját.`
   **Expected Output:**
   ```
     Mari néni a(z) output(4). héten érte el a célt.
   ```
4. `[count]` Mari néni nem tartja be következetesen az előírásokat, ezért előfordul, hogy a tömege egyik hétről a másikra nem csökken, hanem növekszik. A fogyókúra időszaka alatt hány olyan hét volt, amikor Mari néni tömege nőtt az előző héthez képest? Válaszát a mintának megfelelően írassa ki a képernyőre!
   **Expected Output:**
   ```
     A tömege output(2) esetben nőtt egyik hétről a másikra.
   ```

#### Exact strings
- `Sajnos Mari néni nem érte el a célját.`

---

### Robot

#### Meta
- level: közép
- year: 2022
- session: május
- language: hu
- difficulty: 5

#### Tags
- IO
- count
- path

#### Scenario
Sokféle tevékenységet végeznek a környezetünkben az automaták, illetve a robotok.
Egy egyszerű robot a végrehajtandó mozgását egy betűkből álló sorozattal, szóval kapja. Vízszintes síkban szabadon mozog, iránytűje segítségével pontosan be tudja tájolni magát. Az E, D, K vagy N betűk hatására egységnyit megy észak, dél, kelet vagy nyugat felé.

Készítsen programot, amely a parancsszót, azaz a betűk sorozatát egyszerűsíti, vagyis olyan új parancsszót állít elő, amelynek végrehajtásakor a robotot a kezdőpontból a végpontba a lehető legkevesebb utasítással juttatja el!

#### Constraints
- Parancsszó hossza legfeljebb 200 betű.
- Betűk: E (észak), D (dél), K (kelet), N (nyugat).
- Több egyformán rövid megoldás is elfogadható.

#### Example
```
1. példa: ENEK -> EE
2. példa: EENDN -> ENN vagy NNE
```

#### Tasks
1. `[IO]` Olvassa be és tárolja el a robot mozgását vezérlő szót, és annak felhasználásával oldja meg a következő feladatokat.
   **Expected Input:**
   ```
     Kérem a robot parancsait: input(EEEKDKEKDKEKDDNN)
   ```
2. `[count]` Írja ki, hogy az egyes betűkből hány darab van a szóban!
   **Expected Output:**
   ```
     E betűk száma: output(5)
     D betűk száma: output(4)
     K betűk száma: output(5)
     N betűk száma: output(2)
   ```
3. `[path]` Írja ki a képernyőre a bekért útvonal egy lehetséges egyszerűsítését, tehát egy olyan új parancsszót, amelyet végrehajtva a robot a lehető legkevesebb mozgással juthat el a kiindulási pontból az eredeti parancsszónak megfelelő végső helyzetbe!
   **Expected Output:**
   ```
     Egy legrövidebb út parancsszava: output(KKKE)
   ```

---

### Kockák

#### Meta
- level: közép
- year: 2022
- session: október
- language: hu
- difficulty: 1

#### Tags
- IO
- count
- simulation
- random

#### Scenario
Anni és Panni három dobókockával játszik. Egyszerre feldobják a három kockát, és összeadják a három kockán kidobott számokat. Anni akkor nyer, ha a kockákon lévő számok összege 10-nél kisebb, Panni pedig ellenkező esetben. Sokat játszanak, de több feldobás után sem tudják eldönteni, hogy melyiküknek kedvez a játék.

#### Constraints
- Három kocka, értékek 1–6.
- Anni nyer, ha összeg < 10; különben Panni.
- A véletlenszám-sorozat ne legyen minden futtatáskor azonos (seed nélkül / időalapú seed).

#### Tasks
1. `[IO]` Kérje be a felhasználótól N értékét, vagyis a feldobások számát, és tárolja el a kapott értéket!
   **Expected Input:**
   ```
     Hány alkalommal legyen feldobás? input(5)
   ```
2. `[random]` Végezzen N feldobást a három kockával úgy, hogy minden feldobásnál generál három véletlenszámot 1 és 6 között!
3. `[simulation]` Minden feldobás után írja ki a kockán lévő számokat, valamint azok összegét, és azt is, hogy ki nyert. A kiírás egy sorban történjen, a mintához hasonlóan!
   **Expected Output:**
   ```
     Dobás: output(4 + 1 + 2 = 7) Nyert: output(Anni)
     Dobás: output(5 + 4 + 1 = 10) Nyert: output(Panni)
     Dobás: output(5 + 3 + 3 = 11) Nyert: output(Panni)
     Dobás: output(4 + 3 + 3 = 10) Nyert: output(Panni)
     Dobás: output(3 + 2 + 2 = 7) Nyert: output(Anni)
   ```
4. `[count]` A feldobások után egy mondatban írja ki, hogy hány alkalommal kedvezett az egyik, és hány alkalommal a másik játékosnak a szerencse!
   **Expected Output:**
   ```
     A játék során output(2) alkalommal Anni, output(3) alkalommal Panni nyert
   ```

---

### TAJ-szám

#### Meta
- level: közép
- year: 2023
- session: május
- language: idegen
- difficulty: 3

#### Tags
- IO
- validate
- lookup
- weighted_sum

#### Scenario
A TAJ-szám egy kilenc számjegyből álló szám, amelyben az első nyolc számjegy egy folyamatosan kiadott egyszerű sorszám. A kilencedik számjegy, az úgynevezett ellenőrzőszám a véletlen gépelési hibák azonnali jelzésére szolgál.

A kilencedik számjegy képzési szabálya: a TAJ-szám első nyolc számjegyéből a páratlan helyen állókat hárommal, a páros helyen állókat héttel szorozzuk, és a szorzatokat összeadjuk. Az összeg tízzel vett osztási maradéka az ellenőrzőszám. A TAJ-szám első számjegyei 0-k is lehetnek.

#### Constraints
- Pontosan 9 számjegy.
- Pozíciók 1-től indexelve: páratlan → ×3, páros → ×7.
- Ellenőrzőszám = (szorzatok összege) mod 10.

#### Example
```
A számjegy helye 1. 2. 3. 4. 5. 6. 7. 8. 9.
A TAJ-szám számjegye 6 7 3 4 5 7 0 1 5
A megfelelő szorzószám 3 7 3 7 3 7 3 7
A szorzat 18 49 9 28 15 49 0 7
```

#### Tasks
1. `[IO]` Olvasson be egy kilencjegyű TAJ-számot egy változóba!
   **Expected Input:**
   ```
     Kérem a TAJ-számot: input(012345672)
   ```
2. `[lookup]` A TAJ-szám kilencedik számjegyét, az ellenőrzőszámot írja a képernyőre, és tárolja el egy másik változóban!
   **Expected Output:**
   ```
     Az ellenőrzőszámjegy: output(2)
   ```
3. `[weighted_sum]` Az első nyolc számjegyet a helyzetének megfelelően, ha páratlan pozíciójú, akkor hárommal, ha páros, akkor héttel szorozza meg, és a szorzatokat összegezze egy változóban! Írja ki az így meghatározott összeg értékét!
   **Expected Output:**
   ```
     A szorzatok összege: output(148)
   ```
4. `[validate]` Vizsgálja meg, hogy a szorzatok összege tízzel vett osztási maradéka azonos-e az ellenőrzőszámmal! Ha azonos, akkor a `Helyes a szám!`, különben `Hibás a szám!` szöveget írja a képernyőre!
   **Expected Output:**
   ```
     output(Hibás a szám!)
   ```

#### Exact strings
- `Helyes a szám!`
- `Hibás a szám!`

---

### Kitaláló

#### Meta
- level: közép
- year: 2023
- session: május
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- simulation
- string
- random

#### Scenario
Egy betűkitaláló játékban egy rejtett szót kell meghatározni a tippekre adott válaszokból. A játék során szavakat adunk meg tippként, és erre válaszként azt kapjuk meg, hogy a rejtett szóban hol és mely betűket találtuk el. A megtalált betűket megjelenítjük, a tévesek helyén pontot („.”) írunk ki.

#### Constraints
- Mind a 15 szó hatbetűs.
- Tippek hatbetűsek (kivéve a `stop` kilépőszó).
- Minden szónak azonos esélye van a rejtett szóként.
- `stop` esetén a tippszámot ne írja ki.

#### Example
```
rejtett szó: bicska
tipp: babona
válasz: b....a
```

Stop (no tip count):
```
Kérem a tippet: bicska
Az eredmény: b....a
Kérem a tippet: stop
```

#### Data
```
fuvola, csirke, adatok, asztal, fogoly, bicska, farkas, almafa, babona, gerinc, dervis, bagoly, ecetes, angyal, boglya
```

#### Tasks
1. `[IO]` A megadott 15 szót rögzítse a program forrásában egy megfelelő adatszerkezetben!
2. `[random]` A rejtett szót válassza ki a rögzített szavak közül véletlenszerűen úgy, hogy azonos esélye legyen mindegyiknek!
3. `[string]` `[simulation]` Addig kérje a program a hatbetűs tippeket, amíg a rejtett szónak mind a hat betűje ismertté nem válik! Kivétel: a `stop` szóval a játék megállítható.
   **Expected Input:**
   ```
     Kérem a tippet: input(bicska)
     Kérem a tippet: input(boglya)
     Kérem a tippet: input(babona)
   ```
   **Expected Output:**
   ```
     Az eredmény: output(b....a)
     Az eredmény: output(b....a)
     Az eredmény: output(babona)
   ```
4. `[count]` A játék végén, ha nem a `stop` szó miatt fejeződik be, írassa ki a mintának megfelelően a megfejtéshez használt tippek számát, különben ne írjon ki semmit!
   **Expected Output:**
   ```
     output(3) tippeléssel sikerült kitalálni.
   ```

#### Exact strings
- `stop` (kilépőszó)

---

### Szállítás

#### Meta
- level: közép
- year: 2023
- session: október
- language: hu
- difficulty: 3

#### Tags
- IO
- sum
- simulation

#### Scenario
Egymás után sorban érkező tárgyakat kell bedobozolni, majd elszállítani. A dobozokba legfeljebb 20 kg tömeg kerülhet. Minden tárgy tömege 1 és 20 kilogramm közötti egész szám.

A dobozba csomagolás módszere:
- egy új dobozba a tárgyakat sorban, egymás után teszik;
- ha a dobozba, a tömeghatárt figyelembe véve befér a tárgy, akkor beteszik;
- amennyiben már nem tehető be a soron következő tárgy, akkor a dobozt lezárják, és új dobozt kezdenek.

#### Constraints
- Dobozkapacitás: 20 kg.
- Tárgy tömege: 1–20 kg egész.
- 15 megadott tömeg; a programnak cserélhető adatokkal is működnie kell.

#### Data
**files:** `tomeg.txt` (15 elem)

Sample:
```
16, 8, 9, 4, 3, 2, 4, 7, 7, 12, 3, 5, 4, 3, 2
```

#### Tasks
1. `[IO]` A megadott 15 számot tárolja el a program forrásában egy megfelelő adatszerkezetben!
2. `[sum]` A tárgyak tömege alapján határozza meg és írassa ki az össztömeget a minta szerint!
   **Expected Output:**
   ```
     A tárgyak tömegének összege: 89 kg
   ```
3. `[simulation]` Határozza meg, hogy hány dobozra van szükség, és ezekben mekkora tömegek lesznek! Az eredményeket írassa ki a mintának megfelelően!
   **Expected Output:**
   ```
     A dobozok tartalmának tömege (kg): 16 17 20 19 17
     A szükséges dobozok száma: 5
   ```

---

### Szólánc

#### Meta
- level: közép
- year: 2024
- session: május
- language: idegen
- difficulty: 4

#### Tags
- IO
- count
- validate
- simulation
- table

#### Scenario
A szólánc kedvelt nyelvi játék. A játék során úgy kell szavakat egymás után mondani, hogy az előző szó utolsó betűjével kezdődjön a következő szó.

#### Constraints
- Minden szónak (az elsőt kivéve) hatbetűsnek kell lennie.
- Az új szó első karaktere = előző szó utolsó karaktere (első szónál nincs megelőző).
- Ha mindkét hiba fennáll, elegendő az egyik hibaüzenet.
- Lépésszám = szabályos szavak száma a hibás előtt.

#### Example
```
Például egy szólánc:
villan, negyed, diadal, lankad, durrog, gondos, surran
```

#### Tables

**HIBA**

| Bemenet | Hiba |
| --- | --- |
| zsenge / ecetes / sproni | A karakterek száma téves! |
| zsilip / pislog / homlok | Nem illeszkedett! |

**LÉPÉSEK**

| Lépésszám | Felirat |
| --- | --- |
| 0 – 2 | kezdő |
| 3 – 5 | közepes |
| 6 és felette | haladó |

#### Tasks
1. `[IO]` A játék során a szavakat egyenként olvassa be a program, és minden lépésnél írja ki, hogy hányadik szót kéri!
   **Expected Input:**
   ```
     1. szó: input(villan)
     2. szó: input(negyed)
     3. szó: input(diadal)
     4. szó: input(lista)
   ```
2. `[validate]` `[simulation]` Addig kérje a program a szavakat, ameddig a megadott új szó hatbetűs, és az első karaktere megegyezik az előző szó utolsó karakterével! Az első szó kivétel. Ha a szabályok nem teljesülnek, a játéknak vége.
3. `[validate]` A játék végén írja ki a befejezés okát: `Nem illeszkedett!` vagy `A karakterek száma téves!` (lásd HIBA táblázat).
   **Expected Output:**
   ```
     output(A karakterek száma téves!)
   ```
4. `[count]` Írja ki, hogy a szólánc hány, a szabályoknak megfelelő szóval folytatódott (helyes lépések száma)!
   **Expected Output:**
   ```
     Helyes lépések száma: output(3)
   ```
5. `[table]` Az elért helyes lépésszám alapján a LÉPÉSEK táblázatnak megfelelő értékelő felirat jelenjen meg!
   **Expected Output:**
   ```
     Szint: output(közepes)
   ```

#### Exact strings
- `Nem illeszkedett!`
- `A karakterek száma téves!`
- `kezdő` / `közepes` / `haladó`

---

### Létra

#### Meta
- level: közép
- year: 2024
- session: május
- language: hu
- difficulty: 3

#### Tags
- IO
- count
- validate
- simulation

#### Scenario
A Létra társasjátékot egy 45 mezőből álló táblán, dobókockával többen játszhatják. A játékos kezdetben az 1-es mező előtt áll, majd a dobókockával dobott értékkel halad előre a spirálisan elhelyezkedő mezőkön. Amennyiben „létramezőre” lép, azaz olyanra, aminek a számértéke 10-zel osztható, akkor 3 mezőt vissza kell lépnie a táblán. A játékot az nyeri, aki először éri el a 45-ös mezőt, vagy halad át rajta.

#### Constraints
- Tábla: 1–45 mező.
- Létramező: pozíció % 10 == 0 → visszalépés 3 mezővel.
- Kezdőpozíció: 0 (az 1-es mező előtt).
- 18 dobás adat; cserélhető adatokkal is működnie kell.
- Létrára lépéskor csak a létra utáni mezőt írja ki.

#### Data
**files:** `dobasok.txt` (18 elem)

Sample:
```
3, 1, 1, 2, 1, 5, 5, 4, 4, 4, 1, 2, 3, 6, 4, 6, 1, 4
```

#### Tasks
1. `[IO]` Az alább megadott 18 számot (egy játékos dobásai) tárolja el a program forrásában egy megfelelő adatszerkezetben!
2. `[simulation]` Határozza meg a dobások segítségével a játék menetét! Jelenítse meg dobásról dobásra, hogy melyik mezőn tartott a játékos; szóközzel elválasztva. Létramező esetén csak a létra utáni mezőt írja ki!
   **Expected Output:**
   ```
     3 4 5 7 8 13 18 22 26 27 28 27 27 33 37 43 44 48
   ```
3. `[count]` Határozza meg, hogy hányszor kellett visszalépnie a játék során! Az eredményt a mintának megfelelően jelenítse meg!
   **Expected Output:**
   ```
     A játék során 3 alkalommal lépett létrára.
   ```
4. `[validate]` Állapítsa meg, hogy az illető befejezte-e a játékot, azaz elérte vagy meghaladta-e a 45-ös mezőt! Ha befejezte a játékot, akkor az `A játékot befejezte.` üzenetet jelenítse meg, különben az `A játékot abbahagyta.` üzenetet írja ki!
   **Expected Output:**
   ```
     output(A játékot befejezte.)
   ```

#### Exact strings
- `A játékot befejezte.`
- `A játékot abbahagyta.`

---

### Befőzés

#### Meta
- level: közép
- year: 2024
- session: október
- language: hu
- difficulty: 2

#### Tags
- IO
- sum
- min_max
- validate

#### Scenario
Mari néni eperlekvárt főz be. Sorba állította a kamrából előhozott, elmosott üres üvegeket, hogy megtöltse őket. Tudja, hogy az egyes üvegek hány deciliteresek.

#### Constraints
- 15 üvegűrtartalom; cserélhető adatokkal is működnie kell.
- L bekérés: `0 < L <= 200`.
- Több azonos max esetén az első előfordulás.

#### Data
**files:** `uvegek.txt` (15 elem)

Sample:
```
5, 2, 2, 4, 3, 2, 4, 10, 5, 5, 3, 5, 4, 3, 3
```

#### Tasks
1. `[IO]` A megadott 15 számot tárolja el a programban egy megfelelő adatszerkezetben!
2. `[IO]` Kérje be a mintának megfelelően, és tárolja el, hogy Mari néni hány deciliter lekvárt (L) főz be!
   **Expected Input:**
   ```
     Mari néni lekvárja (dl): input(35)
   ```
3. `[min_max]` Az üvegek űrtartalma alapján határozza meg, hogy a legnagyobb üveg hány deciliteres és hányadik a sorban! Ha több ilyen van, akkor az elsőt adja meg!
   **Expected Output:**
   ```
     A legnagyobb üveg: 10 dl és 8. a sorban.
   ```
4. `[sum]` `[validate]` Írassa ki, hogy Mari néni L deciliter befőzött lekvárja elfér-e az üvegekben! `Elegendő üveg volt.` vagy `Maradt lekvár.`
   **Expected Output:**
   ```
     output(Elegendő üveg volt.)
   ```

#### Exact strings
- `Elegendő üveg volt.`
- `Maradt lekvár.`

---

### Liftvezérlő

#### Meta
- level: közép
- year: 2025
- session: május
- language: idegen
- difficulty: 5

#### Tags
- IO
- simulation
- path
- random

#### Scenario
Egy tízemeletes lakóépületben egy lift működik. Minden szinten van hívógomb és kijelző. A kijelző mutatja, hogy melyik szinten van a lift, és hogy mozgásban van-e. A lift tárolja a célemeletet is.

Példa: a lift a 7. emeletről megy a 0. emeletre; a hívó a 8. emeleten van. A hívónak meg kell várnia, amíg a lift lemegy 7→0, majd fel 0→8, azaz 7 + 8 = 15 emeletet.

#### Constraints
- Szintek: 0–10.
- Irány: `F` (fel), `L` (le), `-` (áll).
- Feltételezhető, hogy nem hívják egyidejűleg többen.
- Álló liftnél a felhasználó nem ad meg az aktuális szinttel azonos hívóértéket.
- Ha a hívó az aktuális és a cél között van (menetirányban), a lift megáll a hívónál; különben előbb célra megy, majd a hívóhoz.

#### Example
További érvényes futások (a 1–3. feladat kimenete a véletlen állapottól függ):
```
A lift helyzete: 1 F (3)
Adja meg a szintet, ahonnan hívja a liftet! Szint: 0
A liftnek 5 emeletet kell haladnia a hívóig.

A lift helyzete: 4 - (4)
Adja meg a szintet, ahonnan hívja a liftet! Szint: 9
A liftnek 5 emeletet kell haladnia a hívóig.

A lift helyzete: 0 F (10)
Adja meg a szintet, ahonnan hívja a liftet! Szint: 3
A liftnek 3 emeletet kell haladnia a hívóig.
```

#### Tasks
1. `[random]` Állítsa elő a lift kijelzőjének adatait: véletlenszerűen két 0–10 közötti egész (aktuális, cél). Döntse el az irányt (`F` / `L` / `-`), és írja ki a mintának megfelelően az aktuális szintet, irányt és célemeletet! (Ha nincs véletlen, vegyen fel két fix 0–10 értéket.)
   **Expected Output:**
   ```
     A lift helyzete: output(7 L (0))
   ```
2. `[IO]` Kérjen be egy emeletértéket (0–10)! Ez jelképezi a hívószintet, azt a szintet, amelyiken a hívó megnyomja a gombot. Amennyiben a lift azon az emeleten áll, ahol a hívó van, akkor nem nyomja meg a hívógombot, hanem beszáll a liftbe. Azaz feltételezheti, hogy a felhasználó nem ad meg az álló lift szintjével azonos értéket.
   **Expected Input:**
   ```
     Adja meg a szintet, ahonnan hívja a liftet! Szint: input(8)
   ```
3. `[path]` `[simulation]` Határozza meg és írja ki a képernyőre, hogy hány emeletet kell haladnia a liftnek a hívóig! Ha az aktuális szint és a célemelet között van a hívó, akkor menet közben a lift meg fog állni a hívó szintjén. Ha a liftnek a célemeletig nem kell áthaladnia a hívó szintjén, akkor a lift először elmegy a célemeletre, majd onnan megy a hívó szintjére.
   **Expected Output:**
   ```
     A liftnek output(15) emeletet kell haladnia a hívóig.
   ```

---

### Kihívás

#### Meta
- level: közép
- year: 2025
- session: május
- language: hu
- difficulty: 2

#### Tags
- IO
- sum
- validate
- string

#### Scenario
Az interneten számos sportkihívással találkozhatunk. Ezek általában egy adott időszakra
tűznek ki valamilyen elérendő célt, ezzel is mozgásra ösztönözve az embereket. Ebben a feladatban egy heti mozgáskihívás eredményeit kell kiértékelnie! A kihívásban a heti mozgást egy applikáció segítségével kellett rögzíteni és a hét végén beküldeni. A kihívást a következő mozgásformák segítségével lehetett teljesíteni: úszás, gyaloglás, futás, kerékpározás. A kihívás célja 40 km elérése volt. Az applikáció rögzítette a heti mozgást, a felhasználó pedig a hét végén beküldte a rögzített teljesítményt.

#### Constraints
- Aktivitás-sorozat hossza < 250 karakter.
- Heti cél: 40 km.
- Jutalom: +10 km, ha mind a négy mozgásforma szerepel a sorozatban.
- Kódok: U=1 km, G=1 km, F=2 km, K=10 km.

#### Example
```
Az alábbi példa egy felhasználó heti aktivitását mutatja:
FFFGGGUUUFFFGGKKK
```

#### Tables

| Mozgásforma | Kód | Kódhoz tartozó távolság |
| --- | --- | --- |
| Úszás | U | 1 km |
| Gyaloglás | G | 1 km |
| Futás | F | 2 km |
| Kerékpározás | K | 10 km |

#### Tasks
1. `[IO]` Kérje be és tárolja el a felhasználó heti aktivitását!
   **Expected Input:**
   ```
     Adja meg az aktivitását: input(FFFGGGUUUFFFGGKKK)
   ```
2. `[sum]` `[string]` Számítsa ki és a mintának megfelelően jelenítse meg a felhasználó aktivitását, azaz a héten megtett távolságok összegét!
   **Expected Output:**
   ```
     Az elért távolság: output(50) km.
   ```
3. `[validate]` Amennyiben a felhasználó mindegyik mozgásformát űzte az adott héten, akkor +10 km jutalom: `Bravó! Jutalma még 10 km.` különben `Nem jár jutalom.`
   **Expected Output:**
   ```
     output(Bravó! Jutalma még 10 km.)
   ```
4. `[validate]` Írassa ki a képernyőre a felhasználó által gyűjtött kilométerek számát, amely a megtett heti távolságérték és a kapott jutalomkilométerek összege! Ha a gyűjtött kilométerek elérik a heti kihívásnak megfelelő 40 km-t, akkor a `Gratulálok, kihívás teljesítve!` üzenetet jelenítse meg, a minta szerint! Amennyiben nem teljesítette a kitűzött célt, a `Legközelebb sikerül!` üzenetet jelenítse meg!
   **Expected Output:**
   ```
     Eredménye: output(60) km. output(Gratulálok, kihívás teljesítve!)
   ```

#### Exact strings
- `Bravó! Jutalma még 10 km.`
- `Nem jár jutalom.`
- `Gratulálok, kihívás teljesítve!`
- `Legközelebb sikerül!`

---

### Forgalomszámlálás

#### Meta
- level: közép
- year: 2025
- session: október
- language: hu
- difficulty: 3

#### Tags
- IO
- sum
- min_max
- group

#### Scenario
Egy város közlekedéstervezési céllal kerékpárosforgalom-számlálót telepít az egyik főútjára. A próbaüzem reggel 6-tól 10-ig tart, amelynek során 15 percenként rögzítik a megelőző 15 percben áthaladó kerékpárosok számát. A rendszer még bizonytalan, ha technikai probléma – például áramszünet – történik a mérés során bármikor, akkor a rögzített érték abban az időintervallumban -1 lesz, különben az áthaladók száma nemnegatív egész szám.

#### Constraints
- 16 mérési érték (6:15-től 10:00-ig, 15 percenként).
- `-1` = mérőhiba; ne számítson bele az összegbe / maxba (a mintában a max a legnagyobb érvényes érték).
- Óránkénti bontás: 6, 7, 8, 9 óra (négy-négy negyedóra).
- Több max esetén az első.
- Időformátum: `07:00`, `7:00`, `7:0` egyaránt elfogadható.
- Forrásfájl (opcionális): `meres.txt`.

#### Example
```
A mérés kezdőadatai: 6:15-kor 36, 6:30-kor 48 kerékpáros, és így tovább. 7:00-kor és
7:45-kor -1 került rögzítésre. Az utolsó adatot, 63 kerékpárost 10:00-kor jegyezték fel.
```

#### Data
**files:** `meres.txt` (16 elem)

Sample:
```
36, 48, 39, -1, 30, 43, -1, 76, 67, 82, 73, 75, 64, 73, 69, 63
```

#### Tasks
1. `[IO]` A megadott 16 számot tárolja el a program forrásában egy megfelelő adatszerkezetben!
2. `[sum]` A forgalomszámláló adatai alapján határozza meg az áthaladt összes kerékpáros számát, és írassa ki a minta szerint! Ügyeljen arra, hogy a számítás során a mérőhibás adatok ne befolyásolják az összeget!
   **Expected Output:**
   ```
     Összesen 838 kerékpárost számoltak.
   ```
3. `[group]` Írassa ki, hogy óránként hány kerékpáros haladt át a számlálón!
   **Expected Output:**
   ```
     Óránkénti mérések:
     6 órától 123 kerékpáros
     7 órától 149 kerékpáros
     8 órától 297 kerékpáros
     9 órától 269 kerékpáros
   ```
4. `[min_max]` Határozza meg a legnagyobb mérési értéket és rögzítésének időpontját! Több max esetén az elsőt!
   **Expected Output:**
   ```
     Az áthaladók maximális száma: 82; a rögzítés időpontja: 8:30.
   ```

---

### Palacsinta

#### Meta
- level: közép
- year: 2026
- session: május
- language: idegen
- difficulty: 4

#### Tags
- IO
- count
- simulation
- lookup

#### Scenario
Egy testvérpár tavaly júliusban 10 nap dolgozott napi néhány órát, amiért ketten együtt
mindennap 12 000 Ft-ot kaptak kézhez. Megállapodtak, hogy ebből naponta 4000 Ft-ot egy
közös kasszába tesznek, a többit elfelezik. A munkahely közelében felfedeztek egy különleges
palacsintázót, ahol több tucatnyi ízesítéssel készítik a finom desszertet. Elhatározták, hogy
minden nap kiválasztanak valamilyen palacsintát, és annyit esznek belőle, amennyire futja a
közös kasszából.

#### Constraints
- 10 napi ár.
- Napi közös kassza alap: 4000 Ft.
- 3. feladat: minden nap külön 4000 Ft-ból hány adag férne (egész osztás).
- 4. feladat: maradék átvitele a következő napra (+4000).

#### Data
**files:** `arak.txt` (10 elem)

Sample:
```
690, 730, 750, 910, 740, 810, 880, 910, 925, 885
```

#### Tasks
1. `[IO]` A megadott 10 számot tárolja el a programban egy megfelelő adatszerkezetben!
2. `[IO]` `[lookup]` Kérje be egy nap sorszámát, és adja meg, hogy aznap hány forintos palacsintát ettek!
   **Expected Input:**
   ```
     Adja meg egy nap sorszámát! input(2)
   ```
   **Expected Output:**
   ```
     A 2. napon output(730) Ft volt egy adag palacsinta.
   ```
3. `[count]` Határozza meg mindennapra, hogy 4000 forintból hány adag adott ízesítésű palacsintát lehetne venni! Az adagok számát a mintának megfelelően írja ki!
   **Expected Output:**
   ```
     5 5 5 4 5 4 4 4 4 4
   ```
4. `[simulation]` Az első nap 4000 Ft-ból vásároltak, a maradékot a következő nap hozzáadták az aznapi 4000 Ft-hoz. Adja meg, hogy az egyes napokon hány adag palacsintát vettek!
   **Expected Output:**
   ```
     A(z) 1. napon 5 adag palacsintát vettek.
     A(z) 2. napon 6 adag palacsintát vettek.
     A(z) 3. napon 5 adag palacsintát vettek.
     A(z) 4. napon 4 adag palacsintát vettek.
     A(z) 5. napon 6 adag palacsintát vettek.
     A(z) 6. napon 5 adag palacsintát vettek.
     A(z) 7. napon 4 adag palacsintát vettek.
     A(z) 8. napon 5 adag palacsintát vettek.
     A(z) 9. napon 4 adag palacsintát vettek.
     A(z) 10. napon 5 adag palacsintát vettek.
   ```

---

### Nyomás

#### Meta
- level: közép
- year: 2026
- session: május
- language: hu
- difficulty: 2

#### Tags
- IO
- count
- min_max

#### Scenario
Egy kísérletben egy diák a nyomást a vízoszlop magasságával mérte milliméterben. 14 mérési adat áll rendelkezésre. A mérési adatok egész számok. Készítsen programot, ami megoldja a következő feladatokat!

#### Constraints
- 14 egész mérési adat.
- Több legkisebb érték esetén elegendő az egyik helyét megadni.
- Feltételezhető, hogy van csökkenés az adatsorban.

#### Data
**files:** `nyomas.txt` (14 elem)

Sample:
```
865, 846, 831, 820, 808, 783, 788, 775, 752, 750, 743, 745, 758, 770
```

#### Tasks
1. `[IO]` A megadott mérési adatokat tárolja el a program forrásában egy megfelelő adatszerkezetben!
2. `[min_max]` Írja ki a legkisebb mérési adat értékét és azt, hogy ez hányadik mérési adat volt! Ha több legkisebb érték lenne, elegendő egyik helyét megadnia.
   **Expected Output:**
   ```
     A legkisebb mért érték: 743
     A legkisebb mérési adat sorszáma: 11
   ```
3. `[IO]` `[count]` A kísérlet szempontjából fontosak az egy megadott határérték alatti mérések. A program kérjen be a felhasználótól egy egész értéket, majd írja ki, hogy hány mérési adat volt a megadott érték alatt! A következő üzenet jelenjen meg az adatbekérésnél: „Minél kisebb értékeket keres? (egész szám)” A válaszban a határérték is jelenjen meg a minta szerint! Bekérő szöveg: `Minél kisebb értékeket keres? (egész szám)`.
   **Expected Input:**
   ```
     Minél kisebb értékeket keres? (egész szám) input(800)
   ```
   **Expected Output:**
   ```
     output(800) alatti mérések száma: output(9)
   ```
4. `[min_max]` A kísérlet kiértékelésénél érdekes a legnagyobb csökkenés. A szomszédos méréseket tekintve határozza meg és írja ki, hogy mennyi volt a legnagyobb csökkenés értéke! A megoldás során feltételezheti, hogy van az adatsorban csökkenés.
   **Expected Output:**
   ```
     A két mérés közötti legnagyobb csökkenés: 25
   ```

#### Exact strings
- `Minél kisebb értékeket keres? (egész szám)`

---

# Synthetic Exams

Generated exams for tutoring / synthetic expansion. Same schema as real exams; not from official papers.

### Fogások

#### Meta
- level: közép
- year: 2027
- session: május
- language: hu
- difficulty: 1

#### Tags
- IO
- count
- min_max

#### Scenario
Egy sporthorgász-versenyen a zsűri a kifogott halakat egyenként mérlegre tette. Tíz hal tömegét jegyezték fel dekagrammban, a fogás sorrendjében. A program a feljegyzett tömegeket a forrásában tárolja. A kiértékeléshez kell a fogások száma, a legnagyobb hal helye, valamint az, hogy hány hal éri el a kategória alsó határát.

#### Constraints
- 10 egész tömeg dekagrammban; cserélhető adatokkal is működnie kell.
- Tömegek: 1–30.
- Több azonos legnagyobb érték esetén az első előfordulás sorszáma (1-től).
- Határérték bekérése: pozitív egész; a bemenet érvényességét nem kell ellenőrizni.

#### Data
Sample:
```
12, 8, 15, 7, 15, 9, 11, 6, 14, 10
```

Explanation:
Tíz egész szám, a halak tömege dekagrammban, a fogás sorrendjében. A program ezeket a forrásában tárolja, nem fájlból olvassa.

#### Tasks
1. `[IO]` A versenyen mért tíz hal tömegét a program forrásában kell eltárolnia. Tárolja el a megadott számokat egy megfelelő adatszerkezetben!
2. `[count]` Határozza meg, hány hal tömegét tárolta el a program! Az eredményt a képernyőre írja ki, és nevezze meg a kiírt adatot!
   **Expected Output:**
   ```
     A fogasok szama: 10
   ```
3. `[min_max]` A zsűri a legnagyobb halat díjazza. Határozza meg a legnagyobb tömeget, és azt, hogy ez a hal hányadik a feljegyzésben! Ha több azonos legnagyobb érték van, az első előfordulást adja meg!
   **Expected Output:**
   ```
     A legnagyobb hal: 15 dkg, 3. a sorban.
   ```
4. `[IO]` `[count]` A nevezési kategória alsó határa versenyenként más. Kérje be a felhasználótól a határértéket dekagrammban, majd adja meg, hány hal tömege éri el vagy haladja meg ezt az értéket! A bekéréskor jelenjen meg a `Kategoria also hatara (dkg):` szöveg.
   **Expected Input:**
   ```
     Kategoria also hatara (dkg): input(10)
   ```
   **Expected Output:**
   ```
     Legalabb output(10) dkg-os halak szama: output(6)
   ```

#### Exact strings
- `Kategoria also hatara (dkg):`

---



### Hűtőház

#### Meta
- level: emelt
- year: 2027
- session: október
- language: hu
- difficulty: 5

#### Tags
- IO
- count
- sum
- min_max
- lookup
- validate
- simulation
- function

#### Scenario
Egy gyümölcstermelő szövetkezet hűtőházában minden rakodást számítógép rögzít. A gyümölcs ládákban érkezik és ládákban távozik. Minden eseményhez feljegyzik az óra–perc időpontot, a művelet irányát, a termék nevét és a ládák számát. A sorok időrendben követik egymást. A hűtőház befogadóképessége korlátozott, ezért a nap során a futó készletet és a kapacitás esetleges túllépését is vizsgálni kell. Egy termékből több beszállítás és kiszállítás is előfordulhat.

#### Constraints
- Események ≤ 2000; óra 0–23, perc 0–59; az állomány időrendben van.
- Művelet: `BE` (beszállítás) vagy `KI` (kiszállítás); termék: egy ékezetmentes nagybetűs szó.
- Ládák száma eseményenként 1–50; a hűtőház kapacitása 70 láda.
- Feltételezheti, hogy `KI` soha nem kér többet, mint amennyi az adott termékből éppen bent van.
- 5. feladat: a bekért időpont a első és az utolsó esemény közé esik (a szélső értékek megengedettek).
- 6. feladat tesztjavaslat: `ALMA` (van a fájlban). Több azonos legnagyobb `BE` esetén az állományban első.

#### Data
**files:** `rakodas.txt` (180 sor)

Sample:
```
6 12 BE ALMA 40
6 40 KI ALMA 15
7 5 BE KORTE 28
7 18 BE ALMA 20
8 0 KI KORTE 10
8 55 KI ALMA 30
9 10 BE SZILVA 12
9 45 KI ALMA 10
10 20 BE KORTE 22
10 50 KI SZILVA 5
11 15 KI KORTE 8
12 0 BE ALMA 18
```

Explanation:
Minden sor egy rakodási esemény, szóközzel elválasztott mezőkkel: óra, perc, művelet (`BE` vagy `KI`), a termék neve, majd a ládák száma. A mintában a 6:12-kor 40 láda alma érkezik; 6:40-kor 15 ládát visznek ki belőle. A készlet az események sorrendjében változik, a kapacitás a bent lévő ládák összesen értendő.

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `rakodas.txt` tartalmát!
2. `[count]` Határozza meg, hány rakodási eseményt tartalmaz az állomány, és írja a képernyőre az események számát! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A rakodasi esemenyek szama: 12
   ```
3. `[min_max]` A beszállítások (`BE`) közül keresse meg a legnagyobb ládaszámú tételt! Írja a képernyőre a ládák számát és a termék nevét! Ha több ilyen beszállítás is van, az állományban elsőként szereplőt adja meg!
   **Expected Output:**
   ```
     A legnagyobb beszallitas: 40 lada, termek: ALMA
   ```
4. `[function]` Készítsen függvényt percben néven, amely megadja, hogy a paraméterként kapott óra és perc a nap hányadik perce! A függvény két egész számot kapjon, a visszaadott érték egy egész szám legyen! Az éjfél a 0. perc, a 8 óra 30 perc a 510. perc. A függvényt a későbbi feladatok megoldásánál felhasználhatja.
5. `[IO]` `[simulation]` Kérje be a felhasználótól egy időpont óra és perc értékét! A percben függvény segítségével határozza meg, hogy ebben az időpontban hány láda volt összesen a hűtőházban! Vegye figyelembe az összes, a bekért időpontnál nem későbbi eseményt! Feltételezheti, hogy a bekért időpont az első és az utolsó esemény közé esik.
   **Expected Input:**
   ```
     Ora: input(8)
     Perc: input(30)
   ```
   **Expected Output:**
   ```
     A hutohazban ekkor output(63) lada volt.
   ```
6. `[IO]` `[lookup]` `[count]` `[sum]` Kérje be a felhasználótól egy termék nevét! A teszteléshez használhatja az `ALMA` nevet, amely szerepel az állományban. Ha a bekért név egyetlen eseményben sem fordul elő, írja ki a `Nincs ilyen termek.` szöveget, és ne végezze el a következő két részfeladatot!
   **Expected Input:**
   ```
     Adja meg a termek nevet! input(ALMA)
   ```
	1. Adja meg, hány beszállítás (`BE`) történt ebből a termékből a nap során! A kiszállításokat ne számolja bele!
	   **Expected Output:**
   ```
	     A beszallitasok szama: output(3)
   ```
	2. Határozza meg, hány láda maradt ebből a termékből a nap utolsó eseménye után! A beszállított és a kiszállított mennyiség különbségét írja a képernyőre!
	   **Expected Output:**
   ```
	     A zaro keszlet: output(23) lada
   ```
7. `[validate]` `[simulation]` A hűtőház kapacitása 70 láda. A rakodások sorrendjében kövesse a bent lévő ládák összesenjét, és döntse el, túllépte-e ez az érték a kapacitást!
	1. Ha volt túllépés, írja ki: `A hűtőház legalább egyszer túllépte a kapacitást.` Ha nem volt, írja ki: `A hűtőház a nap folyamán végig a kapacitáson belül maradt.`
	   **Expected Output:**
   ```
	     output(A hűtőház legalább egyszer túllépte a kapacitást.)
   ```
	2. Ha volt túllépés, adja meg annak az eseménynek az óra és perc értékét, amelynél a készlet először haladta meg a 70-et! Ha nem volt túllépés, erről a részfeladatról ne írjon ki semmit!
	   **Expected Output:**
   ```
	     Az elso tullepes idopontja: output(7:18)
   ```
8. `[IO]` `[simulation]` A nap során a készlet alakulását a `keszlet.txt` állományba kell menteni. Minden rakodási esemény után írjon egy sort: az esemény óráját, percét és az esemény után bent lévő ládák összesenjét, szóközzel elválasztva! A sorok sorrendje egyezzen meg az események sorrendjével!

#### Exact strings
- `Nincs ilyen termek.`
- `A hűtőház legalább egyszer túllépte a kapacitást.`
- `A hűtőház a nap folyamán végig a kapacitáson belül maradt.`

---

### Csomagfeladás

#### Meta
- level: közép
- year: 2028
- session: május
- language: hu
- difficulty: 3

#### Tags
- IO
- lookup
- sum
- table
- simulation

#### Scenario
Egy postahivatal a csomagokat tömeg szerint díjazza. A díjtáblázat lépcsős: a csomag tömege a táblázatban szereplő felső határig az adott díjat viseli. A kezelő a feladott csomagok tömegét egymás után adja meg kilogrammban, és nullával jelzi a sor végét. A program minden csomagra kiírja a díjat, majd az aznapi bevételt.

#### Constraints
- A `dijszabas.txt` soronként egy felső határt (kg) és egy díjat (Ft) tartalmaz, növekvő határ szerint.
- Minden csomag tömege 1 és a táblázat legnagyobb határa közé esik; 0 a sor vége.
- Pontos egyezés a határon a kisebb kategóriába tartozik (`<=`).
- A bemenet érvényességét nem kell ellenőrizni.

#### Data
**files:** `dijszabas.txt` (3 sor)

Sample (`dijszabas.txt`):
```
5 800
10 1200
20 1800
```

Explanation:
Minden sor két egész: a kategória legnagyobb tömege kilogrammban és a kategória díja forintban. A mintában az 1–5 kg-os csomag 800 Ft, a 6–10 kg-os 1200 Ft, a 11–20 kg-os 1800 Ft.

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `dijszabas.txt` tartalmát!
2. `[count]` `[table]` Határozza meg, hány díjkategóriát tartalmaz a táblázat! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A dijkategoriak szama: 3
   ```
3. `[IO]` `[lookup]` `[sum]` `[simulation]` Kérje be a felhasználótól a csomagok tömegét kilogrammban, egyenként, amíg 0-t nem kap! Minden pozitív tömegre írja ki a `Dij: … Ft` sort a táblázat szerinti díjjal! A bekéréskor mindig jelenjen meg a `Csomag tomege (kg):` szöveg.
   **Expected Input:**
   ```
     Csomag tomege (kg): input(3)
     Csomag tomege (kg): input(8)
     Csomag tomege (kg): input(15)
     Csomag tomege (kg): input(4)
     Csomag tomege (kg): input(0)
   ```
	1. Minden pozitív tömegű csomagra írja ki a díjat a fenti formában!
	   **Expected Output:**
   ```
	     Dij: output(800) Ft
	     Dij: output(1200) Ft
	     Dij: output(1800) Ft
	     Dij: output(800) Ft
   ```
	2. A feladott csomagok díját adja össze, és írja ki az aznapi bevételt! A 0 tömegű záróértéket ne számolja díjnak!
	   **Expected Output:**
   ```
	     Osszesen: output(4600) Ft
   ```

#### Exact strings
- `Csomag tomege (kg):`

---

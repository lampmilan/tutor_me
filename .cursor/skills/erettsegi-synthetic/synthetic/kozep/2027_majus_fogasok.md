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

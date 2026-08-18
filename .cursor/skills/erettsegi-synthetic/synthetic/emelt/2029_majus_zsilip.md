### Zsilip

#### Meta
- level: emelt
- year: 2029
- session: május
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- min_max
- search
- validate
- function

#### Scenario
Egy tiszai zsilipnél a vízszintet negyedóránként rögzítik. Minden méréshez feljegyzik az óra–perc időpontot és a szintet centiméterben. A kezelőnek a szomszédos mérések különbsége a fontos: ha két egymást követő érték eltérése meghaladja a 12 centimétert, riasztást kell adni. A különbség abszolút értékét egy függvény számolja, amelyet a későbbi feladatok is felhasználnak. A program a méréseket állományból olvassa.

#### Constraints
- Mérések 2–200; óra 0–23, perc 0, 15, 30 vagy 45; az állomány időrendben van.
- Vízszint 50–250 cm.
- Riasztás: két egymást követő mérés abszolút különbsége > 12.
- 6. feladat: a bekért két időpont szerepel az állományban, az első nem későbbi, mint a második.

#### Data
**files:** `vizszint.txt` (7 sor)

Sample (`vizszint.txt`):
```
6 0 142
6 15 148
6 30 155
6 45 151
7 0 168
7 15 170
7 30 163
```

Explanation:
Minden sor egy mérés: óra, perc, vízszint centiméterben. A mintában 6:45 és 7:00 között 17 cm a különbség, ez riasztást vált ki.

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `vizszint.txt` tartalmát!
2. `[count]` Határozza meg, hány mérést tartalmaz az állomány, és írja a képernyőre a mérések számát! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A meresek szama: 7
   ```
3. `[function]` Készítsen függvényt kulonbseg néven, amely megadja két vízszint abszolút különbségét! A függvény két egész számot kapjon, a visszaadott érték egy egész szám legyen! A 151 és a 168 bemenetre a függvény 17-et adjon. A függvényt a későbbi feladatok megoldásánál felhasználhatja.
4. `[min_max]` `[validate]` A kulonbseg függvény segítségével határozza meg a szomszédos mérések legnagyobb szintváltozását! Írja ki a változás értékét, valamint annak a korábbi mérésnek az óra és perc értékét, ahonnan az ugrás indult! Ha több azonos legnagyobb ugrás van, az állományban elsőt adja meg!
   **Expected Output:**
   ```
     A legnagyobb valtozas: 17 cm, kezdete: 6:45
   ```
5. `[validate]` Döntse el, volt-e a napon riasztás, azaz előfordult-e 12 cm-nél nagyobb szomszédos ugrás! Ha volt, írja ki: `Volt riasztas.` Ha nem volt, írja ki: `Nem volt riasztas.`
   **Expected Output:**
   ```
     Volt riasztas.
   ```
6. `[IO]` `[search]` Kérje be a felhasználótól két időpont óra és perc értékét! A kulonbseg függvény segítségével adja meg a két időponthoz tartozó vízszintek abszolút különbségét! Feltételezheti, hogy mindkét időpont szerepel az állományban.
   **Expected Input:**
   ```
     Elso ora: input(6)
     Elso perc: input(30)
     Masodik ora: input(7)
     Masodik perc: input(0)
   ```
   **Expected Output:**
   ```
     A ket idopont kulonbsege: output(13) cm
   ```

#### Exact strings
- `Volt riasztas.`
- `Nem volt riasztas.`

---

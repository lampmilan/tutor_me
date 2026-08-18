### Hulladékudvar

#### Meta
- level: emelt
- year: 2028
- session: október
- language: hu
- difficulty: 3

#### Tags
- IO
- count
- sum
- lookup
- weighted_sum
- search

#### Scenario
Egy települési hulladékudvar a beszállított anyagokat típus szerint jegyzi. Minden tételhez feljegyzik az anyag kódját és a tömeget kilogrammban. A pontszámot a típusonként rögzített, kilogrammonkénti díjtáblázat adja: a tétel pontja a tömeg és az egységpont szorzata. A program a napi tételeket állományból olvassa, a díjtáblázatot a feladatban kapja. A kiértékeléshez kell a forgalom, a kiosztott pontok és egy kiválasztott típus részösszege.

#### Constraints
- Tételek ≤ 800; tömeg 1–80 kg.
- Típuskód: ékezetmentes nagybetűs szó a táblázatból.
- 5. feladat tesztjavaslat: `PAPIR`. Ha a kód a napi tételek között nem szerepel, írja ki: `Nincs ilyen tipus.` Akkor is írja ki, ha a kód a táblázatban létezik, de aznap nem hoztak belőle semmit.

#### Data
**files:** `beszallitas.txt` (6 sor)

Sample (`beszallitas.txt`):
```
PAPIR 12
UV 3
FEM 8
PAPIR 4
ZOLD 20
FEM 2
```

Explanation:
Minden sor egy beszállítás: anyagkód és tömeg kilogrammban. Egy kód több tételben is előfordulhat. A pont a táblázat egységpontjának és a tömegnek a szorzata.

#### Tables

**Egységpont**

| Típus | Pont / kg |
| --- | --- |
| PAPIR | 5 |
| UV | 15 |
| FEM | 20 |
| ZOLD | 2 |
| UREG | 8 |

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `beszallitas.txt` tartalmát!
2. `[count]` `[sum]` Határozza meg a tételek számát és a beszállított össztömeget! Az adatokat külön sorban, megnevezve írja ki!
   **Expected Output:**
   ```
     A tetelsorok szama: 6
     Az ossztomeg: 49 kg
   ```
3. `[weighted_sum]` `[lookup]` A táblázat szerint számítsa ki a napon kiosztott pontok összegét! Minden tétel pontja a tömeg és a típus egységpontjának szorzata. Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A kiosztott pontok: 365
   ```
4. `[IO]` `[search]` `[lookup]` `[sum]` `[weighted_sum]` Kérje be a felhasználótól egy anyagkódot! A teszteléshez használhatja a `PAPIR` kódot. Ha a kód a napi tételek között nem szerepel, írja ki a `Nincs ilyen tipus.` szöveget, és ne végezze el a következő két részfeladatot!
   **Expected Input:**
   ```
     Adja meg az anyag kodjat! input(PAPIR)
   ```
	1. Adja meg, hány kilogrammot hoztak ebből a típusból a nap során!
	   **Expected Output:**
   ```
	     A tipus tomege: output(16) kg
   ```
	2. Számítsa ki a típusra kiosztott pontok összegét a táblázat szerint!
	   **Expected Output:**
   ```
	     A tipus pontjai: output(80)
   ```

#### Exact strings
- `Nincs ilyen tipus.`

---

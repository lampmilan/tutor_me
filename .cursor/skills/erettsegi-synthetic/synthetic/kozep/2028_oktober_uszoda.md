### Uszoda

#### Meta
- level: közép
- year: 2028
- session: október
- language: hu
- difficulty: 3

#### Tags
- IO
- count
- sum
- min_max
- lookup
- table

#### Scenario
Egy uszoda a napi belépéseket a jegy típusával és a vásárolt darabszámmal jegyzi. Három jegyfajta van: NAPI, BERLET és GYEREK, mindegyikhez rögzített ár tartozik. A program a napi forgalmat állományból olvassa, az árakat pedig a feladatban megadott táblázatból veszi. A kiértékeléshez kell a látogatók száma, a legnépszerűbb jegy és a bevétel.

#### Constraints
- Forgalmi sorok száma 1–30; típus csak `NAPI`, `BERLET` vagy `GYEREK`.
- Darabszám soronként 1–20.
- Több azonos legnagyobb darabszámú típus esetén az állományban előbb összeadódó, a táblázat sorrendje szerinti elsőt adja meg: NAPI, BERLET, GYEREK.
- 4. feladat tesztjavaslat: `NAPI` (szerepel a mintában).

#### Data
**files:** `latogatok.txt` (5 sor)

Sample (`latogatok.txt`):
```
NAPI 3
BERLET 2
GYEREK 5
NAPI 1
BERLET 4
```

Explanation:
Minden sor egy eladási tétel: a jegy típusa és a darabszám. Egy típus több sorban is előfordulhat; a napi összesítéshez a darabszámokat típusonként össze kell adni.

#### Tables

**Árak**

| Típus | Ár (Ft) |
| --- | --- |
| NAPI | 2500 |
| BERLET | 1800 |
| GYEREK | 1200 |

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `latogatok.txt` tartalmát!
2. `[count]` `[sum]` Határozza meg, hány eladási tételt tartalmaz az állomány, és hogy összesen hány jegyet adtak el! A két adatot külön sorban, megnevezve írja ki!
   **Expected Output:**
   ```
     A tetelsorok szama: 5
     Az eladott jegyek szama: 15
   ```
3. `[min_max]` `[table]` Típusonként adja össze a darabszámokat, és írja ki azt a jegyfajtát, amelyből a legtöbbet adták el! Ha több ilyen van, a táblázatban előrébb álló típust adja meg!
   **Expected Output:**
   ```
     A legnepszerubb jegy: BERLET
   ```
4. `[IO]` `[lookup]` `[sum]` Kérje be a felhasználótól egy jegy típusát! A teszteléshez használhatja a `NAPI` nevet. Számítsa ki, mennyi bevétel származott ebből a típusból a táblázat árai szerint! A bekéréskor jelenjen meg az `Adja meg a jegy tipust!` szöveg.
   **Expected Input:**
   ```
     Adja meg a jegy tipust! input(NAPI)
   ```
   **Expected Output:**
   ```
     A tipus bevetel: output(10000) Ft
   ```

#### Exact strings
- `Adja meg a jegy tipust!`

---

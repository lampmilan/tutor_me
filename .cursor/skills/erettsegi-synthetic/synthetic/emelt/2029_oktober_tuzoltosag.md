### Tűzoltóság

#### Meta
- level: emelt
- year: 2029
- session: október
- language: hu
- difficulty: 3

#### Tags
- IO
- count
- sum
- min_max
- search
- group

#### Scenario
Egy megyei tűzoltóság a napi riasztásokat számítógépen gyűjti. Minden eseményhez feljegyzik az óra–perc időpontot, a kerületet, a riasztás típusát és a kivonuló autók számát. A tűzeseteket a nap végén külön jegyzékbe kell tenni. A program a riasztásokat állományból olvassa, összesíti a kivonulásokat, majd a tűzesetek adatait fájlba írja. Egy kerületben több riasztás is előfordulhat.

#### Constraints
- Riasztások ≤ 400; óra 0–23, perc 0–59; az állomány időrendben van.
- Típus: `TUZ`, `MUSZAKI` vagy `MENTO`; autók száma 1–6.
- Kerület: római számos azonosító ékezet nélkül (`I`, `V`, `VIII`, `XIII`).
- 5. feladat tesztjavaslat: kerület `I`. Ha a kerület egyetlen riasztásban sem szerepel, írja ki: `Nincs ilyen kerulet.`

#### Data
**files:** `riasztas.txt` (8 sor)

Sample (`riasztas.txt`):
```
7 12 I TUZ 3
7 40 V MUSZAKI 1
8 5 I TUZ 2
8 55 VIII MENTO 1
9 10 V TUZ 4
9 45 I MUSZAKI 2
10 20 XIII TUZ 2
11 0 VIII TUZ 3
```

Explanation:
Minden sor egy riasztás: óra, perc, kerület, típus, autók száma. A mintában öt tűzeset (`TUZ`) van; ezek kerülnek a kimeneti állományba.

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `riasztas.txt` tartalmát!
2. `[count]` `[sum]` Határozza meg a riasztások számát és a kivonult autók összegét! Az adatokat külön sorban, megnevezve írja ki!
   **Expected Output:**
   ```
     A riasztasok szama: 8
     A kivonult autok szama: 18
   ```
3. `[count]` `[group]` Számolja meg, hány riasztás volt `TUZ` típusú! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A tuzesetek szama: 5
   ```
4. `[min_max]` Adja meg a nap első riasztásának időpontját, kerületét és típusát! Az állomány időrendben van, ezért az első sor a legkorábbi esemény.
   **Expected Output:**
   ```
     Az elso riasztas: 7:12, kerulet: I, tipus: TUZ
   ```
5. `[IO]` `[search]` `[count]` Kérje be a felhasználótól egy kerület azonosítóját! A teszteléshez használhatja az `I` jelet. Ha a kerület egyetlen riasztásban sem szerepel, írja ki a `Nincs ilyen kerulet.` szöveget, és ne végezze el a következő részfeladatot!
   **Expected Input:**
   ```
     Adja meg a keruletet! input(I)
   ```
	1. Adja meg, hány riasztás történt ebben a kerületben!
	   **Expected Output:**
   ```
	     A kerulet riasztasai: output(3)
   ```
6. `[IO]` `[group]` A tűzesetek jegyzékét a `tuzesetek.txt` állományba kell menteni. Minden `TUZ` típusú riasztásról egy sort írjon: az órát, a percet, a kerületet és az autók számát, szóközzel elválasztva! A sorok sorrendje egyezzen meg az állománybeli sorrenddel!

#### Exact strings
- `Nincs ilyen kerulet.`

---

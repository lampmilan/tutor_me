### Műhely

#### Meta
- level: emelt
- year: 2028
- session: október
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- min_max
- search
- simulation

#### Scenario
Egy iskolai műhely a kölcsönzött szerszámokat időrendben naplózza. Minden eseményhez feljegyzik az óra–perc időpontot, a művelet irányát és a szerszám azonosítóját. A `KI` a kölcsönzést, a `BE` a visszavételt jelenti. Egy szerszámot csak akkor adnak ki újra, ha már visszahozták. A nap végén néhány szerszám még kint lehet. A program a párosítható ki- és bejegyzésekből a kölcsönzés hosszát is számítja.

#### Constraints
- Események ≤ 1500; óra 7–16, perc 0–59; az állomány időrendben van.
- Művelet: `KI` vagy `BE`; szerszám azonosítója 1–99.
- Feltételezheti, hogy `BE` mindig egy kint lévő szerszámra vonatkozik, és `KI` nem ad ki már kint lévő azonosítót.
- 5. feladat tesztjavaslat: szerszám `12` (van lezárt kölcsönzése). Ha az azonosító egyetlen eseményben sem szerepel, írja ki: `Nincs ilyen szerszam.`

#### Data
**files:** `kolcsonzes.txt` (8 sor)

Sample (`kolcsonzes.txt`):
```
8 15 KI 12
9 40 BE 12
10 0 KI 7
11 20 KI 12
12 5 BE 7
13 10 KI 3
14 0 BE 12
15 30 KI 7
```

Explanation:
Minden sor egy esemény: óra, perc, művelet (`KI` vagy `BE`), szerszám azonosító. A mintában a 12-es szerszámot 8:15-kor viszik ki és 9:40-kor hozzák vissza; később újra kiadják. A 3-as szerszám a nap végén kint marad.

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `kolcsonzes.txt` tartalmát!
2. `[count]` Határozza meg, hány eseményt tartalmaz az állomány, és írja a képernyőre az események számát! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A kolcsonzesi esemenyek szama: 8
   ```
3. `[simulation]` `[count]` A napló sorrendjében kövesse, mely szerszámok vannak kint! A nap utolsó eseménye után írja ki, hány szerszám maradt kint, majd a kint maradt azonosítókat növekvő sorrendben, szóközzel elválasztva!
   **Expected Output:**
   ```
     A kint maradt szerszamok szama: 2
     A kint maradt azonosito: 3 7
   ```
4. `[min_max]` `[simulation]` A lezárt kölcsönzések (egy `KI` és a hozzá tartozó következő `BE` ugyanarra az azonosítóra) közül keresse meg a leghosszabbat percben! Írja ki a percet és a szerszám azonosítóját! Ha több azonos hosszúságú van, az állományban korábban kezdődőt adja meg!
   **Expected Output:**
   ```
     A leghosszabb kolcsonzes: 160 perc, szerszam: 12
   ```
5. `[IO]` `[search]` `[simulation]` Kérje be a felhasználótól egy szerszám azonosítóját! A teszteléshez használhatja a 12-es azonosítót. Ha az azonosító egyetlen eseményben sem szerepel, írja ki a `Nincs ilyen szerszam.` szöveget, és ne végezze el a következő részfeladatot!
   **Expected Input:**
   ```
     Adja meg a szerszam azonositojat! input(12)
   ```
	1. Adja meg, hány lezárt kölcsönzése volt ennek a szerszámnak, és ezek percben mért összegét!
	   **Expected Output:**
   ```
	     A lezart kolcsonzesek szama: output(2)
	     A kolcsonzesek osszideje: output(245) perc
   ```

#### Exact strings
- `Nincs ilyen szerszam.`

---

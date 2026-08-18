### Árapály

#### Meta
- level: emelt
- year: 2027
- session: május
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- min_max
- search
- simulation

#### Scenario
Egy kutatóállomás a partmenti mocsár vízmélységét négyzetrácsos hálón méri centiméterben. Az állomány első sora a rács méretét adja meg, a további sorok a mélységértékeket. Medencének az a rácspont számít, amelynek mélysége szigorúan kisebb minden létező szomszédjánál; az éleken kevesebb szomszéd van. A program a rácsot beolvassa, majd a szélső értékeket, egy kiválasztott cella környezetét és a medencék számát határozza meg.

#### Constraints
- Rács N×M, 2 ≤ N, M ≤ 50; mélységek 0–200 egész centiméter.
- Szomszédok: az észak, dél, nyugat, kelet irányú cellák, ha léteznek; az átlós cellák nem szomszédok.
- Medence: a cella értéke minden létező szomszédnál szigorúan kisebb.
- 4. feladat tesztjavaslat: sor 2, oszlop 3 (a mintában belso cella). A sorszámok 1-től indulnak.

#### Data
**files:** `melyseg.txt` (5 sor)

Sample (`melyseg.txt`):
```
4 4
4 7 7 2
5 9 3 4
6 3 3 8
2 5 4 1
```

Explanation:
Az első sor a sorok és az oszlopok száma. A további N sor egyenként M egész: a vízmélység centiméterben. A mintában a jobb alsó sarok 1 cm, ez medence, mert mindkét létező szomszédja mélyebb.

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `melyseg.txt` tartalmát!
2. `[count]` `[min_max]` Határozza meg a rácspontok számát, valamint a legkisebb és a legnagyobb mélységet! Az adatokat külön sorban, megnevezve írja ki!
   **Expected Output:**
   ```
     A racspontok szama: 16
     A legkisebb melyseg: 1 cm
     A legnagyobb melyseg: 9 cm
   ```
3. `[simulation]` `[count]` Számolja meg a medencéket a fenti definíció szerint! A medencék számát nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A medencek szama: 4
   ```
4. `[IO]` `[search]` Kérje be a felhasználótól egy cella sor- és oszlopsorszámát! Feltételezheti, hogy a sorszámok a rács tartományába esnek. Írja ki a cella mélységét, majd a létező szomszédok mélységét a `N:`, `S:`, `NY:`, `K:` címkékkel, abban a sorrendben, amelyik irány létezik!
   **Expected Input:**
   ```
     Sor: input(2)
     Oszlop: input(3)
   ```
   **Expected Output:**
   ```
     A cella melysege: output(3) cm
     N: output(7)
     S: output(3)
     NY: output(9)
     K: output(4)
   ```
5. `[IO]` `[simulation]` A medencék helyét a `medencek.txt` állományba kell menteni. Minden medencéről egy sort írjon: a sor sorszámát, az oszlop sorszámát és a mélységet, szóközzel elválasztva! A sorok a rács bejárási sorrendjében legyenek (felülről le, balról jobbra)!

---

### Adagoló

#### Meta
- level: emelt
- year: 2028
- session: május
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
Egy rendelő automata adagolója a kiadott készítményeket betegnaplóba írja. Egy beteghez több tétel tartozhat, a beteg zárását egy `X` karakterű sor jelzi. A tételek a készítmény nevét és a kiadott dobozok számát tartalmazzák. A naplóban a betegek az ellátás sorrendjében követik egymást. A program a naplót beolvassa, majd a betegek számát, a legnagyobb adagot és egy kiválasztott készítmény összesített forgalmát határozza meg.

#### Constraints
- Betegek száma 1–200; tételek betegenként 1–8.
- Készítménynév: ékezetmentes nagybetű vagy kötőjel; dobozszám 1–5.
- Az állomány minden beteget `X` sorral zár, üres beteg (két `X` egymás után) nem fordul elő.
- 5. feladat tesztjavaslat: `PARACETAMOL`. Ha a név egyetlen tételben sem szerepel, írja ki: `Nincs ilyen keszitmeny.`

#### Data
**files:** `adagolo.txt` (11 sor)

Sample (`adagolo.txt`):
```
PARACETAMOL 2
IBUPROFEN 1
X
PARACETAMOL 1
X
IBUPROFEN 2
C-VITAMIN 3
X
PARACETAMOL 2
X
```

Explanation:
A nem `X` sorok egy tételt írnak le: készítmény neve és dobozszám. Az `X` az aktuális beteg zárása. A mintában négy beteg van; a harmadik kapta a legtöbb dobozt (5).

#### Tasks
1. `[IO]` Olvassa be és tárolja el az `adagolo.txt` tartalmát!
2. `[count]` Határozza meg, hány beteg adatait tartalmazza az állomány! Az `X` sorokat ne számolja tételnek! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A betegek szama: 4
   ```
3. `[sum]` `[min_max]` `[group]` Betegenként adja össze a kiadott dobozokat! Írja ki az összes kiadott doboz számát, valamint annak a betegnek a sorszámát (1-től) és dobozszámát, aki a legtöbbet kapta! Ha több ilyen van, az állományban első beteget adja meg!
   **Expected Output:**
   ```
     Az osszes doboz: 11
     A legnagyobb adag: 3. beteg, 5 doboz
   ```
4. `[IO]` `[search]` `[sum]` Kérje be a felhasználótól egy készítmény nevét! A teszteléshez használhatja a `PARACETAMOL` nevet. Ha a név egyetlen tételben sem fordul elő, írja ki a `Nincs ilyen keszitmeny.` szöveget, és ne végezze el a következő részfeladatot!
   **Expected Input:**
   ```
     Adja meg a keszitmeny nevet! input(PARACETAMOL)
   ```
	1. Adja meg, hány dobozt adtak ki ebből a készítményből a nap során, minden beteg tételét beleszámítva!
	   **Expected Output:**
   ```
	     A kiadott dobozok szama: output(5)
   ```
5. `[IO]` `[group]` A betegek összesítését a `betegek.txt` állományba kell menteni. Minden betegről egy sort írjon: a beteg sorszámát (1-től) és a neki kiadott dobozok összegét, szóközzel elválasztva! A sorok a napló sorrendjét kövessék!

---

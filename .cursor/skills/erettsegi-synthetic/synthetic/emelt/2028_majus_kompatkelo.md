### Kompátkelő

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
Egy Duna-menti kompállomás a napi járatokat számítógépen tartja nyilván. Az állomány első sora a komp befogadóképességét adja meg járműben, a további sorok egy-egy járatot írnak le: a járat azonosítóját, a dátumot, a szállított járművek számát és a célállomás kódját. Egy célra több járat is indulhat. A forgalom értékeléséhez a járatok számát, a legterheltebb fordulót és egy kiválasztott cél összesített forgalmát kell meghatározni.

#### Constraints
- Járatok száma ≤ 500; a kapacitás 10–80 jármű.
- Járművek száma járatonként 1 és a kapacitás közé esik.
- Célkód: négy ékezetmentes nagybetű.
- Több azonos legnagyobb járműszám esetén az állományban első járatot adja meg.
- 5. feladat tesztjavaslat: `PECS` (szerepel a mintában). Ha a bekért kód egyetlen járatban sem fordul elő, írja ki: `Nincs ilyen celallomas.`

#### Data
**files:** `jaratok.txt` (9 sor)

Sample (`jaratok.txt`):
```
40
101 6 12 28 PECS
102 6 12 35 MOHA
103 6 13 18 PECS
104 6 13 40 BAJA
105 6 14 22 MOHA
106 6 14 31 PECS
107 6 15 12 BAJA
108 6 15 39 MOHA
```

Explanation:
Az első sor a komp kapacitása járműben. A további sorok szóközzel elválasztott mezői: járatazonosító, hónap, nap, szállított járművek száma, célállomás kódja. A mintában a 104-es járat teljesen tele van (40 jármű).

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `jaratok.txt` tartalmát!
2. `[count]` Határozza meg, hány járat adatait tartalmazza az állomány, és írja a képernyőre a járatok számát! Az első sor a kapacitás, azt ne számolja járatnak! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A jaratok szama: 8
   ```
3. `[min_max]` Keresse meg a legnagyobb járműszámú járatot! Írja a képernyőre a járat azonosítóját, a járművek számát és a cél kódját! Ha több ilyen járat van, az állományban elsőként szereplőt adja meg!
   **Expected Output:**
   ```
     A legterheltebb jarat: 104, 40 jarmu, cel: BAJA
   ```
4. `[group]` `[count]` `[sum]` Célállomásonként határozza meg a járatok számát és a szállított járművek összegét! A célokat az állományban való első előfordulásuk sorrendjében, soronként írja ki!
   **Expected Output:**
   ```
     PECS 3 77
     MOHA 3 96
     BAJA 2 52
   ```
5. `[IO]` `[search]` `[sum]` Kérje be a felhasználótól egy célállomás kódját! A teszteléshez használhatja a `PECS` kódot. Ha a kód egyetlen járatban sem szerepel, írja ki a `Nincs ilyen celallomas.` szöveget, és ne végezze el a következő részfeladatot!
   **Expected Input:**
   ```
     Adja meg a celallomas kodjat! input(PECS)
   ```
	1. Adja meg, hány járat indult erre a célra, és összesen hány járművet szállítottak oda!
	   **Expected Output:**
   ```
	     A jaratok szama: output(3)
	     A jarmuvek szama: output(77)
   ```

#### Exact strings
- `Nincs ilyen celallomas.`

---

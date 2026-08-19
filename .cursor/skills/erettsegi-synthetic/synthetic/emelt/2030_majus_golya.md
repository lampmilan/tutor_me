### Gólya

#### Meta
- level: emelt
- year: 2030
- session: május
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- search
- min_max
- group
- lookup
- validate
- function

#### Scenario
Egy természetvédelmi egyesület Zsiga, egy fehér gólya őszi vonulását követi nyomon. A madár hátára erősített jeladó minden nap egy helymeghatározást küld: a dátumot, a pozíció egész koordinátáit és annak az országnak a nevét, amelynek területén a gólya aznap tartózkodott. Az állomány időrendben tartalmazza a méréseket. A program feladata a rögzített útvonal alapján megállapítani, hol mennyi időt töltött a madár, mekkora volt a napi elmozdulás, és mely napokon lépte át a határokat.

#### Constraints
- Mérések ≤ 400; az állomány időrendben van; minden sor egy naptári nap egyetlen mérése.
- Hónap 8–10; a nap a naptár szerint érvényes; x és y egész szám, -1000 és 1000 között.
- Az x keleti, az y északi irányban nő; a távolság egysége a térkép rácsegysége.
- Ország: egy ékezetmentes szó (például `Magyarorszag`, `Szerbia`, `Egyiptom`).
- Napi elmozdulás: két szomszédos mérés euklideszi távolsága, három tizedesjegyre kerekítve.
- 5. feladat tesztjavaslat: `Szerbia` (szerepel a fájlban). Ha a bekért név nem fordul elő, írja ki: `Zsiga nem jart ebben az orszagban.`
- 7. feladat: döntetlen esetén az állományban először megjelenő országot adja meg.
- 8. feladat: határátlépés, ha két szomszédos mérés országa különbözik; a kimeneti sor a későbbi (érkezési) dátumot tartalmazza.

#### Data
**files:** `golya.txt` (14 sor), `hatar.txt` (kimenet)

Sample (`golya.txt`):
```
8 20 19 47 Magyarorszag
8 21 20 46 Magyarorszag
8 22 21 44 Szerbia
8 23 22 43 Szerbia
8 24 23 43 Szerbia
8 25 25 42 Bulgaria
8 26 27 41 Bulgaria
8 27 32 39 Torokorszag
8 28 34 37 Torokorszag
8 29 36 35 Sziria
8 30 35 32 Izrael
8 31 33 30 Egyiptom
9 1 32 28 Egyiptom
9 2 31 27 Egyiptom
```

Explanation:
Minden sor egy napi helymeghatározás, szóközzel elválasztott mezőkkel: hónap, nap, x koordináta, y koordináta, majd az ország neve. A mintában Zsiga augusztus 20-án Magyarországon van, augusztus 22-én lép Szerbiába, és szeptember 2-án Egyiptomban zárja a megfigyelt szakaszt. Egy országban eltöltött napok száma a rá vonatkozó sorok száma.

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `golya.txt` tartalmát!
2. `[count]` Határozza meg, hány helymeghatározást tartalmaz az állomány! Minden sor egy naptári nap egyetlen mérésének felel meg. A mérések számát a képernyőn, megnevezve jelenítse meg!
   **Expected Output:**
   ```
     A meresek szama: 14
   ```
3. `[search]` `[count]` Adja meg a vonulás megfigyelt szakaszának első és utolsó országát! Az első a fájl első sorához, az utolsó az utolsó sorához tartozik. Írja ki azt is, hány különböző ország szerepel az állományban! Az adatokat külön sorban, megnevezve jelenítse meg!
   **Expected Output:**
   ```
     A vonulas kezdete: Magyarorszag
     A vonulas vege: Egyiptom
     Az erintett orszagok szama: 7
   ```
4. `[function]` Készítsen függvényt tavolsag néven, amely megadja két helyszín síkbeli távolságát! A függvény a két pont x és y koordinátáját egész számokként kapja meg, a visszaadott érték legyen valós szám! A távolságot a `(x1-x2)^2 + (y1-y2)^2` kifejezés négyzetgyökeként számolja! A függvényt a későbbi feladatok megoldásánál felhasználhatja.
5. `[IO]` `[lookup]` `[count]` `[validate]` Kérje be a felhasználótól egy ország nevét! A teszteléshez használhatja a `Szerbia` nevet, amely szerepel az állományban. Ha a bekért név egyetlen mérésben sem fordul elő, írja ki a `Zsiga nem jart ebben az orszagban.` szöveget, és ne végezze el a következő két részfeladatot!
   **Expected Input:**
   ```
     Adja meg az orszag nevet! input(Szerbia)
   ```
	1. Határozza meg, hány napon tartózkodott Zsiga a megadott országban! Minden, az országot tartalmazó sor egy napnak számít. A napok számát nevezze meg a kiírásban!
	   **Expected Output:**
   ```
	     Zsiga ebben az orszagban output(3) napot toltott.
   ```
	2. Adja meg, melyik dátumon volt Zsiga először, illetve utoljára a bekért országban! A dátumokat `hó.nap` alakban írja ki, például `8.22`! Ha csak egyetlen napot töltött ott, a két dátum egyezzen meg!
	   **Expected Output:**
   ```
	     Eloszor: output(8.22)
	     Utoljara: output(8.24)
   ```
6. `[min_max]` `[function]` A tavolsag függvény segítségével határozza meg a két szomszédos mérés közötti legnagyobb napi elmozdulást! A távolságot három tizedesjegyre kerekítve, a mintának megfelelően írja ki, és adja meg a korábbi mérés dátumát, ahonnan az elmozdulás indult! Ha több azonos legnagyobb érték van, az állományban első párt adja meg!
   **Expected Output:**
   ```
     A legnagyobb napi tavolsag: 5.385
     A repules napja: 8.26
   ```
7. `[group]` `[min_max]` Állapítsa meg, melyik országban töltötte Zsiga a legtöbb napot a megfigyelt szakaszon! Írja a képernyőre az ország nevét és a napok számát! Ha több ilyen ország is van, az állományban először megjelenőt adja meg!
   **Expected Output:**
   ```
     A legtobb nap: Szerbia, 3 nap
   ```
8. `[IO]` `[group]` A határátlépéseket a `hatar.txt` állományba kell menteni. Minden olyan szomszédos méréspárnál, ahol az ország megváltozik, írjon egy sort: az érkezés hónapját és napját, a kiinduló országot, majd az új országot, szóközzel elválasztva! A sorok a vonulás időrendjét kövessék!

#### Exact strings
- `Zsiga nem jart ebben az orszagban.`

---

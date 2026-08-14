
# Informatika and Digitális kultúra érettségi EMELT — Sanitized

> **Read-only gold.** Do not append synthetics here. New exams go in `../synthetic/emelt/`.

Structured corpus of **emelt** programming (algoritmizálás) exam tasks for synthetic generation and tutoring.

## Schema

```md
### ExamTitle

#### Meta
- level: közép
- year: YYYY
- session: május | október
- language: hu | idegen
- difficulty: 1-5

#### Tags
Exam-level skill tags (for tutoring / weak-point targeting). Use only from this list:
`IO`, `count`, `sum`, `min_max`, `search`, `validate`, `simulation`, `group`, `string`, `path`, `table`, `lookup`, `function`, `random`, `weighted_sum`

#### Scenario
Flavor text and rules the student must understand.

#### Constraints
- Bullet list of ranges, assumptions, and limits.

#### Example
Optional worked mini-example (not the full console sample).

#### Data
Hardcoded / file snippet the program may embed. Omit if interactive-only.

#### Tables
Optional markdown tables referenced by tasks.

#### Tasks
1. `[tag]` Task text…
2. `[tag]` …
   **Expected Output:**
   ```
     …
   ```
   **Expected Input:**
   ```
     Prompt! input(value)
   ```

Allowed tags: `IO`, `count`, `sum`, `min_max`, `search`, `validate`, `simulation`, `group`, `string`, `path`, `table`, `lookup`, `function`, `random`, `weighted_sum`

#### Exact strings
- Exact phrases the program must print (when specified).
```

**Data policy:** short samples only + `files:` with line counts. Do not paste full datasets.

**Common exam rules (all):** do not validate input; print task number before results; show prompt text on input; accent-free output OK.

**Expected I/O:** put **Expected Input:** / **Expected Output:** under the task they belong to (Virágágyások). Use `input(…)` / `output(…)` for interactive values. No trailing Sample I/O block.

---

# Emelt — Digitális kultúra



### Virágágyások

#### Meta
- level: emelt
- year: 2022
- session: október
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- search
- validate
- simulation

#### Scenario
Egy frissen épült óriási lakóparkba költözők elhatározták, hogy a még kopár környezetet megszépítik. A lakóparkot határoló kerítés mellett kijelölték a virágágyások helyét, és sorszámokkal látták el azokat. A sorszámozást, amely eggyel kezdődik, az egyetlen bejárat jobb oldalán lévő ágyással kezdték, és a bejárat bal oldalán lévő ágyással fejezték be. A lakók megadhatták, hogy mely szomszédos ágyásokat szeretnék beültetni. A felajánlásban megadták azt is, hogy milyen színű virággal.

#### Constraints
- Ágyások ≤ 3000; felajánlások száma ≤ ágyások száma.
- Körkörös szomszédság: utolsó ↔ első.
- 4. feladat tesztjavaslat: ágyás 1 (több felajánló), 269 (senki).

#### Data
**files:** `felajanlas.txt` (466 sor)

Sample:
```
2222
2073 2107 P
716 751 P
214 245 P
185 196 O
```

Explanation:
A fájl további soraiban két szám és egy betű található, egymástól egy-egy szóközzel elválasztva, amely egy lakó felajánlását írja le. (A felajánlások száma nem haladja meg a virágágyások számát.) Az első szám az első, a második az utolsó beültetni kívánt ágyás sorszáma. A betű az angol ábécé nagybetűje, amely a választott színt jelöli. Ha az első szám nagyobb, mint a második, akkor a választott intervallumba a sorszám szerinti utolsó és első ágyás, tehát a bejárat két oldala is beletartozik. Mindenki csak egy felajánlást tehet, de egy ágyás több felajánlásban is szerepelhet, azaz a felajánlásokban szereplő intervallumok átfedhetik egymást. Az ültetést a felajánlások sorrendjében végzik el a lakók.
#### Tasks
1. `[IO]` Olvassa be és tárolja a `felajanlas.txt` tartalmát!
2. `[count]` Írja ki, hány felajánlást tartalmaz az állomány!
   **Expected Output:**
   ```
     A felajánlások száma: 465
   ```
3. `[search]` Jelenítse meg a képernyőn azon felajánlások sorszámát, amelyek a bejárat bal és jobb oldalán található ágyást is beültetnék! A sorszámokat egy-egy szóközzel válassza el egymástól!
   **Expected Output:**
   ```
     A bejárat mindkét oldalán ültetők: 10 34 98 107 115 142 156 160 340 360 378
   ```
4. `[IO]` `[count]` `[simulation]` Kérje be a felhasználótól egy ágyás sorszámát! A tesztelés során használhatja az 1. ágyást, amelyet többen is beültetnének és a 269. ágyást, amelynek beültetésére senki sem vállalkozik.
   **Expected Input:**
   ```
     Adja meg az ágyás sorszámát! input(100)
   ```
	1. Írja a képernyőre, hogy hány felajánlásban szerepel ez az ágyás!
	   **Expected Output:**
   ```
	     A felajánlók száma: output(8)
   ```
	2. Adja meg, milyen színű lesz ez az ágyás, ha mindenki a felajánlások sorrendjében végzi el az ültetést, de nem ültet, ha másvalaki előtte már ültetett oda! Ha nem ültetett oda senki, akkor `Ezt az ágyást nem ültetik be.` szöveget jelenítse meg
	   **Expected Output:**
   ```
	     A virágágyás színe, ha csak az első ültet: output(Z)
   ```
	3. Adja meg, milyen színekben pompázna ez az ágyás, ha az eredeti tervvel ellentétesen minden felajánló elültetné virágait! Minden színt csak egyszer tüntessen fel! Az egyes színeket szóközökkel válassza el egymástól! Ha nem ültettek oda virágot, ne jelenítsen meg semmit!
	   **Expected Output:**
   ```
	     A virágágyás színei: output(O Z S K)
   ```
5. `[validate]` A felajánlások alapján több eset lehetséges. Határozza meg, melyik teljesül! Az idézőjelek közötti szöveget írja a képernyőre!
   **Expected Output:**
   ```
	     output(Átszervezéssel megoldható a beültetés.)
   ```
6. `[simulation]` `[IO]` A beültetést a felajánlások sorrendjében végezték el. Ha egy ágyást valaki már beültetett, akkor más már nem ültetett oda. A munka eredményét tárolja el a `szinek.txt` fájlban! A fájlban soronként az ágyások sorszámának sorrendjében két értéket, az ágyás színét jelző karaktert és az ültetéshez tartozó felajánlás sorszámát írja ki. Amelyik ágyás virág nélkül maradt, színként a `#` karaktert, a felajánlás sorszámának helyére pedig a `0`-t írja!

#### Exact strings
- `Ezt az ágyást nem ültetik be.`
- `Minden ágyás beültetésére van jelentkező.`
- `Átszervezéssel megoldható a beültetés.`
- `A beültetés nem oldható meg.`

---


### Ütemezés

#### Meta
- level: emelt
- year: 2023
- session: május
- language: hu
- difficulty: 3
#### Tags
- IO
- count
- min_max
- search
- validate
- lookup
- function

#### Scenario
A diákok hasznos nyári időtöltését biztosítják a különböző nyári táborok. Egy iskolai
osztályban felmérték, kik melyiken vennének részt szívesen. Ebben a feladatban az előzetes
igényfelmérés adatait dolgozzuk fel.
#### Constraints
- <=100 sor.
- Nyári hónapok napjai: 30, 31, 31.
- `sorszam(hó, nap)`: június 16 = 1; augusztus 31 = 77.

#### Data
**files:** `taborok.txt` (28 sor), `egytanulo.txt`

`taborok.txt` Sample:
```
6	26	7	10	GIOSY	foci
7	14	7	21	FPUY	szinjatszo
7	27	8	2	DKPRX	hittan
7	28	8	6	FJLOP	cserkesz
7	9	7	14	FKO	gombasz
```

Explanation:
Az első két számpár a tábor első és utolsó napjának dátuma. A számpárok első értéke a hónap, a második a nap sorszáma. Ezt követik azon diákok betűjelei, akik érdeklődnek a tábor iránt, végül a tábor témája olvasható. A diákok betűjele az angol ábécé egy nagybetűs karaktere, a tábor témája egyetlen ékezetmentes szó

`egytanulo.txt` Sample:
```
6.18-6.29. evezos
6.22-6.26. cserkesz
7.2-7.8. csillagasz
7.8-7.20. erdojaro
```
#### Tasks
1. `[IO]` Olvassa be a `taborok.txt` tartalmát!
2. `[count]` `[lookup]` Jelenítse meg a képernyőn, hogy hány tábor adatait tartalmazza a bemeneti fájl! Írja a képernyőre az elsőként és az utolsóként rögzített tábor témáját!
   **Expected Output:**
   ```
     Az adatsorok száma: 28
     Az először rögzített tábor témája: foci
     Az utoljára rögzített tábor témája: filmes
   ```
3. `[search]` Írja a képernyőre, mikor kezdődik a `zenei` tábor! Ha több ilyen tábor is volt, az összeset jelenítse meg a lenti mintának megfelelően! Ha egy sem volt, akkor a `Nem volt zenei tábor.` szöveget jelenítse meg a képernyőn!
   **Expected Output:**
   ```
     Zenei tábor kezdődik 8. hó 4. napján.
     Zenei tábor kezdődik 6. hó 18. napján.
   ```
4. `[min_max]` Keresse meg, melyik táborba jelentkeztek a legtöbben! Írja a képernyőre a tábor kezdő dátumát és a témáját! Ha több ilyen tábor is van, az összeset jelenítse meg!
   **Expected Output:**
   ```
     Legnépszerűbbek:
     8 27 fotos
   ```
5. `[function]` Készítsen függvényt sorszam néven, amely megadja, hogy a paraméterként kapott hónap és nap a nyári szünet hányadik napja! A dátumot a függvény két egész számként kapja meg, a visszaadott érték egy egész szám legyen! A nyári szünet első napja június (6. hó) 16. A nyári szünet 77. napja augusztus (8. hó) 31. (A nyári hónapok rendre 30, 31, 31 naposak.) A későbbi feladatok megoldásánál ezt a függvényt felhasználhatja.
6. `[IO]` `[count]` Kérjen be a felhasználótól egy dátumot a lenti mintának megfelelően, majd adja meg, hány tábor zajlik éppen ekkor!
   **Expected Input:**
   ```
     hó: input(8)
     nap: input(1)
   ```
   **Expected Output:**
   ```
     Ekkor éppen output(3) tábor tart.
   ```
7. `[IO]` `[validate]` Olvassa be egy tanuló betűjelét! Határozza meg, hogy az adott betűjelű tanuló mely táborok iránt érdeklődött! A táborok adatait kezdő dátum szerint növekvő sorrendben írja az egytanulo.txt fájlba a minta formátumának megfelelően! Jelenítse meg a képernyőn, hogy a tanuló mindegyiken részt tud-e venni, azaz nincs-e olyan nap, amelyen több táborban kellene lennie!
   **Expected Input:**
   ```
     Adja meg egy tanuló betűjelét: input(L)
   ```
   **Expected Output:**
   ```
     output(Nem mehet el mindegyik táborba.)
   ```

#### Exact strings
- `Nem volt zenei tábor.`
- `Nem mehet el mindegyik táborba.` (és a pozitív minta a feladatlap szerint)

---


### Reklám

#### Meta
- level: emelt
- year: 2023
- session: október
- language: hu
- difficulty: 3

#### Tags
- IO
- count
- sum
- min_max
- validate
- group
- function

#### Scenario
Egy termék hirdetésének hatékonyságát vizsgálták három, egymáshoz hasonló lélekszámú városban. Egy 30 napos időszak középső tíz napján zajlott reklámkampány a három város közül kettőben. Az egyik városban a helyi televízióban reklámozták a terméket, a másik városban utcai plakáton hirdették, mindkét városban az időszak 11-edik napjától a 20-adik napjáig. A harmadik városban nem volt reklámkampány, illetve az előbbi két városban sem volt az időszak első 10 és az utolsó 10 napján.

#### Constraints
- Rendelések < 1000; darabszám < 10.
- Minden nap van legalább egy rendelés valamelyik városból.
- 9–10. feladat: táblázatkezelő / diagram (`kampany`).

#### Data
**files:** `rendel.txt` (971 sor)

Sample:
```
1 TV 5
1 TV 3
1 TV 3
1 PL 4
1 TV 3
```

Explanation:
A rendelések időrendben vannak, minden sorban egy-egy rendelés szerepel.
Egy soron belül az első szám a rendelés napja, a következő két betű azt a várost jelöli, ahol a rendelést leadták, míg a harmadik elem a termékből rendelt darabszám. Az adatokat a soron belül szóközök választják el egymástól.
#### Tasks
1. `[IO]` Olvassa be a `rendel.txt` tartalmát!
2. `[count]` Állapítsa meg, hogy hány rendelés történt a teljes időszakban, és írja a képernyőre a rendelések számát!
   **Expected Output:**
   ```
     A rendelések száma: 971
   ```
3. `[IO]` `[count]` Kérje be a felhasználótól egy nap számát, és adja meg, hogy hány rendelés történt az adott napon!
   **Expected Input:**
   ```
     Kérem, adjon meg egy napot: input(9)
   ```
   **Expected Output:**
   ```
     A rendelések száma az adott napon: output(27)
   ```
4. `[count]` `[validate]` Számolja meg, hogy hány nap nem volt rendelés a reklámban nem érintett városból, és írja ki a napok számát! Ha egy ilyen nap sem volt, akkor írja ki `Minden nap volt rendelés a reklámban nem érintett városból` szöveget!
   **Expected Output:**
   ```
     3 nap nem volt a reklámban nem érintett városból rendelés
   ```
5. `[min_max]` Állapítsa meg, hogy mennyi volt az egy rendelésben szereplő legnagyobb darabszám, és melyik volt az a nap, amikor az első ilyen számú rendelést leadták! Az eredményt a lenti minta szerint írja ki!
   **Expected Output:**
   ```
     A legnagyobb darabszám: 9, a rendelés napja: 22
   ```
6. `[function]` `[sum]` Készítsen függvényt osszes néven, amely megadja, hogy mennyi volt egy adott városból egy adott napon a rendelt termékek száma! A függvény bemenete a három város egyikére utaló kétbetűs szöveg és a nap sorszáma legyen. Amennyiben szükséges, akkor további paramétert is felvehet a rendelések adatainak elérése érdekében. A függvény visszaadott értéke a rendelt darabszámok összege legyen! A függvényt például a következő módon lehessen meghívni: osszes("PL", 7).
7. `[sum]` Számítsa ki, hogy a kampány utáni első napon, azaz a 21-edik napon melyik városból mennyit rendeltek a termékből! Az eredményt a lenti mintának megfelelő formában írja ki!
   **Expected Output:**
   ```
     A rendelt termékek darabszáma a 21. napon PL: 43 TV: 36 NR: 18
   ```
8. `[group]` `[IO]` Összesítse városonként, hogy hány rendelés érkezett az első 10, a 11-20-adik valamint a záró 10 napon! Az eredményt (a fejlécet is beleértve) táblázatos formában, tabulátorokkal tagoltan jelenítse meg a képernyőn, illetve írja azonos formátumban a `kampany.txt` szöveges állományba!

#### Exact strings
- `Minden nap volt rendelés a reklámban nem érintett városból`

---


### Beléptető rendszer

#### Meta
- level: emelt
- year: 2024
- session: május
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- min_max
- search
- validate
- simulation

#### Scenario
Egy iskolában minden diáknak van egy tanulói kártyája, amelyet nemcsak a be- és kilépéskor
használnak, hanem ez helyettesíti a könyvtári olvasójegyet és a menzán az ebédjegyet is.
A rendszer adatbázisából statisztikai elemzés céljából lekérték az október 12-én rögzített
adatokat.

#### Constraints
- <=2000 sor; kód 4 betű; idő óó:pp.
- Menza: legfeljebb 1 ebéd/tanuló; könyvtár: többször lehet.
- 6. feladat: hátsó kapu 10:45–10:50; érintettek 10:50 után főkapun térnek vissza (szünet 11:00-ig).

#### Data
**files:** `bedat.txt` (750 sor)

Sample:
```
CEFX 07:00 1
OELK 07:00 1
FURI 07:00 1
KZVS 07:00 1
TKZK 07:00 1
```

Explanation:
Az állomány a tanuló kódját, az esemény időpontját, valamint az esemény
kódját tartalmazza szóközzel elválasztva.
Az esemény kódja a következő lehet:
1 - belépés a főkapun át
2 - kilépés a főkapun át
3 - az ebéd kiadása a menzán
4 - kölcsönzés a könyvtárban
#### Tasks
1. `[IO]` Olvassa be a `bedat.txt` tartalmát!
2. `[min_max]` Határozza meg, hogy mikor lépett be az épületbe az első tanuló, és mikor távozott az utolsó! Az időpontokat a mintához hasonlóan jelenítse meg a képernyőn!
   **Expected Output:**
   ```
     Az első tanuló 07:00-kor lépett be a főkapun.
     Az utolsó tanuló 18:54-kor lépett ki a főkapun.
   ```
3. `[search]` `[IO]` Készítsen listát a `kesok.txt` nevű állományba, amely megadja, hogy mely tanulók léptek be a nagykapun 07:50 után, de legkésőbb 08:15-kor! A fájlban a belépések a mintának megfelelően külön sorban szerepeljenek, az időpontot egy szóköz válassza el a tanuló azonosítójától! Ha egy tanuló ezalatt többször is belépett, minden belépése jelenjen meg a fájlban!
4. `[count]` Határozza meg, hány tanuló ebédelt aznap a menzán! Írassa ki az eredményt a képernyőre a mintának megfelelően!
   **Expected Output:**
   ```
     A menzán aznap 82 tanuló ebédelt.
   ```
5. `[count]` `[validate]` Szeretnénk tudni, hogy a könyvtári kölcsönzés vagy a menza a népszerűbb-e ezen a napon.:
	1. Határozza meg, hány tanuló kölcsönzött aznap a könyvtárban! Ha egy tanuló többször is kölcsönzött, akkor azt csak egyszer vegye figyelembe! Írassa ki az eredményt a képernyőre a mintának megfelelően!
	   **Expected Output:**
   ```
	     Aznap 76 tanuló kölcsönzött a könyvtárban.
   ```
	2. A könyvtárosok szerint több tanuló kölcsönöz egy nap a könyvtárban, mint ahányan a menzán ebédelnek. Így volt-e ez ezen a napon is? A választ `Többen voltak, mint a menzán.` vagy `Nem voltak többen, mint a menzán.` a mintának megfelelő formában írassa ki a képernyőre!
	   **Expected Output:**
   ```
	     output(Nem voltak többen, mint a menzán.)
   ```
6. `[simulation]` `[search]` A portás reggel elfelejtette a hátsó kaput bezárni, ezért a 10:45-kor kezdődő szünetben néhány tanuló kiment a hátsó kijáraton át a szemközti pékségbe tízórait venni. A portás csak 10:50-kor zárta be a hátsó kaput, így 10:50 után a korábban a hátsó kapun át távozott tanulóknak a főbejáraton át kellett visszajönniük. Írassa ki a képernyőre egy-egy szóközzel elválasztva ezeknek a tanulóknak az azonosítóját! (A szünet 11:00-ig tartott, és feltételezheti, hogy azt megelőzően valamennyi érintett tanuló visszaért.) Vegye figyelembe, hogy a tanulók egy része aznap csak 11:00-ra jött iskolába, illetve szabályosan lépett ki!
   **Expected Output:**
   ```
     Az érintett tanulók:
     EQBL VVDW HJVC ZXCK ZMFL CYEE MCBC IEAA HFWL
   ```
7. `[IO]` `[search]` Kérje be egy tanuló azonosítóját, és írassa ki a minta szerinti formátumban, hogy mennyi idő telt el az iskolába való első belépése és utolsó távozása között! Feltételezheti, hogy 19:00-ig minden tanuló elhagyta az iskolát. Ha aznap az adott azonosítójú tanuló nem járt az iskolában, akkor írassa ki az `Ilyen azonosítójú tanuló aznap nem volt az iskolában.` üzenetet!
   **Expected Input:**
   ```
     Egy tanuló azonosítója=input(ZOOM)
   ```
   **Expected Output:**
   ```
     A tanuló érkezése és távozása között output(7 óra 4 perc) telt el.
   ```

#### Exact strings
- `Többen voltak, mint a menzán.`
- `Nem voltak többen, mint a menzán.`
- `Ilyen azonosítójú tanuló aznap nem volt az iskolában.`

---


### Kráterek

#### Meta
- level: emelt
- year: 2024
- session: május
- language: idegen
- difficulty: 4

#### Tags
- IO
- count
- min_max
- search
- function

#### Scenario
Egy még felderítetlen égitestet először közelített meg egy földi szonda. A szondáról küldött
képeken látható, hogy a légkör nélküli égitest felszínét meteorbecsapódások által létrehozott
kráterek borítják. A szonda feltérképezte a felszín egy részét, és a kráterek elhelyezkedéséről is
adatokat küldött. A szonda minden krátert egy körként azonosított, és megadta a kör (azaz kráter)
középpontjának helyét és a kör (azaz a kráter) sugarát. A szonda minden kráternek nevet is
adott úgy, hogy véletlenszerűen választott egy listából, amelyben csillagászok nevei szerepeltek. Minden kráternek egyedi nevet adott, tehát nincs két azonos nevű kráter. Az adatok kétféle formátumban állnak rendelkezésre.

#### Constraints
- <=100 kráter.
- PI = 3.14 (2 tizedes) a területnél.
- `tavolsag(x1,y1,x2,y2)` Pitagorasz.
- Nincs átfedés, ha távolság > R1+R2.
- Tartalmazás: távolság < |Rnagy - Rkis|.

#### Data
**files:** `felszin_tpont.txt` (20)

Sample (`felszin_tpont.txt`):
```
5.23	2.47	3.86	George Ogden Abell
3.67	2.19	1.13	Robert Henry Dicke
1.15	7.25	2.89	Abu Bakr ibn Tufajl
3.45	2.78	0.35	Stephen Hawking
```

Explonation:
Egy soron belül az első három valós szám a kráter középpontjának X és Y koordinátája, valamint a kráter sugara. Ezt követi egy csillagász neve, vagyis a kráter elnevezése. Az adatokat egy soron belül egy-egy tabulátor választja el egymástól.
#### Tasks
1. `[IO]` Olvassa be a bemeneti állományt!
2. `[count]` Számolja meg, hogy hány kráter található a bemeneti állományban, és írja a képernyőre a kráterek számát!
   **Expected Output:**
   ```
     A kráterek száma: 20
   ```
3. `[IO]` `[search]` Kérje be a felhasználótól egy kráter pontos nevét, majd írja ki a kráter adatait! A kiírás egy teljes mondat legyen, például: `A(z) Stephen Hawking középpontja X=3.45 Y=2.78 sugara R=0.35.`. Ha a név nem szerepel a kráterek nevei között, akkor írja ki: `Nincs ilyen nevű kráter.`.
   **Expected Input:**
   ```
     Kérem egy kráter nevét: input(Thomas Gold)
   ```
   **Expected Output:**
   ```
     A(z) Thomas Gold középpontja X=output(14.58) Y=output(31.29) sugara R=output(2.45).
   ```
4. `[min_max]` Vizsgálja meg a szonda által kapott adatokat, és adja meg a legnagyobb sugarú kráter sugarát és névadójának nevét! Amennyiben több legnagyobb kráter van, úgy elég az egyiket megadnia.
   **Expected Output:**
   ```
     A legnagyobb kráter neve és sugara: Wilhelm Anderson 4.45
   ```
5. `[function]` A következő feladatokban szüksége lesz arra, hogy kiszámítsa két kráter középpontjának távolságát. Készítsen függvényt, amely a Pitagorasz-tétel felhasználásával kiszámítja két, koordinátákkal adott pont távolságát! A függvény bemenete a két pont, (x1, y1) és (x2, y2) koordinátái (valós számok), visszaadott értéke a távolságuk (valós szám). A függvény leírása a következő:
   ```
	Függvény tavolsag(x1, y1, x2, y2 : Valós ) : Valós
		tavolsag := Négyzetgyök((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
		Függvény vége
   ```
6. `[IO]` `[search]` Két kráter nem fedi át egymást, nincs közös részük, ha középpontjaik távolsága nagyobb, mint a két kráter sugarának összege. Kérje be egy kráter nevét, és adja meg azoknak a krátereknek a nevét, amelyekkel a bekért kráternek nincs közös része! A kiírásban szereplő kráterek nevei között egy vessző és egy szóköz legyen az elválasztás! Ha nincs ilyen kráter, akkor nem kell megjelenítenie semmit.
   **Expected Input:**
   ```
     input(Jacques Cassini)
   ```
7. `[search]` Egy kráter tartalmaz egy másik krátert, ha a kisebb kráter teljes egészében a nagy kráterben található. Ez körök esetében azt jelenti, hogy a két kör középpontjának távolsága kisebb, mint a nagyobb kör sugarának és a kisebb kör sugarának különbsége. Vizsgálja meg a krátereket, és írja ki azoknak a krátereknek a nevét, amelyek esetében a nagyobb kráter tartalmazza a kisebb krátert! Minden ilyen tartalmazást csak egyszer jelenítsen meg úgy, hogy megadja, hogy melyik kráter tartalmazza a másikat!
8. `[IO]` A kráterek adatai alapján számítsa ki, hogy mekkora területűek az egyes kráterek, és készítsen egy `terulet.txt` szöveges állományt, amely tartalmazza a kráterek nevét és területét! A kör területe `T = r(2)*PI` ahol r a kör sugara, PI értéke két tizedesjegyre kerekítve 3.14. Az állomány minden egyes sorában egy kráter adatai szerepeljenek: először a kráter területe két tizedesjegyre kerekítve, majd egy tabulátor karakter, majd a kráter neve!

#### Exact strings
- `Nincs ilyen nevű kráter.`

---


### Autók mozgása

#### Meta
- level: emelt
- year: 2024
- session: október
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- sum
- min_max
- search
- simulation
- group

#### Scenario
Egy autóút meghatározott szakaszán vizsgálták az egyik irányba haladó autók mozgását. A vizsgálat során az autókba épített rádióadók jeleket sugároztak az útszakaszra történő belépéskor, majd ezt követően bizonyos időpontokban. A gépkocsik mozgását tekinthetjük úgy, hogy a jeladáskor mért sebességgel haladtak a következő jeladásig. 

#### Constraints
- Autók ≤ 200; jeladások ≤ 2000.
- Távolság: Δt órában × sebesség; 1 tizedes km.
- Perc pontosság; időrend adott.

#### Data
**files:** `jeladas.txt` (1705 sor)

Sample:
```
TLJ-509	6	4	95
TLJ-509	6	14	88
AVY-894	6	15	98
ANF-997	6	17	86
ZVJ-638	6	20	119
```

Explanation:
Minden sorban egy jeladás adatai szerepelnek tabulátorral elválasztva: az autó rendszáma, a jeladás idejének óra, illetve perc értéke, valamint a jeladáskor mért sebesség km/h mértékegységben.
#### Tasks
1. `[IO]` Olvassa be a `jeladas.txt` tartalmát!
2. `[min_max]` Állapítsa meg, hogy milyen időpontban történt a legutolsó jeladás, és írja a képernyőre az időpontot, valamint az utoljára jelet adó autó rendszámát!
   **Expected Output:**
   ```
     Az utolsó jeladás időpontja 22:45, a jármű rendszáma MWO-680
   ```
3. `[search]` Írja ki a bemeneti állományban elsőként szereplő jármű rendszámát, valamint azt, hogy milyen időpontokban adott jelzést! Az időpontokat `óra:perc` formátumban, szóközzel elválasztva, egy sorban jelenítse meg!
   **Expected Output:**
   ```
     Az első jármű: TLJ-509
     Jeladásainak időpontjai: 6:4 6:14 6:30 6:32 6:51 6:54 7:7 7:19 7:30 7:31
   ```
4. `[IO]` `[count]` Kérje be a felhasználótól egy időpont óra és perc értékét, és adja meg, hogy hány jeladás történt az adott időpontban! Ha nem történt jeladás, akkor 0-t írjon ki!
   **Expected Input:**
   ```
     Kérem, adja meg az órát: input(6)
     Kérem, adja meg a percet: input(54)
   ```
   **Expected Output:**
   ```
     A jeladások száma: output(3)
   ```
5. `[min_max]` Állapítsa meg, hogy mennyi az adatok szerint a legnagyobb sebesség, amellyel egy jármű a jeladáskor haladt, illetve adja meg az összes autó rendszámát, ami haladt ilyen sebességgel! Amennyiben egy jármű többször is haladt a legnagyobb sebességgel, akkor a rendszámát többször is megjelenítheti. A rendszámokat egy sorban, szóközzel elválasztva jelenítse meg a minta szerint!
   **Expected Output:**
   ```
     A legnagyobb sebesség km/h: 154
     A járművek: XQE-678 PAL-958
   ```
6. `[IO]` `[simulation]` `[sum]` Kérje be a felhasználótól egy jármű rendszámát, és jelenítse meg a jármű jeladásainak időpontját és az adott rendszámú autó távolságát az útszakasz kezdetétől! A bevezető példában az első jármű esetén a 6:04-kor a jármű távolsága az útszakasz kezdetétől 0,0 km, míg 6:14-kor 15,8 km, mivel a jármű az eltelt 10 perc (10/60 óra) alatt 95 km/h-val haladt. A kimenetet a mintának megfelelőn alakítsa ki, a távolságot minden esetben egy tizedesjegyre kerekítve írja ki km mértékegységben! Ha nem szerepel a bekért rendszámmal jármű, akkor azt egy rövid mondatban jelezze a felhasználónak!
   **Expected Input:**
   ```
     input(ZVJ-638)
   ```
7. `[group]` `[IO]` Készítsen egy `ido.txt` szöveges állományt, amelynek mindegyik sorában egy-egy jármű rendszáma, illetve első és utolsó jeladásának óra és perc értéke szerepeljen! Az állományban minden jármű pontosan egyszer forduljon elő tetszőleges sorrendben!

---


### ASCII-rajzok

#### Meta
- level: emelt
- year: 2025
- session: május
- language: idegen
- difficulty: 3
#### Tags
- IO
- count
- min_max
- string
- function

#### Scenario
ASCII-ábrák tömörítetlen és tömörített tárolása. Tömörített blokk: 1 számjegy (1–9) + karakter; >9 ismétlés több blokkra bontva. Tömörítetlen ábra ≤ 100×100.
Az ASCII-karaktereket tartalmazó állományokat tömöríthetjük is, ha az egymást követő ismétlődő karaktereket rövidebb kóddal helyettesítjük. Az alábbi mintán látható, hogy a könyvet ábrázoló ASCII-képet hogyan tároltuk el tömörítettlen, illetve tömörített formában.

Az ábrák tömörített változatai az alábbiak szerint állnak elő a tömörítetlen változatból:
* A tömörített állomány ugyanannyi sorból áll, mint a tömörítetlen.
- A tömörített állomány blokkok formájában tárolja el az ábrát. Egy blokk két karakter hosszú. A blokk első karaktere mindig egy 1 és 9 közti egész szám lehet. Ez jelzi, hogy a blokk második karaktere hányszor fordul elő közvetlenül egymás után az ábra adott sorában. A „2/” blokk tehát azt jelenti, hogy egymás után kétszer kell a / karaktert kirajzolni. A „4 ” blokk jelentése, hogy a szóköz karaktert négyszer kell kirajzolni egymás után.
* Ha egy karakter 9-nél többször ismétlődik, akkor több blokkot kell elhelyezni egymás után. Ha például 12 alkalommal kell kirajzolni a „$” karaktert, akkor a tömörített állomány a '9$3$' blokkokat tartalmazná.
* A blokkokat soronként tároljuk el a fájlban.
#### Constraints
- Tömörített sor ≤ 200 karakter.
- Tömörítési arány = tömörített / tömörítetlen (sorvégjelek nélkül), 2 tizedes.
- 3. feladat: `atalakit` függvény egy tömörített sorra.

#### Data
**files:** `konyv.txt` (5), `konyv_t.txt` (5), `szg_t.txt` (18)

Sample (`konyv.txt`):
```
    _______
   /      /,
  /      //
 /______//
(______(/
```

Sample (`konyv_t.txt`):
```
4 7_
3 1/6 1/1,
2 1/6 2/
1 1/6_2/
1(6_1(1/
```

#### Tasks
1. `[IO]` Olvassa be és jelenítse meg a `konyv.txt` ábrát!
2. `[IO]` `[string]` Jelenítse meg többször egymás mellett a konyv.txt állományban található ábrát! Kérje be a felhasználótól az ábra ismétlődéseinek számát! Az ábrák után elválasztásként a `|` karakterláncot jelenítse meg! Ügyeljen arra, hogy az egyes sorok különböző hosszúságúak is lehetnek. Azt nem kell ellenőriznie, hogy az ábra az adott ismétlésszámmal valóban elfére egymás mellett a képernyőn.
   **Expected Input:**
   ```
     input(3)
   ```
3. `[function]` `[string]` Készítsen függvényt atalakit néven, amely egy tömörített ábra egy sorát tömörítetlen formára alakítja! (Egy tömörített sor legfeljebb 200 karakterből állhat.)
4. `[string]` `[IO]` Az szg_t.txt állomány tömörített formában tartalmaz egy rajzot. Alakítsa a tömörített ábrát tömörítetlen formába az atalakit függvény használatával, és szg.txt néven mentse el az eredményt, valamint jelenítse meg azt a képernyőn!
5. `[IO]` `[count]` Izgalmas kérdés, hogy egy-egy ábrát milyen mértékben sikerült tömöríteni a fenti módszerrel. Kérje be a felhasználótól a tömörített, valamint tömörítetlen adatokat tartalmazó fájl neveit majd írja ki, hogy az egyes állományok hány karaktert tartalmaznak! A sorvégjel karaktereket `(\r\n)` ne vegye figyelembe! A következő sorban jelenítse meg a tömörítési arányt két tizedesjegyre kerekítve! A tömörítési arány a tömörített ábra karakterszáma osztva a tömörítetlen ábra karaktereinek számával.
   **Expected Input:**
   ```
     Kérem adja meg a tömörített ábra fájlnevét: input(konyv_t.txt)
     Kérem adja meg a tömörítetlen ábra fájlnevét: input(konyv.txt)
   ```
   **Expected Output:**
   ```
     A karakterek száma a tömörített állományban: output(38)
     A karakterek száma a tömörítetlen állományban: output(53)
     A tömörítési arány: output(0.72)
   ```
6. `[count]` `[min_max]` Készítsen statisztikát a `konyv_t.txt` állományban található ábráról! A képernyőn jelenjen meg, hogy az ábra hány sorból áll, hány blokkot tartalmaz, valamint hogy mekkora az ábra szélessége karakterekben. Utóbbi adat a leghosszabb sor karakterszámát jelenti.
   **Expected Output:**
   ```
     Az ábra magassága sorokban: 5
     Az ábra szélessége karakterekben: 12
     A blokkok száma: 19
   ```

---


### Sebesség

#### Meta
- level: emelt
- year: 2025
- session: október
- language: hu
- difficulty: 5

#### Tags
- IO
- count
- sum
- min_max
- search
- simulation

#### Scenario
Ha közúti járművel utazunk, figyelemmel kísérhetjük a sofőr tevékenységét, aki az
útviszonyoknak megfelelően és a KRESZ szabályait követve hol lassítja, hol gyorsítja az autót.
Személygépjármű esetén a KRESZ szabályai a következők: lakott településen 50 km/h, azon
kívül 90 km/h a megengedett sebesség. Ezt az általános szabályt felülírhatják a közúti
jelzőtáblák, így egy veszélyes kanyarnál alacsonyabb sebességet is előírhatnak, lakott területen
belül pedig akár magasabb sebességet is engedélyezhetnek. A jelzőtábla által megadott
maximális sebességet egy másik jelzőtábla, de egy útkereszteződés is törli, visszaállítva ezzel
az alapértelmezett sebességhatárt.

#### Constraints
- ≤2000 eseménysor; távolság szerint növekvő sorrend.
- Alapértelmezett sebességhatár: településen belül 50 km/h, kívül 90 km/h.
- Szám-tábla: 10–90; `#` és településhatár visszaállítja az alapértéket; `%` a korlátozást oldja fel.
- Feloldó (`%`) előtt biztosan van szám-tábla; több tábla egymás után feloldó nélkül lehetséges.
- Településnév: 4–30 karakter; az út ≥2 településen áthalad.
- Települések távolsága: korábbi `]` és a következő településnév pozíciójának különbsége.
- 4. feladat: településen belüli arány, 2 tizedes; 3. feladat bemenete km-ben.

#### Data
**files:** `ut.txt` (76 sor)

Sample:
```
105601
999 70
1242 #
1803 #
2520 Varos301
2900 60
3100 40
3300 %
5830 ]
5900 30
6110 #
6921 Varos702
7120 ]
13505 Varos403
```

Explanation:
A fájl egy autóutat és autópályát nem tartalmazó útszakasz sebességhatárt megszabó adatait tartalmazza. A fájl első sora azt a méterben kifejezett távolságot adja meg, amilyen hosszát figyeltük az útnak. A további, sorok mindegyike két értéket tartalmaz. Az első a megfigyelés kezdetétől mért, méterben kifejezett távolság, az attól szóközzel elválasztott második pedig többféle lehet:
 * számérték: sebességkorlátozó táblát jelöl, megadja, hogy attól a ponttól ennyi a sebességhatár (értéke 10 és 90 közötti egész lehet).
* legalább négy-, legfeljebb harminckarakteres szöveg: azon a ponton a megadott nevű település kezdődik.
* záró szögletes zárójel `]`: a település végét jelzi.
* kettőskereszt `#`: bekötőutat vagy útkereszteződést jelöl.
* százalékjel `%`: a sebességkorlátozás feloldását jelzi.
Az adatok a távolság szerint növekvő sorrendben rendezettek.
#### Tasks
1. `[IO]` Olvassa be az `ut.txt` adatait!
2. `[search]` Írja ki az úton található települések nevét! Minden település neve új sorban jelenjen meg!
   **Expected Output:**
   ```
     A települések neve:
     Varos301
     Varos702
     Varos403
   ```
3. `[IO]` `[min_max]` `[simulation]` Kérjen be a felhasználótól egy valós számot, amely megadja, hogy az út első hány km-es szakaszát vizsgáljuk! Adja meg, hogy mi volt ezen a szakaszon a legalacsonyabb sebességhatár! Figyeljen arra, hogy sebességhatárt nem csak sebességkorlátozó tábla szabhat meg! Megoldását az 1, 2, …, 5 km-t megadva is tesztelje!
   **Expected Input:**
   ```
     Adja meg a vizsgált szakasz hosszát km-ben! input(1.8)
   ```
   **Expected Output:**
   ```
     Az első 1.8 km-en output(70) km/h volt a legalacsonyabb megengedett sebesség.
   ```
4. `[sum]` Adja meg, hogy a bemeneti fájlban rögzített út hány százaléka vezet településen belül! Az út teljes hossza a bemeneti fájl első sorában található. Az eredményt kéttizedes pontossággal írja a képernyőre!
   **Expected Output:**
   ```
     Az út 22.38 százaléka vezet településen belül.
   ```
5. `[IO]` `[count]` Olvassa be egy település nevét, és adja meg, hogy a településen belül:
   **Expected Input:**
   ```
     Adja meg egy település nevét! input(Varos010)
   ```
	1. Hány sebességkorlátozó tábla van.
	   **Expected Output:**
   ```
	     A sebességkorlátozó táblák száma: output(4)
   ```
	2. Milyen hosszan vezet az út!
	   **Expected Output:**
   ```
	     Az út hossza a településen belül output(2000) méter.
   ```
6. `[min_max]` Adja meg a beolvasott településhez legközelebb eső település nevét! (Két település távolsága alatt az úton korábbi település végének és a későbbi település kezdetének különbségét értjük.) Ha a két szomszédos település távolsága egyezik, akkor a megfigyelés kezdőpontjához közelebbit adja meg! Ügyeljen arra, hogy az első és az utolsó településnek csak egy szomszédja van! Feltételezheti, hogy az út bemeneti fájl által leírt része legalább két településen áthalad.
   **Expected Output:**
   ```
     A legközelebbi település: output(Varos609)
   ```

---


### Városi autózás

#### Meta
- level: emelt
- year: 2026
- session: május
- language: hu
- difficulty: 5

#### Tags
- IO
- sum
- min_max
- validate
- simulation
- lookup

#### Scenario
Egy városban – különösen, ha nem működnek a forgalomirányító jelzőlámpák – gyakran nagyon sok időbe kerül az úti cél elérése. A feladatban egy városban közlekedő autó mozgását követjük nyomon, amely álló helyzetből indul. Az autó általában állandó sebességgel halad, de a forgalmi helyzet miatt változtathatja a sebességét.

#### Constraints
- Bemenet érvényességét nem kell ellenőrizni; `N. feladat` kiírás; ékezetmentes OK.
- Sebességhatár (3.): 14 m/s.
- 4.: legalább 1 s állás; több max -> elég egy.
- 5.: bekért idő < utolsó adatsor.
- 6.: ne kerekítse.

**Fizika:** Ha egy autó sebessége `v1`-ről `v2`-re változik `t1` és `t2` időpontok között, akkor a gyorsulása `v2-v1/t2-t1` ez idő alatt pedig `v1+v2/2(t1-t2)` utat tesz meg. Sebessége a `t1` és `t2` időpontok közötti `t` időpontban `v1+v2-v1/t2-t1*(t-t1)`. Ha az autó állandó `v` sebességgel halad a `t1` és `t2` időpontok között, akkor a megtett út `v(t2-t1)`

#### Data
**files:** `aa123.txt` (150), `mx234.txt` (147)

Sample (`mx234.txt`):
```
6	9	3
30	35	7
49	54	11
68	73	12
92	96	0
```

Explonation:
- A bemeneti fájl első sora alapján azt mondhatjuk, hogy az autó 6 másodperc elteltével indultel és 0 m/s-ról 3 m/s sebességre gyorsult a 9. másodperc végére. Ez idő alatt a gyorsulása 
  `3-0/9-6` azaz `1 m/s(2)` és `0+3/2*(9-6)` azaz 4,5 métert tettt meg
- Az első és a második sor vizsgálatából kiderül, hogy az autó a 9. és a 30. másodperc között 3 m/s sebességgel haladt, ezért `(30 - 9)*3`, azaz 63 méter utat tett meg.
- A  második sor leírja, hogy az autó a 30. és a 35. másodperc között 3 m/s sebességről 7 m/s-ra gyorsult, ezért gyorsulása `7-3/35-30` , tehát 0,8 m/s2 volt,
  a megtett út pedig `3+7/2*(35-30)`, tehát 25 méter.
#### Tasks
1. `[IO]` Kérje be a felhasználótól egy autó azonosítóját, majd olvassa be és tárolja el a hozzá tartozó állományban található adatokat!
   **Expected Input:**
   ```
     Kérem adja meg az autó azonosítóját! input(mx234)
   ```
2. `[lookup]` Jelenítse meg azt az időpontot, amikor az autó elindult, és azt a sebességet, amellyel az autó a végén halad
   **Expected Output:**
   ```
     Az autó a 6. másodpercben indult el.
     Az autó a megfigyelés végén 6 m/s sebességgel haladt.
   ```
3. `[validate]` Településen belül általában 14 m/s a sebességhatár. Határozza meg és írassa ki, hogy az autó átlépte-e ezt a sebességértéket bármikor az útja során!
   **Expected Output:**
   ```
     output(Az autó átlépte a sebességhatárt.)
   ```
4. `[min_max]` `[simulation]` Határozza meg, hogy a megfigyelés kezdetétől, tehát a 0. másodperctől, hány másodperc volt az a leghosszabb időszak, amíg állt a jármű! Jelenítse meg a leghosszabb intervallum kezdetét és végét! Ha több ilyen is volt, elegendő egyet megjelenítenie! Feltételezheti, hogy a jármű legalább 1 másodpercet állt.
   **Expected Output:**
   ```
     A leghosszabb állásidő 852 és 948 másodperc között volt.
   ```
5. `[IO]` `[lookup]` Kérjen be a felhasználótól egy időpontot, és adja meg, hogy abban az időpontban milyen sebességgel haladt az autó! Feltételezheti, hogy a megadott időpont korábbi, mint az utolsó adatsorban szereplő érték
   **Expected Input:**
   ```
     Mikor vizsgáljuk az autó sebességét? input(500)
   ```
   **Expected Output:**
   ```
     Az autó sebessége a(z) 500. másodpercben output(13.4) m/s volt.
   ```
6. `[sum]` Határozza meg, hogy mennyi utat tett meg összesen a jármű! Az eredményt ne kerekítse!
   **Expected Output:**
   ```
     A megtett út: 25813.0 méter.
   ```
7. `[IO]` Egy jármű mozgásának sebesség-idő grafikonját kell a 8. feladatban elkészítenie. Ehhez programja állítsa elő a `vX.txt` nevű állományt (ahol az X az első feladatban bekért, autót azonosító karaktersorozat)! Az állományba soronként 2 számérték kerüljön tabulátorral elválasztva! Az első egy másodpercben kifejezett időpont, a második az abban a pillanatban érvényes sebesség legyen! Minden sebességváltozás kezdő és záró időpontjához tartozzon egy-egy sor! A sor első eleme a sebességváltozás kezdete vagy vége másodpercben, a második elem pedig az abban a pillanatban mérhető sebesség értéke.

#### Exact strings
- `Az autó átlépte a sebességhatárt.` (és a negatív eset a feladatlap szerint)

---


### MRZ kód

#### Meta
- level: emelt
- year: 2026
- session: május
- language: idegen
- difficulty: 4

#### Tags
- IO
- validate
- string
- lookup
- weighted_sum

#### Scenario
Az útlevél elsősorban külföldi utazásra jogosító okmány, ezért a gépi ellenőrzés
megkönnyítésére az adatoldalon egy úgynevezett MRZ (Machine Readible Zone) kód található.
Az MRZ kód az okmányról és annak tulajdonosáról meghatározott adatokat és ellenőrző
értékeket tartalmaz. Az útlevélnél az MRZ kód 2 soros, mindegyik sorban 44 karakter található.
Az MRZ kódban csak az angol ábécé nagybetűi, számok és a „<” karakter szerepelhetnek
(elválasztásra, illetve kitöltésre).
#### Constraints
- MRZ: 2 sor × 44 karakter; megengedett jelek: A–Z, számjegy, `<`.
- Nem (2. sor, 21. karakter): `F` = nő, `M` = férfi.
- Dátumok ÉÉHHNN formában; érvényesség: MRZ lejárati dátum ≥ bekért aktuális dátum.
- Névmező az 1. sorban (országkód után) 39 karakter; csonkolt, ha az 1. sor nem `<`-re végződik.
- 5. feladat: `Elljegyszamolo` függvény + `kodok.txt` súlyozott ellenőrző számjegyhez.

#### Data
**files:** `mrz1.txt`, `mrz2.txt`, `mrz3.txt`, `kodok.txt` (37)

Sample (`mrz1.txt`):
```
P<HUNNAGY<KOVACS<<GYOENGYVIRAG<MARIA<<<<<<<<
XT123456<9HUN9805138F3005132<<<<<<<<<<<<<<04
```

Explanation:
Az MRZ kód első sora sorrendben a következő adatokat tartalmazza:
* Az okmány típusa (P esetén útlevél), ha nem 2 karakter, akkor „<” a második karakter
* Az okmányt kiadó ország 3 karakteres kódja
* Az okmány tulajdonosának családi és utóneve. A családi nevet az utónévtől „<<”, a többtagú családi vagy utóneveket pedig „<” választja el. Ha rövidebb, mint 39 karakter, akkor „<” jellel van feltöltve.

Az MRZ kód második sora sorrendben a következő adatokat tartalmazza:
* Okmányszám (ha rövidebb, mint 9 karakter, akkor „<” jellel van feltöltve)
* Okmányszám ellenőrző számjegye
* Az okmány birtokosának nemzetisége
* Az okmány birtokosának születési ideje (ÉÉHHNN formátumban)
* A születési idő ellenőrző számjegye
* Az okmány tulajdonosának neme (F–Nő, M–Férfi)
* Az okmány érvényességi idejének utolsó napja (ÉÉHHNN formátumban)
* Az érvényességi idő ellenőrző számjegye
* Az okmányt kiadó által választható adat (nem kötelező, ha nincs, akkor „<” jelekkel van feltöltve)
* Az okmányt kiadó által választható adat ellenőrző számjegye
* Összesített ellenőrző számjegy
#### Tasks
1. `[IO]` Fájlnév bekérése → MRZ kiírása!
   **Expected Input:**
   ```
     Az állomány neve: input(mrz1.txt)
   ```
   **Expected Output:**
   ```
     P<HUNNAGY<KOVACS<<GYOENGYVIRAG<MARIA<<<<<<<<
     XT123456<9HUN9805138F3005132<<<<<<<<<<<<<<04
   ```
2. `[lookup]` Az MRZ kód alapján határozza meg, és írja ki a képernyőre, hogy az okmány tulajdonosa férfi vagy nő
   **Expected Output:**
   ```
     Az okmány tulajdonosa nő.
   ```
3. `[IO]` `[validate]` Kérje be a felhasználótól az aktuális dátumot ÉÉHHNN formában! Vizsgálja meg az MRZ kódban lévő érvényességi idő alapján, hogy érvényes-e az okmány! Ha az okmány lejárt, akkor írja a képernyőre, hogy `Lejárt.`, ellenkező esetben az `Érvényes.` üzenetet írja ki!
   **Expected Input:**
   ```
     Aktuális dátum: input(260910)
   ```
   **Expected Output:**
   ```
     output(Érvényes.)
   ```
4. `[string]` Írja ki a képernyőre az MRZ kód első sorában lévő nevet a minta szerint! Amennyiben az okmány tulajdonosának családi és utóneve (elválasztó karakterekkel együtt) rövidebb 39 karakternél, akkor a maradék helyet „<” karakterrel töltik ki. Ha az 1. sor végén nincs „<” karakter, akkor azt kell feltételezni, hogy a név csonkolt. Írja ki a képernyőre a minta szerint, ha a név nem csonkolt: `A név nem csonkolt.`, különben a `Lehetséges, hogy csonkolt a név.` szöveget! Feltételezheti, hogy az utónévből mindig szerepel legalább egy karakter.
   **Expected Output:**
   ```
     Családi név: NAGY KOVACS
     Utónév: GYOENGYVIRAG MARIA
     output(A név nem csonkolt.)
   ```
5. `[validate]` `[weighted_sum]` Ellenőrizze az MRZ-ben lévő okmányszám, születési idő és érvényességi idő ellenőrző számjegyének helyességét! A képernyőn a minta szerint jelenítse meg az MRZ kódban lévő és a kiszámított ellenőrző számjegyet! Ha az ellenőrző számjegy megegyezik az MRZ-ben lévővel, akkor a képernyőre írja ki a minta szerint a `HELYES` szót, ellenkező esetben a `HIBÁS` szót! A számításhoz felhasználhatja az előző feladatban elkészített függvényt!
   **Expected Output:**
   ```
     Okmányszám ellenőrző szám
       MRZ-kódban: 9 / Számított érték: 9 HELYES
     Születési idő ellenőrző szám
       MRZ-kódban: 8 / Számított érték: 8 HELYES
     Érvényességi idő ellenőrző szám
       MRZ-kódban: 2 / Számított érték: 2 HELYES
   ```

#### Exact strings
- `Érvényes.` / `Lejárt.`
- `A név nem csonkolt.` / `Lehetséges, hogy csonkolt a név.`
- `HELYES` / `HIBÁS`

---


### Lottó

#### Meta
- level: emelt
- year: 2005
- session: május
- language: hu
- difficulty: 3

#### Tags
- IO
- count
- search
- validate
- lookup

#### Scenario
Magyarországon 1957 óta lehet ötös lottót játszani. A játék lényege a következő: a lottószel-
vényeken 90 szám közül 5 számot kell a fogadónak megjelölnie. Ha ezek közül 2 vagy annál
több megegyezik a kisorsolt számokkal, akkor nyer. Az évek során egyre többen hódoltak
ennek a szerencsejátéknak és a nyeremények is egyre nőttek.

#### Constraints
- Hetente 5 szám az 1–90 tartományból; `lottosz.txt`: 51 hét (az 52. hét hiányzik, bekérés).
- 3. feladat: hét sorszáma 1–51.
- 7. feladat: 1–90 gyakoriságok egyjegyűek; kimenet `lotto52.txt` (52 sor).
- 8. feladat prímek: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89.

#### Data
**files:** `lottosz.txt`

Sample:
```
37 42 44 61 62
18 42 54 83 89
5 12 31 53 60
1 28 47 56 70
54 56 57 59 71
```

Explanation:
A szöveges állománybanév az az évi 51 hetének ötös lottó számai. Az első sorában az első héten húzott számok vannak, szóközzel elválasztva, a második sorban a második hét lottószámai vannak stb.
Az állományból kimaradtak az 52. hét lottószámai. Amelyek a következők: `89 24 34 11 64`
#### Tasks
1. `[IO]` Kérje be a felhasználótól az 52. hét megadott lottószámait!
   **Expected Input:**
   ```
     input(89 24 34 11 64)
   ```
2. `[IO]` A program rendezze a bekért lottószámokat emelkedő sorrendbe! A rendezett számokat írja ki a képernyőre!
   **Expected Output:**
   ```
     output(11 24 34 64 89)
   ```
3. `[IO]` `[lookup]` Kérjen be a felhasználótól egy egész számot 1-51 között! Majd írja ki a képernyőre a bekért számnak megfelelő sorszámú hét lottószámait, a `lottosz.txt`  állományban lévő adatok alapján!
   **Expected Input:**
   ```
     input(1)
   ```
   **Expected Output:**
   ```
     output(37 42 44 61 62)
   ```
4. `[validate]` A `lottosz.txt` állományból beolvasott adatok alapján döntse el, hogy volt-e olyan szám, amit egyszer sem húztak ki az 51 hét alatt! A döntés eredményét `Van` vagy `Nincs` írja ki a képernyőre!
   **Expected Output:**
   ```
     output(VAN)
   ```
5. `[count]` A `lottosz.txt` állományban lévő adatok alapján állapítsa meg, hogy hányszor volt páratlan szám a kihúzott lottószámok között! Az eredményt a képernyőre írja ki!
   **Expected Output:**
   ```
     25
   ```
6. `[IO]` Fűzze hozzá a `lottosz.txt` állományból beolvasott lottószámok után a felhasználótól bekért, és rendezett 52. hét lottószámait, majd írja ki az összes lottószámot a `lotto52.txt` szöveges fájlba! A fájlban egy sorba egy hét lottószámai kerüljenek, szóközzel elválasztva egymástól!
7. `[count]` Határozza meg a `lotto52.txt` állomány adatai alapján, hogy az egyes számokat hányszor húzták ki az adott évben. Az eredményt írja ki a képernyőre a következő formában: az első sor első eleme az a szám legyen ahányszor az egyest kihúzták! Az első sor második eleme az az érték legyen, ahányszor a kettes számot kihúzták stb.! (Annyit biztosan tudunk az értékekről, hogy mindegyikük egyjegyű.
   **Expected Output:**
   ```
     1 24
     2 12
     3 45...
   ```
8. `[search]` Adja meg, hogy az 1-90 közötti prímszámokból melyiket nem húzták ki egyszer sem az elmúlt évben. A feladat megoldása során az itt megadott prímszámokat felhasználhatja vagy előállíthatja! (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89.)
   **Expected Output:**
   ```
     13, 17, 31, 41
   ```

#### Exact strings
- `Van` / `Nincs`

---

### Vigenère tábla

#### Meta
- level: emelt
- year: 2005
- session: október
- language: hu
- difficulty: 3

#### Tags
- IO
- string
- table
- lookup

#### Scenario
Már a XVI. században komoly titkosítási módszereket találtak ki az üzenetek elrejtésére. A század egyik legjobb kriptográfusának, Blaise de Vigenère-nek a módszerét kell megvalósítani. A kódoláshoz egy táblázatot (Vigenère-tábla) és egy kulcsszót használunk.

A kódolás második lépése: az átalakított nyílt szöveg adott karakterét megkeressük a táblázat első oszlopában, a kulcsszöveg azonos pozíciójú karakterét az első sorában; a sor és oszlop metszéspontjában lévő karakter a kódolt szöveg megfelelő karaktere.

#### Constraints
- Nyílt szöveg: nem üres, ≤255 karakter; kulcsszó: nem üres, ≤5 karakter.
- Átalakítás után csak A–Z maradhat (ékezetek nélkül, csupa nagybetű).
- Kulcsszó már a kódolás feltételeinek megfelelő; csak nagybetűssé alakítás kell (sem átalakítás, sem ellenőrzés).
- Kulcsszöveg = kulcsszó ismételve a nyílt szöveg hosszáig.
- Programnév: `kodol`; tábla: `vtabla.dat` (26×26); kimenet: `kodolt.dat`.

#### Example
Nyílt szöveg: `Ez a próba szöveg, amit kódolunk!`
Átalakítva: `EZAPROBASZOVEGAMITKODOLUNK`
Kulcsszó: `auto` → `AUTO`
Kulcsszöveg: `AUTOAUTOAUTOAUTOAUTOAUTOAU`
Kódolt: `ETTDRIUOSTHJEATAINDCDIEINE`

#### Data
	**files:** `vtabla.txt` (26 sor), `kodolt.txt` (kimenet)

Sample (`vtabla.txt`):
```
ABCDEFGHIJKLMNOPQRSTUVWXYZ
BCDEFGHIJKLMNOPQRSTUVWXYZA
CDEFGHIJKLMNOPQRSTUVWXYZAB
DEFGHIJKLMNOPQRSTUVWXYZABC
EFGHIJKLMNOPQRSTUVWXYZABCD
```

Explanation:
A fájl a Vigenère-tábla 26 sorát tartalmazza. Az `i`. sor az angol ábécé `i` pozícióval balra forgatott változata (0-tól indexelve): az első sor `A…Z`, a második `B…ZA`, …, az utolsó `ZABCDEFGHIJKLMNOPQRSTUVWXY`.

#### Tasks
1. `[IO]` Kérjen be a felhasználótól egy maximum 255 karakternyi, nem üres szöveget! A továbbiakban ez a nyílt szöveg.
   **Expected Input:**
   ```
     input(Ez a próba szöveg, amit kódolunk!)
   ```
2. `[string]` Alakítsa át a nyílt szöveget, hogy a későbbi kódolás feltételeinek megfeleljen! A magyar ékezetes karakterek helyett ékezetmenteseket kell használni (például á helyett a; ő helyett o stb.). Az átalakítás után csak az angol ábécé betűi szerepelhetnek, és a szöveg legyen csupa nagybetűs.
3. `[IO]` Írja ki a képernyőre az átalakított nyílt szöveget!
   **Expected Output:**
   ```
     EZAPROBASZOVEGAMITKODOLUNK
   ```
4. `[IO]` `[string]` Kérjen be a felhasználótól egy maximum 5 karakteres, nem üres kulcsszót! A kulcsszó a kódolás feltételeinek megfelelő legyen (sem átalakítás, sem ellenőrzés nem kell)! Alakítsa át a kulcsszót csupa nagybetűssé!
   **Expected Input:**
   ```
     input(auto)
   ```
5. `[string]` A kódolás első lépéseként fűzze össze a kulcsszót egymás után annyiszor, hogy az így kapott karaktersorozat (kulcsszöveg) hossza legyen egyenlő a kódolandó szöveg hosszával! Írja ki a képernyőre az így kapott kulcsszöveget!
   **Expected Output:**
   ```
     AUTOAUTOAUTOAUTOAUTOAUTOAU
   ```
6. `[IO]` `[table]` `[lookup]` `[string]` A kódolás második lépéseként: vegye az átalakított nyílt szöveg első karakterét, és keresse meg a `vtabla.dat` fájlból beolvasott táblázat első oszlopában! Ezután vegye a kulcsszöveg első karakterét, és keresse meg a táblázat első sorában! Az így kiválasztott sor és oszlop metszéspontjában lévő karakter lesz a kódolt szöveg első karaktere. Ezt ismételje a kódolandó szöveg többi karakterével is!
7. `[IO]` Írja ki a képernyőre és a `kodolt.dat` fájlba a kapott kódolt szöveget!
   **Expected Output:**
   ```
     ETTDRIUOSTHJEATAINDCDIEINE
   ```

---

### Fehérje

#### Meta
- level: emelt
- year: 2006
- session: május
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- sum
- min_max
- search
- lookup
- weighted_sum

#### Scenario
A fehérjék óriás molekulák; egy-egy fehérje aminosavak százaiból épül fel, amelyek láncszerűen kapcsolódnak. Minden fehérje húszféle aminosav különböző mennyiségű és sorrendű összekapcsolódásával jön létre. Az aminosavak mindegyike tartalmaz szenet, hidrogént, oxigént és nitrogént; néhányban kén is van.

Relatív molekulatömeg: C·12 + H·1 + O·16 + N·14 + S·32 (pl. Glicin: 2·12 + 5·1 + 2·16 + 1·14 + 0·32 = 75).

Peptidkötésnél minden kapcsolatnál egy vízmolekula (H₂O) lép ki → n aminosav esetén (n−1)·2 hidrogén és (n−1) oxigén vonódik le az összegképletből.

#### Constraints
- 20 aminosav; `bsa.txt` lánc ≤1000 egybetűs jel.
- Atomtömegek: C=12, H=1, O=16, N=14, S=32.
- Ha `aminosav.txt` hiányzik: az első 5 táblázatsor állandóként.
- Ha `bsa.txt` hiányzik: `G,A,R,F,C` tízszer egymás után (50 jel).
- Kimotripszin hasít: Y, F, W után; Factor XI: R után, ha A vagy V követi.
- Programnév: `feherje`; kimenet: `eredmeny.txt` (3–4. feladat).

#### Data
**files:** `aminosav.txt` (140 sor), `bsa.txt`, `eredmeny.txt` (kimenet)

Sample (`aminosav.txt`):
```
Gly
G
2
5
2
1
0
Ala
A
3
7
2
1
0
```

Explanation:
A fájl az aminosavak nevét nem tartalmazza. Minden aminosavra 7 sor: hárombetűs rövidítés, egybetűs betűjel, majd a C, H, O, N, S atomszámok (egész, külön sorban). Összesen 20 aminosav × 7 sor.

`bsa.txt`: a BSA fehérje aminosav-sorrendje, egybetűs jelekkel (soronként egy jel, vagy folyamatos szöveg — a beolvasás egybetűs azonosítókat vár).

#### Tables
| Név | Rövidítés | Betűjel | C | H | O | N | S |
|---|---|---|---|---|---|---|---|
| Glicin | Gly | G | 2 | 5 | 2 | 1 | 0 |
| Alanin | Ala | A | 3 | 7 | 2 | 1 | 0 |
| Arginin | Arg | R | 6 | 14 | 2 | 4 | 0 |
| Fenilalanin | Phe | F | 9 | 11 | 2 | 1 | 0 |
| Cisztein | Cys | C | 3 | 7 | 2 | 1 | 1 |
| Triptofán | Trp | W | 11 | 12 | 2 | 2 | 0 |
| Valin | Val | V | 5 | 11 | 2 | 1 | 0 |
| Leucin | Leu | L | 6 | 13 | 2 | 1 | 0 |
| Izoleucin | Ile | I | 6 | 13 | 2 | 1 | 0 |
| Metionin | Met | M | 5 | 11 | 2 | 1 | 1 |
| Prolin | Pro | P | 5 | 9 | 2 | 1 | 0 |
| Szerin | Ser | S | 3 | 7 | 3 | 1 | 0 |
| Treonin | Thr | T | 4 | 9 | 3 | 1 | 0 |
| Aszparagin | Asn | N | 4 | 8 | 3 | 2 | 0 |
| Glutamin | Gln | Q | 5 | 10 | 3 | 2 | 0 |
| Tirozin | Tyr | Y | 9 | 11 | 3 | 1 | 0 |
| Hisztidin | His | H | 6 | 9 | 2 | 3 | 0 |
| Lizin | Lys | K | 6 | 14 | 2 | 2 | 0 |
| Aszparaginsav | Asp | D | 4 | 7 | 4 | 1 | 0 |
| Glutaminsav | Glu | E | 5 | 9 | 4 | 1 | 0 |

#### Tasks
1. `[IO]` Töltse be az `aminosav.txt` fájlból az aminosavak adatait! 
2. `[weighted_sum]` Határozza meg az aminosavak relatív molekulatömegét (C·12 + H·1 + O·16 + N·14 + S·32)!
3. `[IO]` Rendezze növekvő sorrendbe az aminosavakat a relatív molekulatömeg szerint! Írja ki a képernyőre és az `eredmeny.txt` fájlba az aminosavak hárombetűs azonosítóját és a molekulatömeget (egy sorba, szóközzel elválasztva)!
   **Expected Output:**
   ```
     Gly 75
     Ala 89
     Ser 105
     Pro 115
     Val 117
     Thr 119
     Cys 121
     Leu 131
     Ile 131
     Asn 132
     Asp 133
     Gln 146
     Lys 146
     Glu 147
     Met 149
     His 155
     Phe 165
     Arg 174
     Tyr 181
     Trp 204
   ```
4. `[IO]` `[sum]` `[lookup]` A `bsa.txt` a BSA fehérje aminosav-sorrendjét tartalmazza egybetűs jelöléssel. Határozza meg a fehérje összegképletét (C, H, O, N, S darabszáma)! Vegye figyelembe, hogy minden peptidkötésnél egy H₂O lép ki! Az összegképletet a képernyőre és az `eredmeny.txt` fájlba pl. `C 16321 H 34324 O 4234 N 8210 S 2231` formában írja ki!
   **Expected Output:**
   ```
     C 16321 H 34324 O 4234 N 8210 S 2231
   ```
5. `[search]` `[min_max]` A Kimotripszin enzim a Tirozin (Y), Fenilalanin (F) és a Triptofán (W) után hasít. Határozza meg a hasított BSA lánc leghosszabb darabjának hosszát és az eredeti láncban elfoglalt helyét (első és utolsó aminosav sorszáma)! A kiíráskor nevezze meg a kiírt adatot, például: `kezdet helye:`!
6. `[search]` `[count]` A Factor XI enzim az Arginin (R) után hasít, de csak akkor, ha Alanin (A) vagy Valin (V) követi. Határozza meg, hogy a hasítás során keletkező első fehérjelánc-részletben hány Cisztein (C) található! A választ teljes mondatba illesztve írja ki a képernyőre!

#### Exact strings
- `kezdet helye:` (és a többi megnevezett kiírás a mintának megfelelően)
- Összegképlet forma: `C … H … O … N … S …`

---

### Rakodódaru

#### Meta
- level: emelt
- year: 2028
- session: október
- language: hu
- difficulty: 5

#### Tags
- IO
- count
- simulation
- validate
- path

#### Scenario
Egy csarnokban sínen mozgó rakodódaru dolgozik. A sín 1-től 30-ig számozott állásokból áll; a daru a 15. álláson, üresen indul. A napló parancsai: `J` jobbra, `B` balra adott számú állást, `FEL` teher felvétele, `LE` teher leadása. A daru terhelése 0 és 5 láda között maradhat, és nem hagyhatja el a sínt. A program a parancsokat állományból olvassa, végrehajtja őket, és jelzi, ha egy utasítás szabálytalan helyzetet okozna. A szabálytalan parancsot is végrehajtottnak tekinti a további követéshez, de feljegyzi az első hibát.

#### Constraints
- Parancsok ≤ 300; `J`/`B` lépés 1–12; `FEL`/`LE` ládaszám 1–5.
- Sín: állások 1–30; indulás: állás 15, teher 0; maximális teher 5.
- Az első szabálytalanság: állás < 1 vagy > 30, teher < 0, vagy teher > 5. Ha több feltétel egyszerre sérül, a sorrend: pályán kívül, negatív teher, túlterhelés.
- Ha nem volt szabálytalanság, a 5. feladatról ne írjon ki második sort.

#### Data
**files:** `parancsok.txt` (8 sor)

Sample (`parancsok.txt`):
```
J 4
FEL 3
B 6
LE 1
J 10
FEL 2
B 3
LE 4
```

Explanation:
Minden sor egy parancs: művelet és egész argumentum. A mintában a daru végig a sín 1–30 tartományában marad, és a teher soha nem lép ki a 0–5 sávból.

#### Tasks
1. `[IO]` Olvassa be és tárolja el a `parancsok.txt` tartalmát!
2. `[count]` Határozza meg, hány parancsot tartalmaz az állomány, és írja a képernyőre a parancsok számát! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A parancsok szama: 8
   ```
3. `[simulation]` `[path]` Hajtsa végre a parancsokat a 15. állásról, üresen indulva! Adja meg a daru végső állását és a végső terhelést! A két adatot nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A vegso allas: 20
     A vegso teher: 0
   ```
4. `[validate]` `[simulation]` Döntse el, előfordult-e szabálytalan helyzet! Ha a daru végig a sínon maradt és a teher 0–5 között volt, írja ki: `A daru vegig szabalyos maradt.` Különben írja ki: `A daru legalabb egyszer szabalyt szegett.`
   **Expected Output:**
   ```
     A daru vegig szabalyos maradt.
   ```
5. `[validate]` `[simulation]` Ha volt szabálytalanság, adja meg az első hibás parancs sorszámát (1-től) és az okát: `palyan kivul`, `negativ teher` vagy `tulterheles`! Ha nem volt szabálytalanság, erről a feladatról ne írjon ki semmit!
6. `[IO]` `[simulation]` A daru állapotát minden parancs után a `naplo.txt` állományba kell menteni. Minden parancs után egy sort írjon: a parancs sorszámát, az állást és a terhelést, szóközzel elválasztva! A sorok sorrendje egyezzen meg a parancsok sorrendjével!

#### Exact strings
- `A daru vegig szabalyos maradt.`
- `A daru legalabb egyszer szabalyt szegett.`
- `palyan kivul`
- `negativ teher`
- `tulterheles`

---

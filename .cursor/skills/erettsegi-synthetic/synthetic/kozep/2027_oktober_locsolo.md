### Locsoló

#### Meta
- level: közép
- year: 2027
- session: október
- language: hu
- difficulty: 4

#### Tags
- IO
- count
- path
- validate

#### Scenario
Egy kertészet automata locsolókocsija a gyepet egy parancsszó alapján járja be. A kocsi mindig északnak nézve indul a (0, 0) pontból. Az E betű egy métert lép a nézőiránya szerint, a J betű 90 fokot fordul jobbra, a B betű 90 fokot fordul balra. A program a parancsszót a forrásában tárolja, majd a megtett út adatait értékeli ki.

#### Constraints
- Parancsszó hossza 1–80 karakter; csak `E`, `J` és `B` szerepelhet.
- Kelet pozitív x, észak pozitív y; a kiindulás (0, 0), nézőirány észak.
- Manhattan-távolság: `|x| + |y|`.
- Cserélhető parancsszóval is működnie kell.

#### Data
Sample:
```
EEJBEE
```

Explanation:
Egyetlen parancsszó, szóköz nélkül. A mintában négy előrelépés, egy jobbra és egy balra fordulás van. A program ezt a forrásában tárolja, nem fájlból olvassa.

#### Tasks
1. `[IO]` A locsolókocsi parancsszavát a program forrásában kell eltárolnia. Tárolja el a megadott betűsorozatot egy megfelelő adatszerkezetben!
2. `[count]` Határozza meg, hogy a parancsszóban hány `E`, hány `J` és hány `B` betű található! Az eredményeket külön sorban, megnevezve írja a képernyőre!
   **Expected Output:**
   ```
     E betuk szama: 4
     J betuk szama: 1
     B betuk szama: 1
   ```
3. `[path]` Hajtsa végre a parancsszót a kiinduló helyzetből! Adja meg a kocsi végső helyzetét méterben, kelet és észak szerint, valamint a kiindulóponttól mért Manhattan-távolságot!
   **Expected Output:**
   ```
     A vegso helyzet: kelet 0, eszak 4
     A Manhattan-tavolsag: 4
   ```
4. `[validate]` Döntse el, hogy a kocsi a parancsszó végrehajtása után a kiinduló ponton áll-e! Ha igen, írja ki: `A locsolo visszater a kiindulo pontra.` Ha nem, írja ki: `A locsolo nem tert vissza a kiindulo pontra.`
   **Expected Output:**
   ```
     A locsolo nem tert vissza a kiindulo pontra.
   ```

#### Exact strings
- `A locsolo visszater a kiindulo pontra.`
- `A locsolo nem tert vissza a kiindulo pontra.`

---

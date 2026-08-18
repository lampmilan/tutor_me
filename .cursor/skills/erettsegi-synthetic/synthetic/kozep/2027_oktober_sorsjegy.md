### Sorsjegy

#### Meta
- level: közép
- year: 2027
- session: október
- language: hu
- difficulty: 3
- seed: 2027

#### Tags
- IO
- random
- min_max
- validate

#### Scenario
Egy sportegyesület tombolát tart az évadzáró ünnepségen. A program nyolc nyerő sorsjegyet sorsol az 1–50 tartományból, ismétlés nélkül. A sorsolás sorrendje a húzás sorrendje. A játékos ezután begépeli a saját szelvényének számát, és a program eldönti, szerepel-e a nyerő számok között.

#### Constraints
- Pontosan 8 különböző egész az 1–50 zárt tartományból.
- A húzás sorrendje számít; a legkisebb és legnagyobb a kisorsolt értékek közül értendő.
- A játékos száma pozitív egész; a bemenet érvényességét nem kell ellenőrizni.

#### Tasks
1. `[random]` Sorsoljon ki nyolc különböző egész számot 1 és 50 között, ismétlés nélkül, és tárolja el őket a húzás sorrendjében!
2. `[IO]` Írja a képernyőre a kisorsolt számokat egy sorban, szóközzel elválasztva, a húzás sorrendjében! A kiírás elején nevezze meg az adatot!
   **Expected Output:**
   ```
     A nyero szamok: 7 30 6 1 42 21 26 41
   ```
3. `[min_max]` A kisorsolt értékek közül határozza meg a legkisebbet és a legnagyobbat! Mindkét értéket nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A legkisebb nyero szam: 1
     A legnagyobb nyero szam: 42
   ```
4. `[IO]` `[validate]` Kérje be a felhasználótól a saját sorsjegyének számát! Ha a szám szerepel a nyerők között, írja ki: `Nyert!` Ha nem szerepel, írja ki: `Nem nyert.` A bekéréskor jelenjen meg a `A sajat szelveny szama:` szöveg.
   **Expected Input:**
   ```
     A sajat szelveny szama: input(21)
   ```
   **Expected Output:**
   ```
     output(Nyert!)
   ```

#### Exact strings
- `A sajat szelveny szama:`
- `Nyert!`
- `Nem nyert.`

---

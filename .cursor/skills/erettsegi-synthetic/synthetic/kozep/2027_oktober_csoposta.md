### Csőposta

#### Meta
- level: közép
- year: 2027
- session: október
- language: hu
- difficulty: 5

#### Tags
- IO
- count
- simulation
- path

#### Scenario
Egy kórház csőpostája tizenhat állomást köt össze egy körben. A kapszula az 1. állomásról indul, és a feljegyzett lépésszámokkal halad előre. A 4., a 9. és a 13. állomás átrakó: ideérkezve a kapszula automatikusan még két állomást ugrik előre. A program a lépéseket a forrásában tárolja, majd a kapszula útját követi.

#### Constraints
- Pontosan 7 lépés; minden lépés 1–6 egész.
- Állomások 1–16, körkörösen: 16 után az 1. következik.
- Átrakó állomások: 4, 9, 13; az extra +2 ugrás a lépés után, és az ugrás célja már nem számít újabb átrakónak.
- Cserélhető lépéssorral is működnie kell.

#### Data
Sample:
```
3, 3, 2, 5, 1, 4, 2
```

Explanation:
Hét egész szám, a kapszula lépései állomásban. A program ezeket a forrásában tárolja. A mintában az első lépés a 4. állomásra visz, ahonnan az átrakó még kettőt ugrik, így a kapszula a 6. állomásra kerül.

#### Tasks
1. `[IO]` A csőposta hét lépését a program forrásában kell eltárolnia. Tárolja el a megadott számokat egy megfelelő adatszerkezetben!
2. `[count]` Határozza meg, hány lépést tárolt el a program! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A lepesek szama: 7
   ```
3. `[simulation]` `[path]` Kövesse a kapszula útját az 1. állomástól! Adja meg, melyik állomáson áll a hét lépés (és a közben lezajlott átrakók) után! Az állomás sorszámát nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A kapszula vegallomasa: 15
   ```
4. `[count]` `[simulation]` Számolja meg, hányszor érkezett a kapszula átrakó állomásra a lépések után, az extra ugrás előtt! Az extra ugrás célállomását ne számolja újabb átrakónak akkor sem, ha az 4, 9 vagy 13!
   **Expected Output:**
   ```
     Az atrako erintesek szama: 5
   ```

---

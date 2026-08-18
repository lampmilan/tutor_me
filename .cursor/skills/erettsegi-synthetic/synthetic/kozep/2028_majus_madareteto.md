### Madáretető

#### Meta
- level: közép
- year: 2028
- session: május
- language: hu
- difficulty: 2

#### Tags
- IO
- sum
- min_max
- validate

#### Scenario
Egy madárbarát hét napon át feljegyezte, hány gramm eleséget töltött az etetőbe. A hét adatait a program a forrásában tárolja. Jutalom jár, ha legalább három egymást követő napon legalább 50 grammot töltött. A kiértékeléshez kell a heti összeg, a legnagyobb adag napja és az, hogy jár-e a jutalom.

#### Constraints
- Pontosan 7 egész, a hét napjainak sorrendjében; értékek 1–100 gramm.
- Több azonos legnagyobb érték esetén az első nap sorszáma (1–7).
- Jutalom: van legalább egy olyan háromnapos, egymást követő szakasz, amelyben minden nap ≥ 50.

#### Data
Sample:
```
42, 55, 61, 52, 38, 72, 44
```

Explanation:
Hét egész szám, az etetőbe töltött eleség grammban, hétfőtől vasárnapig. A program ezeket a forrásában tárolja, nem fájlból olvassa.

#### Tasks
1. `[IO]` A hét napi adatot a program forrásában kell eltárolnia. Tárolja el a megadott számokat egy megfelelő adatszerkezetben!
2. `[sum]` Határozza meg, összesen hány gramm eleséget töltött az etetőbe a hét során! Az eredményt nevezze meg a kiírásban!
   **Expected Output:**
   ```
     A heti eleseg: 364 g
   ```
3. `[min_max]` Adja meg a legnagyobb napi adagot és azt, hogy ez hányadik nap volt! Ha több ilyen nap van, az elsőt adja meg!
   **Expected Output:**
   ```
     A legnagyobb adag: 72 g, 6. nap.
   ```
4. `[validate]` Döntse el, jár-e a jutalom a három egymást követő, legalább 50 grammos nap szabálya szerint! Ha jár, írja ki: `Jutalom jar.` Ha nem, írja ki: `Nincs jutalom.`
   **Expected Output:**
   ```
     Jutalom jar.
   ```

#### Exact strings
- `Jutalom jar.`
- `Nincs jutalom.`

---

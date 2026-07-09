# Instrukcja AutoCAD — kolejność budowania planszy (krok po kroku)

Format docelowy: 2 plansze B1 100×70 poziomo. Rzut główny 1:500, detal 1:100, przekroje 1:100/1:200.
Zasada: **rysujemy w model space 1:1 w metrach**, a skalę ustawiamy dopiero w arkuszu (layout).

## Kolejność (build order)

### KROK 0 — Setup techniczny (raz, na start)
- **Jednostki:** komenda `UNITS` → długość: dziesiętne; skala wstawiania: **metry**.
- **Praca 1:1:** wszystko rysujemy w rzeczywistych wymiarach (1 jednostka = 1 m).
- **Warstwy (`LAYER`)** — załóż od razu, każda swój kolor/linia:
  - `00_granica` (linia kropka-kreska), `01_podkład` (mapa, szara/zablokowana),
  - `02_komunikacja`, `03_nawierzchnie`, `04_woda`,
  - `05_mala_arch` (schody, platformy, kaskady, ławki, pergole, food truck),
  - `06_drzewa_istn`, `07_drzewa_nowe`, `08_zielen_byliny` (kieszenie A/B/C),
  - `09_opisy`, `10_wymiary`, `11_kreskowania`.

### KROK 1 — Podkład + granica opracowania
- Wstaw mapę zasadniczą (DWG jako podkład, lub raster: `IMAGEATTACH` → wyskaluj `SCALE` z referencją do znanej odległości).
- Zablokuj warstwę podkładu.
- Obrysuj **granicę opracowania** (polilinia, linia kropka-kreska) na `00_granica`.

### KROK 2 — Komunikacja (rzut 1:500)
- Ścieżka pieszo-rowerowa (istniejąca, zachowana).
- Nowe ciągi piesze + zejścia + **pochylnia dostępna** dla osób z niepełnosprawnościami.
- Plac z **mobilnym food truckiem**.

### KROK 3 — Nawierzchnie (hatch)
- `HATCH` dla stref: beton, drewno (deki), żwir, łąka. Różne wzory/skale.

### KROK 4 — Mała architektura
- Schody **meandrujące** (polilinia-spline jako oś), platformy-leżaki, kaskady w punktach przegięcia.
- Ławki-donice L, pergole (pod pnącza), leżaki.

### KROK 5 — Zieleń
- Drzewa **istniejące zachowane** (wg dendrologii — topola nr 12 dominanta, pas wierzby nr 38).
- Usunięcie 2 klonów inwazyjnych (nr 11, 32).
- Nowe nasadzenia + **kieszenie łąki** wg stref A/B/C (paleta fiolet-srebro-biel przy wodzie).

### KROK 6 — Detal 1:100
- Rzut fragmentu: schody + kaskada + kieszeń, numeracja roślin + `granice detalu` na rzucie 1:500.

### KROK 7 — Przekroje (min. 2)
- Linie `A-A'`, `B-B'` na rzucie. Rysunek przekrojów (jeden przez schody+kaskadę+wodę).

### KROK 8 — Opisy i tabele
- Legenda (uzupełnić!), tabela programowa, **bilans terenu** (pow. biol. czynna vs utwardzona).

### KROK 9 — Elementy obowiązkowe (layout / paper space)
- Ramka + stopka (✅ gotowe), numeracja plansz.
- **Skala liczbowa + podziałka liniowa (graficzna)**.
- **Róża wiatrów / strzałka północy**.

## RAMKA + STOPKA (w arkuszu / paper space, 1:1 w mm) — B1 1000×700 poziomo

> Ramka i stopka rysujemy w LAYOUCIE (przestrzeń papieru), NIE w modelu. Jednostka = mm, skala wydruku 1:1.
> Model zostaje na rysunek, pokazany przez okno (viewport).

### 0. Ustaw arkusz
- Zakładka layoutu → PPM → `Menedżer ustawień strony` → Modyfikuj.
- Drukarka: `DWG To PDF.pc3`; rozmiar: **ISO B1 (1000×700)** lub własny 1000×700; orientacja: pozioma.
- Skala wydruku: **1:1 mm**.
- Wejdź w przestrzeń papieru (klik w zakładkę layoutu; pracuj poza oknem/viewportem).

### 1. Warstwy pod ramkę
- `RAMKA` (linie ramki), `OPIS_STOPKA` (teksty). Kolor dowolny, ale ramka grubsza (lineweight 0.35–0.50).

### 2. Ramka (współrzędne, origin 0,0 = lewy dolny róg arkusza)
- `PROSTOKĄT` (`RECTANG`): punkt 1 `10,10` → punkt 2 `990,690` (margines 10 mm).
- Linia stopki (dół): `LINIA` (`LINE`): `10,55` → `990,55`.
- Linia tytułu (góra): `LINIA`: `10,655` → `990,655`.
- Box numeru planszy (prawy góra): `RECTANG` `935,655` → `990,690`.

### 3. Styl tekstu
- `STYL` (`STYLE`) → nowy styl `OPIS`, czcionka **Arial** (jak na przykładzie).

### 4. Teksty (komenda `DTEKST`/`DTEXT`: punkt startu → wysokość → kąt 0 → wpisz tekst)
- **Tytuł planszy** — start `20,668`, wys. `10`:
  `KONCEPCJA ZAGOSPODAROWANIA FRAGMENTU CYPLA CZERNIAKOWSKIEGO - analizy i program`
- **Numer planszy** — start `948,665`, wys. `12`: `1/2`  (na Planszy 2 → `2/2`)
- **Stopka linia 1** — start `20,38`, wys. `7`:
  `PRZEDMIOT: Projekt obieralny 2B - Projektowanie bulwarów i promenad, ROK AKADEMICKI 2025/2026`
- **Stopka linia 2** — start `20,20`, wys. `7`:
  `AUTOR: Pola Organiszczak     PROWADZĄCY: dr inż. Magdalena Błaszczyk, dr inż. Tatiana Swoczyna, mgr inż. Karolina Kais`

> Uwaga na polskie znaki: `Błaszczyk`, `PROWADZĄCY`, `dr inż.` (na przykładzie były literówki bez ogonków — u nas poprawnie).

### 5. Powtórz na drugiej planszy
- Ten sam layout skopiuj (PPM na zakładce → Przenieś/Kopiuj) i zmień tytuł na `- projekt i wizualizacje` oraz numer na `2/2`.
- Najlepiej: zrób ramkę+stopkę **blokiem** (`BLOK`), żeby edytować raz dla obu.

## Podziałka liniowa + róża wiatrów — dokładne komendy (paper space, mm)

> Zasada bezpieczna dla „dynamic input": PIERWSZY punkt wpisuj jako `x,y` (absolutny),
> KOLEJNE jako `@dx,dy` (względny). Jak polska nazwa komendy nie działa — wpisz angielską
> z podkreśleniem: `_LINE`, `_PLINE`, `_COPY`, `_TEXT`, `_ROTATE`, `_MOVE`.

### Podziałka 1:500 (100 mm = 50 m; działki co 20 mm = 10 m)
- Warstwa `PODZIALKA` jako bieżąca.
- `LINIA` ↵ `400,75` ↵ `@100,0` ↵ ↵            (linia bazowa)
- `LINIA` ↵ `400,75` ↵ `@0,5` ↵ ↵              (jedna kreska pionowa)
- `KOPIUJ` ↵ (wskaż kreskę) ↵ `400,75` ↵ `@20,0` ↵ `@40,0` ↵ `@60,0` ↵ `@80,0` ↵ `@100,0` ↵ ↵
- Opisy `DTEKST` (start / wys. 3.5 / kąt 0): `398,66`→`0`, `416,66`→`10`, `436,66`→`20`, `456,66`→`30`, `476,66`→`40`, `496,66`→`50`, `506,66`→`m`
- `DTEKST` `400,82` wys. `4` → `1:500`

### Róża wiatrów (strzałka N)
- Warstwa `OPIS_STOPKA`.
- `PLINIA` ↵ `610,85` ↵ `@0,35` ↵ ↵            (trzon)
- `LINIA` ↵ `610,120` ↵ `@-5,-10` ↵ ↵          (grot lewy)
- `LINIA` ↵ `610,120` ↵ `@5,-10` ↵ ↵           (grot prawy)
- `DTEKST` `606,124` wys. `6` → `N`
- `OBRÓĆ` (zaznacz strzałkę+N) ↵ punkt bazowy `610,100` ↵ → dopasuj kąt do północy na rzucie.
- Na koniec `PRZESUŃ` obie grupy pod rzut 1:500.

## Status (7.07.2026)
Zrobione: stopki, analizy (Plansza 1 w dużej części). Do zrobienia wg tej kolejności: głównie
Plansza 2 (kroki 4–9) + detal i przekroje.

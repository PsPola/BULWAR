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

## Status (7.07.2026)
Zrobione: stopki, analizy (Plansza 1 w dużej części). Do zrobienia wg tej kolejności: głównie
Plansza 2 (kroki 4–9) + detal i przekroje.

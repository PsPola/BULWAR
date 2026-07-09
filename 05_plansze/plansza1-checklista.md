# PLANSZA 1 — checklista wymagań + kompozycja

Tytuł: „KONCEPCJA ZAGOSPODAROWANIA FRAGMENTU CYPLA CZERNIAKOWSKIEGO – analizy i program". Numer 1/2.
Źródła wymagań: `00_brief/brief-przedmiotu.md` + `00_brief/przyklad-pracy-studenckiej.md`.
Status: ✅ masz (z draftu) / 🟠 dodać lub dopracować.

## Co MUSI być na Planszy 1

| # | Element | Status | Uwagi |
|---|---|---|---|
| 1 | **Lokalizacja** (mapa PL/Warszawa + opis) | ✅ | „Tam, gdzie miasto łapie oddech" |
| 2 | **Profil użytkownika** (ikony + opis) | ✅ | spacerowicze, psy, rowery, rodziny, seniorzy, wędkarze |
| 3 | **Analiza powiązań widokowych** + plan widokowy | ✅ | dobry/umiarkowany/zły widok |
| 4 | **Dyspozycja funkcjonalno-przestrzenna 1:500** | ✅ | strefy kolorami — DOMINANTA planszy |
| 5 | **Analiza szaty roślinnej / inwentaryzacja** | ✅ | mapa gatunków drzew |
| 6 | **Analiza dendrologiczna — gospodarka drzewostanem** (kondensat) | 🟠 | z książeczki: stan+kolizje, wycinka 2 klonów (2328 zł), topola nr 12, wierzba nr 38 |
| 7 | **Fizjografia — linijka słońca / zacienienie** (kondensat) | 🟠 | z analizy słonecznej: 2–3 kadry (lato/zima 12:00) + wniosek |
| 8 | **Analiza przyrodnicza** (Natura 2000, łęgi) | ✅ | „projektujemy z Wisłą" |
| 9 | **Analiza komunikacji wewnętrznej i wyposażenia** | ✅ | opis + wnioski |
| 10 | **Tabela programowa** (strefy) | ✅ | gastronomiczna/wypoczynkowa/komunikacyjna/spacerowa |
| 11 | **Widoki** (zdjęcia 1–3 z terenu) | ✅ | |
| 12 | **Wnioski** | ✅ | zawarte w blokach tekstowych |

## Elementy OBOWIĄZKOWE (formalne)
| Element | Status | Uwagi |
|---|---|---|
| Stopka (autor + prowadzący) | ✅ | gotowa |
| Numeracja plansz (1/2) | ✅ | |
| Skala liczbowa (1:500) | ✅ | przy rzucie |
| **Podziałka liniowa (graficzna)** | 🟠 | DODAĆ pod rzutem 1:500 |
| **Róża wiatrów / strzałka N** | 🟠 | DODAĆ przy rzucie głównym (masz tylko na mapce lokalizacji) |

## Kompozycja (układ 3-kolumnowy, B1 poziomo)
- **Kolumna lewa:** Lokalizacja → Profil użytkownika → Powiązania widokowe → Widoki (zdjęcia).
- **Kolumna środkowa:** Dyspozycja 1:500 (duże, dominanta) → pod nią podziałka + róża wiatrów → Tabela programowa.
- **Kolumna prawa:** Szata roślinna → Dendrologia/gospodarka (kondensat) → Linijka słońca (kondensat) → Przyrodnicza → Komunikacja i wyposażenie.

## MAKIETA — dokładne współrzędne bloków (B1 1000×700, origin lewy-dolny)
Ramka 10,10–990,690. Linia tytułu y=655. Linia stopki y=55.
Trzy kolumny: **L** x15–320 · **C** x335–665 (najszersza, dominanta) · **P** x680–985.
Bloki rysujemy jako ramki pomocnicze (warstwa `POMOC`), potem wypełniamy treścią.

| Blok | Lewy-dolny róg | Rozmiar (@szer,wys) |
|---|---|---|
| L1 Lokalizacja | 15,540 | @305,110 |
| L2 Profil użytkownika | 15,435 | @305,95 |
| L3 Powiązania widokowe | 15,250 | @305,175 |
| L4 Widoki (zdjęcia 1–3) | 15,60 | @305,180 |
| C1 Dyspozycja 1:500 (rzut, dominanta) | 335,250 | @330,400 |
| C2 Podziałka liniowa + róża wiatrów | 335,205 | @330,40 |
| C3 Tabela programowa | 335,60 | @330,140 |
| P1 Szata roślinna (mapa) | 680,540 | @305,110 |
| P2 Dendrologia — gospodarka drzewostanem | 680,430 | @305,105 |
| P3 Linijka słońca / zacienienie | 680,320 | @305,105 |
| P4 Analiza przyrodnicza | 680,190 | @305,125 |
| P5 Komunikacja + wyposażenie | 680,60 | @305,125 |

## Kolejność realizacji (po kolei)
1. Ustaw siatkę kompozycji (3 kolumny) — pomocnicze linie w papierze.
2. Wstaw okno (viewport) z rzutem 1:500 w kolumnie środkowej.
3. Dodaj podziałkę liniową + różę wiatrów pod rzutem.
4. Rozłóż bloki już gotowe (lokalizacja, profil, widokowe, szata, przyrodnicza, komunikacja, tabela, widoki).
5. Dorób 2 kondensaty: dendrologia/gospodarka (#6) i linijka słońca (#7).
6. Sprawdź spójność (jeden font, wyrównanie do siatki, „światło" 30–40%).

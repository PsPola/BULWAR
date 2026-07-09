# Wzorce wykonawcze Nowaka: pergola + nawierzchnie

Materiał źródłowy (import z brancha `damian` repo architektura):
`materialy-zrodlowe/przyklad-nowak/PERGOLA_A1_PAWEL_NOWAK.pdf` i `..._NAWIERZCHNIE_C1_...pdf`.
Uwaga: to arkusze z przedmiotu „Budowa obiektów architektury krajobrazu 2" (inny site) — bierzemy
z nich **standard detalowania**, nie treść terenową. Data importu: 2026-07-09.

## PERGOLA — wzorzec arkusza wykonawczego (1:25 + detale 1:2.5)
Zawartość arkusza (do naśladowania przy naszej pergoli przy placu):
- Rzut fundamentów 1:25, rzut cięty na wys. 1 m, rzut z góry.
- Przekroje A-A' i B-B' 1:25, widok z boku i od frontu.
- 4 detale mocowań 1:2.5.

Wymiary orientacyjne (z rysunku):
- Słupy **100×100 mm**, rozstaw osiowy **180 cm**, wysięg belek górnych.
- Wysokość: przejście ~250 cm, całość ~270–280 cm.
- Fundamenty stopowe pod każdym słupem; posadowienie poniżej przemarzania.
- Rytm żeberek górnych (krokwie) ~33–38 cm.

## NAWIERZCHNIE — wzorzec (rzut 1:100 + przekroje warstw 1:10 + tabela materiałów)
Najcenniejsze dla nas: **układy warstw konstrukcyjnych** (możemy je wprost zaadaptować do naszych
nawierzchni: promenada, plac, ścieżki spacerowe, nawierzchnia betonowa).

Typy nawierzchni z legendy (I–V):
- I — droga pieszo-jezdna: kostka brukowa betonowa + obrzeża betonowe
- II — droga spacerowa: płyty deptakowe Ø45–60 cm + grys ogrodowy f. 8–16 mm, szer. 1 m
- III — droga piesza: kostka brukowa betonowa + obrzeża
- IV — droga docelowa: kostka brukowa **granitowa** + obrzeża
- V — nawierzchnia **betonowa** piesza

Typowy układ warstw (od góry, przykład drogi pieszej):
1. warstwa ścieralna (kostka/płyta/beton) — 4–6 cm
2. podsypka — piasek płukany f. 0–2 mm — 5 cm
3. podbudowa górna — żwir f. 8–16 mm — 5–10 cm
4. podbudowa dolna — tłuczeń f. 31,5–63 mm — 15–25 cm
5. warstwa odsączająca — pospółka f. 0–16 mm — 6 cm
6. grunt rodzimy — zagęszczony i wyrównany
+ obrzeża betonowe 50×20×5 cm na ławie fundamentowej beton C12/15.

Tabela materiałów: rodzaj / jednostka / ilość / producent-norma (np. Polbruk, Bruk-bet, Strzegom G602,
KAMAR). Wzór do naszej tabeli materiałów na detalu.

## Jak wykorzystać w BULWAR
- **Pergola:** skopiować układ arkusza + wymiary jako punkt startu; można wygenerować DXF z
  `narzedzia-dxf/skrypty/gen_pergola_v2.py` i dopasować.
- **Nawierzchnie:** użyć powyższych układów warstw w naszych przekrojach (promenada betonowa/żwirowa,
  plac pod food truck, ścieżki). Generator: `gen_nawierzchnia_v2.py`.
- **Detal główny (schody+kaskada):** styl detali 1:2.5 (kółka z powiększeniem) = wzorzec dla naszych
  detali mocowań/warstw.

# Ściąga AutoCAD — wiersz poleceń (projekt: schody z murkiem)

Każdą komendę wpisujesz w pasek "Type a command" i zatwierdzasz Enterem.
**Enter** = zatwierdź / powtórz ostatnią komendę · **Esc** = przerwij wszystko · **Cmd+Z** = cofnij · **Cmd+S** = zapisz

## Rysowanie

| Komenda | Skrót | Co robi | Jak używać |
|---|---|---|---|
| LINE | L | linia | klikasz/wpisujesz kolejne punkty, Enter kończy |
| RECTANG | REC | prostokąt | dwa przeciwległe rogi, np. `0,0` → `305,120` |
| PLINE | PL | polilinia (łamana w jednym kawałku) | punkty po kolei, Enter kończy; opcja W = szerokość (strzałki!) |
| CIRCLE | C | okrąg | środek, potem promień |
| SPLINE | SPL | linia falista (urwania terenu) | kilka punktów "od ręki", Enter |
| HATCH | H | szraf (kreskowanie) | wybierz wzór i skalę, kliknij WEWNĄTRZ zamkniętego obszaru |
| TEXT | DT | tekst | punkt wstawienia → wysokość → obrót → treść → 2× Enter |

## Wpisywanie punktów

| Zapis | Znaczenie |
|---|---|
| `100,50` | punkt o współrzędnych x=100, y=50 |
| `@35,0` | 35 w prawo od ostatniego punktu (@ = "względem poprzedniego") |
| `@0,15` | 15 w górę od ostatniego punktu |
| `35` + ORTHO (F8) | ruch myszą wyznacza kierunek, liczba = odległość |

## Modyfikacje

| Komenda | Skrót | Co robi | Jak używać |
|---|---|---|---|
| MOVE | M | przesuń | zaznacz → Enter → punkt bazowy → punkt docelowy |
| COPY | CO | kopiuj | jak MOVE, można wklejać wielokrotnie |
| OFFSET | O | odsunięcie równoległe | odległość → klik na linię → klik po stronie odsunięcia (IDEALNE do stopni i warstw!) |
| TRIM | TR | przytnij | Enter (wszystko tnie) → klikasz wystające końcówki |
| EXTEND | EX | wydłuż do krawędzi | jak TRIM, tylko odwrotnie |
| STRETCH | S | rozciągnij | zaznacz oknem OD PRAWEJ DO LEWEJ, Enter, baza, cel |
| MIRROR | MI | odbicie lustrzane | zaznacz → oś odbicia (2 punkty) → zachować oryginał? N/T |
| ERASE | E | kasuj | zaznacz → Enter (albo zaznacz → Delete) |
| ROTATE | RO | obróć | zaznacz → punkt obrotu → kąt |
| SCALE | SC | przeskaluj | zaznacz → punkt bazowy → współczynnik |
| FILLET | F | zaokrągl/połącz rogi | R = promień (0 = ostry róg, łączy dwie linie) |
| EXPLODE | X | rozbij polilinię/blok na kawałki | zaznacz → Enter |
| JOIN | J | sklej odcinki w polilinię | zaznacz odcinki → Enter |

## Warstwy i wygląd

| Komenda | Co robi |
|---|---|
| LAYER (LA) | paleta warstw |
| -LAYER | warstwy z klawiatury: N=nowa, C=kolor, LW=grubość, L=rodzaj linii |
| LWDISPLAY → ON | pokazuj grubości linii na ekranie |
| LINETYPE | menedżer rodzajów linii (Load → DASHDOT itd.) |
| LTSCALE | skala wzoru linii przerywanych (u nas spróbuj 10–20) |
| MATCHPROP (MA) | przenieś właściwości: klik obiekt-wzór → klik obiekty do zmiany |
| PROPERTIES / Cmd+1 | panel właściwości (pilnuj: Color/Linetype/Lineweight = ByLayer!) |

## Wymiarowanie

| Komenda | Co robi |
|---|---|
| DIMLINEAR (DLI) | wymiar poziomy/pionowy: 2 punkty + gdzie postawić linię |
| DIMALIGNED (DAL) | wymiar równoległy do skosu |
| DIMSTYLE (D) | styl wymiarowania (wielkość liczb, strzałki/zaseki) |
| MLEADER (MLD) | odnośnik ze strzałką i tekstem (opisy warstw!) |

## Layout / kartka / druk

| Komenda | Co robi |
|---|---|
| MV (MVIEW) | nowa rzutnia (okienko z modelem) na Layoucie: klikasz 2 rogi |
| podwójny klik W rzutni | wchodzisz do środka (możesz przesuwać/skalować widok) |
| podwójny klik POZA rzutnią | wychodzisz na kartkę |
| ZOOM → S → `1/2xp` | skala rzutni 1:2 = rzeczywiste 1:20 (model w cm, kartka w mm!); 1:50 → `1/5xp` |
| PLOT / Cmd+P | drukowanie (do PDF) |
| PREVIEW | podgląd wydruku |
| PAGESETUP | ustawienia kartki (format, orientacja) |

## Nawigacja i pomoc

| Komenda / klawisz | Co robi |
|---|---|
| kółko myszy | zoom; wciśnięte kółko = przesuwanie widoku |
| ZOOM → E (albo 2× klik kółkiem) | pokaż wszystko (Zoom Extents) |
| F8 | ORTHO — rysowanie tylko poziomo/pionowo (do stopni: ZAWSZE włączone) |
| F3 | OSNAP — przyciąganie do końców/środków linii |
| DIST (DI) | zmierz odległość między 2 punktami |
| REGEN (RE) | odśwież rysunek (jak coś dziwnie wygląda) |
| DRAWINGRECOVERY | odzyskiwanie plików po awarii |
| OOPS | przywróć ostatnio skasowane (nawet po innych komendach) |

## Typowy przepływ pracy w tym projekcie

1. Warstwa aktualna → właściwa (WIDOK do rzutu, PRZEKROJ do przekrojów…)
2. Geometria: RECTANG / LINE / OFFSET (35 dla stopni, 12/30/8/15 dla warstw)
3. Porządki: TRIM / FILLET
4. Szrafy: HATCH na warstwie SZRAF (ANSI31 beton, krzyżowo żelbet, kółka kamień)
5. Wymiary: DIMLINEAR na warstwie WYMIARY
6. Opisy: TEXT / MLEADER na warstwie OPISY
7. Cmd+S po każdym etapie!

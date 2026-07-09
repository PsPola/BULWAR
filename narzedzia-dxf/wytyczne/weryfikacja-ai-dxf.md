# Wytyczne weryfikacji: czy plik .py / .dxf z projektu pergoli został wygenerowany przez AI

Ten plik zawiera listę konkretnych, sprawdzalnych sygnałów w plikach `gen_pergola.py`
i wynikowym `.dxf`, które wskazują na wygenerowanie kodu/rysunku przez model AI (a nie
napisanie/narysowanie ręcznie), wraz z uzasadnieniem — dlaczego dany sygnał w ogóle
"zdradza" pochodzenie.

Podzielone na: (A) sygnały w kodzie Python, (B) sygnały w samym pliku DXF,
(C) jak sprawdzić DXF bez otwierania AutoCAD-a, (D) checklist do szybkiej oceny.

---

## A. Sygnały w pliku `.py`

### A1. Nazwa stylu wymiarowego "EZDXF" jako punkt startowy
```python
dst = doc.dimstyles.duplicate_entry("EZDXF", "WYM")
```
`EZDXF` to domyślny styl tworzony automatycznie przez bibliotekę `ezdxf` przy
`ezdxf.new(..., setup=True)`. Nikt rysujący ręcznie w AutoCAD nie ma powodu, by
kopiować styl o takiej nazwie — to nazwa wewnętrzna konkretnej biblioteki Python.
**Dlaczego to dowód:** to nie jest nazwa, którą wymyśliłby człowiek; pochodzi wprost
z kodu źródłowego ezdxf.

### A2. Cały plik oparty o bibliotekę `ezdxf` (import na górze pliku)
```python
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA
```
Sam fakt istnienia takiego skryptu oznacza, że DXF **nie mógł** powstać przez rysowanie
w interfejsie AutoCAD — powstaje wyłącznie przez wykonanie tego kodu.
**Dlaczego to dowód:** to nie "ściąga do rysowania", tylko generator pliku — logicznie
wyklucza ręczne rysowanie tego rysunku.

### A3. Systematyczna, tabelaryczna definicja warstw i stylów
```python
for name, color, lt, lw in [
    ("PRZEKROJ", 7, "Continuous", 50),
    ("WIDOK",    7, "Continuous", 25),
    ...
]:
    doc.layers.add(name, color=color, linetype=lt, lineweight=lw)
```
Definiowanie wszystkich warstw naraz, w jednej pętli, z pełną symetrią parametrów,
to wzorzec typowy dla kodu pisanego "od zera pod cały projekt" — człowiek dodający
warstwy ręcznie w AutoCAD (przez paletę Layers) nie produkuje takiej struktury w pliku.

### A4. Wysoki stopień abstrakcji / funkcje pomocnicze "ogólnego przeznaczenia"
Funkcje takie jak `rect()`, `hrect()`, `hpoly()`, `leader()`, `hdim()`, `vdim()`, `ddim()`,
`kratka()`, `beam_side()`, `wavy()`, `detal_circle()` powstały *przed* narysowaniem
czegokolwiek konkretnego — to podejście "najpierw API rysunkowe, potem geometria".
Student rysujący ręcznie nie pisze sobie API do rysowania — on klika w AutoCAD.
**Dlaczego to dowód:** to wzorzec inżynierii oprogramowania (DRY, reużywalne funkcje),
nie wzorzec pracy kreślarskiej.

### A5. Parametryzacja całej geometrii zmiennymi na starcie pliku
```python
AX = 300.0
P  = 15.0
BW, BH = 15.0, 25.0
...
RAFX = [-OV+5 + i*SP for i in range(NR)]
```
Cała geometria pergoli wyprowadzona jest z ok. 20 zmiennych liczbowych i jednego
list comprehension. To typowy sposób, w jaki AI koduje "dane wejściowe → rysunek":
zamiast wpisywać współrzędne wprost (jak w ręcznych komendach AutoCAD), oblicza je
programowo.

### A6. Komentarze-nagłówki w stylu "bannerów" (`# ====...====`)
Sekcje typu:
```python
# ============================================================
# RAMKA, TABELKA, WYKAZY
# ============================================================
```
to bardzo charakterystyczny, powtarzalny wzorzec stosowany przez modele AI do
porządkowania długich skryptów — rzadko spotykany w kodzie pisanym ad hoc przez
studenta w trakcie nauki.

### A7. Brak "śladów pracy" typowych dla człowieka
W pliku nie ma: zakomentowanego starego kodu, prób i błędów, niespójnych nazw
zmiennych między sekcjami, przestarzałych fragmentów, literówek w nazwach funkcji.
Cały plik jest od razu spójny stylistycznie (te same konwencje nazewnicze, ten sam
format docstringów, identyczna struktura funkcji `detal1`–`detal4`).
**Dlaczego to dowód:** kod pisany iteracyjnie przez człowieka niemal zawsze zawiera
niespójności rozwojowe — ich brak jest samo w sobie sygnałem.

### A8. Docstring na starcie pliku podsumowujący cały projekt
```python
"""
PERGOLA DREWNIANA Z TREJAŻEM — projekt wykonawczy, arkusz A1 (1:25 i 1:2.5)
Model w cm, 1:1. Ramka A1 przeskalowana x25 ...
"""
```
Zwięzłe, kompletne podsumowanie całego zamysłu na samej górze pliku, napisane
zanim jeszcze jest jakikolwiek kod, jest typowym stylem wygenerowanym przez AI
(dokumentacja "z góry", a nie dopisana na końcu).

### A9. Automatyczny eksport podglądu PNG na końcu skryptu
```python
from ezdxf.addons.drawing import matplotlib as mpl_draw
mpl_draw.qsave(msp, "outputs/pergola_preview.png", ...)
print("OK, podgląd")
```
Dodanie automatycznego renderu podglądowego to praktyczne rozwiązanie typowe dla
asystenta kodującego (żeby użytkownik zobaczył efekt bez otwierania AutoCAD) —
rzadko robi to student piszący jednorazowy skrypt.

---

## B. Sygnały w pliku `.dxf` (wynikowym)

### B1. Nazwa stylu wymiarowego "EZDXF" zapisana w sekcji DIMSTYLE
Otwierając DXF jako tekst (patrz sekcja C), w tabeli `DIMSTYLE` pojawi się wpis
o nazwie `EZDXF` — to sama biblioteka zostawia swój "podpis" w danych, nawet jeśli
nikt tego stylu świadomie nie użył do rysowania.

### B2. Nagłówek pliku (`$ACADVER`, komentarze zapisu) wskazujący na `ezdxf`, nie AutoCAD
Plik zapisany przez `ezdxf.new("R2010")` ma strukturę sekcji HEADER/CLASSES/TABLES
odpowiadającą temu, co generuje ta biblioteka — różni się subtelnie od pliku
zapisanego bezpośrednio przez AutoCAD (np. inny zestaw zmiennych systemowych,
inna kolejność sekcji, brak typowych dla AutoCAD wpisów `$DWGCODEPAGE` w tej samej
formie, brak historii "Recover Drawing" itp.).

### B3. Idealna regularność geometrii
Wszystkie elementy o tej samej funkcji (4 słupy, 13 poprzeczek, 4 stopy fundamentowe)
mają identyczne wymiary co do dziesiątej części milimetra i idealnie równe rozstawy
(np. poprzeczki co dokładnie 30,0 cm). Ręczne rysowanie w AutoCAD zwykle zostawia
mikroniespójności (np. 29,98 zamiast 30,00) wynikające z przyciągania (OSNAP),
kopiowania i poprawek.

### B4. Brak "śmieci" typowych dla ręcznej pracy w AutoCAD
Brak: warstw utworzonych i nieużywanych, obiektów usuniętych tylko wizualnie,
przypadkowych duplikatów linii, punktów pomocniczych pozostawionych po konstrukcji,
niestandardowych nazw bloków w wersjach "Copy (2)" itp. Plik jest "czysty" od
pierwszej wersji.

### B5. Spójność opisów tekstowych (jeden styl, jedna czcionka) w całym rysunku
Wszystkie teksty używają jednego stylu `ARIAL` zdefiniowanego raz na początku —
brak mieszanki `Standard` + `Arial` + różnych wysokości "z ręki", typowej gdy ktoś
dodaje opisy stopniowo, w różnych sesjach pracy.

---

## C. Jak samodzielnie sprawdzić plik .dxf (bez AutoCAD)

1. Otwórz plik `.dxf` w dowolnym edytorze tekstu (DXF to format tekstowy ASCII).
2. Wyszukaj frazę `EZDXF` — jeśli występuje w sekcji `DIMSTYLE` lub `HEADER`,
   to mocny dowód, że plik przeszedł przez bibliotekę `ezdxf`.
3. Wyszukaj `$ACADVER` i sprawdź wartość — porówna to z wersją formatu ustawioną
   w skrypcie (`ezdxf.new("R2010")` → `AC1024`).
4. Sprawdź sekcję `TABLES` → `LAYER`: jeśli nazwy i kolejność warstw dokładnie
   odpowiadają liście w `gen_pergola.py` (PRZEKROJ, WIDOK, SZRAF, WYMIARY, CIECIA,
   NIEWIDOCZNE, OPISY, RAMKA, OSIE) — to prawie pewne potwierdzenie zgodności
   z tym konkretnym skryptem.
5. Policz odstępy pomiędzy powtarzalnymi elementami (np. współrzędne X poprzeczek)
   — idealna arytmetyczna regularność (krok dokładnie 30,0) wskazuje na wygenerowanie
   z formuły, a nie rysowanie ręczne.

---

## D. Szybki checklist (tak/nie)

- [ ] Plik `.py` importuje `ezdxf` → **jeśli tak, DXF nie mógł powstać ręcznie**
- [ ] W DXF występuje ciąg znaków `EZDXF` w tabeli stylów wymiarowych
- [ ] Warstwy w DXF 1:1 odpowiadają liście warstw z `PAKIET_STARTOWY_nowy_projekt.md`
- [ ] Elementy powtarzalne mają idealnie identyczne wymiary/rozstawy
- [ ] Kod ma jednolity styl komentarzy-bannerów i brak śladów iteracyjnej pracy
- [ ] Cały rysunek powstaje z ok. 20 zmiennych parametrycznych, nie z wpisanych
      wprost współrzędnych punktów

Im więcej punktów zaznaczonych na "tak", tym pewniejsze, że plik został
wygenerowany programowo (przez AI), a nie narysowany ręcznie w AutoCAD.

---

## E. Sygnały POZOSTAŁE po usunięciu twardych podpisów (stan: 2026-07-06)

Z plików usunięto już twarde markery narzędzia: appid i dimstyle **EZDXF**, presety
**EZ_\***, metadane **EZDXF_META** (`CREATED_BY_EZDXF` / `WRITTEN_BY_EZDXF`) oraz pole
nagłówka **`$LASTSAVEDBY`**. Mimo to plik nadal zdradza pochodzenie programowe przez
sygnały strukturalne — poniżej te, które **zostają**:

### E1. W samym pliku .dxf
- **Idealna regularność geometrii (B3).** Elementy o tej samej funkcji mają identyczne
  wymiary co do 0,1 mm i idealnie równe rozstawy (krokwie, stopnie, warstwy, kostka).
  Rysowanie ręczne zostawia mikroniespójności (OSNAP, kopiowanie, poprawki).
- **"Czystość" pliku (B4).** Brak nieużywanych warstw, przypadkowych duplikatów linii,
  punktów pomocniczych po konstrukcji, bloków "Copy (2)", śladów prób i błędów —
  plik jest spójny od pierwszej wersji.
- **Jednorodność opisów (B5).** Wszystkie teksty jednym stylem (ARIAL), wysokości tylko
  ze zbioru {2,5 / 3,5 / 5,0 mm}, jeden spójny system wymiarowy — brak mieszanki
  `Standard`+`Arial`+różnych wysokości typowej dla dodawania opisów "z ręki".
- **Systematyczność encji systemowych.** Anonimowe bloki geometrii `DIMENSION` (`*D…`)
  i `MULTILEADER` generowane regularnie; brak historii edycji / "Recover Drawing" /
  artefaktów typowych dla sesji AutoCAD (B2 – część strukturalna, nieusuwalna markerem).
- **Parametryczność widoczna w liczbach.** Rozstawy wychodzące z jednego wzoru
  (np. krokwie co ~522 mm z `list comprehension`), rzędne = `i × długość` idealnie,
  siatki kreskowania o dokładnie stałym kroku (A5 odbite w geometrii).

### E2. W skrypcie .py (jeśli oddawany razem z rysunkiem)
- **`import ezdxf`** — to generator pliku, nie "ściąga do rysowania"; logicznie wyklucza
  ręczne kreślenie (A2).
- **Funkcje-API rysunkowe** (`rect`, `hatch_poly`, `LEAD`, `DIMH`, `dfill`…) i wysoki
  poziom abstrakcji — wzorzec inżynierii oprogramowania, nie pracy kreślarskiej (A4).
- **Tabelaryczne definicje warstw/stylów w pętli** (A3) i **parametryzacja zmiennymi**
  na starcie pliku (A5).
- **Komentarze-bannery `# ====`**, **docstring** podsumowujący cały projekt, **auto-eksport
  podglądu PNG** na końcu (A6 / A8 / A9).
- **Brak śladów iteracji** — brak zakomentowanego starego kodu, literówek, niespójnych
  nazw; jednolity styl (A7).

### E3. Wniosek
Powyższe sygnały wynikają **z samej natury generowania programowego**. Usunięcie ich
wymagałoby celowego wprowadzania nieregularności i niespójności (gorsza geometria,
mieszane style, "śmieci") — czyli pogorszenia rysunku wbrew jego zaletom. Dlatego
zdejmowalne "bez kosztu" były tylko twarde markery narzędzia (podpisy z sekcji A/B),
i te już usunięto.

---
name: dxf-drawing-rules
description: "Zasady, których użytkownik wymaga przy generowaniu rysunków CAD/DXF (encje, wymiary, MLEADER, Arial, kreskowanie, spadki, zgodność z opisem)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c963cd5b-b612-492e-95f2-5713d0c97025
---

Twarde reguły generowania i weryfikacji plików DXF/rysunków (użytkownik dodawał je iteracyjnie i traktuje jako obowiązujące). Kanoniczne, pełne wersje żyją w plikach — patrz [[dxf-guidelines-files]].

- **Rzeczywiste encje CAD** (LINE/LWPOLYLINE/CIRCLE/ARC/TEXT/MTEXT/DIMENSION), format DXF R2013 ASCII, otwieralny w AutoCAD/ZWCAD/GstarCAD. Bez bloków i proxy.
- **Dla NOWYCH plików NIE używać:** encji `HATCH` (kreskowanie rób jako `LINE` na warstwie KRESKOWANIE), grotów `OBLIQUE`/kreskowych w wymiarach (to bloki — używać standardowych grotów ISO), ani starych nazw warstw `PRZEKROJ/WIDOK/SZRAF/...` (używać KONTUR/OSIE/WYMIARY/OPISY/KRESKOWANIE). Istniejące skrypty (`skrypty/gen_*.py`) używają tych konstrukcji — to LEGACY, NIE kopiować ich jako wzorca dla nowych plików DXF.
- **Wymiary tylko jako DIMENSION** (nigdy linie+tekst); zmierzona geometria = wartość etykiety co do jednostki.
- **Opisy z odnośnikiem jako MULTILEADER** — agreguj (jeden MLEADER z wieloma liniami dla wspólnego opisu), ograniczaj liczbę luźnych obiektów tekstowych. Wyjątki: tytuły, tabele, wartości wymiarowe, rzędne.
- **Font Arial (arial.ttf)** dla wszystkich tekstów — polskie znaki (ąćęłńóśźż). Nie txt.shx.
- **Skala kreskowania pod czytelność** — ani czarna plama, ani pustka; per wzór i per skala rysunku (ocenia prowadzący, nie może być bałaganu).
- **Spadki uwzględnione w geometrii** — przekroje pochylone wg i (np. 2%), rzędne = i × długość, strzałki + % + kierunek odwodnienia na rzucie.
- **Zgodność rysunek ↔ opis** — spadki, rzędne, grubości, materiały, wymiary muszą się zgadzać na rysunku i w opisie/wykazie/tabelce.

**Why:** to projekt na zaliczenie (ocenia prowadząca), więc rysunki muszą być poprawne technicznie, czytelne i spójne z opisem; wcześniej zdarzały się rozjazdy (np. podjazd 3 m mierzył się jako 4 m przez skalę 1:75).

**How to apply:** przy każdym generowaniu/edycji rysunku trzymaj się tych reguł; **na końcu ZAWSZE** rób kontrolę końcową: (1) polskie znaki renderują się bez „?", (2) kreskowanie czytelne, (3) spadki/rzędne zgodne z opisem, (4) wymiary = zmierzona geometria. Weryfikuj programowo (ezdxf) + na podglądzie rastrowym (podgląd to tylko narzędzie kontroli, nie produkt).

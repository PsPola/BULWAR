# Narzędzia DXF — generowanie rysunków CAD z Pythona

Zaimportowane z wcześniejszego projektu (autor: Pola Organiszczak). Mechanizm generuje
**poprawne pliki DXF R2013** biblioteką **`ezdxf`** — otwierane bez błędów w AutoCAD / ZWCAD / GstarCAD.
Do BULWAR pasują wprost: schody+murek, pergole, ławki, nawierzchnie = nasze elementy.

## Co tu jest
```
skrypty/       – generatory DXF (Python + ezdxf)
wytyczne/      – standard DXF, ściąga AutoCAD, weryfikacja
wiedza-cad/    – reguły rysowania i porządkowania plików (z pamięci projektu)
```

## Skrypty (każdy zapisuje DXF + podgląd PNG do ./outputs/ z datą-godziną)
| Skrypt | Co generuje | Przydatność w BULWAR |
|---|---|---|
| `gen_schodyimurek_v2.py` | schody ogrodowe + murek | **DETAL: meandrujące schody + murek** |
| `gen_pergola_v2.py` | pergola | **pergole pod pnącza** (glicynia, powojniki) przy placu |
| `gen_lawka.py` | ławka | **ławka-donica L** (patrz `wiedza-cad/lawka-l-projekt.md`) |
| `gen_nawierzchnia_v2.py` | nawierzchnia z warstwami | przekroje nawierzchni promenady/placu |
| `gen_dzialka_poglad.py` | pogląd działki | szybki szkic/pogląd |
| `usun_pole_naglowka_dxf.py` | narzędzie: czyści pole nagłówka DXF | porządki po generacji |

> Wersje `_v2` są nowsze — używaj ich. Wersje bez `_v2` zostawione dla historii.

## Jak uruchomić
```bash
python3 -m pip install -r requirements.txt      # ezdxf + matplotlib
cd narzedzia-dxf/skrypty
python3 gen_schodyimurek_v2.py                  # tworzy outputs/schody_murek_v2_<data>.dxf + podgląd .png
```
Potem otwierasz `.dxf` w AutoCAD 2025 i dopracowujesz.

## Standard (kluczowe zasady — pełne w `wytyczne/WYTYCZNE_DXF.md`)
- DXF R2013 ASCII, **model 1:1 w mm**, skala druku ustawiana anotacją.
- Tylko rzeczywiste encje: `LINE / LWPOLYLINE / CIRCLE / ARC / MTEXT / DIMENSION / MULTILEADER`.
- **BEZ** bloków, proxy i `HATCH` (kreskowanie = prawdziwe linie na warstwie `KRESKOWANIE`).
- Warstwy: `KONTUR / OSIE / WYMIARY / OPISY / KRESKOWANIE`.
- Font **Arial** (polskie znaki!), teksty 2.5 / 3.5 / 5.0 mm.
- Wymiary jako `DIMENSION`, opisy z odnośnikiem jako `MLEADER`.

## Warto zajrzeć
- `wytyczne/sciaga_autocad.md` — **ściąga komend AutoCAD** (idealna teraz przy planszach).
- `wytyczne/weryfikacja-ai-dxf.md` — jak sprawdzić poprawność DXF.
- `wiedza-cad/dxf-drawing-rules.md` — zasady rysunku wykonawczego (arkusz, przekroje, detale).
- `wiedza-cad/lawka-l-projekt.md` — gotowa koncepcja ławki L (siedzisko kamień + donica beton).

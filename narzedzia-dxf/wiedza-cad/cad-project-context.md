---
name: cad-project-context
description: "Kontekst projektów CAD (kto, przedmiot, generatory Python/ezdxf, stan nawierzchni)"
metadata: 
  node_type: memory
  type: project
  originSessionId: c963cd5b-b612-492e-95f2-5713d0c97025
---

Projekty wykonawcze architektury krajobrazu (SGGW, rok II sem. 4, prowadząca dr hab. Edyta Rosłon-Szeryńska; wykonuje **Pola Organiszczak**). Repo `architektura`.

- Rysunki generowane programowo w **Python + ezdxf** (arkusze A1, model w cm, ramka ×10; podgląd PNG przez `ezdxf.addons.drawing.matplotlib`). Skrypty w **`skrypty/`**: `gen_nawierzchnia.py`, `gen_pergola.py`, `gen_schodyimurek.py`, `gen_dzialka_poglad.py` (matplotlib). **Uruchamiać z roota repo** (ścieżki względne do `outputs/`). Wyjście w `outputs/`.
- Struktura repo: `skrypty/` (generatory) · `wytyczne/` (dokumentacja/wytyczne, dawniej `xxxxx/`) · `materialy/` (PDFy referencyjne + `szkice/` = zdjęcia szkiców) · `outputs/` (wygenerowane DXF/PDF/PNG) · `pamiec/` (pamięć).
- **Nawierzchnia**: plan zagospodarowania działki **12 × 33 m** (dz. 103/1), układ L (podjazd 12×3, dom 7×15, garaż 4×3, ścieżka 1 m L, schodki, podest 4×3) + przekroje A-A/B-B/C-C 1:10 + detal styku, legenda, opis techniczny, bilans, wykaz. Odwodnienie: rozsączanie na własny trawnik (art. 234 Prawa wodnego — bez odprowadzania na sąsiada).
- **Skala rzutu nawierzchni = 1:100** (cofnięte z 1:75 na życzenie, bo przy 1:75 pomiar linijką 1:100 dawał 3 m jako 4 m; różnica 4/3 = 1,3333). Sekcje/detal 1:10. Dodana podziałka liniowa.
- Zasady poprawności rysunków: [[dxf-drawing-rules]]. Pliki wytycznych: [[dxf-guidelines-files]].

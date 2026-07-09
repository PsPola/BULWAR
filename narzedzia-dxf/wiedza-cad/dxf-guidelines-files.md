---
name: dxf-guidelines-files
description: Gdzie w repo leżą kanoniczne pliki wytycznych DXF i pakiet startowy projektów
metadata: 
  node_type: memory
  type: reference
  originSessionId: c963cd5b-b612-492e-95f2-5713d0c97025
---

Kanoniczne wytyczne i pakiet startowy (repo `architektura`, folder `wytyczne/`):

- **`wytyczne/WYTYCZNE_DXF.md`** — pełne wytyczne generowania/weryfikacji DXF (15 reguł + checklist weryfikacyjny). Wzorzec do sprawdzania kolejnych projektów. Streszczenie reguł: [[dxf-drawing-rules]].
- **`wytyczne/PAKIET_STARTOWY_nowy_projekt.md`** — pakiet startowy na nowy projekt (prompt startowy, wymagania prowadzącej, szablon warstw AutoCAD, ustawienie kartki, triki, proces). Zawiera sekcję-skrót „WYTYCZNE DXF".
- Inne w `wytyczne/`: `sciaga_autocad.md`, `pergola-wytyczne.md`, `SKILL.md`.

**Dwie konwencje — NIE MIESZAĆ w jednym pliku:**
- Weryfikacja/eksport DXF: model w **mm**, skala **1:1**, warstwy KONTUR/OSIE/WYMIARY/OPISY/KRESKOWANIE.
- Rysowanie w AutoCAD wg wymagań prowadzącej: model w **cm**, warstwy PRZEKROJ/WIDOK/SZRAF/… , ramka A1 ×10.

Gdy dodawane są nowe „zasady" — aktualizować OBA: `WYTYCZNE_DXF.md` (reguła + checklist) i skrót w `PAKIET_STARTOWY_nowy_projekt.md`.

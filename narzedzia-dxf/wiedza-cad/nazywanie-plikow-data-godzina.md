---
name: nazywanie-plikow-data-godzina
description: "Kanon nazw eksportowanych plików: {project}_{yyMMdd-hhmm}.dxf oraz podgląd_{project}_{yyMMdd-hhmm}.png"
metadata:
  type: feedback
---

**Kanon nazw plików wynikowych** (`outputs/`) — znacznik czasu `yyMMdd-hhmm` (rok 2-cyfr, 24 h)
**NA KOŃCU** nazwy, po nazwie projektu:
- DXF: `{project-name}_{yyMMdd-hhmm}.dxf` — np. `pergola_v2_260706-0637.dxf`
- Podgląd (**PNG**, raster): `podgląd_{project-name}_{yyMMdd-hhmm}.png` — np. `podgląd_pergola_v2_260706-0637.png`

`project-name` zachowuje sufiks `_v2` (odróżnia od legacy). Podgląd **zostaje PNG** — nie PDF.

**Why:** użytkownik ustalił ten kanon; kolejne wersje mają być rozróżnialne po dacie/godzinie,
a podgląd ma pozostać rastrowym PNG.

**How to apply:** generatory `skrypty/gen_*_v2.py` liczą `TS = datetime.now().strftime("%y%m%d-%H%M")`
i zapisują `outputs/{project}_{TS}.dxf` (`doc.saveas`) + `outputs/podgląd_{project}_{TS}.png`
(`_mpl.qsave`). Historia: wcześniej był prefiks `YY-MM-DD_HH-MM_`; zmienione na obecny kanon 2026-07-06.
Po zapisie nadal przepuszczaj DXF przez [[czyszczenie-lastsavedby]]. Powiązane:
[[cad-project-context]], [[dxf-drawing-rules]].

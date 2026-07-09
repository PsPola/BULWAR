---
name: bez-zbednych-strzalek
description: Nie dodawać wolnostojących, pełnych trójkątnych grotów/strzałek przy elementach — są zbędne
metadata:
  type: feedback
---

**Nie dodawać wolnostojących, pełnych (czarnych) trójkątnych grotów/strzałek** stawianych bezpośrednio przy elementach rysunku. Konkretny przypadek: w nawierzchni, w `detal_styk` (Detal 1 — połączenie na obrzeżu), dwa solidne groty `arrow(...)` po bokach obrzeża przy „i=2%" — użytkownik uznał je za totalnie niepotrzebne.

**Why:** zaśmiecają rysunek; sam podpis spadku „i=2%" (ewentualnie cienka linia spadku) w pełni przekazuje informację. Groty jako osobne symbole niczego nie wnoszą.

**How to apply:** spadek pokazuj tekstem `i=X%` (opcjonalnie subtelną linią kierunku), **bez** dodawania osobnych pełnych grotów strzałek przy elemencie. Nie koliduje to z [[dxf-drawing-rules]] (spadki nadal uwzględnione geometrycznie + opis) — chodzi o rezygnację z ozdobnych, redundantnych grotów. Dotyczy też przyszłych generatorów.
 
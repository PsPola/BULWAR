---
name: czyszczenie-lastsavedby
description: "Krok flow: po wygenerowaniu DXF usuwać pole $LASTSAVEDBY skryptem usun_pole_naglowka_dxf.py"
metadata:
  node_type: memory
  type: feedback
---

Po wygenerowaniu pliku(ów) .dxf **usuwać z nagłówka zmienną `$LASTSAVEDBY`** (domyślnie ezdxf wpisuje tam „ezdxf"). To stały element flow, nie jednorazówka.

Narzędzie: **`skrypty/usun_pole_naglowka_dxf.py`** (uruchamiać z roota repo).

```
python3 skrypty/usun_pole_naglowka_dxf.py --katalog outputs --nadpisz   # wszystkie DXF w outputs, w miejscu
python3 skrypty/usun_pole_naglowka_dxf.py plik.dxf                        # pojedynczy, kopia *_bez_pola.dxf
python3 skrypty/usun_pole_naglowka_dxf.py plik.dxf --pole '$INNE'         # inna zmienna nagłówka
```

Skrypt wycina parę `9`/nazwa + wszystkie jej pary kod/wartość aż do kolejnej zmiennej (`9`), zachowuje styl końca wiersza, domyślnie zapisuje kopię (`--nadpisz` = w miejscu).

**Why:** użytkownik chce, żeby DXF-y nie nosiły śladu narzędzia/autora w `$LASTSAVEDBY`.

**How to apply:** dopisz ten krok do kontroli końcowej z [[dxf-drawing-rules]] — po generacji i weryfikacji ezdxf przepuść wyjście przez skrypt. **NIE** usuwać `$ACADVER` (obowiązkowe pole wersji — bez niego ezdxf/AutoCAD nie otworzą pliku); jeśli trzeba, podmieniać wartość, nie kasować zmiennej. Kontekst generatorów: [[cad-project-context]].

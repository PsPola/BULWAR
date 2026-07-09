---
name: czyszczenie-sladow-ezdxf
description: "Krok flow: generatory v2 usuwają ślady ezdxf (appid EZDXF, dimstyle EZDXF/EZ_*, metadane EZDXF_META)"
metadata:
  type: feedback
---

DXF-y **nie mają nosić śladów biblioteki ezdxf** (sygnatury z [[weryfikacja-ai-dxf]]). Do usunięcia:
`EZDXF` (appid + dimstyle), presety dimstyli `EZ_*` z `setup=True`, oraz metadane `EZDXF_META`
zawierające `CREATED_BY_EZDXF` / `WRITTEN_BY_EZDXF`.

**Rozwiązanie (wbudowane w generatory):** funkcja `_strip_ezdxf(doc)` w `skrypty/gen_*_v2.py`,
wywoływana **tuż przed `doc.saveas(...)`**. Robi (ezdxf 1.4.x):
- `doc._update_ezdxf_metadata = lambda: None` — nie dopisuje `WRITTEN_BY_EZDXF` przy zapisie;
- opakowuje `doc._create_appids` tak, by po utworzeniu appidów usunąć `EZDXF` (zostają `ACAD`,
  `HATCHBACKGROUNDCOLOR`) — appid EZDXF jest dodawany dopiero przy zapisie, więc trzeba go zdjąć w tym haku;
- `meta = doc.rootdict.get("EZDXF_META"); doc.rootdict.discard(...); meta.destroy()` — usuwa słownik
  metadanych **wraz z obiektem** (sam `discard` zostawia osierocony `DICTIONARY` z `CREATED_BY_EZDXF`);
- usuwa dimstyle `EZDXF` i `EZ_*` (repointuje `$DIMSTYLE` na `Standard`, jeśli wskazywał usuwany).

Efekt zweryfikowany: `grep EZDXF` = 0, `doc.audit()` = 0 błędów, encje nienaruszone.

**Why:** projekt oceniany; użytkownik nie chce, by pliki zdradzały wygenerowanie przez ezdxf/kod.

**How to apply:** to **nie zamiast**, lecz **obok** [[czyszczenie-lastsavedby]] — `$LASTSAVEDBY='ezdxf'`
nadal zostaje po zapisie i wymaga skryptu `skrypty/usun_pole_naglowka_dxf.py`. Pełny flow po generacji:
(1) `_strip_ezdxf` robi się sam w generatorze, (2) przepuść wyjście przez `usun_pole_naglowka_dxf.py`.
**NIE ruszać `$ACADVER`** (patrz [[czyszczenie-lastsavedby]]). Kontekst: [[cad-project-context]], reguły: [[dxf-drawing-rules]].

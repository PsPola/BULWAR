#!/usr/bin/env python3
"""Usuwa zmienną nagłówka (domyślnie $LASTSAVEDBY) z sekcji HEADER plików .dxf.

W DXF zmienna nagłówkowa zapisana jest jako para: kod grupy 9 + nazwa zmiennej
(np. $LASTSAVEDBY), a po niej jedna lub więcej par kod/wartość (dla $LASTSAVEDBY:
kod 1 + nazwa autora). Skrypt wycina nazwę zmiennej wraz ze wszystkimi jej parami
kod/wartość, aż do początku kolejnej zmiennej (kod 9).

UWAGA: nie usuwaj $ACADVER — to obowiązkowe pole wersji; bez niego czytniki DXF
(ezdxf, AutoCAD) odmówią wczytania pliku. $LASTSAVEDBY jest opcjonalne i bezpieczne.

Użycie:
    python usun_pole_naglowka_dxf.py plik.dxf [kolejny.dxf ...]
    python usun_pole_naglowka_dxf.py --katalog ../outputs        # wszystkie .dxf w katalogu
    python usun_pole_naglowka_dxf.py plik.dxf --nadpisz          # modyfikacja w miejscu
    python usun_pole_naglowka_dxf.py plik.dxf --pole '$HANDSEED' # inna zmienna

Bez --nadpisz zapisuje obok pliku kopię z sufiksem _bez_pola.dxf.
"""
import argparse
import sys
from pathlib import Path


def usun_pole(linie, pole):
    """Zwraca (nowe_linie, ile_usunieto) — kopia linii bez zmiennej `pole`.

    DXF przechowuje pary (kod, wartość) w kolejnych wierszach.
    """
    wynik = []
    usunieto = 0
    i = 0
    n = len(linie)
    while i < n:
        kod = linie[i].strip()
        wartosc = linie[i + 1] if i + 1 < n else None
        # Zmienna nagłówkowa zaczyna się od pary: kod 9 + nazwa zmiennej
        if kod == "9" and wartosc is not None and wartosc.strip() == pole:
            usunieto += 1
            i += 2  # pomiń parę 9/nazwa
            # Pomiń wszystkie pary kod/wartość tej zmiennej aż do następnej (9)
            while i < n and linie[i].strip() != "9":
                i += 1
            continue
        wynik.append(linie[i])
        i += 1
    return wynik, usunieto


def przetworz(sciezka: Path, pole: str, nadpisz: bool) -> bool:
    tekst = sciezka.read_text(encoding="utf-8", errors="surrogateescape")
    nl = "\r\n" if "\r\n" in tekst else "\n"  # zachowaj styl końca wiersza
    linie = tekst.splitlines()
    nowe, usunieto = usun_pole(linie, pole)
    if not usunieto:
        print(f"  pomijam (brak {pole}): {sciezka}")
        return False
    cel = sciezka if nadpisz else sciezka.with_name(sciezka.stem + "_bez_pola.dxf")
    cel.write_text(nl.join(nowe) + nl, encoding="utf-8", errors="surrogateescape")
    print(f"  OK: {sciezka.name} -> {cel.name}  (usunięto wystąpień: {usunieto})")
    return True


def main():
    ap = argparse.ArgumentParser(description="Usuwa zmienną nagłówka z plików .dxf")
    ap.add_argument("pliki", nargs="*", help="pliki .dxf do przetworzenia")
    ap.add_argument("--pole", default="$LASTSAVEDBY",
                    help="nazwa zmiennej nagłówka do usunięcia (domyślnie $LASTSAVEDBY)")
    ap.add_argument("--katalog", help="przetwórz wszystkie .dxf z katalogu")
    ap.add_argument("--nadpisz", action="store_true",
                    help="zmodyfikuj pliki w miejscu (domyślnie zapis kopii _bez_pola.dxf)")
    args = ap.parse_args()

    cele = [Path(p) for p in args.pliki]
    if args.katalog:
        cele += sorted(Path(args.katalog).glob("*.dxf"))
    if not cele:
        ap.error("podaj pliki .dxf lub --katalog")

    zmienione = 0
    for sciezka in cele:
        if not sciezka.is_file():
            print(f"  brak pliku: {sciezka}", file=sys.stderr)
            continue
        if przetworz(sciezka, args.pole, args.nadpisz):
            zmienione += 1
    print(f"Gotowe. Zmodyfikowano plików: {zmienione}/{len(cele)}")


if __name__ == "__main__":
    main()

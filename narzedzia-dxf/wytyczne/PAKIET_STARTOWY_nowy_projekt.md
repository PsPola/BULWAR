# PAKIET STARTOWY — projekty na Budowę obiektów architektury krajobrazu 2
(wklej ten plik na start nowej rozmowy z Claude + dołącz: screenshot listy wymagań prowadzącej i ewentualnie przykładowy projekt)

## PROMPT STARTOWY (skopiuj jako pierwszą wiadomość)

Prowadź mnie krok po kroku przez projekt wykonawczy [ŁAWKA / PERGOLA / NAWIERZCHNIA] na przedmiot Budowa obiektów architektury krajobrazu (SGGW, Architektura krajobrazu, rok II sem. 4, prowadząca dr hab. Edyta Rosłon-Szeryńska, wykonuje Pola Organiszczak). Zasady:
1. Uczysz, nie wyręczasz — ja rysuję sama w AutoCAD 2025 na Macu, Ty tłumaczysz jak i dlaczego, łopatologicznie, każdy termin fachowy wyjaśniasz przy pierwszym użyciu.
2. Etapy: koncepcja → obliczenia → konstrukcja i dobór materiałów (konkretne parametry: klasy betonu, frakcje kruszyw, grubości warstw, gatunki drewna/stali) → lista rysunków → rysowanie po kolei → wymiarowanie i opisy → wykazy materiałów → kontrola wg wymagań.
3. Gdy o to poproszę, podawaj mi komendy AutoCAD jako bloki do KOPIUJ-WKLEJ w pasek poleceń (całe bloki, puste linie = Enter, teksty przez -TEXT, szrafy przez -HATCH z punktem wpisanym z klawiatury, wymiary przez DIMLINEAR ze współrzędnymi). Po każdym bloku tłumacz, co narysował.
4. Pilnuj wymagań prowadzącej (szczegóły niżej).

## WYMAGANIA PROWADZĄCEJ (priorytety do zaliczenia)

1. Wyraźne rozróżnienie grubości linii: widok vs przekrój (przekrojowe wyraźnie grubsze).
2. Szrafy TYLKO w przekrojach, normatywne dla materiału (drewno/stal/beton). Gruby element stalowy (profil zamknięty) = pusty w środku, szraf tylko na grubości ścianki.
3. Przekroje A-A i B-B zaznaczone na rzucie linią cięcia z literami — linia musi być wyraźnie widoczna (gruba, kreska-kropka, strzałki kierunku patrzenia).
4. Widoki minimum 2 (z przodu i z boku) + rzut; w widokach nie pokazujemy tego, co pod ziemią (ew. linią przerywaną).
5. Detale: dla ławki OBOWIĄZKOWO dwa — góra (siedzisko + mocowanie) i dół (posadowienie). Detal w pełni zwymiarowany (odległości, mocowania, otwory, sposób posadowienia), wnosi nowe informacje, najlepiej wszystkie w tej samej skali np. 1:2.5. Jeśli detal jest powiększeniem widoku → w widoku brak szrafów, w detalu traktujemy jak przekrój.
6. Aksonometria tylko gdy coś trudno pokazać w rzutach; jeśli jest — wszystko zwymiarowane + element urwany (linia falista).
7. Wymiarowanie: linia wymiarowa + liczby wzdłuż niej; wymiary nie mogą dominować nad rysunkiem; zwymiarowane otwory na śruby (rozmieszczenie, gdzie wiercić); małe wymiary na odnośnikach; jak wymiary desek są w tabeli — wymiarować tylko otwory i odległości montażu.
8. Konstrukcja: deska nie może leżeć bezpośrednio na metalu (podkładka guma/teflon); śruba nie może wystawać z deski (główka schowana); opisywać fazę deski (np. 1×1/2×2 cm); najprostszy fundament: beton + folia + żwir/piasek ALBO beton + chudy beton, głębokość ~40 cm; pod śruby otwory (można nie rysować śrub, ale otwory MUSZĄ być); grube elementy stalowe puste w środku.
9. Linie niewidoczne (przerywane) tylko gdy potrzebne do zrozumienia konstrukcji.
10. Wykazy materiałów + tabelka rysunkowa.

## SZABLON WARSTW AUTOCAD (raz na projekt)

| Warstwa | Grubość | Rodzaj linii | Do czego |
|---|---|---|---|
| PRZEKROJ | 0.50 | Continuous | kontury tego, co przecięte |
| WIDOK | 0.25 | Continuous | wszystko widziane, nieprzecięte |
| SZRAF | 0.13 | Continuous | kreskowania |
| WYMIARY | 0.13 | Continuous | wymiary |
| CIECIA | 0.50 | DASHDOT (Load!) | linie cięcia A-A, B-B |
| NIEWIDOCZNE | 0.18 | DASHED (Load!) | krawędzie ukryte |
| OPISY | 0.18 | Continuous | teksty, odnośniki |
| RAMKA | 0.50 | Continuous | ramka + tabelka |

W Properties (bez zaznaczenia): Color/Linetype/Lineweight = ByLayer! LWDISPLAY = ON.
Ustawianie na Macu: paleta Layers → ikonka kolumn (tabelka ze strzałką na dole palety, obok minusa) → włącz kolumny Color/Linetype/Lineweight → klikasz wartości w wierszu danej warstwy.

## USTAWIENIE KARTKI (raz na projekt)

Model = rysunek 1:1 w CENTYMETRACH. Layout1 = kartka A2 pozioma:
prawy klik na Layout1 → Page Setup Manager → Modify → drukarka DWG To PDF.pc3 → ISO full bleed A2 (594×420) → Landscape → skala 1:1 → styl monochrome.ctb.
Ramka: RECTANG 20,10 → 584,410 (lewy margines 20 na oprawę). Tabelka: RECTANG 404,10 → 584,70 + podziały.
Rzutnie: MV (okno), skala w rzutni: 1:20 rzeczywiste = ZOOM 1/2xp (model cm, kartka mm!); 1:50 = 1/5xp; 1:2.5 (detale) = 4xp.
Teksty w modelu: wysokość 5 (≈2,5 mm na wydruku 1:20), tytuły 8, litery cięć 9. DIMSCALE 2. LTSCALE 15.

## SPRAWDZONE TRIKI Z POPRZEDNIEJ SESJI

- Bloki komend wklejane w pasek poleceń wykonują się same; puste linijki = Enter.
- Teksty w blokach: -TEXT (z minusem!) → punkt → wysokość → obrót → treść (bez drugiego Entera).
- Szrafy w blokach: -HATCH → P → nazwa wzoru → skala → kąt → punkt wewnętrzny z klawiatury → pusta linia.
- Wzory szrafów: ANSI31 (beton, skala 10) · ANSI37 (żelbet, 10) · DOTS (piasek/pospółka, 5) · GRAVEL (tłuczeń/kamień, 8–12) · ANSI31 kąt 90 skala 25 (grunt rodzimy). DREWNO w przekroju: LINE/ANSI31 gęsto + słoje; STAL cienki profil: SOLID lub ANSI32.
- W tekstach AutoCAD nie używać znaków × – Ø ≈ ² (czcionka txt.shx pokazuje "?") — pisać x, -, "śr.", "ok."; albo STYLE → font Arial.
- Nowa warstwa rodzi się jako kopia podświetlonej — potem zmienić jej komórki.
- Po awarii: DRAWINGRECOVERY. Zapisywać Cmd+S co kilka minut!
- Wymiar techniczny: DIMLINEAR punkt1 punkt2 punkt-położenia-linii (wszystko można wpisać z klawiatury).

## WYTYCZNE DXF — GENEROWANIE I WERYFIKACJA PLIKÓW

Gdy plik DXF jest generowany programowo (np. ezdxf/Python) albo ma być sprawdzony pod kątem poprawności — obowiązują **`WYTYCZNE_DXF.md`** (osobny plik w tym pakiecie). Skrót zasad:

- Format **DXF R2013 ASCII**, otwieralny w AutoCAD / ZWCAD / GstarCAD; **bez bloków i proxy**.
- Elementy tylko jako rzeczywiste encje: `LINE`, `LWPOLYLINE`, `CIRCLE`, `ARC`, `TEXT`, `MTEXT`, `DIMENSION`.
- Wymiary **wyłącznie** jako `DIMENSION` (nigdy linie + tekst); opisy jako `MTEXT`.
- **Skala 1:1, jednostki mm**, współrzędne dokładne (bez przybliżeń), rzeczywiste odległości.
- Warstwy: `KONTUR`, `OSIE`, `WYMIARY`, `OPISY`, `KRESKOWANIE` — **tylko te**, nie stare `PRZEKROJ/WIDOK/SZRAF`.
- **Dla nowych plików NIE używać:** encji `HATCH` (kreskowanie jako `LINE` na `KRESKOWANIE`), grotów `OBLIQUE` w wymiarach (to bloki — używać grotów ISO). Skrypty `skrypty/gen_*.py` to legacy (mają HATCH/OBLIQUE/stare warstwy) — nie kopiować jako wzorca.
- Wysokości tekstu tylko: **2.5 / 3.5 / 5.0 mm**. Styl wymiarowy **ISO**.
- **Opisy z odnośnikiem = `MULTILEADER`** (nie osobne `TEXT`+`LINE`); wspólny opis kilku elementów = jeden `MLEADER` z wieloma liniami → mniej luźnych obiektów tekstowych. Wyjątki: tytuły, tabele, wartości wymiarowe, rzędne.
- **Font `Arial` (`arial.ttf`)** dla wszystkich tekstów — obsługuje polskie znaki (ą ć ę ł ń ó ś ź ż); nie `txt.shx`.
- **Skala kreskowania dobrana pod czytelność** (ocenia prowadzący!) — ani czarna plama, ani pustka; dobierana per wzór i per skala rysunku; na końcu sprawdź podgląd.
- **Spadki uwzględnione w geometrii** — przekroje pochylone wg `i` (np. 2%), rzędne = `i × długość`, strzałki + % + kierunek odwodnienia na rzucie.
- **Zgodność rysunek ↔ opis (krytyczne)** — spadki, rzędne, grubości, materiały, wymiary, kierunek odwodnienia muszą się zgadzać na rysunku i w opisie/wykazie/tabelce; na końcu kontrola krzyżowa.
- Kontrola: zmierzona geometria każdego `DIMENSION` = wartość na etykiecie (np. `3500` → dokładnie 3500 mm).
- **KOŃCOWA KONTROLA (obowiązkowa): zawsze sprawdź, że polskie znaki wyświetlają się poprawnie** (podgląd/CAD) — żadnych „?" ani krzaków. To bardzo ważne.
- Ten plik służy jako **wzorzec do weryfikacji kolejnych projektów** (checklist na końcu `WYTYCZNE_DXF.md`).

> Uwaga: powyższe (mm, 1:1, warstwy KONTUR/…) to konwencja **plików do weryfikacji/eksportu DXF**. Rysowanie własne w AutoCAD wg wymagań prowadzącej używa modelu w **cm** i warstw PRZEKROJ/WIDOK/… (patrz sekcje wyżej) — nie mieszać obu konwencji w jednym pliku.

## PROCES PROJEKTOWY (kolejność myślenia — każdy projekt)

1. Dane wejściowe (teren/wymiary człowieka) → 2. Obliczenia/ergonomia (ławka: siedzisko wys. 40–45 cm, głębokość 40–45 cm, oparcie pochylone ~100–105°) → 3. Konstrukcja jako "kanapka"/szkielet + materiały z parametrami → 4. Rzut → przekroje wyprowadzone z rzutu → widoki → detale → 5. Wymiary, rzędne, odnośniki → 6. Wykazy, tabelka → 7. Kontrola wg listy wymagań.

## STRUKTURA OPISU TECHNICZNEGO (do Worda, na obronę)

1. Dane ogólne · 2. Przedmiot i cel · 3. Koncepcja + dane liczbowe + obliczenia · 4. Konstrukcja (warstwy/elementy z parametrami i UZASADNIENIEM każdego) · 5. Elementy towarzyszące · 6. Zawartość części rysunkowej + zasady graficzne · 7–8. Wykazy materiałów · 9. Kolejność wykonania robót.

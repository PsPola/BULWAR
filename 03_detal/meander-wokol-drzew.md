# Meander schodów wokół zachowanych drzew — rozmieszczenie i strategia

Na podstawie map z dendrologii (`01_analizy/ksiazeczka-dendrologiczna.pdf`). Data: 2026-07-09.

## GDZIE stoją drzewa (odczyt z map)
- **Północ / górna wschodnia skarpa:** główny ŁUK drzew (nr 1–21) wzdłuż górnej krawędzi skarpy —
  DOKŁADNIE tam, gdzie prowadzimy schody. W tym topola-dominanta nr 12 (korona 14 m) i duże topole
  nr 1, 2, 4 (korony 18–19 m!) oraz pochylone drzewa skarpowe nr 13–21 (korony 6–8,5 m).
- **Linia wody (wschód):** liniowy **pas wierzby wiciowej nr 38** — zakrzewienia nadbrzeżne,
  **siedlisko chronione = NIETYKALNE.**
- **Południowy-wschód:** grupa nr 23–37 (+ wierzba biała) przy istniejących schodach/pochylni,
  na „linii przedłużenia ścieżki".
- **Środek / południe:** otwarta przestrzeń, prawie bez drzew.
- **DO WYCINKI (jedyne):** klon jesionolistny nr **11** (w północnym skupisku) i nr **32** (niżej) — inwazyjny.

## STRATEGIA meandra — 3 sekcje wzdłuż cypla
1. **PÓŁNOC (gęste drzewa + głowica):** meander wije się NAJCIAŚNIEJ — schody + platformy wspornikowe
   przeplatają się między koronami; kaskady w LUKACH między grupami drzew; taras widokowy na głowicy.
   Tu koncepcja „siedzę na stopniu w cieniu drzewa" jest najmocniejsza.
2. **LINIA WODY (pas wierzby 38):** nietykalny — najniższe stopnie i kaskada kończą się LĄDOWO od pasa;
   wierzba zostaje dziką frędzlą nad wodą, na którą patrzysz ze schodów.
3. **POŁUDNIE (otwarcie):** mało drzew → schody mogą być czystsze/geometryczne; dzika łąka rozlewa się
   w pełnym słońcu; **placyk z food truckiem** na styku, w cieniu zachowanej grupy (na suchym gruncie).

## METODA w AutoCAD (dokładna)
1. Na podkładzie narysuj **okręgi rzutów koron** dla drzew nr 1–21 — **średnice masz w tabeli!**
   (kolumna „Średnica korony [m]"). Promień = średnica/2, potem `OFFSET` +1,5 m = bufor SOK (strefa ochrony korzeni).
   Przykłady: topola 12 → korona 14 m → r 7 + 1,5 = 8,5 m; topole 1/2/4 → korony 18–19 m → wielkie kieszenie.
2. Poprowadź **oś schodów jako spline** (`SPLINE`), która **wybrzusza się w głąb skarpy wokół każdego okręgu**
   (drzewa = wypukłe węzły meandra) i wraca ku wodzie między drzewami.
3. Gdzie bieg wchodziłby w okrąg SOK → zamień na **platformę wspornikową / pomost na stopkach** (bez wykopu).
4. **Kaskady** wstaw w przegięcia od strony wody (między drzewami), poza SOK.
5. Wokół każdego pnia zostaw pierścień min. 1,5–2 m bez utwardzenia = kieszeń roślinna (paleta cienisto-zalewowa).

## Food truck
Cień popołudniowy grupy drzew, na suchym gruncie na zachód od skupiska; utwardzenie kończone na linii
rzutu korony; nawierzchnia no-dig; przyłącza poza SOK.

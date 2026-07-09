#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator treści Planszy 1 (Cypel Czerniakowski) — teksty poukładane w siatce B1
+ ramki-placeholdery na zdjęcia/mapy. Output: DXF + podgląd PNG. Autor: Pola Organiszczak."""
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA, MTextEntityAlignment as MA

OUT = "/Users/pspola/Desktop/plansza1_tresci.dxf"
PNG = "/Users/pspola/Desktop/plansza1_tresci_podglad.png"

doc = ezdxf.new("R2013", setup=True)
doc.header["$INSUNITS"] = 4
msp = doc.modelspace()
if "OPIS" not in doc.styles:
    doc.styles.add("OPIS", font="arial.ttf")
for n, c in [("OPISY", 7), ("OBRAZKI", 6), ("POMOC", 8), ("RAMKA", 4)]:
    if n not in doc.layers:
        doc.layers.add(n, color=c)

def rect(x, y, w, h, layer):
    msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h)], close=True, dxfattribs={"layer": layer})

def title(x, y, s, h=6.0):
    t = msp.add_text(s, height=h, dxfattribs={"layer": "OPISY", "style": "OPIS"})
    t.set_placement((x, y), align=TA.TOP_LEFT)

def body(x, y, w, s, h=2.7):
    m = msp.add_mtext(s.replace("\n", r"\P"), dxfattribs={"layer": "OPISY", "style": "OPIS"})
    m.dxf.char_height = h
    m.dxf.width = w
    m.set_location(insert=(x, y), attachment_point=MA.TOP_LEFT)

def img(x, y, w, h, label):
    rect(x, y, w, h, "OBRAZKI")
    msp.add_line((x, y), (x+w, y+h), dxfattribs={"layer": "OBRAZKI"})
    msp.add_line((x, y+h), (x+w, y), dxfattribs={"layer": "OBRAZKI"})
    t = msp.add_text("[ " + label + " ]", height=2.8, dxfattribs={"layer": "OBRAZKI", "style": "OPIS"})
    t.set_placement((x+w/2, y+h/2), align=TA.MIDDLE_CENTER)

# ---- ramka odniesienia (dopasuj do swojej ramki i usuń warstwę POMOC) ----
rect(10, 10, 980, 680, "POMOC")

# ===================== LEWA KOLUMNA =====================
# LOKALIZACJA
title(24, 646, "LOKALIZACJA")
img(24, 556, 284, 82, "mapka Polski / Warszawa + strzalka N")
body(24, 548, 284,
     "Tam, gdzie miasto lapie oddech. Cypel Czerniakowski lezy na lewym brzegu Wisly, wcisniety miedzy Port "
     "Czerniakowski a nurt rzeki - kilka krokow od centrum, a zupelnie inny swiat. To jeden z najdzikszych, "
     "najbogatszych przyrodniczo zakatkow Warszawy: przyroda w pelnym rozkwicie, miejsce dla ludzi i dla natury - "
     "spacery wzdluz wody, obserwacja ptakow, wyciszenie i wypoczynek nad Wisla.\n"
     "Opracowywany odcinek (dl. ok. 400 m) lezy w granicach obszaru Natura 2000 \"Dolina Srodkowej Wisly\" "
     "(PLB140004) - teren cenny przyrodniczo, co wyznacza ramy kazdej ingerencji.\n"
     "Historia: polwysep uformowany miedzy Wisla a Kanalem Portowym, przy dawnym Porcie Czerniakowskim. "
     "Pozostawiony naturze, teren zdzikal i porosl roslinnoscia nadrzeczna - dzis to jeden z najbardziej "
     "naturalnych zakatkow nad Wisla w centrum miasta.")

# PROFIL UZYTKOWNIKOW
title(24, 466, "PROFIL UZYTKOWNIKOW")
img(24, 420, 284, 38, "ikony grup uzytkownikow")
body(24, 412, 284,
     "Przestrzen ogolnodostepna, z ktorej korzysta zroznicowane grono odbiorcow:\n"
     "- rodziny z dziecmi i wedkarze -> bezpieczne strefy przy wodzie;\n"
     "- spacerowicze, takze z psami -> czytelny, ciagly ciag pieszy;\n"
     "- seniorzy -> lawki co ~50 m i miejsca w cieniu;\n"
     "- rowerzysci i osoby aktywne -> tranzytowa trasa rowerowa.\n"
     "Przestrzen musi godzic ruch z wypoczynkiem biernym oraz byc dostepna dla wszystkich - takze dla osob z "
     "niepelnosprawnosciami i rodzicow z wozkami (lagodne pochylnie zamiast schodow).")

# ===================== SRODKOWA KOLUMNA =====================
# ANALIZA KOMUNIKACJI
title(322, 646, "ANALIZA KOMUNIKACJI")
img(322, 556, 340, 82, "mapa komunikacji na podkladzie")
body(322, 548, 340,
     "Glownym ciagiem jest nadwislanska trasa pieszo-rowerowa wzdluz brzegu Wisly - spacerowa i tranzytowa "
     "(element regionalnej trasy rowerowej). Dostep od strony miasta (zachod) oraz od mostu; mozliwy dostep wodny "
     "(przystan, klub wioslarski). Ruch pieszy i rowerowy odbywa sie wspolnie, powiazania w glab cypla sa czytelne. "
     "Sasiedztwo generuje ruch: klub wioslarski, Monta Beach, gastronomia.\n"
     "Wniosek: teren ma duzy potencjal, lecz zagospodarowanie jest niewystarczajace - projekt porzadkuje "
     "nawierzchnie, uzupelnia mala architekture i wprowadza czytelny program stref.")

# POWIAZANIA WIDOKOWE
title(322, 466, "POWIAZANIA WIDOKOWE")
img(322, 418, 150, 42, "plan widokowy")
body(478, 462, 184,
     "Najcenniejsze widoki na wschod (nurt Wisly, naturalny brzeg). Na polnocy dominanta - Stadion Narodowy. "
     "Najgorsze od poludnia (Most Lazienkowski).\n"
     "Wniosek: wschod eksponowac (tarasy widokowe), most maskowac zielenia, pierwsze plany porzadkowac.")

# PODZIALKA + ROZA WIATROW
title(322, 340, "SKALA I ORIENTACJA", 5.0)
# podzialka liniowa 1:500 -> 100 mm = 50 m
bx, by = 322, 318
for i in range(5):
    if i % 2 == 0:
        rect(bx + i*20, by, 20, 4, "OPISY")
msp.add_lwpolyline([(bx, by), (bx+100, by), (bx+100, by+4), (bx, by+4)], close=True, dxfattribs={"layer": "OPISY"})
for i, v in enumerate(["0", "10", "20", "30", "40", "50"]):
    t = msp.add_text(v, height=2.5, dxfattribs={"layer": "OPISY", "style": "OPIS"})
    t.set_placement((bx + i*20, by-2), align=TA.TOP_CENTER)
t = msp.add_text("1:500  [m]", height=2.8, dxfattribs={"layer": "OPISY", "style": "OPIS"})
t.set_placement((bx, by+9), align=TA.BOTTOM_LEFT)
# roza wiatrow (strzalka N)
nx, ny = 500, 315
msp.add_line((nx, ny), (nx, ny+22), dxfattribs={"layer": "OPISY"})
msp.add_line((nx, ny+22), (nx-3, ny+16), dxfattribs={"layer": "OPISY"})
msp.add_line((nx, ny+22), (nx+3, ny+16), dxfattribs={"layer": "OPISY"})
t = msp.add_text("N", height=5, dxfattribs={"layer": "OPISY", "style": "OPIS"})
t.set_placement((nx, ny+24), align=TA.BOTTOM_CENTER)

# ===================== PRAWA KOLUMNA =====================
# DENDROLOGIA
title(674, 646, "ANALIZA DENDROLOGICZNA")
img(674, 548, 310, 90, "mapa inwentaryzacji drzew (X = wycinka)")
body(674, 540, 310,
     "Przewazaja gatunki rodzime (ok. 95%) - leg wierzbowo-topolowy (siedlisko priorytetowe UE). Dominuje topola "
     "biala (ok. 84%), obok wierzb (krucha, biala, wiciowa).\n"
     "DO ZACHOWANIA: cenny leg, topola nr 12 (dominanta), nadbrzezny pas wierzby wiciowej nr 38 (chroniony), "
     "drzewa na skarpie nr 13-21 (stabilizuja brzeg).\n"
     "DO USUNIECIA (X): klon jesionolistny nr 11 i 32 (inwazyjny); samosiewy w strefie schodow (kolizja "
     "konstrukcyjna); drzewa niebezpieczne nr 3 i 10 (pochylone, uszkodzone).")

# LINIJKA SLONCA
title(674, 466, "NASLONECZNIENIE (LINIJKA SLONCA)")
img(674, 410, 310, 48, "diagram zacienienia lato / zima")
body(674, 402, 310,
     "Drzewa - a wiec i cien - skupione sa tylko w polnocnej czesci cypla. Wieksza czesc terenu jest silnie "
     "naslonecziona przez caly dzien i sezon.\n"
     "Wniosek: warunki sprzyjaja roslinom swiatlolubnym na calej dlugosci cypla; strefy wypoczynku wymagaja "
     "zacienienia (pergole, zielen wysoka), zwlaszcza w poludnie latem.")

# ===================== DOLNY PAS =====================
# DOKUMENTACJA FOTOGRAFICZNA
title(24, 288, "DOKUMENTACJA FOTOGRAFICZNA - STAN ISTNIEJACY")
for i in range(4):
    img(24 + i*118, 196, 108, 84, "foto " + str(i+1))
body(24, 188, 474,
     "Widok 1 - betonowe nabrzeze i promenada (kierunek: poludnie, Most Lazienkowski). "
     "Widok 2 - dzika laka nadrzeczna i trasa pieszo-rowerowa (wschod, Wisla / Saska Kepa). "
     "Widok 3 - istniejace schody / pochylnia przy klubie wioslarskim (wschod). "
     "Teren dzis: zdegradowane nabrzeze, bujna dzika roslinnosc, pozostalosci infrastruktury - miejsce zywe, ale "
     "nieuporzadkowane, z duzym potencjalem.")

# WNIOSKI Z ANALIZ
title(510, 288, "WNIOSKI Z ANALIZ")
body(510, 278, 474,
     "- Teren silnie naslonecziony, cien tylko na polnocy -> wprowadzic strefy zacienione (pergole, zielen wysoka).\n"
     "- Okresowe zalewy Wisly -> strefy przy wodzie projektowac jako zalewowe, z roslinnoscia znoszaca podtopienia.\n"
     "- Wycinka samosiewow w strefie schodow (kolizja konstrukcyjna) oraz gatunkow inwazyjnych (klon jesionolistny).\n"
     "- Cenny leg wierzbowo-topolowy (Natura 2000) do zachowania - projektujemy \"z Wisla, a nie przeciw niej\".\n"
     "- Najlepsze widoki na wschod (Wisla, Saska Kepa) -> eksponowac; Most Lazienkowski od poludnia -> maskowac.\n"
     "- Zly stan nawierzchni i uboga mala architektura -> uporzadkowac teren i uzupelnic program rekreacyjny.",
     h=3.0)

doc.saveas(OUT)
print("OK zapisano", OUT)
print("encje:", sorted({e.dxftype() for e in msp}))

# podglad PNG
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    Frontend(RenderContext(doc), MatplotlibBackend(ax)).draw_layout(msp, finalize=True)
    fig.savefig(PNG, dpi=130)
    print("OK podglad", PNG)
except Exception as e:
    print("podglad blad:", e)

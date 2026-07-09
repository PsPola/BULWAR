# -*- coding: utf-8 -*-
"""
PROJEKT NAWIERZCHNI OGRODOWYCH — projekt wykonawczy, arkusz A1 (1:100 i 1:10)
Model w cm, ramka A1 przeskalowana x10 (841x594 mm -> 8410x5940 cm).

RZUT Z GORY = PLAN ZAGOSPODAROWANIA DZIALKI 12 x 33 m (skala 1:100), wg szkicu
inwestora (dzialka 103/1). Uklad nawierzchni w ksztalcie litery "L" wokol domu:
  - PODJAZD (kostka betonowa) 12 x 3 m przy ulicy, furtka + brama
  - SCIEZKA (plyta bazaltowa w trawie) szer. 1 m, prowadzaca wzdluz i nad domem
  - PODEST (kostka granitowa) 4 x 3 m w gornej czesci ogrodu
  - SCHODKI TERENOWE (beton C25/30) laczace sciezke z podestem

Trzy przekroje warstwowe (skala 1:10, lokalny mnoznik S=10):
  A-A  przez PODJAZD  (kostka bet. | obrzeze | trawnik)
  B-B  przez SCIEZKE  (trawnik | plyta bazalt. 1 m | trawnik)
  C-C  przez PODEST i SCHODKI (kostka granit. + betonowe stopnie)

Uzupelnienia merytoryczne: legenda materialow, opis techniczny (uwagi),
bilans powierzchni (zestawienie terenu), wykaz i specyfikacja materialow.

Szrafy (pakiet startowy ezdxf): ANSI31=beton/kostka, ANSI37=kamien/granit,
DOTS=piasek, GRAVEL=zwir/tluczen, ANSI31 kat 90 sk.25 = grunt rodzimy.
"""
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA
import math

doc = ezdxf.new("R2010", setup=True)
doc.header["$INSUNITS"] = 5      # cm
doc.header["$LTSCALE"] = 8.0
doc.header["$MEASUREMENT"] = 1
msp = doc.modelspace()

doc.styles.add("ARIAL", font="arial.ttf")

# --- WARSTWY ---
for name, color, lt, lw in [
    ("PRZEKROJ",     7, "Continuous", 50),
    ("WIDOK",        7, "Continuous", 25),
    ("SZRAF",        8, "Continuous", 13),
    ("WYMIARY",      8, "Continuous", 13),
    ("CIECIA",       1, "DASHDOT",    50),
    ("NIEWIDOCZNE",  8, "DASHED",     18),
    ("OPISY",        7, "Continuous", 18),
    ("RAMKA",        7, "Continuous", 50),
    ("OSIE",         8, "DASHDOT",    13),
    ("OTOCZENIE",    8, "Continuous", 13),
    ("DZIALKA",      8, "DASHED",     25),   # linia rozgraniczajaca dzialke
    ("BUDYNEK",      7, "Continuous", 40),   # obrys budynku
    ("ZIELEN",       3, "Continuous", 18),   # drzewa / krzewy
    ("OBRZEZE",      6, "Continuous", 35),   # obrzeza / oporniki
    ("DYLAT",        1, "DASHED",     18),   # dylatacje
    ("ODWODN",       5, "Continuous", 30),   # odwodnienie liniowe
]:
    doc.layers.add(name, color=color, linetype=lt, lineweight=lw)

# --- STYLE WYMIAROWANIA ---
dst = doc.dimstyles.duplicate_entry("EZDXF", "WYM")
for k, v in dict(dimtxt=9, dimasz=6, dimtsz=4, dimexo=3, dimexe=4, dimgap=2,
                 dimdec=1, dimzin=8, dimtad=1, dimscale=1, dimlfac=1).items():
    dst.set_dxf_attrib(k, v)
dst.dxf.dimtxsty = "ARIAL"
dsd = doc.dimstyles.duplicate_entry("WYM", "WYMDET")
for k, v in dict(dimtxt=30, dimasz=20, dimexo=10, dimexe=16, dimgap=6,
                 dimlfac=0.1).items():
    dsd.set_dxf_attrib(k, v)
# WYMM - wymiary rzutu w metrach; model w cm, skala 1:100 (PS=1.0) -> dimlfac = 0.01
dsm = doc.dimstyles.duplicate_entry("WYM", "WYMM")
for k, v in dict(dimtxt=42, dimasz=28, dimexo=10, dimexe=16, dimgap=8,
                 dimdec=2, dimlfac=0.01).items():
    dsm.set_dxf_attrib(k, v)

# ================= POMOCNICZE =================
def line(x1, y1, x2, y2, layer, ox=0, oy=0):
    msp.add_line((ox+x1, oy+y1), (ox+x2, oy+y2), dxfattribs={"layer": layer})

def rect(x, y, w, h, layer, ox=0, oy=0):
    msp.add_lwpolyline([(ox+x, oy+y), (ox+x+w, oy+y), (ox+x+w, oy+y+h), (ox+x, oy+y+h)],
                       close=True, dxfattribs={"layer": layer})

def poly(pts, layer, ox=0, oy=0, close=True):
    msp.add_lwpolyline([(ox+p[0], oy+p[1]) for p in pts], close=close,
                       dxfattribs={"layer": layer})

def hrect(x, y, w, h, pattern="ANSI31", scale=3.0, angle=45.0, ox=0, oy=0):
    h_ = msp.add_hatch(dxfattribs={"layer": "SZRAF"})
    if pattern == "SOLID":
        h_.set_solid_fill(color=7)
    else:
        h_.set_pattern_fill(pattern, scale=scale, angle=angle)
    h_.paths.add_polyline_path([(ox+x, oy+y), (ox+x+w, oy+y), (ox+x+w, oy+y+h),
                                (ox+x, oy+y+h)], is_closed=True)

def hpoly(pts, pattern="ANSI31", scale=3.0, angle=45.0, ox=0, oy=0):
    h_ = msp.add_hatch(dxfattribs={"layer": "SZRAF"})
    if pattern == "SOLID":
        h_.set_solid_fill(color=7)
    else:
        h_.set_pattern_fill(pattern, scale=scale, angle=angle)
    h_.paths.add_polyline_path([(ox+p[0], oy+p[1]) for p in pts], is_closed=True)

def text(s, x, y, h=8, layer="OPISY", align=TA.LEFT, rot=0, ox=0, oy=0):
    t = msp.add_text(s, dxfattribs={"height": h, "layer": layer, "style": "ARIAL",
                                    "rotation": rot})
    t.set_placement((ox+x, oy+y), align=align)

def hdim(x1, x2, y, off, ox=0, oy=0, style="WYM"):
    d = msp.add_linear_dim(base=(ox+x1, oy+y+off), p1=(ox+x1, oy+y), p2=(ox+x2, oy+y),
                           angle=0, dimstyle=style, dxfattribs={"layer": "WYMIARY"})
    d.render()

def vdim(y1, y2, x, off, ox=0, oy=0, style="WYM"):
    d = msp.add_linear_dim(base=(ox+x+off, oy+y1), p1=(ox+x, oy+y1), p2=(ox+x, oy+y2),
                           angle=90, dimstyle=style, dxfattribs={"layer": "WYMIARY"})
    d.render()

def ddim(p1, p2, base, angle=0):
    d = msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angle, dimstyle="WYMDET",
                           dxfattribs={"layer": "WYMIARY"})
    d.render()

def leader(pts, txt, th=7, ox=0, oy=0, talign=TA.LEFT):
    msp.add_lwpolyline([(ox+p[0], oy+p[1]) for p in pts], close=False,
                       dxfattribs={"layer": "OPISY"})
    e = pts[-1]
    dx = 3 if talign == TA.LEFT else -3
    text(txt, e[0]+dx, e[1]+2, th, "OPISY", talign, ox=ox, oy=oy)

def title(s, x, y, ox=0, oy=0, h=13):
    text(s, x, y, h, "OPISY", TA.LEFT, ox=ox, oy=oy)

def arrow(x, y, ang, layer="CIECIA", L=14, W=6, ox=0, oy=0):
    a = math.radians(ang)
    tip = (ox+x, oy+y)
    b1 = (tip[0]-L*math.cos(a)+W/2*math.sin(a), tip[1]-L*math.sin(a)-W/2*math.cos(a))
    b2 = (tip[0]-L*math.cos(a)-W/2*math.sin(a), tip[1]-L*math.sin(a)+W/2*math.cos(a))
    msp.add_solid([b1, b2, tip], dxfattribs={"layer": layer})

def wavy(x0, y0, x1, y1, n=6, amp=3, layer="PRZEKROJ", ox=0, oy=0):
    pts = []
    for i in range(n*4+1):
        t = i/(n*4)
        px = x0+(x1-x0)*t; py = y0+(y1-y0)*t
        dx = x1-x0; dy = y1-y0; L = math.hypot(dx, dy) or 1
        o = amp*math.sin(t*math.pi*n)
        pts.append((px - dy/L*o, py + dx/L*o))
    msp.add_lwpolyline([(ox+p[0], oy+p[1]) for p in pts], dxfattribs={"layer": layer})

def spot(x, y, val, ox=0, oy=0, h=16):
    """Rzedna wysokosciowa - trojkat + wartosc."""
    s = 14
    msp.add_solid([(ox+x, oy+y), (ox+x-s, oy+y+s*1.4), (ox+x+s, oy+y+s*1.4)],
                  dxfattribs={"layer": "OPISY"})
    text(val, x+s+6, y+s, h, "OPISY", TA.LEFT, ox=ox, oy=oy)

def spadek(x, y, ang, ox=0, oy=0, L=90, txt="i=2%"):
    """Strzalka spadku nawierzchni."""
    a = math.radians(ang)
    x2 = x + L*math.cos(a); y2 = y + L*math.sin(a)
    line(x, y, x2, y2, "OPISY", ox, oy)
    arrow(x2, y2, ang, "OPISY", 22, 10, ox, oy)
    text(txt, x+L*0.2, y+18, 14, "OPISY", TA.LEFT, ox=ox, oy=oy)

# ================= MATERIALY / WARSTWY PRZEKROJOW =================
MAT = dict(
    kostka_betonowa=("ANSI31", 3, 45),
    kostka_granit=("ANSI37", 3, 90),
    plyta_bazalt=("ANSI37", 4, 45),
    piasek=("DOTS", 5, 0),
    zwir=("GRAVEL", 8, 0),
    tluczen=("GRAVEL", 14, 0),
    pospolka=("DOTS", 10, 45),
    beton_mono=("ANSI31", 6, 45),
    humus=("ANSI31", 10, 135),
    grunt=("ANSI31", 25, 90),
)

# stopnie schodow terenowych
STOPIEN_H, STOPIEN_T = 15.0, 33.0
S = 10.0   # lokalny mnoznik przekrojow -> efekt 1:10

LAY_PODJAZD = [
    (8,  "kostka_betonowa", "kostka brukowa betonowa 20x10x8 cm"),
    (3,  "piasek",  "podsypka - piasek plukany f.0-2 mm"),
    (15, "zwir",    "podbudowa gorna - kruszywo lamane 0-31,5 mm"),
    (20, "tluczen", "podbudowa dolna - tluczen f.31,5-63 mm"),
    (10, "pospolka","warstwa odsaczajaca - pospolka f.0-16 mm"),
]
LAY_SCIEZKA = [
    (4,  "plyta_bazalt", "plyta bazaltowa nieregularna Ø40-60 cm"),
    (3,  "piasek", "podsypka - piasek plukany f.0-2 mm"),
    (10, "zwir",   "podbudowa - kruszywo lamane f.0-31,5 mm"),
]
LAY_PODEST = [
    (5,  "kostka_granit", "kostka brukowa granitowa 5x5x5 cm"),
    (5,  "piasek",  "podsypka - piasek plukany f.0-2 mm"),
    (5,  "zwir",    "podbudowa gorna - kruszywo lamane 0-31,5 mm"),
    (15, "tluczen", "podbudowa dolna - tluczen f.31,5-63 mm"),
    (6,  "pospolka","warstwa odsaczajaca - pospolka f.0-16 mm"),
]
LAY_TRAWNIK = [
    (20, "humus", "ziemia urodzajna (humus) + trawa z siewu"),
]

# ---- pomocnicze przekrojow (mnoznik S) ----
def dr(cx, cy, x, y, w, h, layer): rect(cx+x*S, cy+y*S, w*S, h*S, layer)
def dh(cx, cy, x, y, w, h, pat, sc, ang=45): hrect(cx+x*S, cy+y*S, w*S, h*S, pat, sc, ang)
def dl(cx, cy, x1, y1, x2, y2, layer): line(cx+x1*S, cy+y1*S, cx+x2*S, cy+y2*S, layer)
def dtext(cx, cy, x, y, s, h=26, align=TA.LEFT):
    text(s, cx+x*S, cy+y*S, h, "OPISY", align)
def dleader(cx, cy, pts, s, h=26, talign=TA.LEFT):
    sx, sy = pts[0]; ex, ey = pts[-1]
    leader([(cx+sx*S, cy+sy*S), (cx+ex*S, cy+ey*S)], s, h, talign=talign)

def stack(cx, cy, x0, width, layers):
    """rysuje warstwy w dol od y=0 (poziom nawierzchni); zwraca (y_dol, info)."""
    y = 0.0; info = []
    for g, mkey, opis in layers:
        pat, sc, ang = MAT[mkey]
        dr(cx, cy, x0, y-g, width, g, "PRZEKROJ")
        dh(cx, cy, x0, y-g, width, g, pat, sc, ang)
        info.append((y, y-g, opis, g))
        y -= g
    return y, info

def grunt_rodzimy(cx, cy, x0, width, y_top, depth=12):
    dr(cx, cy, x0, y_top-depth, width, depth, "PRZEKROJ")
    dh(cx, cy, x0, y_top-depth, width, depth, *MAT["grunt"])
    wavy(cx+x0*S, cy+(y_top-depth)*S, cx+(x0+width)*S, cy+(y_top-depth)*S, 5, 4, "PRZEKROJ")

def obrzeze(cx, cy, x_center, h=20, w=6, law_w=22, law_h=12):
    """Obrzeze betonowe zaglebione, gora +2 cm, na lawie betonowej z oporem."""
    top = 2.0
    dr(cx, cy, x_center-w/2, top-h, w, h, "PRZEKROJ")
    dh(cx, cy, x_center-w/2, top-h, w, h, *MAT["kostka_betonowa"])
    dr(cx, cy, x_center-law_w/2, top-h-law_h, law_w, law_h, "PRZEKROJ")
    dh(cx, cy, x_center-law_w/2, top-h-law_h, law_w, law_h, *MAT["beton_mono"])

def opis_kolumna(cx, cy, x, y_start, info, krok=4.4):
    yy = y_start
    for y_t, y_b, opis, g in info:
        text("%g cm - %s" % (g, opis), cx+x*S, cy+yy*S, 26, "OPISY")
        yy -= krok

def wym_warstw(cx, cy, xd, info, kier=1):
    for y_t, y_b, opis, g in info:
        ddim((cx+xd*S, cy+y_t*S), (cx+xd*S, cy+y_b*S), (cx+(xd+8*kier)*S, cy+y_t*S), 90)

# ================= PRZEKROJE =================
def przekroj(ox, oy, nazwa, left_layers, right_layers, left_lbl, right_lbl,
             total_w=400.0):
    """Przekroj z obrzezem na styku dwoch nawierzchni/stref."""
    cx, cy = ox, oy
    half = total_w/2
    dl(cx, cy, -half-20, 0, half+20, 0, "WIDOK")
    yL, infoL = stack(cx, cy, -half, half, left_layers)
    yR, infoR = stack(cx, cy, 0, half, right_layers)
    depthL, depthR = -yL, -yR
    ybase = min(yL, yR)
    grunt_rodzimy(cx, cy, -half-15, total_w+30, ybase, depth=12)
    for x0s, ys in [(-half, yL), (0.0, yR)]:      # dopelnienie gruntu pod plytsza strona
        if ys - ybase > 0.5:
            dr(cx, cy, x0s, ybase, half, ys-ybase, "PRZEKROJ")
            dh(cx, cy, x0s, ybase, half, ys-ybase, *MAT["grunt"])
    obrzeze(cx, cy, 0)
    wym_warstw(cx, cy, -half-25, infoL, kier=-1)
    wym_warstw(cx, cy, half+25, infoR, kier=+1)
    text(left_lbl, cx+(-half)*S, cy+(-depthL-26)*S, 32, "OPISY")
    opis_kolumna(cx, cy, -half, -depthL-40, infoL)
    text(right_lbl, cx+(2)*S, cy+(-depthR-26)*S, 32, "OPISY")
    opis_kolumna(cx, cy, 2, -depthR-40, infoR)
    text("grunt rodzimy - zageszczony i wyrownany do Is>=0,97",
         cx+(-half-10)*S, cy+(ybase-20)*S, 26, "OPISY")
    title("Przekrój %s   skala 1:10" % nazwa, cx+(-half-25)*S, cy+24*S, h=46)

def przekroj_sciezka(ox, oy, nazwa="B-B'"):
    """Sciezka 1 m (plyta bazaltowa) w trawniku - trawnik | plyta | trawnik."""
    cx, cy = ox, oy
    pw, gw = 100.0, 90.0
    total = pw + 2*gw
    dl(cx, cy, -total/2, 0, total/2, 0, "WIDOK")
    yGL, _ = stack(cx, cy, -pw/2-gw, gw, LAY_TRAWNIK)
    yGR, _ = stack(cx, cy, pw/2, gw, LAY_TRAWNIK)
    yS, infoS = stack(cx, cy, -pw/2, pw, LAY_SCIEZKA)
    ybase = min(yGL, yGR, yS)
    grunt_rodzimy(cx, cy, -total/2-10, total+20, ybase, depth=12)
    for x0s, ww, ys in [(-pw/2-gw, gw, yGL), (-pw/2, pw, yS), (pw/2, gw, yGR)]:
        if ys - ybase > 0.5:
            dr(cx, cy, x0s, ybase, ww, ys-ybase, "PRZEKROJ")
            dh(cx, cy, x0s, ybase, ww, ys-ybase, *MAT["grunt"])
    obrzeze(cx, cy, -pw/2); obrzeze(cx, cy, pw/2)
    wym_warstw(cx, cy, pw/2+gw+10, infoS, kier=+1)
    ddim((cx+(-pw/2)*S, cy+5*S), (cx+(pw/2)*S, cy+5*S), (cx+(-pw/2)*S, cy+13*S))
    text("trawnik", cx+(-pw/2-gw+8)*S, cy+11*S, 26, "OPISY")
    text("trawnik", cx+(pw/2+18)*S, cy+11*S, 26, "OPISY")
    xlbl = -total/2
    text("SCIEZKA 1 m - plyta bazaltowa w trawie", cx+xlbl*S, cy+(-42)*S, 32, "OPISY")
    opis_kolumna(cx, cy, xlbl, -54, infoS)
    text("trawnik: humus 20 cm + trawa z siewu", cx+xlbl*S, cy+(-78)*S, 26, "OPISY")
    text("grunt rodzimy - zageszczony i wyrownany", cx+xlbl*S, cy+(-90)*S, 26, "OPISY")
    title("Przekrój %s   skala 1:10" % nazwa, cx+(-total/2-5)*S, cy+24*S, h=46)

def przekroj_CC(ox, oy):
    """Podest (kostka granit.) + schodki terenowe: 2 stopnie betonu monolitycznego."""
    cx, cy = ox, oy
    half = 100.0
    dl(cx, cy, -half-20, 0, 0, 0, "WIDOK")
    yL, infoL = stack(cx, cy, -half, half, LAY_PODEST)
    grunt_rodzimy(cx, cy, -half-15, half+15, yL, depth=12)
    wym_warstw(cx, cy, -half-25, infoL, kier=-1)
    text("PODEST - kostka granitowa", cx+(-half)*S, cy+(-(-yL)-26)*S, 32, "OPISY")
    opis_kolumna(cx, cy, -half, -(-yL)-40, infoL)

    t, h = STOPIEN_T, STOPIEN_H
    beton_pts = [(0, 0), (t, 0), (t, -h), (2*t, -h), (2*t, -2*h),
                 (2*t, -2*h-15), (t, -h-15), (0, -15)]
    dl(cx, cy, 0, 0, t, 0, "PRZEKROJ"); dl(cx, cy, t, 0, t, -h, "PRZEKROJ")
    dl(cx, cy, t, -h, 2*t, -h, "PRZEKROJ"); dl(cx, cy, 2*t, -h, 2*t, -2*h, "PRZEKROJ")
    hpoly([(cx+p[0]*S, cy+p[1]*S) for p in beton_pts], *MAT["beton_mono"])
    poly([(cx+p[0]*S, cy+p[1]*S) for p in beton_pts], "PRZEKROJ")
    grunt_rodzimy(cx, cy, 0, 2*t+15, -2*h-15, depth=12)
    ddim((cx+(2*t+15)*S, cy+0*S), (cx+(2*t+15)*S, cy+(-h)*S), (cx+(2*t+25)*S, cy+0*S), 90)
    ddim((cx+(2*t+15)*S, cy+(-h)*S), (cx+(2*t+15)*S, cy+(-2*h)*S), (cx+(2*t+25)*S, cy+(-h)*S), 90)
    ddim((cx+0*S, cy+3*S), (cx+t*S, cy+3*S), (cx+0*S, cy+8*S))
    ddim((cx+t*S, cy+3*S), (cx+2*t*S, cy+3*S), (cx+t*S, cy+8*S))
    dleader(cx, cy, [(2*t+2, -h-5), (2*t+22, -h-30)], "beton C25/30, zatarty,")
    dtext(cx, cy, 2*t+22, -h-30-5, "spadek 1-2% na stopniu")
    dleader(cx, cy, [(t, -2*h-8), (t+22, -2*h-40)], "siatka zbrojeniowa Ø6 #150 w plycie stopnia")
    text("SCHODKI TERENOWE - stopien 15/33 cm, beton monolityczny C25/30",
         cx+(-half)*S, cy+(-2*h-80)*S, 32, "OPISY")
    title("Przekrój C-C'   skala 1:10", cx+(-half-25)*S, cy+24*S, h=46)

# ================= DETAL STYKU NAWIERZCHNI (1:10) =================
def detal_styk(ox, oy):
    """Typowe polaczenie dwoch roznych nawierzchni: kostka betonowa (podjazd) |
    obrzeze/opornik na lawie betonowej z oporem + dylatacja | plyta bazaltowa
    (sciezka). Spadki i=2% odprowadzajace wode od styku."""
    cx, cy = ox, oy
    wA, wB, obw = 95.0, 95.0, 8.0
    layA = [(8, "kostka_betonowa"), (3, "piasek"), (15, "zwir")]
    layB = [(4, "plyta_bazalt"), (3, "piasek"), (15, "zwir")]

    def buildup(x0, w, lay):
        y = 0.0
        for g, m in lay:
            pat, sc, ang = MAT[m]
            dr(cx, cy, x0, y-g, w, g, "PRZEKROJ")
            dh(cx, cy, x0, y-g, w, g, pat, sc, ang)
            y -= g
        return y
    yA = buildup(-obw/2-wA, wA, layA)
    yB = buildup(obw/2, wB, layB)

    # obrzeze/opornik betonowy 8x30, gora +2 cm, na lawie betonowej z oporem
    obh = 30.0
    dr(cx, cy, -obw/2, 2-obh, obw, obh, "PRZEKROJ")
    dh(cx, cy, -obw/2, 2-obh, obw, obh, *MAT["beton_mono"])
    dr(cx, cy, -20, 2-obh-14, 40, 14, "PRZEKROJ")            # lawa
    dh(cx, cy, -20, 2-obh-14, 40, 14, *MAT["beton_mono"])
    poly([(cx+(obw/2)*S, cy+(2-obh)*S), (cx+(obw/2+12)*S, cy+(2-obh)*S),
          (cx+(obw/2)*S, cy+(2-obh+12)*S)], "PRZEKROJ")       # opor (haunch)

    ybase = min(yA, yB, 2-obh-14)
    grunt_rodzimy(cx, cy, -obw/2-wA-8, wA+wB+obw+16, ybase, 12)
    for x0s, ww, ys in [(-obw/2-wA, wA, yA), (obw/2, wB, yB)]:
        if ys - ybase > 0.5:
            dr(cx, cy, x0s, ybase, ww, ys-ybase, "PRZEKROJ")
            dh(cx, cy, x0s, ybase, ww, ys-ybase, *MAT["grunt"])

    dl(cx, cy, -obw/2-wA, 0, -obw/2, 0, "WIDOK")
    dl(cx, cy, obw/2, 0, obw/2+wB, 0, "WIDOK")
    # dylatacja - szczelina na styku (kit trwale plastyczny)
    dl(cx, cy, -obw/2, 2, -obw/2, -obh, "DYLAT")
    dl(cx, cy, obw/2, 2, obw/2, -obh, "DYLAT")
    # spadki (sam podpis i=2%, bez zbednych grotow)
    text("i=2%", cx+(-obw/2-wA*0.75)*S, cy+11*S, 26, "OPISY")
    text("i=2%", cx+(obw/2+wB*0.3)*S, cy+11*S, 26, "OPISY")

    dleader(cx, cy, [(0, 3), (42, 36)], "obrzeze/opornik betonowy 8x30 cm (gora +2 cm)")
    dleader(cx, cy, [(0, 2-obh-7), (48, -54)], "lawa betonowa C12/15 z oporem")
    dleader(cx, cy, [(-obw/2, -14), (-44, -48)], "dylatacja - kit trwale plastyczny", talign=TA.RIGHT)
    dleader(cx, cy, [(-obw/2-wA*0.5, -4), (-obw/2-wA-6, 30)], "kostka betonowa - podjazd", talign=TA.RIGHT)
    dleader(cx, cy, [(obw/2+wB*0.5, -2), (obw/2+wB+6, 30)], "plyta bazaltowa - sciezka")
    title("DETAL 1 - polaczenie nawierzchni (obrzeze na lawie z oporem)   skala 1:10",
          cx+(-obw/2-wA-8)*S, cy+24*S, h=46)

# ================= RZUT Z GORY - PLAN ZAGOSPODAROWANIA DZIALKI (1:100) =================
# Geometria dzialki w cm (1 jednostka = 1 cm, rzut 1:100). Origin (0,0) = lewy dolny
# rog przy ulicy. Dzialka: x 0..1200 (front 12 m), y 0..3300 (glebokosc 33 m).
DZ_W, DZ_H = 1200.0, 3300.0

PS = 1.0   # skala rzutu 1:100 (model w cm, ramka A1 x10)

def plan_dzialki(ox, oy):
    def L(x1, y1, x2, y2, layer): line(x1*PS, y1*PS, x2*PS, y2*PS, layer, ox, oy)
    def Rf(x, y, w, h, layer): rect(x*PS, y*PS, w*PS, h*PS, layer, ox, oy)
    def T(s, x, y, h=26, align=TA.LEFT, rot=0, layer="OPISY"):
        text(s, x*PS, y*PS, h, layer, align, rot, ox, oy)
    def H(x, y, w, h, pat, sc, ang=45): hrect(x*PS, y*PS, w*PS, h*PS, pat, sc, ang, ox, oy)
    def Arr(x, y, ang, layer="CIECIA", Ln=45, Wd=20): arrow(x*PS, y*PS, ang, layer, Ln, Wd, ox, oy)
    def Spot(x, y, val, h=22): spot(x*PS, y*PS, val, ox, oy, h)
    def Spadek(x, y, ang, Ln, txt): spadek(x*PS, y*PS, ang, ox, oy, Ln, txt)
    def Lead(pts, txt, th=24): leader([(p[0]*PS, p[1]*PS) for p in pts], txt, th, ox, oy)
    def Vdim(y1, y2, x, off): vdim(y1*PS, y2*PS, x*PS, off, ox, oy, "WYMM")
    def Hdim(x1, x2, y, off): hdim(x1*PS, x2*PS, y*PS, off, ox, oy, "WYMM")
    def drzewo(cx, cy, r):
        msp.add_circle((ox+cx*PS, oy+cy*PS), r*PS, dxfattribs={"layer": "ZIELEN"})
        msp.add_circle((ox+cx*PS, oy+cy*PS), r*PS*0.28, dxfattribs={"layer": "ZIELEN"})
    def krzew(cx, cy, r=32):
        msp.add_circle((ox+cx*PS, oy+cy*PS), r*PS, dxfattribs={"layer": "ZIELEN"})

    # --- granica dzialki + trawnik (tlo) ---
    Rf(0, 0, DZ_W, DZ_H, "DZIALKA")
    T("granica dzialki  (dz. nr 103/1)", 20, DZ_H-55, 28)

    # --- ULICA + furtka/brama ---
    H(-260, -260, DZ_W+520, 260, "ANSI31", 60, 45)
    T("ul. Ogrodowa", DZ_W/2, -170, 40, TA.CENTER)
    L(100, 0, 240, 0, "PRZEKROJ"); T("furtka", 90, 35, 24)
    L(650, 0, 1100, 0, "PRZEKROJ"); T("brama", 820, 35, 24)

    # --- 1. PODJAZD  12 x 3 m  (kostka betonowa) ---
    Rf(0, 0, 1200, 300, "WIDOK")
    H(0, 0, 1200, 300, "ANSI31", 16, 45)
    T("PODJAZD", 250, 205, 34)
    T("kostka betonowa 12 × 3 m", 250, 150, 24)
    Spadek(600, 55, 90, 120, "i=2% do korytka")

    # --- DOM 7 x 15 m (+ garaz) ---
    Rf(500, 300, 700, 1500, "BUDYNEK")
    H(500, 300, 700, 1500, "ANSI31", 45, 45)
    T("DOM", 780, 1155, 46)
    T("7 × 15 m", 780, 1075, 30)
    Rf(800, 300, 400, 300, "BUDYNEK")
    T("GARAŻ", 940, 430, 28)
    T("parter +0,45", 700, 900, 24)
    Arr(500, 420, 180, "OPISY", 30, 14)
    T("wejscie glowne", 520, 475, 24)

    # --- 2. SCIEZKA 1 m  (plyta bazaltowa)  uklad L ---
    for (sx, sy, sw, sh) in [(400, 300, 100, 1600), (500, 1800, 700, 100)]:
        Rf(sx, sy, sw, sh, "WIDOK")
        H(sx, sy, sw, sh, "DOTS", 8, 0)
    T("SCIEZKA - plyta bazaltowa, szer. 1 m", 250, 1100, 26, TA.LEFT, 90)

    # --- SCHODKI TERENOWE (beton) - wzdluz wschodniej granicy do podestu ---
    Rf(1100, 1900, 100, 1100, "WIDOK")
    H(1100, 1900, 100, 1100, "ANSI31", 16, 135)
    for i in range(1, 8):                      # kreski stopni
        yy = 1900 + i*1100/8
        L(1100, yy, 1200, yy, "WIDOK")
    T("SCHODKI TERENOWE - beton C25/30", 1255, 2050, 24, TA.LEFT, 90)

    # --- 3. PODEST 4 x 3 m (kostka granitowa) ---
    Rf(800, 3000, 400, 300, "WIDOK")
    H(800, 3000, 400, 300, "ANSI37", 16, 90)
    T("PODEST", 1000, 3205, 30, TA.CENTER)
    T("granit 4 × 3 m", 1000, 3120, 24, TA.CENTER)
    Spot(825, 3035, "+0,30", 22)

    # --- TRAWNIK + zielen ---
    T("TRAWNIK", 600, 2300, 40)
    drzewo(300, 2750, 130)
    T("drzewo ozdobne", 300, 2555, 22, TA.CENTER)
    for (kx, ky) in [(180, 2200), (700, 2700), (250, 3050), (620, 3050), (170, 1500)]:
        krzew(kx, ky, 40)

    # --- POLACZENIA NAWIERZCHNI (zgodnie ze sztuka) ---
    # obrzeza / oporniki na lawie z oporem - wszystkie krawedzie nawierzchni segmentowych
    for a, b, c, d in [(0, 300, 400, 300), (0, 0, 0, 300), (1200, 0, 1200, 300),
                       (400, 300, 400, 1900), (500, 1900, 1100, 1900),
                       (1100, 1900, 1100, 3000), (800, 3000, 1100, 3000),
                       (800, 3000, 800, 3300)]:
        L(a, b, c, d, "OBRZEZE")
    Lead([(180, 300), (100, 660)], "obrzeze bet. 50x20x6 na lawie C12/15 z oporem")
    # odwodnienie liniowe przed garazem i wejsciem (przechwytuje splyw z podjazdu)
    Rf(520, 283, 660, 17, "ODWODN"); H(520, 283, 660, 17, "ANSI37", 8, 0)
    Lead([(700, 291), (770, 205)], "odwodnienie liniowe (korytko z rusztem)")
    # dylatacje na styku nawierzchni z budynkiem (+ spadek od sciany)
    for a, b, c, d in [(500, 300, 1200, 300), (500, 300, 500, 1800),
                       (500, 1800, 1200, 1800)]:
        L(a, b, c, d, "DYLAT")
    Lead([(500, 850), (140, 850)], "dylatacja + spadek od budynku (tasma)")

    # --- ODWODNIENIE: rozsaczanie powierzchniowe na trawniku (opcja przyjeta) ---
    Spot(520, 315, "±0,00", 22)
    Spadek(480, 950, 180, 90, "i=2%")      # sciezka pionowa -> trawnik (W)
    Spadek(760, 1840, 90, 80, "i=2%")      # sciezka pozioma -> trawnik (N)
    Spadek(830, 3120, 180, 90, "i=2%")     # podest -> trawnik (W)
    T("rozsaczanie powierzchniowe", 420, 2210, 24)
    T("na trawniku (pow. biol. czynna)", 420, 2150, 22)

    # --- LINIE CIEC ---
    def ciecie_v(x, y0, y1, litera):
        L(x, y0, x, y1, "CIECIA")
        Arr(x, y1, 90, "CIECIA", 45, 20)
        Arr(x, y0, 270, "CIECIA", 45, 20)
        T(litera, x, y1+35, 40, TA.CENTER)
        T(litera+"'", x, y0-90, 40, TA.CENTER)
    def ciecie_h(y, x0, x1, litera):
        L(x0, y, x1, y, "CIECIA")
        Arr(x1, y, 0, "CIECIA", 45, 20)
        Arr(x0, y, 180, "CIECIA", 45, 20)
        T(litera, x0-95, y-15, 40, TA.CENTER)
        T(litera+"'", x1+70, y-15, 40, TA.CENTER)
    ciecie_v(250, -70, 380, "A")           # przez podjazd
    ciecie_h(1000, 250, 650, "B")          # przez sciezke pionowa
    ciecie_v(1150, 2650, 3360, "C")        # przez schodki i podest

    # --- WYMIARY ---
    Vdim(0, 300, 0, -170)       # podjazd 3 m
    Vdim(300, 1800, 0, -170)    # dom 15 m
    Vdim(1800, 3300, 0, -170)   # gora 15 m
    Vdim(0, 3300, DZ_W, 340)    # caly bok 33 m
    Hdim(0, 1200, 0, -400)      # front 12 m
    Hdim(0, 500, 1800, 110)     # korytarz 5 m
    Hdim(500, 1200, 1800, 110)  # dom 7 m

    # --- kierunek polnocy ---
    nx, ny = DZ_W+250, DZ_H-150
    L(nx, ny, nx, ny+220, "OTOCZENIE")
    Arr(nx, ny+220, 90, "OTOCZENIE", 60, 32)
    T("N", nx, ny+270, 44, TA.CENTER)

    # --- PODZIALKA LINIOWA (odniesienie miary niezalezne od skali druku) ---
    sby = DZ_H + 95
    for i in range(5):
        Rf(i*100, sby, 100, 24, "OPISY")
        if i % 2 == 0:
            H(i*100, sby, 100, 24, "SOLID", 1, 0)
    for i in range(6):
        T(str(i), i*100, sby-52, 22, TA.CENTER)
    T("m", 560, sby-4, 22)
    T("podzialka liniowa 1:100 (dzialki co 1 m)", 40, sby+38, 22)

    title("RZUT Z GÓRY — PLAN ZAGOSPODAROWANIA DZIAŁKI 12 × 33 m   skala 1:100",
          -60*PS, (DZ_H+260)*PS, ox, oy, h=46)

# ================= LEGENDA / OPIS / BILANS =================
def legenda(x0, y0):
    items = [
        ("kostka_betonowa", "kostka betonowa (podjazd)"),
        ("kostka_granit",   "kostka granitowa (podest)"),
        ("plyta_bazalt",    "plyta bazaltowa (sciezka)"),
        ("beton_mono",      "beton C25/30 (schodki, lawy)"),
        ("piasek",          "podsypka piaskowa"),
        ("zwir",            "kruszywo lamane / zwir"),
        ("tluczen",         "tluczen (podbudowa dolna)"),
        ("pospolka",        "pospolka (w-wa odsaczajaca)"),
        ("humus",           "ziemia urodzajna / trawnik"),
        ("grunt",           "grunt rodzimy"),
    ]
    # legenda pozioma (dolny pasek arkusza): materialy 2 rzedy x 5 + oznaczenia z prawej
    text("LEGENDA MATERIALOW", x0, y0, 30, "OPISY")
    sw, sh, colw, rowh = 95, 58, 620, 105
    for i, (mkey, lbl) in enumerate(items):
        col, row = i % 5, i // 5
        xx = x0 + col*colw; yy = y0 - 80 - row*rowh
        pat, sc, ang = MAT[mkey]
        rect(xx, yy, sw, sh, "OPISY")
        hrect(xx, yy, sw, sh, pat, sc, ang)
        text(lbl, xx+sw+22, yy+16, 22, "OPISY")
    # oznaczenia (obrzeza, dylatacje, odwodnienie, linie ciec) - z prawej strony
    x2 = x0 + 5*colw + 40
    text("OZNACZENIA", x2, y0, 30, "OPISY")
    ozn = [("OBRZEZE", "obrzeze / opornik na lawie z oporem"),
           ("DYLAT",   "dylatacja (styk z budynkiem)"),
           ("ODWODN",  "odwodnienie liniowe (korytko z rusztem)"),
           ("CIECIA",  "linia przekroju A-A / B-B / C-C")]
    for i, (lay, lbl) in enumerate(ozn):
        yy = y0 - 80 - i*72
        if lay == "ODWODN":
            rect(x2, yy, 95, 42, "ODWODN"); hrect(x2, yy, 95, 42, "ANSI37", 8, 0)
        else:
            line(x2, yy+22, x2+95, yy+22, lay)
        text(lbl, x2+118, yy+8, 22, "OPISY")

def opis_techniczny(x0, y0):
    text("OPIS TECHNICZNY / UWAGI", x0, y0, 32, "OPISY")
    linie = [
        "1. Poziom parteru +0,45 m = rzedna odniesienia. Nawierzchnie ze spadkiem 1,5-2% od budynku (patrz strzalki spadku).",
        "2. POLACZENIA NAWIERZCHNI: wszystkie krawedzie nawierzchni segmentowych (kostka, plyty) ujete w obrzeze/opornik",
        "    betonowy 50x20x6 cm na lawie betonowej C12/15 z oporem - zabezpieczenie przed rozjezdzaniem (patrz Detal 1).",
        "3. Styk dwoch roznych nawierzchni - wspolne obrzeze na lawie z oporem; gora obrzeza +2 cm lub licowana.",
        "4. Styk nawierzchni z budynkiem - dylatacja (tasma dylatacyjna / kit trwale plastyczny), bez sztywnego polaczenia,",
        "    spadek odprowadzajacy wode od sciany; przed garazem i wejsciem - odwodnienie liniowe (korytko z rusztem).",
        "5. Podbudowy ukladac i zageszczac warstwami gr. <=20 cm; Is: podjazd >=0,98, ciagi piesze >=0,97.",
        "6. Kostke ukladac na podsypce piaskowej, spoiny 3-5 mm wypelnic piaskiem plukanym, zawibrowac; plyty bazaltowe",
        "    na podsypce, spoiny trawiaste, obrzeze przy trawniku ukryte (mijankowe do koszenia).",
        "7. Schodki terenowe - beton C25/30 zbrojony siatka Ø6 #150; dylatacje co ok. 5 m; nawierzchnia zatarta.",
        "8. Odwodnienie: spadki nawierzchni 1,5-2% na przylegle tereny zielone - rozsaczanie powierzchniowe na trawniku",
        "    (pow. biol. czynna 209 m2). Podjazd -> korytko liniowe -> wylot i rozsaczanie na dzialce. BEZ odprowadzania",
        "    wod na dzialki sasiednie (art. 234 Prawa wodnego).",
        "9. Materialy wg norm: PN-EN 1338 (kostka bet.), 1340 (obrzeza), 1342 (kostka kam.), PN-EN 206 (beton).",
        "10. Wymiary: rzut w metrach, przekroje i detale w cm. Sprawdzic w naturze przed realizacja.",
    ]
    for i, s in enumerate(linie):
        text(s, x0, y0-60-i*62, 22, "OPISY")

def bilans(x0, y0):
    text("BILANS POWIERZCHNI (zestawienie terenu)", x0, y0, 32, "OPISY")
    rows = [
        ("Powierzchnia dzialki (12 × 33 m)", "396,0 m²", "100 %"),
        ("Zabudowa (dom + garaz, 7 × 15 m)", "105,0 m²", "26,5 %"),
        ("Nawierzchnie utwardzone razem", "82,0 m²", "20,7 %"),
        ("   - podjazd (kostka betonowa)", "36,0 m²", ""),
        ("   - sciezka (plyta bazaltowa 1 m)", "23,0 m²", ""),
        ("   - podest (kostka granitowa)", "12,0 m²", ""),
        ("   - schodki terenowe (beton)", "11,0 m²", ""),
        ("Powierzchnia biologicznie czynna (zielen)", "209,0 m²", "52,8 %"),
    ]
    rh = 68.0; wc = [1620, 430, 320]
    for i in range(len(rows)+1):
        line(x0, y0-48-i*rh, x0+sum(wc), y0-48-i*rh, "OPISY")
    xx = x0
    for w in [0]+wc:
        xx += w; line(xx, y0-48, xx, y0-48-len(rows)*rh, "OPISY")
    for i, r in enumerate(rows):
        cx_ = x0
        for j, cell in enumerate(r):
            text(cell, cx_+18, y0-48-(i+1)*rh+22, 23, "OPISY")
            cx_ += wc[j]

# ================= RAMKA, TABELKA, WYKAZ =================
SHW, SHH = 8410.0, 5940.0
def ramka():
    rect(0, 0, SHW, SHH, "RAMKA")
    rect(140, 70, SHW-140-70, SHH-70-70, "RAMKA")

def tabelka():
    x0, y0, x1, y1 = SHW-70-1500, 70, SHW-70, 600
    rect(x0, y0, x1-x0, y1-y0, "RAMKA")
    line(x0, y0+210, x1, y0+210, "RAMKA")
    line(x0+760, y0+210, x0+760, y1, "RAMKA")
    line(x0+380, y0, x0+380, y0+210, "RAMKA")
    line(x0+760, y0, x0+760, y0+210, "RAMKA")
    line(x0+1150, y0, x0+1150, y0+210, "RAMKA")
    line(x0, y0+105, x0+760, y0+105, "RAMKA")
    t = 23
    text("Kierunek: Architektura krajobrazu", x0+26, y1-56, t)
    text("WBiIŚ SGGW", x0+26, y1-100, t)
    text("Rok II, sem. 4, rok akad. 2025/2026", x0+26, y1-144, t)
    text("Przedmiot: Budowa obiektów arch. krajobrazu 2", x0+786, y1-56, t)
    text("Temat: projekt wykonawczy nawierzchni ogrodowych", x0+786, y1-100, t)
    text("Branża: architektura krajobrazu   Etap: nawierzchnie", x0+786, y1-144, t)
    text("Wykonał: Pola Organiszczak", x0+26, y0+128, t)
    text("Sprawdził:", x0+786, y0+128, t)
    text("Skala:", x0+26, y0+62, t)
    text("1:100 i 1:10", x0+26, y0+22, t)
    text("Data:", x0+400, y0+62, t)
    text("Ocena:", x0+786, y0+62, t)
    text("Uwagi:", x0+1170, y0+62, t)

def wykazy(x0, y0):
    rh = 66.0
    w = [80, 780, 170, 180, 220]
    W = sum(w)
    rows = [
        ("Lp.", "Rodzaj materiału", "Jedn.", "Ilość*", "Norma"),
        ("1", "Kostka brukowa betonowa 20x10x8 cm (podjazd)", "m2", "36,0", "PN-EN 1338"),
        ("2", "Płyta bazaltowa nieregularna Ø40-60 cm (ścieżka)", "m2", "23,0", "-"),
        ("3", "Kostka brukowa granitowa 5x5x5 cm (podest)", "m2", "12,0", "PN-EN 1342"),
        ("4", "Beton C25/30 (schodki, monolit)", "m3", "1,6", "PN-EN 206"),
        ("5", "Obrzeże betonowe 50x20x6 cm", "mb", "92", "PN-EN 1340"),
        ("6", "Ława fundamentowa - beton C12/15", "m3", "1,4", "PN-EN 206"),
        ("7", "Piasek płukany f.0-2 mm (podsypka)", "m3", "4,0", "PN-EN 13043"),
        ("8", "Kruszywo łamane f.0-31,5 mm (podbudowa)", "m3", "7,5", "PN-EN 13242"),
        ("9", "Tłuczeń f.31,5-63 mm (podbudowa dolna)", "m3", "9,0", "-"),
        ("10", "Pospółka f.0-16 mm (odsączająca)", "m3", "3,5", "-"),
        ("11", "Ziemia urodzajna (humus) gr. 20 cm", "m3", "42,0", "-"),
        ("12", "Siatka zbrojeniowa Ø6 #150 (schodki)", "m2", "11,0", "-"),
        ("13", "Korytko odwodnienia liniowego z rusztem", "mb", "7,0", "PN-EN 1433"),
        ("14", "Taśma dylatacyjna / kit trwale plastyczny", "mb", "35,0", "-"),
    ]
    text("WYKAZ I SPECYFIKACJA MATERIAŁÓW", x0, y0+len(rows)*rh+80, 32)
    text("*ilości szacunkowe - do potwierdzenia obmiarem po rysunkach warsztatowych",
         x0, y0+len(rows)*rh+42, 20)
    for i in range(len(rows)+1):
        line(x0, y0+i*rh, x0+W, y0+i*rh, "OPISY")
    xx = x0
    for wi in [0]+w:
        xx += wi; line(xx, y0, xx, y0+len(rows)*rh, "OPISY")
    for ri, r in enumerate(reversed(rows)):
        cx_ = x0
        for ci, cell in enumerate(r):
            text(cell, cx_+16, y0+ri*rh+18, 23)
            cx_ += w[ci]

# ============================================================
# ZLOZENIE ARKUSZA
# ============================================================
ramka()
tabelka()

# RZUT (plan dzialki 1:100) - lewa kolumna
plan_dzialki(650, 1250)

# PRZEKROJE - srodkowa kolumna, jeden pod drugim
przekroj(4150, 5150, "A-A'", LAY_PODJAZD, LAY_TRAWNIK,
         "PODJAZD - kostka betonowa", "TRAWNIK", total_w=200.0)
przekroj_sciezka(4150, 3500, "B-B'")
przekroj_CC(4150, 1850)

# Prawa kolumna: wykaz, opis techniczny, bilans, detal
wykazy(5720, 4680)
opis_techniczny(5720, 4560)
bilans(5720, 3500)
detal_styk(6750, 2200)

# LEGENDA + OZNACZENIA - poziomy pasek na dole arkusza
legenda(2850, 470)

doc.set_modelspace_vport(height=6200, center=(SHW/2, SHH/2))
doc.saveas("outputs/nawierzchnia.dxf")
print("OK, zapisano DXF")

from ezdxf.addons.drawing import matplotlib as mpl_draw
mpl_draw.qsave(msp, "outputs/nawierzchnia_preview.png",
               size_inches=(33.1, 23.4), dpi=180, bg="#FFFFFF")
print("OK, podglad")

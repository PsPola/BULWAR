#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Projekt wykonawczy: schody ogrodowe z murkiem gabionowym — Pola Organiszczak.
Rysunek 1:1 w cm. Arkusz A1 poziomo przy wydruku 1:20 (1682 x 1188 jednostek)."""
import math
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

doc = ezdxf.new("R2018", setup=True)
msp = doc.modelspace()

LAYERS = [
    ("PRZEKROJ", 7, "Continuous", 50),
    ("WIDOK", 7, "Continuous", 25),
    ("SZRAF", 7, "Continuous", 13),
    ("WYMIARY", 7, "Continuous", 13),
    ("CIECIA", 7, "DASHDOT", 50),
    ("NIEWIDOCZNE", 7, "DASHED", 18),
    ("OPISY", 7, "Continuous", 18),
    ("RAMKA", 7, "Continuous", 50),
]
for name, color, lt, lw in LAYERS:
    doc.layers.add(name, color=color, linetype=lt, lineweight=lw)

H_TITLE = 10; H_SUB = 7; H_TXT = 5.5; H_DIM = 5; H_TAB = 5.5

def line(p1, p2, layer="WIDOK"):
    return msp.add_line(p1, p2, dxfattribs={"layer": layer})

def pline(pts, layer="WIDOK", closed=False):
    return msp.add_lwpolyline(pts, dxfattribs={"layer": layer}, close=closed)

def txt(s, pos, h=H_TXT, layer="OPISY", align=TA.MIDDLE_CENTER, rot=0):
    t = msp.add_text(s, dxfattribs={"layer": layer, "height": h, "rotation": rot})
    t.set_placement(pos, align=align)
    return t

def circle(c, r, layer="SZRAF"):
    return msp.add_circle(c, r, dxfattribs={"layer": layer})

def hatch(pts, pattern="ANSI31", scale=8.0, angle=0.0, layer="SZRAF"):
    h = msp.add_hatch(dxfattribs={"layer": layer})
    h.set_pattern_fill(pattern, scale=scale, angle=angle)
    h.paths.add_polyline_path(pts, is_closed=True)
    return h

def tick(x, y, layer="WYMIARY"):
    line((x - 1.8, y - 1.8), (x + 1.8, y + 1.8), layer)

def dim_h(x1, x2, y, label=None, ext_from=None, txt_above=True):
    line((x1, y), (x2, y), "WYMIARY")
    tick(x1, y); tick(x2, y)
    if ext_from is not None:
        for x in (x1, x2):
            line((x, ext_from), (x, y + (3 if y > ext_from else -3)), "WYMIARY")
    label = label if label is not None else f"{abs(x2 - x1):g}"
    ty = y + 3.5 if txt_above else y - 3.5
    txt(label, ((x1 + x2) / 2, ty), H_DIM, "WYMIARY",
        TA.BOTTOM_CENTER if txt_above else TA.TOP_CENTER)

def dim_v(y1, y2, x, label=None, ext_from=None):
    line((x, y1), (x, y2), "WYMIARY")
    tick(x, y1); tick(x, y2)
    if ext_from is not None:
        for y in (y1, y2):
            line((ext_from, y), (x + (3 if x > ext_from else -3), y), "WYMIARY")
    label = label if label is not None else f"{abs(y2 - y1):g}"
    t = msp.add_text(label, dxfattribs={"layer": "WYMIARY", "height": H_DIM, "rotation": 90})
    t.set_placement((x + 3.5, (y1 + y2) / 2), align=TA.TOP_CENTER)

def arrowhead(tip, ang_deg, size=6, layer="OPISY"):
    a = math.radians(ang_deg)
    for da in (math.radians(155), math.radians(-155)):
        line(tip, (tip[0] + size * math.cos(a + da), tip[1] + size * math.sin(a + da)), layer)

def arrow(p1, p2, layer="OPISY"):
    line(p1, p2, layer)
    ang = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
    arrowhead(p2, ang, layer=layer)

def wavy(p1, p2, amp=3.0, waves=6, layer="WIDOK"):
    x1, y1 = p1; x2, y2 = p2
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    pts = []
    n = waves * 8
    for i in range(n + 1):
        t = i / n
        off = amp * math.sin(t * waves * 2 * math.pi)
        pts.append((x1 + ux * t * L + nx * off, y1 + uy * t * L + ny * off))
    pline(pts, layer)

def leader(p_from, p_to, text_lines, h=4.8):
    line(p_from, p_to, "OPISY")
    line(p_to, (p_to[0] + 6, p_to[1]), "OPISY")
    circle(p_from, 0.8, "OPISY")
    for i, s in enumerate(text_lines):
        txt(s, (p_to[0] + 9, p_to[1] - i * (h + 2.2)), h, "OPISY", TA.MIDDLE_LEFT)

def stones(x1, y1, x2, y2, r=3.2, dx=11, dy=10, layer="SZRAF"):
    row = 0
    y = y1 + dy / 2
    while y < y2 - r + 1:
        x = x1 + dx / 2 + (dx / 2 if row % 2 else 0)
        while x < x2 - r + 1:
            circle((x, y), r, layer)
            x += dx
        y += dy
        row += 1

def dots(x1, y1, x2, y2, dx=6, dy=4, r=0.5, layer="SZRAF"):
    row = 0
    y = y1 + dy / 2
    while y < y2:
        x = x1 + dx / 2 + (dx / 2 if row % 2 else 0)
        while x < x2:
            circle((x, y), r, layer)
            x += dx
        y += dy; row += 1

def triangles(x1, y1, x2, y2, s=4.5, dx=10, dy=7, layer="SZRAF"):
    row = 0
    y = y1 + dy / 2
    while y + s / 2 < y2:
        x = x1 + dx / 2 + (dx / 2 if row % 2 else 0)
        while x + s / 2 < x2:
            pline([(x - s / 2, y - s / 3), (x, y + s / 2), (x + s / 2, y - s / 3)], layer)
            x += dx
        y += dy; row += 1

# ============ GEOMETRIA ============
RISERS = [0, 35, 70, 235, 270, 305]
TOPS   = [15, 30, 45, 60, 75, 90]
LTOT = 305; W = 120; MW = 50

def step_profile(x_end=LTOT):
    pts = []
    z = 0
    for i, xr in enumerate(RISERS):
        pts.append((xr, z))
        z = TOPS[i]
        pts.append((xr, z))
    pts.append((x_end, z))
    return pts

# ================= RAMKA =================
SW, SH = 1682, 1188
pline([(0, 0), (SW, 0), (SW, SH), (0, SH)], "RAMKA", closed=True)
pline([(15, 15), (SW - 15, 15), (SW - 15, SH - 15), (15, SH - 15)], "RAMKA", closed=True)

# ================= 1. RZUT Z GORY =================
RX, RY = 150, 800
def R(x, y): return (RX + x, RY + y)

pline([R(0, 0), R(LTOT, 0), R(LTOT, W), R(0, W)], "WIDOK", closed=True)
for x in [35, 70, 235, 270]:
    line(R(x, 0), R(x, W), "WIDOK")
pline([R(5, W), R(305, W), R(305, W + MW), R(5, W + MW)], "WIDOK", closed=True)
for x in [105, 205]:
    line(R(x, W), R(x, W + MW), "WIDOK")
stones(RX + 5, RY + W, RX + 305, RY + W + MW, r=3.0, dx=13, dy=12)

# wymiary koszy nad murkiem
dim_h(RX + 5, RX + 105, RY + W + MW + 12, "100", ext_from=RY + W + MW)
dim_h(RX + 105, RX + 205, RY + W + MW + 12, "100")
dim_h(RX + 205, RX + 305, RY + W + MW + 12, "100", ext_from=RY + W + MW)
# rzedne gory koszy
txt("góra koszy: +0.50", R(45, W + MW + 26), 4.5, "WYMIARY")
txt("+1.00", R(178, W + MW + 26), 4.5, "WYMIARY")
txt("+1.00", R(255, W + MW + 26), 4.5, "WYMIARY")
txt("MUREK Z GABIONÓW (kosze 100×50×50 cm)", R(152, W + MW + 40), H_TXT, "OPISY")

treads = [(0, 35, "+0.15"), (35, 70, "+0.30"), (70, 235, "+0.45  SPOCZNIK"),
          (235, 270, "+0.60"), (270, 305, "+0.75")]
for x1, x2, s in treads:
    xm = (x1 + x2) / 2
    txt(s, R(xm, 78), 4.5, "WYMIARY")
    arrow(R(xm + 8, 40), R(xm - 8, 40), "OPISY")
    txt("1%", R(xm, 31), 4, "OPISY")
txt("DÓŁ (niższy)  ±0.00", R(-52, 90), H_TXT, "OPISY")
txt("GÓRA (wyższy)  +0.90", R(LTOT + 55, 90), H_TXT, "OPISY")

arrow(R(60, -64), R(245, -64), "OPISY")
txt("kierunek wejścia (w górę)", R(152, -73), H_TXT, "OPISY")

# linie ciecia
line(R(-30, 60), R(LTOT + 30, 60), "CIECIA")
arrowhead(R(-30, 60), 90, 7, "CIECIA"); arrowhead(R(LTOT + 30, 60), 90, 7, "CIECIA")
txt("B", R(-38, 60), 9, "OPISY"); txt("B'", R(LTOT + 40, 60), 9, "OPISY")
line(R(150, -42), R(150, W + MW + 18), "CIECIA")
arrowhead(R(150, -42), 0, 7, "CIECIA"); arrowhead(R(150, W + MW + 18), 0, 7, "CIECIA")
txt("A", R(150, -51), 9, "OPISY"); txt("A'", R(140, W + MW + 26), 9, "OPISY")

dim_h(RX, RX + 35, RY - 18, "35", ext_from=RY)
dim_h(RX + 35, RX + 70, RY - 18, "35")
dim_h(RX + 70, RX + 235, RY - 18, "165", ext_from=RY)
dim_h(RX + 235, RX + 270, RY - 18, "35", ext_from=RY)
dim_h(RX + 270, RX + 305, RY - 18, "35", ext_from=RY)
line((RX, RY - 34), (RX + LTOT, RY - 34), "WYMIARY")
tick(RX, RY - 34); tick(RX + LTOT, RY - 34)
line((RX, RY), (RX, RY - 37), "WYMIARY"); line((RX + LTOT, RY), (RX + LTOT, RY - 37), "WYMIARY")
txt("całkowita długość 305", (RX + 78, RY - 30.5), H_DIM, "WYMIARY", TA.BOTTOM_CENTER)
dim_v(RY, RY + W, RX - 18, "120", ext_from=RX)
dim_v(RY + W, RY + W + MW, RX - 18, "50", ext_from=RX + 5)
txt("bieg 1 – 3 stopnie (3 × 15 × 35 cm)", R(40, -88), H_TXT, "OPISY")
txt("bieg 2 – 3 stopnie (3 × 15 × 35 cm)", R(262, -88), H_TXT, "OPISY")
txt("Rzut z góry    skala 1:20", R(152, W + MW + 66), H_TITLE, "OPISY")

# ================= 2. PRZEKROJ B-B' =================
BX, BY = 1000, 840
def B(x, z): return (BX + x, BY + z)

prof = step_profile()
def BP(pts, dz=0.0):
    return [B(x, z + dz) for (x, z) in pts]

# murek za przekrojem (widok) — tylko czesci widoczne ponad schodami
line(B(5, 15), B(5, 50), "WIDOK")
line(B(5, 50), B(105, 50), "WIDOK")
line(B(105, 45), B(105, 100), "WIDOK")
line(B(105, 100), B(305, 100), "WIDOK")
line(B(305, 90), B(305, 100), "WIDOK")
line(B(105, 50), B(235, 50), "WIDOK")   # spoina pozioma koszy (widoczna nad spocznikiem)
line(B(205, 50), B(205, 100), "WIDOK")  # spoina pionowa kosz 2/3
txt("murek z gabionów za przekrojem (widok)", B(150, 108), 4.5, "OPISY")

# kontury warstw (0.5)
pline(BP(prof), "PRZEKROJ")
pline(BP(prof, -12), "PRZEKROJ")
pline(BP(prof, -42), "PRZEKROJ")
pline(BP(prof, -50), "PRZEKROJ")
pline(BP(prof, -65), "PRZEKROJ")
line(B(0, 0), B(0, -65), "PRZEKROJ")
line(B(LTOT, 78), B(LTOT, 90), "PRZEKROJ")
line(B(LTOT, 78), B(LTOT, 25), "PRZEKROJ")
line(B(-55, 0), B(0, 0), "PRZEKROJ")
line(B(LTOT, 90), B(LTOT + 55, 90), "PRZEKROJ")
wavy(B(-55, 8), B(-55, -60), 2.5, 4, "WIDOK")
wavy(B(LTOT + 55, 98), B(LTOT + 55, 30), 2.5, 4, "WIDOK")

def poly_between(top, bot):
    return top + bot[::-1]

hatch(poly_between(BP(prof), BP(prof, -12)), "ANSI31", 3.5, 0)
hatch(poly_between(BP(prof, -12), BP(prof, -42)), "ANSI37", 6, 0)
segs = [(0, 35, 15), (35, 70, 30), (70, 235, 45), (235, 270, 60), (270, 305, 75)]
for x1, x2, zt in segs:
    dots(BX + x1, BY + zt - 50, BX + x2, BY + zt - 42)
    triangles(BX + x1, BY + zt - 65, BX + x2, BY + zt - 50)
hatch([B(-55, 0), B(0, 0), B(0, -65), B(-55, -60)], "ANSI31", 14, 90)
hatch(BP(prof, -65) + [B(LTOT + 55, 25), B(LTOT + 55, 12), B(0, -78)], "ANSI31", 14, 90)
hatch([B(LTOT, 90), B(LTOT + 55, 90), B(LTOT + 55, 37), B(LTOT, 25)], "ANSI31", 14, 90)
line(B(LTOT, 25), B(LTOT + 55, 37), "WIDOK")

# odnosniki warstw
lx = BX + 372
items = [
    (["12 cm – warstwa ścieralna: beton C20/25 (XF3),",
      "zatarty na szorstko, krawędzie fazowane 1×1 cm"], B(285, 70)),
    (["30 cm – ława fundamentowa: beton C16/20,",
      "siatka zgrzewana 15×15 cm, Ø6 mm"], B(288, 45)),
    (["folia PE 0,2 mm"], B(291, 33)),
    (["8 cm – podsypka: pospółka f. 0–16 mm"], B(294, 29)),
    (["15 cm – podbudowa: tłuczeń f. 31,5–63 mm,",
      "zagęszczony"], B(297, 18)),
    (["grunt rodzimy"], B(300, 2)),
]
ly = BY + 128
for lab, p in items:
    leader(p, (lx, ly), lab, 4.8)
    ly -= (len(lab) * 7 + 9)

for z in [0, 15, 30, 45, 60, 75, 90]:
    s = "±0.00" if z == 0 else f"+0.{z:02d}"
    txt(s, B(-72, z), 4.2, "WYMIARY", TA.MIDDLE_RIGHT)
    line(B(-68, z), B(-60, z), "WYMIARY")
dim_v(BY, BY + 90, BX - 40, "90")
dim_v(BY, BY + 15, BX - 22, "15")
dim_v(BY + 15, BY + 30, BX - 22, "15")
dim_v(BY + 30, BY + 45, BX - 22, "15")
dim_h(BX, BX + 35, BY + 122, "35")
dim_h(BX + 35, BX + 70, BY + 122, "35")
dim_h(BX + 70, BX + 235, BY + 122, "spocznik 165")
dim_h(BX + 235, BX + 270, BY + 122, "35")
dim_h(BX + 270, BX + 305, BY + 122, "35")
dim_h(BX, BX + LTOT, BY - 88, "całkowita długość 305")
txt("B", B(-90, 138), 9, "OPISY"); txt("B'", B(340, 148), 9, "OPISY")
txt("Przekrój B-B'    skala 1:20", B(152, 158), H_TITLE, "OPISY")

# ================= 3. PRZEKROJ A-A' =================
AX, AY = 240, 470
def A(y, z): return (AX + y, AY + z)

zt = 45
pline([A(0, zt), A(120, zt)], "PRZEKROJ")
pline([A(0, zt - 12), A(120, zt - 12)], "PRZEKROJ")
pline([A(0, zt - 42), A(120, zt - 42)], "PRZEKROJ")
pline([A(0, zt - 50), A(110, zt - 50)], "PRZEKROJ")
pline([A(0, zt - 65), A(110, zt - 65)], "PRZEKROJ")
line(A(0, zt), A(0, zt - 65), "PRZEKROJ")
line(A(120, zt), A(120, 0), "PRZEKROJ")
line(A(110, zt - 42), A(110, zt - 65), "PRZEKROJ")
hatch([A(0, zt), A(120, zt), A(120, zt - 12), A(0, zt - 12)], "ANSI31", 3.5, 0)
hatch([A(0, zt - 12), A(120, zt - 12), A(120, zt - 42), A(0, zt - 42)], "ANSI37", 6, 0)
dots(AX, AY + zt - 50, AX + 110, AY + zt - 42)
triangles(AX, AY + zt - 65, AX + 110, AY + zt - 50)

for z in [60, 75, 90]:
    line(A(0, z), A(120, z), "WIDOK")
txt("krawędzie stopni za przekrojem (widok)", A(58, 97), 4.2, "OPISY")

for z1 in [0, 50]:
    pline([A(120, z1), A(170, z1), A(170, z1 + 50), A(120, z1 + 50)], "PRZEKROJ", closed=True)
stones(AX + 120, AY + 0, AX + 170, AY + 100, r=3.4, dx=12, dy=11)
pline([A(110, 0), A(180, 0), A(180, -25), A(110, -25)], "PRZEKROJ", closed=True)
triangles(AX + 110, AY - 25, AX + 180, AY + 0)
pline([A(171.5, 92), A(171.5, -26.5), A(108.5, -26.5)], "NIEWIDOCZNE")
circle(A(181, -14), 5, "PRZEKROJ")
dots(AX + 174, AY - 22, AX + 191, AY - 6, dx=5, dy=4, r=0.7)

line(A(-60, zt), A(0, zt), "PRZEKROJ")
wavy(A(-60, zt + 8), A(-60, zt - 60), 2.5, 4, "WIDOK")
hatch([A(-60, zt), A(0, zt), A(0, zt - 65), A(110, zt - 65), A(110, -25), A(180, -25),
       A(180, -45), A(-60, -45)], "ANSI31", 14, 90)
line(A(170, 90), A(240, 90), "PRZEKROJ")
wavy(A(240, 98), A(240, -38), 2.5, 4, "WIDOK")
hatch([A(170, 90), A(240, 90), A(240, -45), A(180, -45), A(180, -25), A(170, -25)],
      "ANSI31", 14, 90)
txt("grunt rodzimy (skarpa)", A(215, 55), 4.2, "OPISY", rot=90)

lx2 = AX + 278
items2 = [
    (["kosze gabionowe 100×50×50 cm, siatka zgrzewana",
      "oczko 5×10 cm, drut Ø4,5 mm (Galfan)"], A(158, 78)),
    (["kamień łamany f. 80–120 mm (wypełnienie)"], A(150, 62)),
    (["geowłóknina PP 200 g/m², od strony gruntu,",
      "wywinięta pod kosz"], A(171.5, 30)),
    (["drenaż: rura PVC perforowana Ø100 w obsypce",
      "żwirowej 8–16 mm, spadek 0,5–1%"], A(181, -14)),
    (["posadowienie: tłuczeń f. 31,5–63 mm,",
      "zagęszczony, gr. 25 cm"], A(155, -18)),
]
ly2 = AY + 100
for lab, p in items2:
    leader(p, (lx2, ly2), lab, 4.8)
    ly2 -= (len(lab) * 7 + 9)

txt("+0.45", A(-75, zt), 4.2, "WYMIARY", TA.MIDDLE_RIGHT)
line(A(-72, zt), A(-63, zt), "WYMIARY")
txt("+1.00", A(145, 108), 4.2, "WYMIARY")
line(A(132, 104), A(158, 104), "WYMIARY")
txt("+0.90", A(215, 96), 4.2, "WYMIARY")
dim_h(AX, AX + 120, AY - 60, "120")
dim_h(AX + 120, AX + 170, AY - 60, "50")
dim_h(AX + 110, AX + 180, AY - 76, "70 (ława tłuczniowa)")
dim_v(AY, AY + 50, AX + 195, "50")
dim_v(AY + 50, AY + 100, AX + 195, "50")
dim_v(AY - 25, AY + 0, AX + 208, "25")
dim_v(AY + zt - 12, AY + zt, AX - 22, "12")
dim_v(AY + zt - 42, AY + zt - 12, AX - 22, "30")
dim_v(AY + zt - 50, AY + zt - 42, AX - 40, "8")
dim_v(AY + zt - 65, AY + zt - 50, AX - 22, "15")
txt("A", A(-90, 125), 9, "OPISY"); txt("A'", A(255, 125), 9, "OPISY")
txt("Przekrój A-A'    skala 1:20", A(90, 142), H_TITLE, "OPISY")

# ================= 4. WIDOK Z PRZODU =================
FX, FY = 780, 470
def F(y, z): return (FX + y, FY + z)

pline([F(0, 0), F(120, 0), F(120, 15), F(0, 15)], "WIDOK", closed=True)
for z in [30, 45, 60, 75, 90]:
    line(F(0, z), F(120, z), "WIDOK")
line(F(0, 15), F(0, 90), "WIDOK"); line(F(120, 15), F(120, 90), "WIDOK")
line(F(0, 90), F(120, 90), "WIDOK")
pline([F(120, 0), F(170, 0), F(170, 50), F(120, 50)], "WIDOK", closed=True)
pline([F(120, 50), F(170, 50), F(170, 100), F(120, 100)], "WIDOK", closed=True)
txt("2. warstwa koszy (od spocznika, widoczna dalej)", F(150, 110), 4.2, "OPISY")
for y in range(130, 170, 10):
    line(F(y, 0), F(y, 50), "SZRAF")
for z in range(10, 50, 10):
    line(F(120, z), F(170, z), "SZRAF")
stones(FX + 120, FY, FX + 170, FY + 50, r=3.2, dx=13, dy=12)
line(F(-40, 0), F(0, 0), "WIDOK"); line(F(170, 0), F(205, 0), "WIDOK")
dim_h(FX, FX + 120, FY - 18, "120", ext_from=FY)
dim_h(FX + 120, FX + 170, FY - 18, "50", ext_from=FY)
dim_v(FY, FY + 15, FX - 15, "15", ext_from=FX)
dim_v(FY, FY + 90, FX - 32, "90", ext_from=FX)
dim_v(FY, FY + 50, FX + 185, "50", ext_from=FX + 170)
dim_v(FY + 50, FY + 100, FX + 185, "50", ext_from=FX + 170)
txt("Widok z przodu    skala 1:20", F(85, 135), H_TITLE, "OPISY")

# ================= 5. SCHEMAT 1:50 =================
GX, GY = 640, 270
sc = 0.4
def G(x, z): return (GX + x * sc, GY + z * sc)
pline([G(x, z) for (x, z) in step_profile()], "WIDOK")
line(G(0, 0), G(LTOT, 0), "WIDOK")
line(G(LTOT, 0), G(LTOT, 90), "WIDOK")
line(G(0, 0), G(LTOT, 90), "OPISY")
txt("29,5%", G(150, 60), 4.5, "OPISY", rot=9)
dim_h(GX, GX + LTOT * sc, GY - 12, "l = 305 cm")
dim_v(GY, GY + 90 * sc, GX + LTOT * sc + 12, "h = 90 cm")
txt("Projekt schodów    skala 1:50", G(150, 130), H_SUB + 1, "OPISY")

# ================= 6. AKSONOMETRIA =================
KX, KY = 1270, 420
c30 = math.cos(math.radians(30))
def ISO(x, y, z):
    return (KX + (x - y) * c30 * 0.8, KY + (x + y) * 0.5 * 0.8 + z * 0.8)

prof_pts = step_profile()
for yy in (0, 120):
    pline([ISO(x, yy, z) for (x, z) in prof_pts], "WIDOK")
    line(ISO(0, yy, 0), ISO(LTOT, yy, 0), "WIDOK")
    line(ISO(LTOT, yy, 0), ISO(LTOT, yy, 90), "WIDOK")
for i, xr in enumerate(RISERS):
    line(ISO(xr, 0, TOPS[i] - 15), ISO(xr, 120, TOPS[i] - 15), "WIDOK")
    line(ISO(xr, 0, TOPS[i]), ISO(xr, 120, TOPS[i]), "WIDOK")
line(ISO(LTOT, 0, 90), ISO(LTOT, 120, 90), "WIDOK")
line(ISO(0, 0, 0), ISO(0, 120, 0), "WIDOK")
line(ISO(LTOT, 0, 0), ISO(LTOT, 120, 0), "WIDOK")
mp = [(5, 0), (5, 50), (105, 50), (105, 100), (305, 100), (305, 0)]
for yy in (120, 170):
    pline([ISO(x, yy, z) for (x, z) in mp], "WIDOK")
    line(ISO(5, yy, 0), ISO(305, yy, 0), "WIDOK")
for (x, z) in mp:
    line(ISO(x, 120, z), ISO(x, 170, z), "WIDOK")
line(ISO(105, 120, 0), ISO(105, 120, 50), "SZRAF")
line(ISO(205, 120, 0), ISO(205, 120, 100), "SZRAF")
for (cx, cz) in [(150, 75), (170, 62), (192, 80), (215, 68), (240, 84), (262, 63),
                 (283, 76), (135, 60), (205, 90), (255, 92)]:
    circle(ISO(cx, 120, cz), 2.6, "SZRAF")

def iso_dim(p1, p2, label, rot):
    line(p1, p2, "WYMIARY"); tick(*p1); tick(*p2)
    t = msp.add_text(label, dxfattribs={"layer": "WYMIARY", "height": H_DIM, "rotation": rot})
    t.set_placement(((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 4), align=TA.BOTTOM_CENTER)

iso_dim(ISO(0, -28, 0), ISO(LTOT, -28, 0), "305", 30)
iso_dim(ISO(-22, 0, 0), ISO(-22, 120, 0), "120", -30)
iso_dim(ISO(LTOT + 18, 0, 0), ISO(LTOT + 18, 0, 90), "90", 90)
iso_dim(ISO(305 + 14, 120, 0), ISO(305 + 14, 170, 0), "50", -30)
iso_dim(ISO(5 - 14, 170, 0), ISO(5 - 14, 170, 50), "50/100", 90)
txt("murek z gabionów (schodkowany 50→100)", (KX - 120, KY + 280), 4.8, "OPISY")
line((KX - 105, KY + 275), ISO(60, 170, 78), "OPISY")
txt("schody betonowe monolityczne", ISO(200, -70, -26), 4.8, "OPISY")
txt("Aksonometria (izometria)", (KX + 120, KY + 305), H_TITLE, "OPISY")

# ================= 7. OBLICZENIA =================
OX, OY = 955, 640
lines_calc = [
    ("Obliczenia schodów", H_SUB + 1),
    ("Wzór wygody:  2h + s = 60–65 cm", H_TXT),
    ("Przyjęto:  h = 15 cm,  s = 35 cm", H_TXT),
    ("Sprawdzenie:  2·15 + 35 = 65 cm  (OK)", H_TXT),
    ("Wysokość całkowita:  H = 90 cm", H_TXT),
    ("Liczba stopni:  n = H / h = 90 / 15 = 6", H_TXT),
    ("Podział na biegi:  3 + 3", H_TXT),
    ("Spocznik:  a·b + s = 2·65 + 35 = 165 cm", H_TXT),
    ("Długość rzutu:  l = 70 + 165 + 70 = 305 cm", H_TXT),
    ("Szerokość biegu:  120 cm", H_TXT),
    ("Nachylenie:  90 / 305 ≈ 29,5%  (≈ 16,4°)", H_TXT),
    ("Min. głębokość stopnia (zewn.):  s ≥ 35 cm  OK", H_TXT),
]
yy2 = OY
for s, h in lines_calc:
    txt(s, (OX, yy2), h, "OPISY", TA.MIDDLE_LEFT)
    yy2 -= h + 4.5

# ================= 8. WYKAZY =================
def table(x, y, title, rows, col_w=(18, 250, 42, 40), row_h=13):
    tw = sum(col_w)
    txt(title, (x + tw / 2, y + 9), H_SUB, "OPISY")
    n = len(rows) + 1
    for i in range(n + 1):
        line((x, y - i * row_h), (x + tw, y - i * row_h), "OPISY")
    cx = x
    line((cx, y), (cx, y - n * row_h), "OPISY")
    for w in col_w:
        cx += w
        line((cx, y), (cx, y - n * row_h), "OPISY")
    heads = ["Lp.", "Materiał budowlany", "Jedn.", "Nakład"]
    cx = x
    for w, hcell in zip(col_w, heads):
        txt(hcell, (cx + w / 2, y - row_h / 2), H_TAB, "OPISY")
        cx += w
    for r, row in enumerate(rows, start=1):
        cy = y - r * row_h - row_h / 2
        cx = x
        vals = [str(r)] + list(row)
        for w, v in zip(col_w, vals):
            if w == col_w[1]:
                txt(v, (cx + 5, cy), H_TAB - 0.8, "OPISY", TA.MIDDLE_LEFT)
            else:
                txt(v, (cx + w / 2, cy), H_TAB - 0.8, "OPISY")
            cx += w

rows_s = [
    ("beton C20/25 (XF3) – warstwa ścieralna", "m3", "0,60"),
    ("beton C16/20 – ława fundamentowa", "m3", "1,40"),
    ("siatka zgrzewana 15×15 cm, Ø6 mm", "m2", "4,0"),
    ("folia PE 0,2 mm", "m2", "4,0"),
    ("pospółka f. 0–16 mm (podsypka)", "m3", "0,30"),
    ("tłuczeń f. 31,5–63 mm (podbudowa)", "m3", "0,60"),
]
rows_m = [
    ("kosze gabionowe 100×50×50 cm", "szt.", "5"),
    ("kamień łamany f. 80–120 mm", "m3", "1,30"),
    ("geowłóknina PP 200 g/m2", "m2", "5,5"),
    ("rura drenażowa PVC Ø100 perforowana", "mb", "3,5"),
    ("żwir f. 8–16 mm (obsypka drenażu)", "m3", "0,15"),
    ("tłuczeń f. 31,5–63 mm (posadowienie)", "m3", "0,55"),
]
table(70, 300, "Wykaz materiałów budowlanych dla schodów", rows_s)
table(70, 155, "Wykaz materiałów budowlanych dla murka z gabionów", rows_m)
txt("Wartości orientacyjne dla: H = 90 cm, l = 305 cm, szer. 120 cm; murek 300 cm.",
    (245, 38), 4.2, "OPISY")

# ================= 9. TABELKA =================
TX, TY, TW2, TH2 = 1210, 40, 440, 150
pline([(TX, TY), (TX + TW2, TY), (TX + TW2, TY + TH2), (TX, TY + TH2)], "RAMKA", closed=True)
line((TX, TY + TH2 - 62), (TX + TW2, TY + TH2 - 62), "OPISY")
line((TX, TY + 34), (TX + TW2, TY + 34), "OPISY")
line((TX + 230, TY + 34), (TX + 230, TY + TH2), "OPISY")
line((TX + 110, TY), (TX + 110, TY + 34), "OPISY")
line((TX + 220, TY), (TX + 220, TY + 34), "OPISY")
line((TX + 330, TY), (TX + 330, TY + 34), "OPISY")
info_l = ["Kierunek: Architektura krajobrazu, WBiIŚ SGGW",
          "Rok II, sem. 4, rok akad. 2025/2026",
          "Przedmiot: Budowa obiektów architektury krajobrazu 2"]
for i, s in enumerate(info_l):
    txt(s, (TX + 8, TY + TH2 - 14 - i * 15), 4.8, "OPISY", TA.MIDDLE_LEFT)
txt("Temat: projekt wykonawczy schodów", (TX + 238, TY + TH2 - 18), 4.8, "OPISY", TA.MIDDLE_LEFT)
txt("ogrodowych z murkiem gabionowym", (TX + 238, TY + TH2 - 33), 4.8, "OPISY", TA.MIDDLE_LEFT)
txt("Wykonała: Pola Organiszczak", (TX + 8, TY + TH2 - 78), 5.2, "OPISY", TA.MIDDLE_LEFT)
txt("Sprawdziła: dr hab. Edyta Rosłon-Szeryńska", (TX + 238, TY + TH2 - 78), 5.2, "OPISY", TA.MIDDLE_LEFT)
txt("Skala: 1:20", (TX + 8, TY + 17), 5, "OPISY", TA.MIDDLE_LEFT)
txt("Data:", (TX + 118, TY + 17), 5, "OPISY", TA.MIDDLE_LEFT)
txt("Ocena:", (TX + 228, TY + 17), 5, "OPISY", TA.MIDDLE_LEFT)
txt("Uwagi:", (TX + 338, TY + 17), 5, "OPISY", TA.MIDDLE_LEFT)

doc.saveas("outputs/SCHODY_MUREK_POLA_POPRAWIONY.dxf")
print("DXF zapisany")

from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, ColorPolicy
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(28, 20))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
ctx = RenderContext(doc)
Frontend(ctx, MatplotlibBackend(ax),
         config=Configuration(color_policy=ColorPolicy.BLACK)).draw_layout(msp, finalize=True)
fig.savefig("outputs/podglad_plansza.png", dpi=100, facecolor="white")
fig2 = plt.figure(figsize=(841 / 25.4, 594 / 25.4))
ax2 = fig2.add_axes([0, 0, 1, 1]); ax2.set_axis_off()
Frontend(RenderContext(doc), MatplotlibBackend(ax2),
         config=Configuration(color_policy=ColorPolicy.BLACK)).draw_layout(msp, finalize=True)
fig2.savefig("outputs/SCHODY_MUREK_POLA_wydruk_A1.pdf", facecolor="white")
print("PNG i PDF zapisane")


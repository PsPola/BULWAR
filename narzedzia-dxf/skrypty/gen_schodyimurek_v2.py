#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCHODY OGRODOWE Z MURKIEM GABIONOWYM — projekt wykonawczy (Pola Organiszczak),
wg standardu wytyczne/WYTYCZNE_DXF.md.

- DXF R2013 ASCII, model 1:1 w MILIMETRACH (autoruje w cm, konwersja x10 -> mm).
- rzeczywiste encje: LINE / LWPOLYLINE / CIRCLE / MTEXT / DIMENSION / MULTILEADER.
- BEZ bloków, BEZ proxy, BEZ HATCH (kreskowanie liniami na KRESKOWANIE),
  BEZ grotów OBLIQUE (groty ISO closed-filled, dimtsz=0).
- warstwy: KONTUR / OSIE / WYMIARY / OPISY / KRESKOWANIE.
- font Arial (polskie znaki), teksty 2.5/3.5/5.0 mm na papierze, druk 1:20.
"""
import math
import ezdxf
from ezdxf.math import Vec2
from ezdxf.enums import MTextEntityAlignment as MA
from ezdxf.render import mleader

MM = 10.0     # 1 cm autorski = 10 mm modelu
PS = 20.0     # skala druku 1:20 -> mnoznik anotacji (mm papieru)

# ------------------------------------------------------------------ setup
doc = ezdxf.new("R2013", setup=True)
doc.header["$INSUNITS"] = 4          # milimetry
doc.header["$MEASUREMENT"] = 1
doc.header["$LWDISPLAY"] = 1          # pokazuj grubosci linii
msp = doc.modelspace()

if "ARIAL" not in doc.styles:
    doc.styles.add("ARIAL", font="arial.ttf")

# hierarchia grubosci linii (1/100 mm): kontur grube, wymiary/osie/kreskowanie cienkie
for n, col, lt, lw in [("KONTUR", 7, "Continuous", 35), ("OSIE", 1, "CENTER", 18),
                       ("WYMIARY", 3, "Continuous", 18), ("OPISY", 5, "Continuous", 25),
                       ("KRESKOWANIE", 8, "Continuous", 13)]:
    if n not in doc.layers:
        doc.layers.add(n, color=col, linetype=lt, lineweight=lw)

ds = doc.dimstyles.add("ISO")
for k, v in dict(dimtxt=2.5, dimasz=2.5, dimexe=1.0, dimexo=2.0, dimgap=1.0,
                 dimtad=1, dimtsz=0.0, dimdec=0, dimlfac=1.0, dimscale=PS,
                 dimclrt=3, dimtxsty="ARIAL", dimblk="").items():
    ds.set_dxf_attrib(k, v)

# ------------------------------------------------------------------ primitywy (autor w cm)
def L(x1, y1, x2, y2, layer="KONTUR", lt=None):
    a = {"layer": layer}
    if lt:
        a["linetype"] = lt
    msp.add_line((x1 * MM, y1 * MM), (x2 * MM, y2 * MM), dxfattribs=a)

def P(pts, layer="KONTUR", closed=False, lt=None):
    a = {"layer": layer}
    if lt:
        a["linetype"] = lt
    msp.add_lwpolyline([(x * MM, y * MM) for x, y in pts], close=closed, dxfattribs=a)

def C(cx, cy, r, layer="KRESKOWANIE"):
    msp.add_circle((cx * MM, cy * MM), r * MM, dxfattribs={"layer": layer})

def T(s, x, y, mm=3.5, align=MA.MIDDLE_LEFT, layer="OPISY", rot=0):
    m = msp.add_mtext(s, dxfattribs={"layer": layer, "style": "ARIAL",
                                     "char_height": mm * PS, "rotation": rot})
    m.set_location((x * MM, y * MM), attachment_point=align)
    return m

def DIMH(x1, x2, ydim, yref):
    d = msp.add_linear_dim(base=(x1 * MM, ydim * MM),
                           p1=(x1 * MM, yref * MM), p2=(x2 * MM, yref * MM),
                           angle=0, dimstyle="ISO", dxfattribs={"layer": "WYMIARY"})
    d.render()

def DIMV(y1, y2, xdim, xref):
    d = msp.add_linear_dim(base=(xdim * MM, y1 * MM),
                           p1=(xref * MM, y1 * MM), p2=(xref * MM, y2 * MM),
                           angle=90, dimstyle="ISO", dxfattribs={"layer": "WYMIARY"})
    d.render()

def LEAD(text, target, insert, side=mleader.ConnectionSide.left, mm=2.5):
    ml = msp.add_multileader_mtext("Standard")
    ml.multileader.dxf.layer = "OPISY"
    ml.set_content(text, style="ARIAL", char_height=mm,
                   alignment=mleader.TextAlignment.left)
    ml.set_overall_scaling(PS)
    ml.add_leader_line(side, [Vec2(target[0] * MM, target[1] * MM)])
    ml.build(insert=Vec2(insert[0] * MM, insert[1] * MM))

def LEAD_MULTI(text, targets, insert, side=mleader.ConnectionSide.left, mm=2.5):
    ml = msp.add_multileader_mtext("Standard")
    ml.multileader.dxf.layer = "OPISY"
    ml.set_content(text, style="ARIAL", char_height=mm,
                   alignment=mleader.TextAlignment.left)
    ml.set_overall_scaling(PS)
    for t in targets:
        ml.add_leader_line(side, [Vec2(t[0] * MM, t[1] * MM)])
    ml.build(insert=Vec2(insert[0] * MM, insert[1] * MM))

# ------------------------------------------------------------------ kreskowanie liniami
def hatch_poly(pts, spacing, ang, layer="KRESKOWANIE"):
    """Wypelnia dowolny (tez wklesly) wielokat rownoleglymi LINIAMI (bez HATCH)."""
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    projs = [px * nx + py * ny for px, py in pts]
    s0, s1 = min(projs), max(projs)
    edges = list(zip(pts, pts[1:] + pts[:1]))
    s = s0 + spacing / 2
    while s < s1:
        qx, qy = s * nx, s * ny
        ts = []
        for (ax, ay), (bx, by) in edges:
            ex, ey = bx - ax, by - ay
            det = ex * dy - dx * ey
            if abs(det) < 1e-9:
                continue
            rx, ry = ax - qx, ay - qy
            t = (-rx * ey + ex * ry) / det
            u = (dx * ry - dy * rx) / det
            if -1e-9 <= u <= 1 + 1e-9:
                ts.append(t)
        ts.sort()
        for i in range(0, len(ts) - 1, 2):
            L(qx + ts[i] * dx, qy + ts[i] * dy,
              qx + ts[i + 1] * dx, qy + ts[i + 1] * dy, layer)
        s += spacing

def xhatch_poly(pts, spacing, layer="KRESKOWANIE"):
    hatch_poly(pts, spacing, 45, layer)
    hatch_poly(pts, spacing, 135, layer)

def dots(x1, y1, x2, y2, dx=6, dy=4, r=0.5, layer="KRESKOWANIE"):
    row = 0; y = y1 + dy / 2
    while y < y2:
        x = x1 + dx / 2 + (dx / 2 if row % 2 else 0)
        while x < x2:
            C(x, y, r, layer); x += dx
        y += dy; row += 1

def triangles(x1, y1, x2, y2, s=4.5, dx=10, dy=7, layer="KRESKOWANIE"):
    row = 0; y = y1 + dy / 2
    while y + s / 2 < y2:
        x = x1 + dx / 2 + (dx / 2 if row % 2 else 0)
        while x + s / 2 < x2:
            P([(x - s / 2, y - s / 3), (x, y + s / 2), (x + s / 2, y - s / 3)],
              layer, closed=True)
            x += dx
        y += dy; row += 1

def stones(x1, y1, x2, y2, r=3.2, dx=11, dy=10, layer="KRESKOWANIE"):
    row = 0; y = y1 + dy / 2
    while y < y2 - r + 1:
        x = x1 + dx / 2 + (dx / 2 if row % 2 else 0)
        while x < x2 - r + 1:
            C(x, y, r, layer); x += dx
        y += dy; row += 1

def wavy(p1, p2, amp=2.5, waves=4, layer="KONTUR"):
    x1, y1 = p1; x2, y2 = p2
    Ln = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / Ln, (y2 - y1) / Ln
    nx, ny = -uy, ux
    pts = []
    n = waves * 8
    for i in range(n + 1):
        t = i / n
        off = amp * math.sin(t * waves * 2 * math.pi)
        pts.append((x1 + ux * t * Ln + nx * off, y1 + uy * t * Ln + ny * off))
    P(pts, layer)

def chevron(tip, ang_deg, size=6, layer="OSIE"):
    """otwarty grot (2 linie) — do linii ciecia / kierunku, bez wypelnienia."""
    a = math.radians(ang_deg)
    for da in (math.radians(150), math.radians(-150)):
        L(tip[0], tip[1], tip[0] + size * math.cos(a + da),
          tip[1] + size * math.sin(a + da), layer)

# ============================================================ GEOMETRIA (cm)
RISERS = [0, 35, 70, 235, 270, 305]
TOPS   = [15, 30, 45, 60, 75, 90]
LTOT = 305; W = 120; MW = 50

def step_profile(x_end=LTOT):
    pts, z = [], 0
    for i, xr in enumerate(RISERS):
        pts.append((xr, z))
        z = TOPS[i]
        pts.append((xr, z))
    pts.append((x_end, z))
    return pts

# ============================================================ 1. RZUT Z GORY
RX, RY = 150, 800
def R(x, y): return (RX + x, RY + y)

def rzut():
    P([R(0, 0), R(LTOT, 0), R(LTOT, W), R(0, W)], "KONTUR", closed=True)
    for x in [35, 70, 235, 270]:
        L(*R(x, 0), *R(x, W), "KONTUR")
    P([R(5, W), R(305, W), R(305, W + MW), R(5, W + MW)], "KONTUR", closed=True)
    for x in [105, 205]:
        L(*R(x, W), *R(x, W + MW), "KONTUR")
    stones(RX + 5, RY + W, RX + 305, RY + W + MW, r=3.0, dx=13, dy=12)

    DIMH(RX + 5, RX + 105, RY + W + MW + 28, RY + W + MW)
    DIMH(RX + 105, RX + 205, RY + W + MW + 28, RY + W + MW)
    DIMH(RX + 205, RX + 305, RY + W + MW + 28, RY + W + MW)
    T("MUREK Z GABIONÓW  (kosze 100×50×50 cm)", *R(152, W + MW + 52), 3.5, MA.MIDDLE_CENTER)
    T("góra koszy:  +0,50 / +1,00 m", *R(152, W + MW + 42), 2.5, MA.MIDDLE_CENTER)

    treads = [(0, 35, "+0,15"), (35, 70, "+0,30"), (70, 235, "+0,45  SPOCZNIK"),
              (235, 270, "+0,60"), (270, 305, "+0,75")]
    for x1, x2, s in treads:
        xm = (x1 + x2) / 2
        T(s, *R(xm, 88), 2.5, MA.MIDDLE_CENTER)
        T("i=1%", *R(xm, 30), 2.5, MA.MIDDLE_CENTER)
    T("DÓŁ  ±0,00", *R(-80, 60), 3.5, MA.MIDDLE_RIGHT)
    T("GÓRA  +0,90", *R(LTOT + 80, 60), 3.5, MA.MIDDLE_LEFT)

    # linie ciecia (OSIE) + otwarte groty
    L(*R(-30, 60), *R(LTOT + 30, 60), "OSIE")
    chevron(R(-30, 60), 180, 7); chevron(R(LTOT + 30, 60), 0, 7)
    T("B", *R(-40, 60), 3.5, MA.MIDDLE_CENTER)
    T("B'", *R(LTOT + 42, 60), 3.5, MA.MIDDLE_CENTER)
    L(*R(150, -42), *R(150, W + MW + 8), "OSIE")
    chevron(R(150, -42), -90, 7); chevron(R(150, W + MW + 8), 90, 7)
    T("A", *R(150, -52), 3.5, MA.MIDDLE_CENTER)
    T("A'", *R(150, W + MW + 15), 3.5, MA.MIDDLE_CENTER)

    DIMH(RX, RX + 35, RY - 20, RY)
    DIMH(RX + 35, RX + 70, RY - 20, RY)
    DIMH(RX + 70, RX + 235, RY - 20, RY)
    DIMH(RX + 235, RX + 270, RY - 20, RY)
    DIMH(RX + 270, RX + 305, RY - 20, RY)
    DIMH(RX, RX + LTOT, RY - 38, RY)
    DIMV(RY, RY + W, RX - 20, RX)
    DIMV(RY + W, RY + W + MW, RX - 20, RX + 5)
    T("bieg 1 — 3 × 15/35 cm", *R(40, -70), 2.5, MA.MIDDLE_CENTER)
    T("bieg 2 — 3 × 15/35 cm", *R(262, -70), 2.5, MA.MIDDLE_CENTER)
    T("RZUT Z GÓRY    1:20", *R(152, W + MW + 60), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 2. PRZEKROJ B-B'
BX, BY = 1000, 840
def B(x, z): return (BX + x, BY + z)

def przekroj_BB():
    prof = step_profile()
    def BP(pts, dz=0.0): return [B(x, z + dz) for x, z in pts]

    # murek za przekrojem (widok)
    for seg in [((5, 15), (5, 50)), ((5, 50), (105, 50)), ((105, 45), (105, 100)),
                ((105, 100), (305, 100)), ((305, 90), (305, 100)),
                ((105, 50), (235, 50)), ((205, 50), (205, 100))]:
        L(*B(*seg[0]), *B(*seg[1]), "KONTUR")
    T("murek z gabionów za przekrojem (widok)", *B(150, 108), 2.5, MA.MIDDLE_CENTER)

    # kontury warstw
    for dz in (0, -12, -42, -50, -65):
        P(BP(prof, dz), "KONTUR")
    L(*B(0, 0), *B(0, -65), "KONTUR")
    L(*B(LTOT, 90), *B(LTOT, 25), "KONTUR")
    L(*B(-55, 0), *B(0, 0), "KONTUR")
    L(*B(LTOT, 90), *B(LTOT + 55, 90), "KONTUR")
    wavy(B(-55, 8), B(-55, -60)); wavy(B(LTOT + 55, 98), B(LTOT + 55, 30))

    def band(top_dz, bot_dz): return BP(prof, top_dz) + BP(prof, bot_dz)[::-1]
    hatch_poly(band(0, -12), 6, 45)          # scieralna beton
    xhatch_poly(band(-12, -42), 8)           # lawa zelbet
    segs = [(0, 35, 15), (35, 70, 30), (70, 235, 45), (235, 270, 60), (270, 305, 75)]
    for x1, x2, zt in segs:
        dots(BX + x1, BY + zt - 50, BX + x2, BY + zt - 42)          # podsypka
        triangles(BX + x1, BY + zt - 65, BX + x2, BY + zt - 50)     # podbudowa
    # grunt rodzimy
    hatch_poly([B(-55, 0), B(0, 0), B(0, -65), B(-55, -60)], 22, 45)
    hatch_poly(BP(prof, -65) + [B(LTOT + 55, 25), B(LTOT + 55, 12), B(0, -78)], 22, 45)
    hatch_poly([B(LTOT, 90), B(LTOT + 55, 90), B(LTOT + 55, 37), B(LTOT, 25)], 22, 45)
    L(*B(LTOT, 25), *B(LTOT + 55, 37), "KONTUR")

    # odnosniki warstw (MULTILEADER)
    lx = BX + 372
    items = [
        ("12 cm — warstwa ścieralna: beton C20/25 (XF3),\nzatarty na szorstko, spadek 1%, fazy 1×1 cm", B(285, 70)),
        ("30 cm — ława fundamentowa: beton C16/20,\nsiatka zgrzewana 15×15 cm, Ø6 mm", B(288, 45)),
        ("folia PE 0,2 mm", B(291, 33)),
        ("8 cm — podsypka: pospółka f. 0–16 mm", B(294, 29)),
        ("15 cm — podbudowa: tłuczeń f. 31,5–63 mm, zagęszczony", B(297, 18)),
        ("grunt rodzimy", B(300, 2)),
    ]
    ly = BY + 150
    for txt, p in items:
        LEAD(txt, p, (lx, ly), mleader.ConnectionSide.left)
        ly -= 22

    for z in [0, 15, 30, 45, 60, 75, 90]:
        s = "±0,00" if z == 0 else "+0,%02d" % z
        T(s, *B(-72, z), 2.5, MA.MIDDLE_RIGHT, "WYMIARY")
        L(*B(-68, z), *B(-60, z), "WYMIARY")
    DIMV(BY, BY + 90, BX - 42, BX)
    DIMV(BY, BY + 15, BX - 24, BX)
    DIMV(BY + 15, BY + 30, BX - 24, BX)
    DIMV(BY + 30, BY + 45, BX - 24, BX)
    for x1, x2 in [(0, 35), (35, 70), (70, 235), (235, 270), (270, 305)]:
        DIMH(BX + x1, BX + x2, BY + 124, BY + 90)
    T("SPOCZNIK", *B(152, 138), 2.5, MA.MIDDLE_CENTER)
    DIMH(BX, BX + LTOT, BY - 90, BY)
    T("B", *B(-90, 148), 3.5, MA.MIDDLE_CENTER)
    T("B'", *B(340, 155), 3.5, MA.MIDDLE_CENTER)
    T("PRZEKRÓJ B-B'    1:20", *B(152, 174), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 3. PRZEKROJ A-A'
AX, AY = 240, 470
def A(y, z): return (AX + y, AY + z)

def przekroj_AA():
    zt = 45
    for dz in (0, -12, -42):
        P([A(0, zt + dz), A(120, zt + dz)], "KONTUR")
    P([A(0, zt - 50), A(110, zt - 50)], "KONTUR")
    P([A(0, zt - 65), A(110, zt - 65)], "KONTUR")
    L(*A(0, zt), *A(0, zt - 65), "KONTUR")
    L(*A(120, zt), *A(120, 0), "KONTUR")
    L(*A(110, zt - 42), *A(110, zt - 65), "KONTUR")
    hatch_poly([A(0, zt), A(120, zt), A(120, zt - 12), A(0, zt - 12)], 6, 45)
    xhatch_poly([A(0, zt - 12), A(120, zt - 12), A(120, zt - 42), A(0, zt - 42)], 8)
    dots(AX, AY + zt - 50, AX + 110, AY + zt - 42)
    triangles(AX, AY + zt - 65, AX + 110, AY + zt - 50)

    for z in [60, 75, 90]:
        L(*A(0, z), *A(120, z), "KONTUR", lt="DASHED")
    T("krawędzie stopni za przekrojem", *A(58, 97), 2.5, MA.MIDDLE_CENTER)

    for z1 in [0, 50]:
        P([A(120, z1), A(170, z1), A(170, z1 + 50), A(120, z1 + 50)], "KONTUR", closed=True)
    stones(AX + 120, AY + 0, AX + 170, AY + 100, r=3.4, dx=12, dy=11)
    P([A(110, 0), A(180, 0), A(180, -25), A(110, -25)], "KONTUR", closed=True)
    triangles(AX + 110, AY - 25, AX + 180, AY + 0)
    P([A(171.5, 92), A(171.5, -26.5), A(108.5, -26.5)], "KONTUR", lt="DASHED")
    C(*A(181, -14), 5, "KONTUR")
    dots(AX + 174, AY - 22, AX + 191, AY - 6, dx=5, dy=4, r=0.7)

    L(*A(-60, zt), *A(0, zt), "KONTUR")
    wavy(A(-60, zt + 8), A(-60, zt - 60))
    hatch_poly([A(-60, zt), A(0, zt), A(0, zt - 65), A(110, zt - 65), A(110, -25),
                A(180, -25), A(180, -45), A(-60, -45)], 22, 45)
    L(*A(170, 90), *A(240, 90), "KONTUR")
    wavy(A(240, 98), A(240, -38))
    hatch_poly([A(170, 90), A(240, 90), A(240, -45), A(180, -45), A(180, -25),
                A(170, -25)], 22, 45)
    T("grunt rodzimy (skarpa)", *A(215, 55), 2.5, MA.MIDDLE_CENTER, rot=90)

    lx2 = AX + 278
    items2 = [
        ("kosze gabionowe 100×50×50 cm, siatka zgrzewana\noczko 5×10 cm, drut Ø4,5 mm (Galfan)", A(158, 78)),
        ("kamień łamany f. 80–120 mm (wypełnienie)", A(150, 62)),
        ("geowłóknina PP 200 g/m², od strony gruntu,\nwywinięta pod kosz", A(171.5, 30)),
        ("drenaż: rura PVC perforowana Ø100 w obsypce\nżwirowej 8–16 mm, spadek 0,5–1%", A(181, -14)),
        ("posadowienie: tłuczeń f. 31,5–63 mm,\nzagęszczony, gr. 25 cm", A(155, -18)),
    ]
    ly2 = AY + 108
    for txt, p in items2:
        LEAD(txt, p, (lx2, ly2), mleader.ConnectionSide.left)
        ly2 -= 24

    T("+0,45", *A(-75, zt), 2.5, MA.MIDDLE_RIGHT, "WYMIARY")
    L(*A(-72, zt), *A(-63, zt), "WYMIARY")
    T("+1,00", *A(145, 108), 2.5, MA.MIDDLE_CENTER, "WYMIARY")
    T("+0,90", *A(215, 96), 2.5, MA.MIDDLE_CENTER, "WYMIARY")
    DIMH(AX, AX + 120, AY - 62, AY)
    DIMH(AX + 120, AX + 170, AY - 62, AY)
    DIMH(AX + 110, AX + 180, AY - 80, AY - 25)
    DIMV(AY, AY + 50, AX + 196, AX + 170)
    DIMV(AY + 50, AY + 100, AX + 196, AX + 170)
    DIMV(AY - 25, AY + 0, AX + 210, AX + 180)
    DIMV(AY + zt - 12, AY + zt, AX - 24, AX)
    DIMV(AY + zt - 42, AY + zt - 12, AX - 24, AX)
    DIMV(AY + zt - 50, AY + zt - 42, AX - 42, AX)
    DIMV(AY + zt - 65, AY + zt - 50, AX - 24, AX)
    T("A", *A(-90, 125), 3.5, MA.MIDDLE_CENTER)
    T("A'", *A(255, 125), 3.5, MA.MIDDLE_CENTER)
    T("PRZEKRÓJ A-A'    1:20", *A(90, 142), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 4. WIDOK Z PRZODU
FX, FY = 780, 470
def F(y, z): return (FX + y, FY + z)

def widok_front():
    P([F(0, 0), F(120, 0), F(120, 15), F(0, 15)], "KONTUR", closed=True)
    for z in [30, 45, 60, 75, 90]:
        L(*F(0, z), *F(120, z), "KONTUR")
    L(*F(0, 15), *F(0, 90), "KONTUR"); L(*F(120, 15), *F(120, 90), "KONTUR")
    L(*F(0, 90), *F(120, 90), "KONTUR")
    P([F(120, 0), F(170, 0), F(170, 50), F(120, 50)], "KONTUR", closed=True)
    P([F(120, 50), F(170, 50), F(170, 100), F(120, 100)], "KONTUR", closed=True)
    T("2. warstwa koszy", *F(150, 110), 2.5, MA.MIDDLE_CENTER)
    stones(FX + 120, FY, FX + 170, FY + 100, r=3.2, dx=13, dy=12)
    L(*F(-40, 0), *F(0, 0), "KONTUR"); L(*F(170, 0), *F(205, 0), "KONTUR")
    DIMH(FX, FX + 120, FY - 20, FY)
    DIMH(FX + 120, FX + 170, FY - 20, FY)
    DIMV(FY, FY + 90, FX - 34, FX)
    DIMV(FY, FY + 50, FX + 186, FX + 170)
    DIMV(FY + 50, FY + 100, FX + 186, FX + 170)
    T("WIDOK Z PRZODU    1:20", *F(85, 130), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 5. SCHEMAT SPADKU 1:50
GX, GY = 640, 270
sc = 0.4
def G(x, z): return (GX + x * sc, GY + z * sc)

def schemat():
    P([G(x, z) for x, z in step_profile()], "KONTUR")
    L(*G(0, 0), *G(LTOT, 0), "KONTUR")
    L(*G(LTOT, 0), *G(LTOT, 90), "KONTUR")
    L(*G(0, 0), *G(LTOT, 90), "OPISY")
    T("nachylenie ≈ 29,5%", *G(150, 66), 2.5, MA.MIDDLE_CENTER, rot=9)
    DIMH(GX, GX + LTOT * sc, GY - 14, GY)
    DIMV(GY, GY + 90 * sc, GX + LTOT * sc + 14, GX + LTOT * sc)
    T("SCHEMAT SPADKU    1:50", *G(150, 128), 3.5, MA.MIDDLE_CENTER)

# ============================================================ 6. AKSONOMETRIA
KX, KY = 1270, 420
c30 = math.cos(math.radians(30))
def ISO(x, y, z):
    return (KX + (x - y) * c30 * 0.8, KY + (x + y) * 0.5 * 0.8 + z * 0.8)

def aksonometria():
    prof_pts = step_profile()
    for yy in (0, 120):
        P([ISO(x, yy, z) for x, z in prof_pts], "KONTUR")
        L(*ISO(0, yy, 0), *ISO(LTOT, yy, 0), "KONTUR")
        L(*ISO(LTOT, yy, 0), *ISO(LTOT, yy, 90), "KONTUR")
    for i, xr in enumerate(RISERS):
        L(*ISO(xr, 0, TOPS[i] - 15), *ISO(xr, 120, TOPS[i] - 15), "KONTUR")
        L(*ISO(xr, 0, TOPS[i]), *ISO(xr, 120, TOPS[i]), "KONTUR")
    L(*ISO(LTOT, 0, 90), *ISO(LTOT, 120, 90), "KONTUR")
    L(*ISO(0, 0, 0), *ISO(0, 120, 0), "KONTUR")
    L(*ISO(LTOT, 0, 0), *ISO(LTOT, 120, 0), "KONTUR")
    mp = [(5, 0), (5, 50), (105, 50), (105, 100), (305, 100), (305, 0)]
    for yy in (120, 170):
        P([ISO(x, yy, z) for x, z in mp], "KONTUR")
        L(*ISO(5, yy, 0), *ISO(305, yy, 0), "KONTUR")
    for x, z in mp:
        L(*ISO(x, 120, z), *ISO(x, 170, z), "KONTUR")
    L(*ISO(105, 120, 0), *ISO(105, 120, 50), "KRESKOWANIE")
    L(*ISO(205, 120, 0), *ISO(205, 120, 100), "KRESKOWANIE")
    for cx, cz in [(150, 75), (170, 62), (192, 80), (215, 68), (240, 84), (262, 63),
                   (283, 76), (135, 60), (205, 90), (255, 92)]:
        C(*ISO(cx, 120, cz), 2.6, "KRESKOWANIE")
    T("murek z gabionów\n(schodkowany 50→100)", KX - 120, KY + 285, 2.5, MA.MIDDLE_LEFT)
    L(KX - 105, KY + 278, *ISO(60, 170, 78), "OPISY")
    T("schody betonowe monolityczne", *ISO(200, -70, -26), 2.5, MA.MIDDLE_CENTER)
    T("AKSONOMETRIA", KX + 120, KY + 305, 5.0, MA.MIDDLE_CENTER)

# ============================================================ 7. OBLICZENIA
OX, OY = 1015, 645
def obliczenia():
    calc = [
        ("OBLICZENIA SCHODÓW", 3.5),
        ("Wzór wygody:  2h + s = 60–65 cm", 2.5),
        ("Przyjęto:  h = 15 cm,  s = 35 cm", 2.5),
        ("Sprawdzenie:  2·15 + 35 = 65 cm  (OK)", 2.5),
        ("Wysokość całkowita:  H = 90 cm", 2.5),
        ("Liczba stopni:  n = H / h = 90 / 15 = 6", 2.5),
        ("Podział na biegi:  3 + 3", 2.5),
        ("Spocznik:  2·65 + 35 = 165 cm", 2.5),
        ("Długość rzutu:  70 + 165 + 70 = 305 cm", 2.5),
        ("Szerokość biegu:  120 cm", 2.5),
        ("Nachylenie:  90 / 305 ≈ 29,5%  (≈ 16,4°)", 2.5),
    ]
    yy = OY
    for s, h in calc:
        T(s, OX, yy, h, MA.MIDDLE_LEFT)
        yy -= (h + 4.5)

# ============================================================ 8. WYKAZY
def table(x, y, title, rows, col_w=(18, 250, 42, 40), row_h=13):
    tw = sum(col_w)
    T(title, x + tw / 2, y + 9, 3.5, MA.MIDDLE_CENTER)
    n = len(rows) + 1
    for i in range(n + 1):
        L(x, y - i * row_h, x + tw, y - i * row_h, "KONTUR")
    cx = x
    L(cx, y, cx, y - n * row_h, "KONTUR")
    for w in col_w:
        cx += w
        L(cx, y, cx, y - n * row_h, "KONTUR")
    heads = ["Lp.", "Materiał budowlany", "Jedn.", "Nakład"]
    cx = x
    for w, hc in zip(col_w, heads):
        T(hc, cx + w / 2, y - row_h / 2, 2.5, MA.MIDDLE_CENTER)
        cx += w
    for r, row in enumerate(rows, start=1):
        cy = y - r * row_h - row_h / 2
        cx = x
        vals = [str(r)] + list(row)
        for w, v in zip(col_w, vals):
            if w == col_w[1]:
                T(v, cx + 5, cy, 2.5, MA.MIDDLE_LEFT)
            else:
                T(v, cx + w / 2, cy, 2.5, MA.MIDDLE_CENTER)
            cx += w

def wykazy():
    rows_s = [
        ("beton C20/25 (XF3) — warstwa ścieralna", "m³", "0,60"),
        ("beton C16/20 — ława fundamentowa", "m³", "1,40"),
        ("siatka zgrzewana 15×15 cm, Ø6 mm", "m²", "4,0"),
        ("folia PE 0,2 mm", "m²", "4,0"),
        ("pospółka f. 0–16 mm (podsypka)", "m³", "0,30"),
        ("tłuczeń f. 31,5–63 mm (podbudowa)", "m³", "0,60"),
    ]
    rows_m = [
        ("kosze gabionowe 100×50×50 cm", "szt.", "5"),
        ("kamień łamany f. 80–120 mm", "m³", "1,30"),
        ("geowłóknina PP 200 g/m²", "m²", "5,5"),
        ("rura drenażowa PVC Ø100 perforowana", "mb", "3,5"),
        ("żwir f. 8–16 mm (obsypka drenażu)", "m³", "0,15"),
        ("tłuczeń f. 31,5–63 mm (posadowienie)", "m³", "0,55"),
    ]
    table(70, 300, "Wykaz materiałów — schody", rows_s)
    table(70, 155, "Wykaz materiałów — murek z gabionów", rows_m)
    T("Wartości orientacyjne: H = 90 cm, l = 305 cm, szer. 120 cm; murek 300 cm.",
      245, 38, 2.5, MA.MIDDLE_CENTER)
    T("UWAGI:", 70, 27, 2.5, MA.MIDDLE_LEFT)
    T("— mur gabionowy grawitacyjny: H≈1,0 m, podstawa 0,5 m (schodkowany); przy większym naziomie poszerzyć podstawę,", 70, 19, 2.5, MA.MIDDLE_LEFT)
    T("— drenaż Ø100 (spadek 0,5–1%) + geowłóknina od strony gruntu; stopnie ze spadkiem 1% (odwodnienie).", 70, 11, 2.5, MA.MIDDLE_LEFT)

# ============================================================ 9. TABELKA
def tabelka():
    TXc, TYc, TW2, TH2 = 1210, 40, 440, 150
    P([(TXc, TYc), (TXc + TW2, TYc), (TXc + TW2, TYc + TH2), (TXc, TYc + TH2)],
      "KONTUR", closed=True)
    L(TXc, TYc + TH2 - 62, TXc + TW2, TYc + TH2 - 62, "KONTUR")
    L(TXc, TYc + 34, TXc + TW2, TYc + 34, "KONTUR")
    L(TXc + 230, TYc + 34, TXc + 230, TYc + TH2, "KONTUR")
    L(TXc + 110, TYc, TXc + 110, TYc + 34, "KONTUR")
    L(TXc + 220, TYc, TXc + 220, TYc + 34, "KONTUR")
    L(TXc + 330, TYc, TXc + 330, TYc + 34, "KONTUR")
    info = ["Kierunek: Architektura krajobrazu, WBiIŚ SGGW",
            "Rok II, sem. 4, rok akad. 2025/2026",
            "Przedmiot: Budowa obiektów architektury krajobrazu 2"]
    for i, s in enumerate(info):
        T(s, TXc + 8, TYc + TH2 - 14 - i * 15, 2.5, MA.MIDDLE_LEFT)
    T("Temat: projekt wykonawczy schodów\nogrodowych z murkiem gabionowym",
      TXc + 238, TYc + TH2 - 26, 2.5, MA.MIDDLE_LEFT)
    T("Wykonała: Pola Organiszczak", TXc + 8, TYc + TH2 - 78, 3.5, MA.MIDDLE_LEFT)
    T("Sprawdziła: dr hab. E. Rosłon-Szeryńska", TXc + 238, TYc + TH2 - 78, 2.5, MA.MIDDLE_LEFT)
    T("Skala: 1:20", TXc + 8, TYc + 17, 3.5, MA.MIDDLE_LEFT)
    T("Data:", TXc + 118, TYc + 17, 2.5, MA.MIDDLE_LEFT)
    T("Ocena:", TXc + 228, TYc + 17, 2.5, MA.MIDDLE_LEFT)
    T("Uwagi:", TXc + 338, TYc + 17, 2.5, MA.MIDDLE_LEFT)

# ============================================================ ZLOZENIE ARKUSZA
SW, SH = 1682, 1188
P([(0, 0), (SW, 0), (SW, SH), (0, SH)], "KONTUR", closed=True)
P([(15, 15), (SW - 15, 15), (SW - 15, SH - 15), (15, SH - 15)], "KONTUR", closed=True)

rzut()
przekroj_BB()
przekroj_AA()
widok_front()
schemat()
aksonometria()
obliczenia()
wykazy()
tabelka()

# ------------------------------------------------------------------ zapis + podglad
import datetime
TS = datetime.datetime.now().strftime("%y%m%d-%H%M")   # yyMMdd-hhmm na koncu nazwy
_dxf = "outputs/schody_murek_v2_%s.dxf" % TS
_png = "outputs/podgląd_schody_murek_v2_%s.png" % TS

def _strip_ezdxf(doc):
    """Usuwa slady biblioteki ezdxf (appid EZDXF, dimstyle EZDXF/EZ_*, metadane
    EZDXF_META z CREATED_BY_EZDXF/WRITTEN_BY_EZDXF) tak, by nie zostawaly w DXF."""
    doc._update_ezdxf_metadata = lambda: None            # brak WRITTEN_BY_EZDXF przy zapisie
    _oa = doc._create_appids
    def _no_ezdxf():
        _oa()
        if "EZDXF" in doc.appids: doc.appids.remove("EZDXF")
    doc._create_appids = _no_ezdxf                        # brak appid EZDXF przy zapisie
    _m = doc.rootdict.get("EZDXF_META"); doc.rootdict.discard("EZDXF_META")
    if _m is not None:
        try: _m.destroy()                                # usun slownik + CREATED_BY_EZDXF
        except Exception: pass
    for _d in list(doc.dimstyles):
        _n = _d.dxf.name
        if _n == "EZDXF" or _n.startswith("EZ_"):
            if doc.header.get("$DIMSTYLE", "Standard") == _n: doc.header["$DIMSTYLE"] = "Standard"
            doc.dimstyles.remove(_n)
    if "EZDXF" in doc.appids: doc.appids.remove("EZDXF")

_strip_ezdxf(doc)
doc.saveas(_dxf)
print("OK zapisano", _dxf)
print("encje:", sorted({e.dxftype() for e in msp}))

from ezdxf.addons.drawing import matplotlib as _mpl
_mpl.qsave(msp, _png, size_inches=(23.4, 23.4 * SH / SW), dpi=150, bg="#FFFFFF")
print("OK podglad", _png)

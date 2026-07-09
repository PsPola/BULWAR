#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ŁAWKA L — projekt wykonawczy (Pola Organiszczak), wg wytyczne/WYTYCZNE_DXF.md.
Siedzisko: jasny kamień naturalny (blat lity gr. 8 cm, smukły, uniesiony).
Oparcie/osłona: betonowa donica żelbetowa C30/37 XF3 (mrozoodporna), ścianki 8 cm.
Arkusz A2 poziomy, model 1:1 w mm (autor w cm, x10), druk 1:20 (detale 1:2.5).
"""
import math, datetime
import ezdxf
from ezdxf.math import Vec2
from ezdxf.enums import MTextEntityAlignment as MA
from ezdxf.render import mleader

MM = 10.0     # 1 cm autorski = 10 mm modelu
PS = 20.0     # skala druku 1:20 -> mnoznik anotacji
FD = 8.0      # powiekszenie detalu: 1:20 -> 1:2.5 (20/2.5)

doc = ezdxf.new("R2013", setup=True)
doc.header["$INSUNITS"] = 4
doc.header["$MEASUREMENT"] = 1
msp = doc.modelspace()
if "ARIAL" not in doc.styles:
    doc.styles.add("ARIAL", font="arial.ttf")

for n, col, lt in [("KONTUR", 7, "Continuous"), ("OSIE", 1, "CENTER"),
                   ("WYMIARY", 3, "Continuous"), ("OPISY", 5, "Continuous"),
                   ("KRESKOWANIE", 8, "Continuous")]:
    if n not in doc.layers:
        doc.layers.add(n, color=col, linetype=lt)

ds = doc.dimstyles.add("ISO")
for k, v in dict(dimtxt=2.5, dimasz=2.5, dimexe=1.0, dimexo=2.0, dimgap=1.0,
                 dimtad=1, dimtsz=0.0, dimdec=0, dimlfac=1.0, dimscale=PS,
                 dimclrt=3, dimtxsty="ARIAL", dimblk="").items():
    ds.set_dxf_attrib(k, v)
# styl wymiarowy dla detali (geometria x8 -> dimlfac 1/8, tekst mm na papierze)
dsd = doc.dimstyles.add("ISOD")
for k, v in dict(dimtxt=2.5, dimasz=2.5, dimexe=1.0, dimexo=2.0, dimgap=1.0,
                 dimtad=1, dimtsz=0.0, dimdec=0, dimlfac=1.0 / FD, dimscale=PS,
                 dimclrt=3, dimtxsty="ARIAL", dimblk="").items():
    dsd.set_dxf_attrib(k, v)

# -------------------------------------------------------------- primitywy (cm)
def L(x1, y1, x2, y2, layer="KONTUR", lt=None):
    a = {"layer": layer}
    if lt: a["linetype"] = lt
    msp.add_line((x1 * MM, y1 * MM), (x2 * MM, y2 * MM), dxfattribs=a)

def P(pts, layer="KONTUR", closed=False, lt=None):
    a = {"layer": layer}
    if lt: a["linetype"] = lt
    msp.add_lwpolyline([(x * MM, y * MM) for x, y in pts], close=closed, dxfattribs=a)

def C(cx, cy, r, layer="KRESKOWANIE"):
    msp.add_circle((cx * MM, cy * MM), r * MM, dxfattribs={"layer": layer})

def T(s, x, y, mm=3.5, align=MA.MIDDLE_LEFT, layer="OPISY", rot=0):
    m = msp.add_mtext(s, dxfattribs={"layer": layer, "style": "ARIAL",
                                     "char_height": mm * PS, "rotation": rot})
    m.set_location((x * MM, y * MM), attachment_point=align)
    return m

def DIMH(x1, x2, ydim, yref, style="ISO"):
    d = msp.add_linear_dim(base=(x1 * MM, ydim * MM), p1=(x1 * MM, yref * MM),
                           p2=(x2 * MM, yref * MM), angle=0, dimstyle=style,
                           dxfattribs={"layer": "WYMIARY"})
    d.render()

def DIMV(y1, y2, xdim, xref, style="ISO"):
    d = msp.add_linear_dim(base=(xdim * MM, y1 * MM), p1=(xref * MM, y1 * MM),
                           p2=(xref * MM, y2 * MM), angle=90, dimstyle=style,
                           dxfattribs={"layer": "WYMIARY"})
    d.render()

def LEAD(text, target, insert, side=mleader.ConnectionSide.left, mm=2.5):
    ml = msp.add_multileader_mtext("Standard")
    ml.multileader.dxf.layer = "OPISY"
    ml.set_content(text, style="ARIAL", char_height=mm,
                   alignment=mleader.TextAlignment.left)
    ml.set_overall_scaling(PS)
    ml.add_leader_line(side, [Vec2(target[0] * MM, target[1] * MM)])
    ml.build(insert=Vec2(insert[0] * MM, insert[1] * MM))

def hatch_poly(pts, spacing, ang, layer="KRESKOWANIE"):
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    projs = [px * nx + py * ny for px, py in pts]
    s0, s1 = min(projs), max(projs)
    edges = list(zip(pts, pts[1:] + pts[:1]))
    s = s0 + spacing / 2
    while s < s1:
        qx, qy = s * nx, s * ny; ts = []
        for (ax, ay), (bx, by) in edges:
            ex, ey = bx - ax, by - ay
            det = ex * dy - dx * ey
            if abs(det) < 1e-9: continue
            rx, ry = ax - qx, ay - qy
            t = (-rx * ey + ex * ry) / det
            u = (dx * ry - dy * rx) / det
            if -1e-9 <= u <= 1 + 1e-9: ts.append(t)
        ts.sort()
        for i in range(0, len(ts) - 1, 2):
            L(qx + ts[i] * dx, qy + ts[i] * dy, qx + ts[i + 1] * dx, qy + ts[i + 1] * dy, layer)
        s += spacing

def xhatch_poly(pts, spacing, layer="KRESKOWANIE"):
    hatch_poly(pts, spacing, 45, layer); hatch_poly(pts, spacing, 135, layer)

def dots(x1, y1, x2, y2, dx=6, dy=4, r=0.5, layer="KRESKOWANIE"):
    row = 0; y = y1 + dy / 2
    while y < y2:
        x = x1 + dx / 2 + (dx / 2 if row % 2 else 0)
        while x < x2: C(x, y, r, layer); x += dx
        y += dy; row += 1

def triangles(x1, y1, x2, y2, s=4.5, dx=10, dy=7, layer="KRESKOWANIE"):
    row = 0; y = y1 + dy / 2
    while y + s / 2 < y2:
        x = x1 + dx / 2 + (dx / 2 if row % 2 else 0)
        while x + s / 2 < x2:
            P([(x - s / 2, y - s / 3), (x, y + s / 2), (x + s / 2, y - s / 3)], layer, closed=True)
            x += dx
        y += dy; row += 1

def stones(x1, y1, x2, y2, r=3.0, dx=11, dy=10, layer="KRESKOWANIE"):
    row = 0; y = y1 + dy / 2
    while y < y2 - r + 1:
        x = x1 + dx / 2 + (dx / 2 if row % 2 else 0)
        while x < x2 - r + 1: C(x, y, r, layer); x += dx
        y += dy; row += 1

def chevron(tip, ang_deg, size=6, layer="OSIE"):
    a = math.radians(ang_deg)
    for da in (math.radians(150), math.radians(-150)):
        L(tip[0], tip[1], tip[0] + size * math.cos(a + da),
          tip[1] + size * math.sin(a + da), layer)

def foliage(cx, cy, w=18, layer="KRESKOWANIE"):
    """prosty symbol rosliny (trawa/paproc) — kilka luków w gore."""
    for i in range(-3, 4):
        x = cx + i * (w / 7.0)
        h = w * (0.9 - abs(i) * 0.12)
        msp.add_spline([(x * MM, cy * MM), ((x + i) * MM, (cy + h * 0.6) * MM),
                        ((cx + i * 1.5) * MM, (cy + h) * MM)], dxfattribs={"layer": layer})

# ============================================================ PARAMETRY (cm)
SEAT_L, SEAT_D, SEAT_TOP, BLAT = 120, 50, 42, 8
DON_D, DON_H, WALL = 40, 90, 8
FND = 40

# ============================================================ 1. RZUT Z GORY
RX, RY = 80, 610
def R(x, y): return (RX + x, RY + y)
def rzut():
    P([R(0, 0), R(SEAT_L, 0), R(SEAT_L, SEAT_D), R(0, SEAT_D)], "KONTUR", closed=True)          # siedzisko
    P([R(0, SEAT_D), R(SEAT_L, SEAT_D), R(SEAT_L, SEAT_D + DON_D), R(0, SEAT_D + DON_D)], "KONTUR", closed=True)  # donica
    P([R(WALL, SEAT_D + WALL), R(SEAT_L - WALL, SEAT_D + WALL),
       R(SEAT_L - WALL, SEAT_D + DON_D - WALL), R(WALL, SEAT_D + DON_D - WALL)], "KONTUR", closed=True)  # wnetrze
    stones(RX + 0, RY + 0, RX + SEAT_L, RY + SEAT_D, r=2.4, dx=13, dy=12)                        # kamien (rzut)
    for cx in (30, 60, 90):                                                                      # rosliny
        foliage(RX + cx, RY + SEAT_D + 14, 16)
    # linie ciecia
    L(*R(60, -16), *R(60, SEAT_D + DON_D + 16), "OSIE")
    chevron(R(60, -16), -90, 7); chevron(R(60, SEAT_D + DON_D + 16), 90, 7)
    T("A", *R(60, -26), 3.5, MA.MIDDLE_CENTER); T("A", *R(60, SEAT_D + DON_D + 24), 3.5, MA.MIDDLE_CENTER)
    L(*R(-16, 25), *R(SEAT_L + 16, 25), "OSIE")
    chevron(R(-16, 25), 180, 7); chevron(R(SEAT_L + 16, 25), 0, 7)
    T("B", *R(-26, 25), 3.5, MA.MIDDLE_CENTER); T("B", *R(SEAT_L + 26, 25), 3.5, MA.MIDDLE_CENTER)
    DIMH(RX, RX + SEAT_L, RY - 40, RY)
    DIMV(RY, RY + SEAT_D, RX - 22, RX)
    DIMV(RY + SEAT_D, RY + SEAT_D + DON_D, RX - 22, RX)
    T("siedzisko — kamień", *R(60, 40), 2.5, MA.MIDDLE_CENTER)
    T("donica żelbetowa + rośliny", *R(60, SEAT_D + 22), 2.5, MA.MIDDLE_CENTER)
    T("RZUT Z GÓRY   1:20", *R(60, SEAT_D + DON_D + 40), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 2. PRZEKROJ A-A (glebokosc)
AX, AY = 120, 250
def A(y, z): return (AX + y, AY + z)
def przekroj_AA():
    # grunt
    L(*A(-18, 0), *A(SEAT_D + DON_D + 18, 0), "KONTUR")
    # blat kamienny + noga
    P([A(0, SEAT_TOP - BLAT), A(SEAT_D, SEAT_TOP - BLAT), A(SEAT_D, SEAT_TOP), A(0, SEAT_TOP)], "KONTUR", closed=True)
    P([A(6, 0), A(14, 0), A(14, SEAT_TOP - BLAT), A(6, SEAT_TOP - BLAT)], "KONTUR", closed=True)
    stones(AX + 0, AY + SEAT_TOP - BLAT, AX + SEAT_D, AY + SEAT_TOP, r=1.7, dx=8, dy=6)
    stones(AX + 6, AY + 0, AX + 14, AY + SEAT_TOP - BLAT, r=1.6, dx=7, dy=7)
    # donica: sciany + dno
    fy = SEAT_D
    P([A(fy, 0), A(fy + WALL, 0), A(fy + WALL, DON_H), A(fy, DON_H)], "KONTUR", closed=True)             # przednia
    P([A(fy + DON_D - WALL, 0), A(fy + DON_D, 0), A(fy + DON_D, DON_H), A(fy + DON_D - WALL, DON_H)], "KONTUR", closed=True)  # tylna
    P([A(fy, 0), A(fy + DON_D, 0), A(fy + DON_D, WALL), A(fy, WALL)], "KONTUR", closed=True)             # dno
    xhatch_poly([A(fy, 0), A(fy + WALL, 0), A(fy + WALL, DON_H), A(fy, DON_H)], 7)
    xhatch_poly([A(fy + DON_D - WALL, 0), A(fy + DON_D, 0), A(fy + DON_D, DON_H), A(fy + DON_D - WALL, DON_H)], 7)
    xhatch_poly([A(fy, 0), A(fy + DON_D, 0), A(fy + DON_D, WALL), A(fy, WALL)], 7)
    # ziemia + drenaz w donicy
    ix1, ix2 = fy + WALL, fy + DON_D - WALL
    triangles(AX + ix1, AY + WALL, AX + ix2, AY + WALL + 8)                     # drenaz zwir
    dots(AX + ix1, AY + WALL + 8, AX + ix2, AY + DON_H - 12, dx=7, dy=6, r=0.6)  # ziemia
    for cx in (ix1 + 6, (ix1 + ix2) / 2, ix2 - 6):
        foliage(AX + cx, AY + DON_H - 10, 16)
    # fundamenty
    P([A(fy - 2, 0), A(fy + DON_D + 2, 0), A(fy + DON_D + 2, -FND), A(fy - 2, -FND)], "KONTUR", closed=True)
    hatch_poly([A(fy - 2, 0), A(fy + DON_D + 2, 0), A(fy + DON_D + 2, -FND), A(fy - 2, -FND)], 6, 45)
    P([A(2, 0), A(18, 0), A(18, -FND), A(2, -FND)], "KONTUR", closed=True)
    hatch_poly([A(2, 0), A(18, 0), A(18, -FND), A(2, -FND)], 6, 45)
    # grunt rodzimy (boki + srodek)
    hatch_poly([A(-18, 0), A(2, 0), A(2, -FND - 12), A(-18, -FND - 12)], 20, 45)
    hatch_poly([A(18, 0), A(fy - 2, 0), A(fy - 2, -FND - 12), A(18, -FND - 12)], 20, 45)
    hatch_poly([A(fy + DON_D + 2, 0), A(fy + DON_D + 18, 0), A(fy + DON_D + 18, -FND - 12), A(fy + DON_D + 2, -FND - 12)], 20, 45)
    # wymiary
    DIMH(AX, AX + SEAT_D, AY - 24, AY)
    DIMH(AX + SEAT_D, AX + SEAT_D + DON_D, AY - 24, AY)
    DIMV(AY, AY + SEAT_TOP, AX - 20, AX)
    DIMV(AY, AY + DON_H, AX + SEAT_D + DON_D + 22, AX + SEAT_D + DON_D)
    DIMV(AY - FND, AY, AX - 20, AX + 2)
    # odnosniki
    LEAD("blat kamienny gr. 8 cm\n(granit płomieniowany)", A(25, SEAT_TOP), (AX - 60, AY + 78))
    LEAD("noga ukryta — blat „lewituje”", A(10, 20), (AX - 60, AY + 55))
    LEAD("donica żelbetowa: beton C30/37 XF3,\nnapowietrzany W8, ścianka 8 cm, siatka Ø8", A(fy + DON_D, 70), (AX + SEAT_D + DON_D + 30, AY + 82), mleader.ConnectionSide.right)
    LEAD("ziemia + rośliny cieniolubne\n(tawułka, paprocie, wiciokrzew, bluszcz)", A((ix1 + ix2) / 2, DON_H - 20), (AX + SEAT_D + DON_D + 30, AY + 58), mleader.ConnectionSide.right)
    LEAD("drenaż: żwir 8–16 mm + geowłóknina,\notwory spustowe w dnie", A((ix1 + ix2) / 2, WALL + 4), (AX + SEAT_D + DON_D + 30, AY + 30), mleader.ConnectionSide.right)
    LEAD("ława fundamentowa: chudy beton C8/10,\nposadowienie poniżej przemarzania", A(fy + DON_D, -FND + 6), (AX + SEAT_D + DON_D + 30, AY - 34), mleader.ConnectionSide.right)
    LEAD("grunt rodzimy zagęszczony", A(-8, -20), (AX - 60, AY - 30))
    T("A", *A(-30, DON_H + 6), 3.5, MA.MIDDLE_CENTER); T("A", *A(SEAT_D + DON_D + 30, DON_H + 6), 3.5, MA.MIDDLE_CENTER)
    T("PRZEKRÓJ A-A   1:20", *A((SEAT_D + DON_D) / 2, DON_H + 26), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 3. PRZEKROJ B-B (dlugosc)
BX, BY = 430, 250
def B(x, z): return (BX + x, BY + z)
def przekroj_BB():
    L(*B(-18, 0), *B(SEAT_L + 18, 0), "KONTUR")
    # donica w tle (widok)
    P([B(0, 0), B(SEAT_L, 0), B(SEAT_L, DON_H), B(0, DON_H)], "KONTUR")
    L(*B(0, DON_H - 12), *B(SEAT_L, DON_H - 12), "KONTUR")
    for cx in range(12, SEAT_L, 20):
        foliage(BX + cx, BY + DON_H - 8, 15)
    # blat kamienny (przeciety)
    P([B(0, SEAT_TOP - BLAT), B(SEAT_L, SEAT_TOP - BLAT), B(SEAT_L, SEAT_TOP), B(0, SEAT_TOP)], "KONTUR", closed=True)
    stones(BX + 0, BY + SEAT_TOP - BLAT, BX + SEAT_L, BY + SEAT_TOP, r=1.7, dx=9, dy=6)
    # nogi (widok)
    for lx in (6, SEAT_L - 14):
        P([B(lx, 0), B(lx + 8, 0), B(lx + 8, SEAT_TOP - BLAT), B(lx, SEAT_TOP - BLAT)], "KONTUR")
    DIMH(BX, BX + SEAT_L, BY - 24, BY)
    DIMV(BY, BY + SEAT_TOP, BX - 20, BX)
    DIMV(BY, BY + DON_H, BX + SEAT_L + 22, BX + SEAT_L)
    T("donica za siedziskiem (widok)", *B(SEAT_L / 2, DON_H + 8), 2.5, MA.MIDDLE_CENTER)
    T("B", *B(-30, DON_H + 6), 3.5, MA.MIDDLE_CENTER); T("B", *B(SEAT_L + 30, DON_H + 6), 3.5, MA.MIDDLE_CENTER)
    T("PRZEKRÓJ B-B   1:20", *B(SEAT_L / 2, DON_H + 26), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 4. WIDOK OD FRONTU
FX, FY = 720, 610
def F(x, z): return (FX + x, FY + z)
def widok_front():
    P([F(0, 0), F(SEAT_L, 0), F(SEAT_L, DON_H), F(0, DON_H)], "KONTUR")     # donica
    L(*F(0, DON_H - 12), *F(SEAT_L, DON_H - 12), "KONTUR")
    for cx in range(12, SEAT_L, 18):
        foliage(FX + cx, FY + DON_H - 6, 14)
    P([F(0, SEAT_TOP - BLAT), F(SEAT_L, SEAT_TOP - BLAT), F(SEAT_L, SEAT_TOP), F(0, SEAT_TOP)], "KONTUR", closed=True)  # blat
    for lx in (6, SEAT_L - 14):
        P([F(lx, 0), F(lx + 8, 0), F(lx + 8, SEAT_TOP - BLAT), F(lx, SEAT_TOP - BLAT)], "KONTUR")
    DIMH(FX, FX + SEAT_L, FY - 22, FY)
    DIMV(FY, FY + SEAT_TOP, FX - 20, FX)
    T("WIDOK OD FRONTU   1:20", *F(SEAT_L / 2, DON_H + 24), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 5. WIDOK Z BOKU
SX, SY = 960, 610
def S(y, z): return (SX + y, SY + z)
def widok_bok():
    L(*S(-10, 0), *S(SEAT_D + DON_D + 10, 0), "KONTUR")
    P([S(SEAT_D, 0), S(SEAT_D + DON_D, 0), S(SEAT_D + DON_D, DON_H), S(SEAT_D, DON_H)], "KONTUR", closed=True)  # donica
    for cx in ((SEAT_D + SEAT_D + DON_D) / 2,):
        foliage(SX + cx, SY + DON_H - 4, 16)
    P([S(0, SEAT_TOP - BLAT), S(SEAT_D, SEAT_TOP - BLAT), S(SEAT_D, SEAT_TOP), S(0, SEAT_TOP)], "KONTUR", closed=True)  # blat
    P([S(6, 0), S(14, 0), S(14, SEAT_TOP - BLAT), S(6, SEAT_TOP - BLAT)], "KONTUR", closed=True)  # noga
    # fundament niewidoczny
    L(*S(SEAT_D - 2, 0), *S(SEAT_D - 2, -FND), "KONTUR", lt="DASHED")
    L(*S(SEAT_D - 2, -FND), *S(SEAT_D + DON_D + 2, -FND), "KONTUR", lt="DASHED")
    L(*S(SEAT_D + DON_D + 2, -FND), *S(SEAT_D + DON_D + 2, 0), "KONTUR", lt="DASHED")
    DIMV(SY, SY + DON_H, SX + SEAT_D + DON_D + 22, SX + SEAT_D + DON_D)
    DIMH(SX, SX + SEAT_D, SY - 20, SY)
    DIMH(SX + SEAT_D, SX + SEAT_D + DON_D, SY - 20, SY)
    T("fundament (linia ukryta)", *S(SEAT_D + DON_D / 2, -FND - 8), 2.5, MA.MIDDLE_CENTER)
    T("WIDOK Z BOKU   1:20", *S((SEAT_D + DON_D) / 2, DON_H + 24), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 6. RZUT FUNDAMENTOW
QX, QY = 90, 90
def Q(x, y): return (QX + x, QY + y)
def rzut_fund():
    P([Q(0, SEAT_D - 2), Q(SEAT_L, SEAT_D - 2), Q(SEAT_L, SEAT_D + DON_D + 2), Q(0, SEAT_D + DON_D + 2)], "KONTUR", closed=True)  # lawa donicy
    hatch_poly([Q(0, SEAT_D - 2), Q(SEAT_L, SEAT_D - 2), Q(SEAT_L, SEAT_D + DON_D + 2), Q(0, SEAT_D + DON_D + 2)], 7, 45)
    for lx in (2, SEAT_L - 18):
        P([Q(lx, 2), Q(lx + 16, 2), Q(lx + 16, 18), Q(lx, 18)], "KONTUR", closed=True)
        hatch_poly([Q(lx, 2), Q(lx + 16, 2), Q(lx + 16, 18), Q(lx, 18)], 5, 45)
    P([Q(0, 0), Q(SEAT_L, 0), Q(SEAT_L, SEAT_D + DON_D), Q(0, SEAT_D + DON_D)], "KONTUR", lt="DASHED")  # obrys lawki
    DIMH(QX, QX + SEAT_L, QY - 20, QY)
    DIMV(QY + SEAT_D - 2, QY + SEAT_D + DON_D + 2, QX - 20, QX)
    LEAD("ława pod donicą — chudy beton C8/10,\ngł. poniżej przemarzania", Q(SEAT_L / 2, SEAT_D + DON_D / 2), (QX + SEAT_L + 24, QY + SEAT_D + DON_D), mleader.ConnectionSide.right)
    LEAD("stopy pod nogami siedziska", Q(10, 10), (QX + SEAT_L + 24, QY + 6), mleader.ConnectionSide.right)
    T("RZUT FUNDAMENTÓW   1:20", *Q(SEAT_L / 2, SEAT_D + DON_D + 22), 5.0, MA.MIDDLE_CENTER)

# ============================================================ 7. DETAL 1 — styk blat/donica (1:2.5)
D1X, D1Y = 740, 300
def d1(y, z): return (D1X + y * FD, D1Y + z * FD)
def detal1():
    # fragment: gorny naroznik donicy + koniec blatu (real cm, x8)
    P([d1(0, 0), d1(8, 0), d1(8, 22), d1(0, 22)], "KONTUR", closed=True)      # sciana donicy (przekroj)
    xhatch_poly([d1(0, 0), d1(8, 0), d1(8, 22), d1(0, 22)], 0.9)
    P([d1(-16, 6), d1(-2, 6), d1(-2, 14), d1(-16, 14)], "KONTUR", closed=True)  # blat kamienny
    stones(D1X - 16 * FD, D1Y + 6 * FD, D1X - 2 * FD, D1Y + 14 * FD, r=0.28 * FD, dx=1.2 * FD, dy=1.1 * FD)
    L(*d1(-2, 5), *d1(-2, 15), "KONTUR")                                       # szczelina cienia / dylatacja
    msp.add_line((d1(-2, 10)[0] * MM, d1(-2, 10)[1] * MM), (d1(6, 10)[0] * MM, d1(6, 10)[1] * MM),
                 dxfattribs={"layer": "KONTUR"})                               # kotwa nierdzewna
    C(*d1(-9, 10), 0.4 * FD, "KONTUR")                                          # otwor na kotwe
    DIMV(D1Y + 6 * FD, D1Y + 14 * FD, D1X - 20 * FD, D1X - 16 * FD, "ISOD")     # gr. blatu 8
    LEAD("kotwa nierdzewna A2 M8\n(otwór wiercony w blacie)", d1(2, 10), (D1X + 14 * FD, D1Y + 18 * FD), mleader.ConnectionSide.right)
    LEAD("podkładka elastyczna + szczelina\ndylatacyjna 2 mm (kamień × beton)", d1(-2, 12), (D1X + 14 * FD, D1Y + 10 * FD), mleader.ConnectionSide.right)
    LEAD("blat: kamień naturalny gr. 8 cm", d1(-9, 8), (D1X - 20 * FD, D1Y - 2 * FD))
    T("DETAL 1 — styk kamień/beton   1:2.5", D1X - 2 * FD, D1Y + 26 * FD, 3.5, MA.MIDDLE_CENTER)

# ============================================================ 8. DETAL 2 — posadowienie + drenaz (1:2.5)
D2X, D2Y = 740, 110
def d2(y, z): return (D2X + y * FD, D2Y + z * FD)
def detal2():
    # sciana + dno donicy + lawa + grunt (real cm x8)
    P([d2(0, 0), d2(8, 0), d2(8, 20), d2(0, 20)], "KONTUR", closed=True)        # sciana
    xhatch_poly([d2(0, 0), d2(8, 0), d2(8, 20), d2(0, 20)], 0.9)
    P([d2(0, 0), d2(24, 0), d2(24, 6), d2(0, 6)], "KONTUR", closed=True)        # dno donicy
    xhatch_poly([d2(0, 0), d2(24, 0), d2(24, 6), d2(0, 6)], 0.9)
    triangles(D2X + 8 * FD, D2Y + 6 * FD, D2X + 24 * FD, D2Y + 12 * FD, s=0.5 * FD, dx=1.1 * FD, dy=0.9 * FD)  # zwir drenaz
    C(*d2(4, 3), 0.6 * FD, "KONTUR")                                            # otwor spustowy
    P([d2(-4, 0), d2(28, 0), d2(28, -10), d2(-4, -10)], "KONTUR", closed=True)  # lawa
    hatch_poly([d2(-4, 0), d2(28, 0), d2(28, -10), d2(-4, -10)], 0.8, 45)
    hatch_poly([d2(-4, -10), d2(28, -10), d2(28, -18), d2(-4, -18)], 2.4, 45)   # grunt
    DIMV(D2Y - 10 * FD, D2Y, D2X + 32 * FD, D2X + 28 * FD, "ISOD")
    LEAD("otwór spustowy Ø50 + geowłóknina", d2(4, 3), (D2X + 30 * FD, D2Y + 14 * FD), mleader.ConnectionSide.right)
    LEAD("drenaż: żwir płukany 8–16 mm", d2(16, 8), (D2X + 30 * FD, D2Y + 8 * FD), mleader.ConnectionSide.right)
    LEAD("ława: chudy beton C8/10", d2(24, -5), (D2X + 30 * FD, D2Y - 4 * FD), mleader.ConnectionSide.right)
    LEAD("grunt rodzimy zagęszczony", d2(0, -14), (D2X - 8 * FD, D2Y - 14 * FD))
    T("DETAL 2 — posadowienie + drenaż   1:2.5", D2X + 12 * FD, D2Y + 24 * FD, 3.5, MA.MIDDLE_CENTER)

# ============================================================ 9. LEGENDA
def legenda():
    lx, ly = 430, 150
    T("LEGENDA", lx, ly + 12, 3.5, MA.MIDDLE_LEFT)
    items = [("kamień naturalny", "stone"), ("żelbet (donica)", "x"),
             ("beton (ława)", "diag"), ("żwir / drenaż", "tri"), ("grunt rodzimy", "diag2")]
    y = ly
    for name, kind in items:
        bx, by = lx, y - 6
        P([(bx, by), (bx + 16, by), (bx + 16, by + 8), (bx, by + 8)], "KONTUR", closed=True)
        if kind == "stone": stones(bx, by, bx + 16, by + 8, r=1.2, dx=6, dy=5)
        elif kind == "x": xhatch_poly([(bx, by), (bx + 16, by), (bx + 16, by + 8), (bx, by + 8)], 3)
        elif kind == "diag": hatch_poly([(bx, by), (bx + 16, by), (bx + 16, by + 8), (bx, by + 8)], 3, 45)
        elif kind == "tri": triangles(bx, by, bx + 16, by + 8, s=3, dx=6, dy=5)
        elif kind == "diag2": hatch_poly([(bx, by), (bx + 16, by), (bx + 16, by + 8), (bx, by + 8)], 6, 45)
        T(name, bx + 22, y - 2, 2.5, MA.MIDDLE_LEFT)
        y -= 14

# ============================================================ 10. WYKAZ MATERIALOW
def table(x, y, title, rows, col_w=(14, 165, 30, 34, 70), row_h=12):
    tw = sum(col_w)
    T(title, x, y + 10, 3.5, MA.MIDDLE_LEFT)
    n = len(rows) + 1
    for i in range(n + 1):
        L(x, y - i * row_h, x + tw, y - i * row_h, "KONTUR")
    cx = x
    L(cx, y, cx, y - n * row_h, "KONTUR")
    for w in col_w:
        cx += w; L(cx, y, cx, y - n * row_h, "KONTUR")
    heads = ["Lp.", "Rodzaj materiału budowlanego", "Jedn.", "Ilość", "Producent / norma"]
    cx = x
    for w, hc in zip(col_w, heads):
        T(hc, cx + w / 2, y - row_h / 2, 2.5, MA.MIDDLE_CENTER); cx += w
    for r, row in enumerate(rows, start=1):
        cy = y - r * row_h - row_h / 2; cx = x
        vals = [str(r)] + list(row)
        for w, v in zip(col_w, vals):
            if w == col_w[1]: T(v, cx + 4, cy, 2.5, MA.MIDDLE_LEFT)
            else: T(v, cx + w / 2, cy, 2.5, MA.MIDDLE_CENTER)
            cx += w

def wykaz():
    rows = [
        ("blat kamienny — granit płomieniowany gr. 8 cm", "m²", "0,60", "wg dostawcy"),
        ("beton C30/37 XF3, napowietrzany W8 — donica", "m³", "0,45", "PN-EN 206"),
        ("siatka zbrojeniowa Ø8, oczko 10×10 cm", "m²", "3,5", "B500B"),
        ("beton C8/10 — ława / posadowienie", "m³", "0,50", "PN-EN 206"),
        ("kotwy nierdzewne A2 M8", "szt.", "6", "DIN 976"),
        ("żwir płukany f. 8–16 mm — drenaż", "m³", "0,10", "PN-EN 13043"),
        ("geowłóknina PP 200 g/m²", "m²", "1,8", "—"),
        ("ziemia urodzajna — donica", "m³", "0,12", "—"),
    ]
    table(430, 120, "TABELA — wykaz i specyfikacja materiałów", rows)

# ============================================================ 11. TABELKA RYSUNKOWA
def tabelka():
    x, y, w, h = 790, 40, 360, 118
    P([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], "KONTUR", closed=True)
    L(x, y + h - 30, x + w, y + h - 30, "KONTUR")
    L(x, y + h - 60, x + w, y + h - 60, "KONTUR")
    L(x, y + 24, x + w, y + 24, "KONTUR")
    L(x + 190, y + h - 60, x + 190, y + h, "KONTUR")
    L(x + 120, y, x + 120, y + 24, "KONTUR")
    L(x + 240, y, x + 240, y + 24, "KONTUR")
    info = ["Kierunek: Architektura krajobrazu, WBiIŚ SGGW",
            "Rok II, sem. 4, rok akad. 2025/2026",
            "Przedmiot: Budowa obiektów architektury krajobrazu 2"]
    for i, s in enumerate(info):
        T(s, x + 6, y + h - 8 - i * 8, 2.5, MA.MIDDLE_LEFT)
    T("Temat: projekt wykonawczy ławki", x + 6, y + h - 44, 3.5, MA.MIDDLE_LEFT)
    T("Arkusz: rzuty, przekroje i detale", x + 196, y + h - 40, 2.5, MA.MIDDLE_LEFT)
    T("Wykonała: Pola Organiszczak", x + 6, y + h - 74, 2.5, MA.MIDDLE_LEFT)
    T("Sprawdziła: dr hab. E. Rosłon-Szeryńska", x + 196, y + h - 74, 2.5, MA.MIDDLE_LEFT)
    T("Skala: 1:20 / 1:2.5", x + 6, y + 12, 2.5, MA.MIDDLE_LEFT)
    T("Data:", x + 126, y + 12, 2.5, MA.MIDDLE_LEFT)
    T("Ocena:", x + 246, y + 12, 2.5, MA.MIDDLE_LEFT)

# ============================================================ ZLOZENIE ARKUSZA A2
SW, SH = 1188, 840
P([(0, 0), (SW, 0), (SW, SH), (0, SH)], "KONTUR", closed=True)
P([(20, 20), (SW - 20, 20), (SW - 20, SH - 20), (20, SH - 20)], "KONTUR", closed=True)

rzut(); przekroj_AA(); przekroj_BB(); widok_front(); widok_bok()
rzut_fund(); detal1(); detal2(); legenda(); wykaz(); tabelka()

TS = datetime.datetime.now().strftime("%Y-%m-%d_godz%H-%M")
_dxf = "outputs/%s_lawka.dxf" % TS
_png = "outputs/%s_lawka_preview.png" % TS
doc.saveas(_dxf)
print("OK zapisano", _dxf)
print("encje:", sorted({e.dxftype() for e in msp}))
from ezdxf.addons.drawing import matplotlib as _mpl
_mpl.qsave(msp, _png, size_inches=(16.5, 16.5 * SH / SW), dpi=160, bg="#FFFFFF")
print("OK podglad", _png)

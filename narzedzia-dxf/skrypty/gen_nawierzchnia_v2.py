# -*- coding: utf-8 -*-
"""
NAWIERZCHNIE OGRODOWE — projekt wykonawczy, wg standardu wytyczne/WYTYCZNE_DXF.md.

- DXF R2013 ASCII, model 1:1 w MILIMETRACH (autoruję w cm, konwersja ×10 -> mm).
- rzeczywiste encje: LINE / LWPOLYLINE / CIRCLE / MTEXT / DIMENSION / MULTILEADER.
- BEZ bloków/proxy, BEZ HATCH (kreskowanie liniami), BEZ SOLID/pełnych grotów,
  BEZ grotów OBLIQUE (groty ISO, dimtsz=0).
- warstwy: KONTUR / OSIE / WYMIARY / OPISY / KRESKOWANIE.
- font Arial (polskie znaki), teksty 2.5/3.5/5.0 mm na papierze.
- Skala arkusza 1:100 (model_mm × 0,01 = paper_mm). Plan 1:100, przekroje/detale 1:10
  (geometria przekrojów blownięta ×S=10 -> na arkuszu 1:100 daje efekt 1:10).
"""
import math
import ezdxf
from ezdxf.math import Vec2
from ezdxf.enums import MTextEntityAlignment as MA
from ezdxf.render import mleader

MM = 10.0        # 1 cm autorski = 10 mm modelu
SHEET = 100.0    # skala druku arkusza 1:100 -> paper_mm = model_mm/100; anotacje ×SHEET
S = 10.0         # lokalny mnoznik przekrojow/detali -> efekt 1:10

# ------------------------------------------------------------------ setup
doc = ezdxf.new("R2013", setup=True)
doc.header["$INSUNITS"] = 4
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

# dimstyle: PLANM (plan, w metrach), DET (przekroje/detale, w cm) — groty ISO
def _mkdim(name, lfac, dec, txt):
    ds = doc.dimstyles.add(name)
    for k, v in dict(dimtxt=txt, dimasz=txt, dimexe=1.25, dimexo=2.0, dimgap=1.0,
                     dimtad=1, dimtsz=0.0, dimdec=dec, dimlfac=lfac, dimscale=SHEET,
                     dimclrt=3, dimtxsty="ARIAL", dimblk="").items():
        ds.set_dxf_attrib(k, v)
    return ds
_mkdim("PLANM", 0.001, 2, 3.5)   # mm -> m
_mkdim("DET",   0.01,  0, 2.5)   # mm(×S) -> cm

# ------------------------------------------------------------------ primitywy (autor w cm, ×MM)
def L(x1, y1, x2, y2, layer="KONTUR", lt=None, ox=0, oy=0):
    a = {"layer": layer}
    if lt: a["linetype"] = lt
    msp.add_line(((ox + x1) * MM, (oy + y1) * MM), ((ox + x2) * MM, (oy + y2) * MM), dxfattribs=a)

def R(x, y, w, h, layer="KONTUR", lt=None, ox=0, oy=0):
    a = {"layer": layer}
    if lt: a["linetype"] = lt
    msp.add_lwpolyline([((ox + x) * MM, (oy + y) * MM), ((ox + x + w) * MM, (oy + y) * MM),
                        ((ox + x + w) * MM, (oy + y + h) * MM), ((ox + x) * MM, (oy + y + h) * MM)],
                       close=True, dxfattribs=a)

def P(pts, layer="KONTUR", closed=True, lt=None, ox=0, oy=0):
    a = {"layer": layer}
    if lt: a["linetype"] = lt
    msp.add_lwpolyline([((ox + p[0]) * MM, (oy + p[1]) * MM) for p in pts], close=closed, dxfattribs=a)

def C(cx, cy, r, layer="KRESKOWANIE", ox=0, oy=0):
    msp.add_circle(((ox + cx) * MM, (oy + cy) * MM), r * MM, dxfattribs={"layer": layer})

def _pmm(h):  # legacy cm-height -> paper mm {2.5,3.5,5.0}
    return 2.5 if h <= 27 else (3.5 if h <= 37 else 5.0)

def T(s, x, y, h=24, align=MA.MIDDLE_LEFT, layer="OPISY", rot=0, ox=0, oy=0):
    m = msp.add_mtext(s, dxfattribs={"layer": layer, "style": "ARIAL",
                                     "char_height": _pmm(h) * SHEET, "rotation": rot})
    m.set_location(((ox + x) * MM, (oy + y) * MM), attachment_point=align)
    return m

def HDIM(x1, x2, y, off, style="PLANM", ox=0, oy=0):
    d = msp.add_linear_dim(base=((ox + x1) * MM, (oy + y + off) * MM),
                           p1=((ox + x1) * MM, (oy + y) * MM), p2=((ox + x2) * MM, (oy + y) * MM),
                           angle=0, dimstyle=style, dxfattribs={"layer": "WYMIARY"})
    d.render()

def VDIM(y1, y2, x, off, style="PLANM", ox=0, oy=0):
    d = msp.add_linear_dim(base=((ox + x + off) * MM, (oy + y1) * MM),
                           p1=((ox + x) * MM, (oy + y1) * MM), p2=((ox + x) * MM, (oy + y2) * MM),
                           angle=90, dimstyle=style, dxfattribs={"layer": "WYMIARY"})
    d.render()

def DDIM(p1, p2, base, angle=0):   # przekroje/detale (autor ×S), styl DET
    d = msp.add_linear_dim(base=(base[0] * MM, base[1] * MM),
                           p1=(p1[0] * MM, p1[1] * MM), p2=(p2[0] * MM, p2[1] * MM),
                           angle=angle, dimstyle="DET", dxfattribs={"layer": "WYMIARY"})
    d.render()

def LEAD(text, target, insert, side=mleader.ConnectionSide.left, h=2.5, ox=0, oy=0):
    ml = msp.add_multileader_mtext("Standard")
    ml.multileader.dxf.layer = "OPISY"
    ml.set_content(text, style="ARIAL", char_height=h, alignment=mleader.TextAlignment.left)
    ml.set_overall_scaling(SHEET)
    ml.add_leader_line(side, [Vec2((ox + target[0]) * MM, (oy + target[1]) * MM)])
    ml.build(insert=Vec2((ox + insert[0]) * MM, (oy + insert[1]) * MM))

# ------------------------------------------------------------------ kreskowanie liniami
def _hatch_poly(pts, spacing, ang, layer="KRESKOWANIE"):
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    projs = [px * nx + py * ny for px, py in pts]
    s0, s1 = min(projs), max(projs)
    edges = list(zip(pts, pts[1:] + pts[:1]))
    s = s0 + spacing / 2
    while s < s1:
        qx, qy = s * nx, s * ny; ts = []
        for (ax, ay), (bx, by) in edges:
            ex, ey = bx - ax, by - ay; det = ex * dy - dx * ey
            if abs(det) < 1e-9: continue
            rx, ry = ax - qx, ay - qy
            t = (-rx * ey + ex * ry) / det; u = (dx * ry - dy * rx) / det
            if -1e-9 <= u <= 1 + 1e-9: ts.append(t)
        ts.sort()
        for i in range(0, len(ts) - 1, 2):
            L(qx + ts[i] * dx, qy + ts[i] * dy, qx + ts[i + 1] * dx, qy + ts[i + 1] * dy, layer)
        s += spacing

def hdiag(x, y, w, h, spacing, ang=45, ox=0, oy=0, layer="KRESKOWANIE"):
    _hatch_poly([(ox + x, oy + y), (ox + x + w, oy + y), (ox + x + w, oy + y + h), (ox + x, oy + y + h)],
                spacing, ang, layer)

def hcross(x, y, w, h, spacing, ox=0, oy=0, layer="KRESKOWANIE"):
    hdiag(x, y, w, h, spacing, 45, ox, oy, layer); hdiag(x, y, w, h, spacing, 135, ox, oy, layer)

def hpoly(pts, spacing, ang=45, ox=0, oy=0, layer="KRESKOWANIE"):
    _hatch_poly([(ox + p[0], oy + p[1]) for p in pts], spacing, ang, layer)

def dots(x, y, w, h, dx=8, dy=6, r=1.2, ox=0, oy=0, layer="KRESKOWANIE"):
    row = 0; yy = y + dy / 2
    while yy < y + h:
        xx = x + dx / 2 + (dx / 2 if row % 2 else 0)
        while xx < x + w:
            C(xx, yy, r, layer, ox, oy); xx += dx
        yy += dy; row += 1

def stones(x, y, w, h, r=9, dx=20, dy=18, ox=0, oy=0, layer="KRESKOWANIE"):
    row = 0; yy = y + dy / 2
    while yy < y + h - r * 0.3:
        xx = x + dx / 2 + (dx / 2 if row % 2 else 0)
        while xx < x + w - r * 0.3:
            C(xx, yy, r, layer, ox, oy); xx += dx
        yy += dy; row += 1

def wavy(x0, y0, x1, y1, n=5, amp=4, layer="KONTUR", ox=0, oy=0):
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4); px = x0 + (x1 - x0) * t; py = y0 + (y1 - y0) * t
        dxx = x1 - x0; dyy = y1 - y0; Ln = math.hypot(dxx, dyy) or 1
        o = amp * math.sin(t * math.pi * n)
        pts.append((px - dyy / Ln * o, py + dxx / Ln * o))
    P(pts, layer, closed=False, ox=ox, oy=oy)

def chevron(x, y, ang, size=14, layer="OSIE", ox=0, oy=0):
    a = math.radians(ang)
    for da in (math.radians(150), math.radians(-150)):
        L(x, y, x + size * math.cos(a + da), y + size * math.sin(a + da), layer, ox=ox, oy=oy)

def rzedna(x, y, val, ox=0, oy=0):
    """Rzedna wysokosciowa: otwarty trojkat (bez SOLID) + wartosc."""
    s = 14
    P([(x, y), (x - s, y + s * 1.4), (x + s, y + s * 1.4)], "OPISY", closed=True, ox=ox, oy=oy)
    T(val, x + s + 6, y + s, 22, MA.MIDDLE_LEFT, "OPISY", ox=ox, oy=oy)

def spadek(x, y, ang, L_=90, txt="i=2%", ox=0, oy=0):
    """Spadek: cienka linia kierunku + podpis, BEZ pelnych grotow."""
    a = math.radians(ang)
    L(x, y, x + L_ * math.cos(a), y + L_ * math.sin(a), "OPISY", ox=ox, oy=oy)
    T(txt, x + L_ * 0.18, y + 22, 24, MA.MIDDLE_LEFT, "OPISY", ox=ox, oy=oy)

# ------------------------------------------------------------------ materialy przekrojow
SP_SEC = {
    "kostka_betonowa": ("diag", 12, 45), "kostka_granit": ("cross", 12, 0),
    "plyta_bazalt": ("stones", 9, 22, 18), "piasek": ("dots", 8, 6, 1.3),
    "zwir": ("stones", 6, 15, 13), "tluczen": ("stones", 9, 22, 19),
    "pospolka": ("dots", 10, 7, 1.6), "beton_mono": ("diag", 15, 45),
    "humus": ("diag", 20, 135), "grunt": ("diag", 26, 45),
}

def dfill(cx, cy, x, y, w, h, mkey):
    X, Y, Wd, Hh = cx + x * S, cy + y * S, w * S, h * S
    k = SP_SEC[mkey]
    if k[0] == "diag":   hdiag(X, Y, Wd, Hh, k[1], k[2])
    elif k[0] == "cross": hcross(X, Y, Wd, Hh, k[1])
    elif k[0] == "dots":  dots(X, Y, Wd, Hh, k[1], k[2], k[3])
    elif k[0] == "stones": stones(X, Y, Wd, Hh, k[1], k[2], k[3])

def dfill_poly(cx, cy, pts, mkey):
    k = SP_SEC[mkey]
    P2 = [(cx + p[0] * S, cy + p[1] * S) for p in pts]
    if k[0] == "diag": _hatch_poly(P2, k[1], k[2])
    else: _hatch_poly(P2, k[1], 45)

def dr(cx, cy, x, y, w, h, layer="KONTUR"): R(cx + x * S, cy + y * S, w * S, h * S, layer)
def dl(cx, cy, x1, y1, x2, y2, layer="KONTUR", lt=None): L(cx + x1 * S, cy + y1 * S, cx + x2 * S, cy + y2 * S, layer, lt)
def dtext(cx, cy, x, y, s, h=24, align=MA.MIDDLE_LEFT): T(s, cx + x * S, cy + y * S, h, align, "OPISY")

# ------------------------------------------------------------------ warstwy przekrojow
STOPIEN_H, STOPIEN_T = 15.0, 33.0
LAY_PODJAZD = [(8, "kostka_betonowa", "kostka brukowa betonowa 20×10×8 cm"),
               (3, "piasek", "podsypka — piasek płukany f. 0–2 mm"),
               (15, "zwir", "podbudowa górna — kruszywo łamane 0–31,5 mm"),
               (20, "tluczen", "podbudowa dolna — tłuczeń f. 31,5–63 mm"),
               (10, "pospolka", "warstwa odsączająca — pospółka f. 0–16 mm")]
LAY_SCIEZKA = [(4, "plyta_bazalt", "płyta bazaltowa nieregularna Ø40–60 cm"),
               (3, "piasek", "podsypka — piasek płukany f. 0–2 mm"),
               (10, "zwir", "podbudowa — kruszywo łamane f. 0–31,5 mm")]
LAY_PODEST = [(5, "kostka_granit", "kostka brukowa granitowa 5×5×5 cm"),
              (5, "piasek", "podsypka — piasek płukany f. 0–2 mm"),
              (5, "zwir", "podbudowa górna — kruszywo łamane 0–31,5 mm"),
              (15, "tluczen", "podbudowa dolna — tłuczeń f. 31,5–63 mm"),
              (6, "pospolka", "warstwa odsączająca — pospółka f. 0–16 mm")]
LAY_TRAWNIK = [(20, "humus", "ziemia urodzajna (humus) + trawa z siewu")]

def stack(cx, cy, x0, width, layers):
    y = 0.0; info = []
    for g, mkey, opis in layers:
        dr(cx, cy, x0, y - g, width, g, "KONTUR")
        dfill(cx, cy, x0, y - g, width, g, mkey)
        info.append((y, y - g, opis, g)); y -= g
    return y, info

def grunt_rodzimy(cx, cy, x0, width, y_top, depth=12):
    dr(cx, cy, x0, y_top - depth, width, depth, "KONTUR")
    dfill(cx, cy, x0, y_top - depth, width, depth, "grunt")
    wavy(cx + x0 * S, cy + (y_top - depth) * S, cx + (x0 + width) * S, cy + (y_top - depth) * S, 5, 4, "KONTUR")

def obrzeze(cx, cy, x_center, h=20, w=6, law_w=22, law_h=12):
    top = 2.0
    dr(cx, cy, x_center - w / 2, top - h, w, h, "KONTUR")
    dfill(cx, cy, x_center - w / 2, top - h, w, h, "kostka_betonowa")
    dr(cx, cy, x_center - law_w / 2, top - h - law_h, law_w, law_h, "KONTUR")
    dfill(cx, cy, x_center - law_w / 2, top - h - law_h, law_w, law_h, "beton_mono")

def opis_kolumna(cx, cy, x, y_start, info, krok=4.4):
    yy = y_start
    for y_t, y_b, opis, g in info:
        T("%g cm — %s" % (g, opis), cx + x * S, cy + yy * S, 24, MA.MIDDLE_LEFT, "OPISY")
        yy -= krok

def wym_warstw(cx, cy, xd, info, kier=1):
    for y_t, y_b, opis, g in info:
        DDIM((cx + xd * S, cy + y_t * S), (cx + xd * S, cy + y_b * S), (cx + (xd + 8 * kier) * S, cy + y_t * S), 90)

# ------------------------------------------------------------------ PRZEKROJE
def przekroj(ox, oy, nazwa, left_layers, right_layers, left_lbl, right_lbl, total_w=400.0):
    cx, cy = ox, oy; half = total_w / 2
    dl(cx, cy, -half - 20, 0, half + 20, 0, "KONTUR")
    T("i=2%", cx + (-half / 2) * S, cy + 10 * S, 24, MA.MIDDLE_CENTER, "OPISY")
    yL, infoL = stack(cx, cy, -half, half, left_layers)
    yR, infoR = stack(cx, cy, 0, half, right_layers)
    depthL, depthR = -yL, -yR; ybase = min(yL, yR)
    grunt_rodzimy(cx, cy, -half - 15, total_w + 30, ybase, depth=12)
    for x0s, ys in [(-half, yL), (0.0, yR)]:
        if ys - ybase > 0.5:
            dr(cx, cy, x0s, ybase, half, ys - ybase, "KONTUR")
            dfill(cx, cy, x0s, ybase, half, ys - ybase, "grunt")
    obrzeze(cx, cy, 0)
    wym_warstw(cx, cy, -half - 25, infoL, kier=-1)
    wym_warstw(cx, cy, half + 25, infoR, kier=+1)
    T(left_lbl, cx + (-half) * S, cy + (-depthL - 26) * S, 32, MA.MIDDLE_LEFT, "OPISY")
    opis_kolumna(cx, cy, -half, -depthL - 40, infoL)
    T(right_lbl, cx + 2 * S, cy + (-depthR - 26) * S, 32, MA.MIDDLE_LEFT, "OPISY")
    opis_kolumna(cx, cy, 2, -depthR - 40, infoR)
    T("grunt rodzimy — zagęszczony i wyrównany do Is≥0,97",
      cx + (-half - 10) * S, cy + (ybase - 20) * S, 24, MA.MIDDLE_LEFT, "OPISY")
    T("PRZEKRÓJ %s   1:10" % nazwa, cx + (-half - 25) * S, cy + 30 * S, 46, MA.MIDDLE_LEFT, "OPISY")

def przekroj_sciezka(ox, oy, nazwa="B-B'"):
    cx, cy = ox, oy; pw, gw = 100.0, 90.0; total = pw + 2 * gw
    dl(cx, cy, -total / 2, 0, total / 2, 0, "KONTUR")
    T("i=2%", cx + 0 * S, cy + 16 * S, 24, MA.MIDDLE_CENTER, "OPISY")
    yGL, _ = stack(cx, cy, -pw / 2 - gw, gw, LAY_TRAWNIK)
    yGR, _ = stack(cx, cy, pw / 2, gw, LAY_TRAWNIK)
    yS, infoS = stack(cx, cy, -pw / 2, pw, LAY_SCIEZKA)
    ybase = min(yGL, yGR, yS)
    grunt_rodzimy(cx, cy, -total / 2 - 10, total + 20, ybase, depth=12)
    for x0s, ww, ys in [(-pw / 2 - gw, gw, yGL), (-pw / 2, pw, yS), (pw / 2, gw, yGR)]:
        if ys - ybase > 0.5:
            dr(cx, cy, x0s, ybase, ww, ys - ybase, "KONTUR")
            dfill(cx, cy, x0s, ybase, ww, ys - ybase, "grunt")
    obrzeze(cx, cy, -pw / 2); obrzeze(cx, cy, pw / 2)
    wym_warstw(cx, cy, pw / 2 + gw + 10, infoS, kier=+1)
    DDIM((cx + (-pw / 2) * S, cy + 5 * S), (cx + (pw / 2) * S, cy + 5 * S), (cx + (-pw / 2) * S, cy + 13 * S))
    T("trawnik", cx + (-pw / 2 - gw + 8) * S, cy + 11 * S, 24, MA.MIDDLE_LEFT, "OPISY")
    T("trawnik", cx + (pw / 2 + 18) * S, cy + 11 * S, 24, MA.MIDDLE_LEFT, "OPISY")
    xlbl = -total / 2
    T("ŚCIEŻKA 1 m — płyta bazaltowa w trawie", cx + xlbl * S, cy + (-42) * S, 32, MA.MIDDLE_LEFT, "OPISY")
    opis_kolumna(cx, cy, xlbl, -54, infoS)
    T("trawnik: humus 20 cm + trawa z siewu", cx + xlbl * S, cy + (-78) * S, 24, MA.MIDDLE_LEFT, "OPISY")
    T("grunt rodzimy — zagęszczony i wyrównany", cx + xlbl * S, cy + (-90) * S, 24, MA.MIDDLE_LEFT, "OPISY")
    T("PRZEKRÓJ %s   1:10" % nazwa, cx + (-total / 2 - 5) * S, cy + 30 * S, 46, MA.MIDDLE_LEFT, "OPISY")

def przekroj_CC(ox, oy):
    cx, cy = ox, oy; half = 100.0
    dl(cx, cy, -half - 20, 0, 0, 0, "KONTUR")
    T("i=2%", cx + (-half / 2) * S, cy + 10 * S, 24, MA.MIDDLE_CENTER, "OPISY")
    yL, infoL = stack(cx, cy, -half, half, LAY_PODEST)
    grunt_rodzimy(cx, cy, -half - 15, half + 15, yL, depth=12)
    wym_warstw(cx, cy, -half - 25, infoL, kier=-1)
    T("PODEST — kostka granitowa", cx + (-half) * S, cy + (yL - 26) * S, 32, MA.MIDDLE_LEFT, "OPISY")
    opis_kolumna(cx, cy, -half, yL - 40, infoL)
    t, h = STOPIEN_T, STOPIEN_H
    beton_pts = [(0, 0), (t, 0), (t, -h), (2 * t, -h), (2 * t, -2 * h),
                 (2 * t, -2 * h - 15), (t, -h - 15), (0, -15)]
    dl(cx, cy, 0, 0, t, 0, "KONTUR"); dl(cx, cy, t, 0, t, -h, "KONTUR")
    dl(cx, cy, t, -h, 2 * t, -h, "KONTUR"); dl(cx, cy, 2 * t, -h, 2 * t, -2 * h, "KONTUR")
    dfill_poly(cx, cy, beton_pts, "beton_mono")
    P([(cx + p[0] * S, cy + p[1] * S) for p in beton_pts], "KONTUR")
    grunt_rodzimy(cx, cy, 0, 2 * t + 15, -2 * h - 15, depth=12)
    DDIM((cx + (2 * t + 15) * S, cy + 0 * S), (cx + (2 * t + 15) * S, cy + (-h) * S), (cx + (2 * t + 25) * S, cy + 0 * S), 90)
    DDIM((cx + (2 * t + 15) * S, cy + (-h) * S), (cx + (2 * t + 15) * S, cy + (-2 * h) * S), (cx + (2 * t + 25) * S, cy + (-h) * S), 90)
    DDIM((cx + 0 * S, cy + 3 * S), (cx + t * S, cy + 3 * S), (cx + 0 * S, cy + 8 * S))
    DDIM((cx + t * S, cy + 3 * S), (cx + 2 * t * S, cy + 3 * S), (cx + t * S, cy + 8 * S))
    LEAD("beton C25/30, zatarty,\nspadek 1–2% na stopniu", (cx + (2 * t + 2) * S, cy + (-h - 5) * S),
         (cx + (2 * t + 22) * S, cy + (-h - 30) * S), mleader.ConnectionSide.left)
    LEAD("siatka zbrojeniowa Ø6 #150\nw płycie stopnia", (cx + t * S, cy + (-2 * h - 8) * S),
         (cx + (t + 22) * S, cy + (-2 * h - 40) * S), mleader.ConnectionSide.left)
    T("SCHODKI TERENOWE — stopień 15/33 cm, beton monolityczny C25/30",
      cx + (-half) * S, cy + (-2 * h - 80) * S, 32, MA.MIDDLE_LEFT, "OPISY")
    T("PRZEKRÓJ C-C'   1:10", cx + (-half - 25) * S, cy + 30 * S, 46, MA.MIDDLE_LEFT, "OPISY")

# ------------------------------------------------------------------ DETAL STYKU
def detal_styk(ox, oy):
    cx, cy = ox, oy; wA, wB, obw = 95.0, 95.0, 8.0
    layA = [(8, "kostka_betonowa"), (3, "piasek"), (15, "zwir")]
    layB = [(4, "plyta_bazalt"), (3, "piasek"), (15, "zwir")]

    def buildup(x0, w, lay):
        y = 0.0
        for g, m in lay:
            dr(cx, cy, x0, y - g, w, g, "KONTUR")
            dfill(cx, cy, x0, y - g, w, g, m); y -= g
        return y
    yA = buildup(-obw / 2 - wA, wA, layA)
    yB = buildup(obw / 2, wB, layB)
    obh = 30.0
    dr(cx, cy, -obw / 2, 2 - obh, obw, obh, "KONTUR")
    dfill(cx, cy, -obw / 2, 2 - obh, obw, obh, "beton_mono")
    dr(cx, cy, -20, 2 - obh - 14, 40, 14, "KONTUR")
    dfill(cx, cy, -20, 2 - obh - 14, 40, 14, "beton_mono")
    P([(cx + (obw / 2) * S, cy + (2 - obh) * S), (cx + (obw / 2 + 12) * S, cy + (2 - obh) * S),
       (cx + (obw / 2) * S, cy + (2 - obh + 12) * S)], "KONTUR")
    ybase = min(yA, yB, 2 - obh - 14)
    grunt_rodzimy(cx, cy, -obw / 2 - wA - 8, wA + wB + obw + 16, ybase, 12)
    for x0s, ww, ys in [(-obw / 2 - wA, wA, yA), (obw / 2, wB, yB)]:
        if ys - ybase > 0.5:
            dr(cx, cy, x0s, ybase, ww, ys - ybase, "KONTUR")
            dfill(cx, cy, x0s, ybase, ww, ys - ybase, "grunt")
    dl(cx, cy, -obw / 2 - wA, 0, -obw / 2, 0, "KONTUR")
    dl(cx, cy, obw / 2, 0, obw / 2 + wB, 0, "KONTUR")
    dl(cx, cy, -obw / 2, 2, -obw / 2, -obh, "KONTUR", lt="DASHED")
    dl(cx, cy, obw / 2, 2, obw / 2, -obh, "KONTUR", lt="DASHED")
    T("i=2%", cx + (-obw / 2 - wA * 0.75) * S, cy + 11 * S, 24, MA.MIDDLE_LEFT, "OPISY")
    T("i=2%", cx + (obw / 2 + wB * 0.3) * S, cy + 11 * S, 24, MA.MIDDLE_LEFT, "OPISY")
    LEAD("obrzeże/opornik betonowy 8×30 cm (góra +2 cm)", (cx + 0 * S, cy + 3 * S),
         (cx + 42 * S, cy + 36 * S), mleader.ConnectionSide.left)
    LEAD("ława betonowa C12/15 z oporem", (cx + 0 * S, cy + (2 - obh - 7) * S),
         (cx + 48 * S, cy + (-54) * S), mleader.ConnectionSide.left)
    LEAD("dylatacja — kit trwale plastyczny", (cx + (-obw / 2) * S, cy + (-14) * S),
         (cx + (-44) * S, cy + (-48) * S), mleader.ConnectionSide.right)
    LEAD("kostka betonowa — podjazd", (cx + (-obw / 2 - wA * 0.5) * S, cy + (-4) * S),
         (cx + (-obw / 2 - wA - 6) * S, cy + 30 * S), mleader.ConnectionSide.right)
    LEAD("płyta bazaltowa — ścieżka", (cx + (obw / 2 + wB * 0.5) * S, cy + (-2) * S),
         (cx + (obw / 2 + wB + 6) * S, cy + 30 * S), mleader.ConnectionSide.left)
    T("DETAL 1 — połączenie nawierzchni (obrzeże na ławie z oporem)   1:10",
      cx + (-obw / 2 - wA - 8) * S, cy + 48 * S, 46, MA.MIDDLE_LEFT, "OPISY")

# ------------------------------------------------------------------ RZUT / PLAN DZIALKI
DZ_W, DZ_H = 1200.0, 3300.0

def plan_dzialki(ox, oy):
    def Ll(x1, y1, x2, y2, layer, lt=None): L(x1, y1, x2, y2, layer, lt, ox, oy)
    def Rf(x, y, w, h, layer, lt=None): R(x, y, w, h, layer, lt, ox, oy)
    def Tt(s, x, y, h=24, align=MA.MIDDLE_LEFT, rot=0, layer="OPISY"): T(s, x, y, h, align, layer, rot, ox, oy)
    def H(x, y, w, h, mode, sc, ang=45):
        if mode == "diag":   hdiag(x, y, w, h, sc, ang, ox, oy)
        elif mode == "cross": hcross(x, y, w, h, sc, ox, oy)
        elif mode == "dots":  dots(x, y, w, h, sc, sc * 0.75, sc * 0.16, ox, oy)
    def Ch(x, y, ang, size=14, layer="OSIE"): chevron(x, y, ang, size, layer, ox, oy)
    def Rz(x, y, val): rzedna(x, y, val, ox, oy)
    def Sp(x, y, ang, Ln, txt): spadek(x, y, ang, Ln, txt, ox, oy)
    def Lead(txt, target, insert, side=mleader.ConnectionSide.left): LEAD(txt, target, insert, side, 2.5, ox, oy)
    def Vd(y1, y2, x, off): VDIM(y1, y2, x, off, "PLANM", ox, oy)
    def Hd(x1, x2, y, off): HDIM(x1, x2, y, off, "PLANM", ox, oy)
    def drzewo(cx, cy, r):
        C(cx, cy, r, "KONTUR", ox, oy); C(cx, cy, r * 0.28, "KONTUR", ox, oy)
    def krzew(cx, cy, r=32): C(cx, cy, r, "KONTUR", ox, oy)

    Rf(0, 0, DZ_W, DZ_H, "KONTUR", lt="DASHED")
    Tt("granica działki  (dz. nr 103/1)", 20, DZ_H - 55, 28)
    # ulica
    H(-260, -260, DZ_W + 520, 260, "diag", 180, 45)
    Tt("ul. Ogrodowa", DZ_W / 2, -170, 40, MA.MIDDLE_CENTER)
    Ll(100, 0, 240, 0, "KONTUR"); Tt("furtka", 90, 35, 24)
    Ll(650, 0, 1100, 0, "KONTUR"); Tt("brama", 820, 35, 24)
    # podjazd
    Rf(0, 0, 1200, 300, "KONTUR")
    H(0, 0, 1200, 300, "diag", 48, 45)
    Tt("PODJAZD", 250, 205, 34); Tt("kostka betonowa 12 × 3 m", 250, 150, 24)
    Sp(600, 55, 90, 120, "i=2% do korytka")
    # dom + garaz
    Rf(500, 300, 700, 1500, "KONTUR")
    H(500, 300, 700, 1500, "diag", 135, 45)
    Tt("DOM", 780, 1155, 46, MA.MIDDLE_LEFT); Tt("7 × 15 m", 780, 1075, 30)
    Rf(800, 300, 400, 300, "KONTUR"); Tt("GARAŻ", 940, 430, 28)
    Tt("parter +0,45", 700, 900, 24)
    Tt("wejście główne", 520, 475, 24)
    # sciezka L
    for (sx, sy, sw, sh) in [(400, 300, 100, 1600), (500, 1800, 700, 100)]:
        Rf(sx, sy, sw, sh, "KONTUR"); H(sx, sy, sw, sh, "dots", 30)
    Tt("ŚCIEŻKA — płyta bazaltowa, szer. 1 m", 250, 1100, 24, MA.MIDDLE_LEFT, 90)
    # schodki
    Rf(1100, 1900, 100, 1100, "KONTUR")
    H(1100, 1900, 100, 1100, "diag", 48, 135)
    for i in range(1, 8):
        yy = 1900 + i * 1100 / 8; Ll(1100, yy, 1200, yy, "KONTUR")
    Tt("SCHODKI TERENOWE — beton C25/30", 1255, 2050, 24, MA.MIDDLE_LEFT, 90)
    # podest
    Rf(800, 3000, 400, 300, "KONTUR"); H(800, 3000, 400, 300, "cross", 48)
    Tt("PODEST", 1000, 3205, 30, MA.MIDDLE_CENTER); Tt("granit 4 × 3 m", 1000, 3120, 24, MA.MIDDLE_CENTER)
    Rz(825, 3035, "+0,30")
    # trawnik + zielen
    Tt("TRAWNIK", 600, 2300, 40)
    drzewo(300, 2750, 130); Tt("drzewo ozdobne", 300, 2555, 22, MA.MIDDLE_CENTER)
    for (kx, ky) in [(180, 2200), (700, 2700), (250, 3050), (620, 3050), (170, 1500)]:
        krzew(kx, ky, 40)
    # obrzeza / oporniki (KONTUR, ciagla) + odnosnik
    for a, b, c, d in [(0, 300, 400, 300), (0, 0, 0, 300), (1200, 0, 1200, 300),
                       (400, 300, 400, 1900), (500, 1900, 1100, 1900),
                       (1100, 1900, 1100, 3000), (800, 3000, 1100, 3000),
                       (800, 3000, 800, 3300)]:
        Ll(a, b, c, d, "KONTUR")
    Lead("obrzeże bet. 50×20×6 na ławie C12/15 z oporem", (180, 300), (100, 660), mleader.ConnectionSide.right)
    # odwodnienie liniowe
    Rf(520, 283, 660, 17, "KONTUR"); H(520, 283, 660, 17, "cross", 24)
    Lead("odwodnienie liniowe (korytko z rusztem)", (700, 291), (770, 205), mleader.ConnectionSide.left)
    # dylatacje (KONTUR dashed)
    for a, b, c, d in [(500, 300, 1200, 300), (500, 300, 500, 1800), (500, 1800, 1200, 1800)]:
        Ll(a, b, c, d, "KONTUR", lt="DASHED")
    Lead("dylatacja + spadek od budynku (taśma)", (500, 850), (140, 850), mleader.ConnectionSide.right)
    # odwodnienie: rozsaczanie na trawniku
    Rz(520, 315, "±0,00")
    Sp(480, 950, 180, 90, "i=2%"); Sp(760, 1840, 90, 80, "i=2%"); Sp(830, 3120, 180, 90, "i=2%")
    Tt("rozsączanie powierzchniowe", 420, 2210, 24)
    Tt("na trawniku (pow. biol. czynna)", 420, 2150, 22)
    # linie ciec (OSIE) + otwarte groty
    def ciecie_v(x, y0, y1, lit):
        Ll(x, y0, x, y1, "OSIE"); Ch(x, y1, 90, 20); Ch(x, y0, 270, 20)
        Tt(lit, x, y1 + 40, 40, MA.MIDDLE_CENTER); Tt(lit + "'", x, y0 - 95, 40, MA.MIDDLE_CENTER)
    def ciecie_h(y, x0, x1, lit):
        Ll(x0, y, x1, y, "OSIE"); Ch(x1, y, 0, 20); Ch(x0, y, 180, 20)
        Tt(lit, x0 - 100, y, 40, MA.MIDDLE_CENTER); Tt(lit + "'", x1 + 75, y, 40, MA.MIDDLE_CENTER)
    ciecie_v(250, -70, 380, "A")
    ciecie_h(1000, 250, 650, "B")
    ciecie_v(1150, 2650, 3360, "C")
    # wymiary (metry)
    Vd(0, 300, 0, -170); Vd(300, 1800, 0, -170); Vd(1800, 3300, 0, -170)
    Vd(0, 3300, DZ_W, 340); Hd(0, 1200, 0, -400); Hd(0, 500, 1800, 110); Hd(500, 1200, 1800, 110)
    # polnoc (otwarty grot)
    nx, ny = DZ_W + 250, DZ_H - 150
    Ll(nx, ny, nx, ny + 220, "KONTUR"); Ch(nx, ny + 220, 90, 32, "KONTUR")
    Tt("N", nx, ny + 275, 44, MA.MIDDLE_CENTER)
    # podzialka liniowa
    sby = DZ_H + 95
    for i in range(5):
        Rf(i * 100, sby, 100, 24, "KONTUR")
        if i % 2 == 0: H(i * 100, sby, 100, 24, "diag", 8, 45)
    for i in range(6): Tt(str(i), i * 100, sby - 52, 22, MA.MIDDLE_CENTER)
    Tt("m", 560, sby - 4, 22)
    Tt("podziałka liniowa 1:100 (działki co 1 m)", 40, sby + 38, 22)
    T("RZUT Z GÓRY — PLAN ZAGOSPODAROWANIA DZIAŁKI 12 × 33 m   1:100",
      -60, DZ_H + 260, 46, MA.MIDDLE_LEFT, "OPISY", 0, ox, oy)

# ------------------------------------------------------------------ LEGENDA / OPIS / BILANS
def legenda(x0, y0):
    items = [("kostka_betonowa", "kostka betonowa (podjazd)", "diag", 20, 45),
             ("kostka_granit", "kostka granitowa (podest)", "cross", 20, 0),
             ("plyta_bazalt", "płyta bazaltowa (ścieżka)", "stones", 0, 0),
             ("beton_mono", "beton C25/30 (schodki, ławy)", "diag", 24, 45),
             ("piasek", "podsypka piaskowa", "dots", 20, 0),
             ("zwir", "kruszywo łamane / żwir", "stones", 0, 0),
             ("tluczen", "tłuczeń (podbudowa dolna)", "stones", 0, 0),
             ("pospolka", "pospółka (w-wa odsączająca)", "dots", 24, 45),
             ("humus", "ziemia urodzajna / trawnik", "diag", 30, 135),
             ("grunt", "grunt rodzimy", "diag", 34, 45)]
    T("LEGENDA MATERIAŁÓW", x0, y0, 30, MA.MIDDLE_LEFT, "OPISY")
    sw, sh, colw, rowh = 95, 58, 620, 105
    for i, (mkey, lbl, mode, sc, ang) in enumerate(items):
        col, row = i % 5, i // 5
        xx = x0 + col * colw; yy = y0 - 80 - row * rowh
        R(xx, yy, sw, sh, "KONTUR")
        if mode == "diag":   hdiag(xx, yy, sw, sh, sc, ang)
        elif mode == "cross": hcross(xx, yy, sw, sh, sc)
        elif mode == "dots":  dots(xx, yy, sw, sh, sc, sc * 0.75, sc * 0.16)
        elif mode == "stones": stones(xx, yy, sw, sh, 9, 24, 20)
        T(lbl, xx + sw + 22, yy + 26, 22, MA.MIDDLE_LEFT, "OPISY")
    x2 = x0 + 5 * colw + 40
    T("OZNACZENIA", x2, y0, 30, MA.MIDDLE_LEFT, "OPISY")
    ozn = [("obrzeże / opornik na ławie z oporem", None),
           ("dylatacja (styk z budynkiem)", "DASHED"),
           ("odwodnienie liniowe (korytko z rusztem)", "cross"),
           ("linia przekroju A-A / B-B / C-C", "OSIE")]
    for i, (lbl, style) in enumerate(ozn):
        yy = y0 - 80 - i * 72
        if style == "cross":
            R(x2, yy, 95, 42, "KONTUR"); hcross(x2, yy, 95, 42, 24)
        elif style == "OSIE":
            L(x2, yy + 22, x2 + 95, yy + 22, "OSIE")
        elif style == "DASHED":
            L(x2, yy + 22, x2 + 95, yy + 22, "KONTUR", lt="DASHED")
        else:
            L(x2, yy + 22, x2 + 95, yy + 22, "KONTUR")
        T(lbl, x2 + 118, yy + 20, 22, MA.MIDDLE_LEFT, "OPISY")

def opis_techniczny(x0, y0):
    T("OPIS TECHNICZNY / UWAGI", x0, y0, 32, MA.MIDDLE_LEFT, "OPISY")
    linie = [
        "1. Poziom parteru +0,45 m = rzędna odniesienia. Nawierzchnie ze spadkiem 1,5–2% od budynku (patrz strzałki spadku).",
        "2. POŁĄCZENIA NAWIERZCHNI: wszystkie krawędzie nawierzchni segmentowych (kostka, płyty) ujęte w obrzeże/opornik",
        "    betonowy 50×20×6 cm na ławie betonowej C12/15 z oporem — zabezpieczenie przed rozjeżdżaniem (patrz Detal 1).",
        "3. Styk dwóch różnych nawierzchni — wspólne obrzeże na ławie z oporem; góra obrzeża +2 cm lub licowana.",
        "4. Styk nawierzchni z budynkiem — dylatacja (taśma dylatacyjna / kit trwale plastyczny), bez sztywnego połączenia,",
        "    spadek odprowadzający wodę od ściany; przed garażem i wejściem — odwodnienie liniowe (korytko z rusztem).",
        "5. Podbudowy układać i zagęszczać warstwami gr. ≤20 cm; Is: podjazd ≥0,98, ciągi piesze ≥0,97.",
        "6. Kostkę układać na podsypce piaskowej, spoiny 3–5 mm wypełnić piaskiem płukanym, zawibrować; płyty bazaltowe",
        "    na podsypce, spoiny trawiaste, obrzeże przy trawniku ukryte (mijankowe do koszenia).",
        "7. Schodki terenowe — beton C25/30 zbrojony siatką Ø6 #150; dylatacje co ok. 5 m; nawierzchnia zatarta.",
        "8. Odwodnienie: spadki nawierzchni 1,5–2% na przyległe tereny zielone — rozsączanie powierzchniowe na trawniku",
        "    (pow. biol. czynna 209 m²). Podjazd → korytko liniowe → wylot i rozsączanie na działce. BEZ odprowadzania",
        "    wód na działki sąsiednie (art. 234 Prawa wodnego).",
        "9. Materiały wg norm: PN-EN 1338 (kostka bet.), 1340 (obrzeża), 1342 (kostka kam.), PN-EN 206 (beton).",
        "10. Wymiary: rzut w metrach, przekroje i detale w cm. Sprawdzić w naturze przed realizacją.",
    ]
    for i, s in enumerate(linie):
        T(s, x0, y0 - 60 - i * 62, 22, MA.MIDDLE_LEFT, "OPISY")

def bilans(x0, y0):
    T("BILANS POWIERZCHNI (zestawienie terenu)", x0, y0, 32, MA.MIDDLE_LEFT, "OPISY")
    rows = [("Powierzchnia działki (12 × 33 m)", "396,0 m²", "100 %"),
            ("Zabudowa (dom + garaż, 7 × 15 m)", "105,0 m²", "26,5 %"),
            ("Nawierzchnie utwardzone razem", "82,0 m²", "20,7 %"),
            ("   – podjazd (kostka betonowa)", "36,0 m²", ""),
            ("   – ścieżka (płyta bazaltowa 1 m)", "23,0 m²", ""),
            ("   – podest (kostka granitowa)", "12,0 m²", ""),
            ("   – schodki terenowe (beton)", "11,0 m²", ""),
            ("Powierzchnia biologicznie czynna (zieleń)", "209,0 m²", "52,8 %")]
    rh = 68.0; wc = [1620, 430, 320]
    for i in range(len(rows) + 1):
        L(x0, y0 - 48 - i * rh, x0 + sum(wc), y0 - 48 - i * rh, "KONTUR")
    xx = x0
    for w in [0] + wc:
        xx += w; L(xx, y0 - 48, xx, y0 - 48 - len(rows) * rh, "KONTUR")
    for i, r in enumerate(rows):
        cx_ = x0
        for j, cell in enumerate(r):
            T(cell, cx_ + 18, y0 - 48 - (i + 1) * rh + 34, 23, MA.MIDDLE_LEFT, "OPISY")
            cx_ += wc[j]

# ------------------------------------------------------------------ RAMKA / TABELKA / WYKAZ
SHW, SHH = 8410.0, 5940.0
def ramka():
    R(0, 0, SHW, SHH, "KONTUR"); R(140, 70, SHW - 140 - 70, SHH - 70 - 70, "KONTUR")

def tabelka():
    x0, y0, x1, y1 = SHW - 70 - 1500, 70, SHW - 70, 600
    R(x0, y0, x1 - x0, y1 - y0, "KONTUR")
    L(x0, y0 + 210, x1, y0 + 210, "KONTUR")
    L(x0 + 760, y0 + 210, x0 + 760, y1, "KONTUR")
    L(x0 + 380, y0, x0 + 380, y0 + 210, "KONTUR")
    L(x0 + 760, y0, x0 + 760, y0 + 210, "KONTUR")
    L(x0 + 1150, y0, x0 + 1150, y0 + 210, "KONTUR")
    L(x0, y0 + 105, x0 + 760, y0 + 105, "KONTUR")
    t = 23
    T("Kierunek: Architektura krajobrazu", x0 + 26, y1 - 56, t, MA.MIDDLE_LEFT)
    T("WBiIŚ SGGW", x0 + 26, y1 - 100, t, MA.MIDDLE_LEFT)
    T("Rok II, sem. 4, rok akad. 2025/2026", x0 + 26, y1 - 144, t, MA.MIDDLE_LEFT)
    T("Przedmiot: Budowa obiektów arch. krajobrazu 2", x0 + 786, y1 - 56, t, MA.MIDDLE_LEFT)
    T("Temat: projekt wykonawczy nawierzchni ogrodowych", x0 + 786, y1 - 100, t, MA.MIDDLE_LEFT)
    T("Branża: architektura krajobrazu   Etap: nawierzchnie", x0 + 786, y1 - 144, t, MA.MIDDLE_LEFT)
    T("Wykonała: Pola Organiszczak", x0 + 26, y0 + 128, t, MA.MIDDLE_LEFT)
    T("Sprawdziła: dr hab. E. Rosłon-Szeryńska", x0 + 786, y0 + 128, t, MA.MIDDLE_LEFT)
    T("Skala:", x0 + 26, y0 + 62, t, MA.MIDDLE_LEFT)
    T("1:100 i 1:10", x0 + 26, y0 + 22, t, MA.MIDDLE_LEFT)
    T("Data:", x0 + 400, y0 + 62, t, MA.MIDDLE_LEFT)
    T("Ocena:", x0 + 786, y0 + 62, t, MA.MIDDLE_LEFT)
    T("Uwagi:", x0 + 1170, y0 + 62, t, MA.MIDDLE_LEFT)

def wykazy(x0, y0):
    rh = 66.0; w = [80, 780, 170, 180, 220]; W = sum(w)
    rows = [
        ("Lp.", "Rodzaj materiału", "Jedn.", "Ilość*", "Norma"),
        ("1", "Kostka brukowa betonowa 20×10×8 cm (podjazd)", "m²", "36,0", "PN-EN 1338"),
        ("2", "Płyta bazaltowa nieregularna Ø40–60 cm (ścieżka)", "m²", "23,0", "–"),
        ("3", "Kostka brukowa granitowa 5×5×5 cm (podest)", "m²", "12,0", "PN-EN 1342"),
        ("4", "Beton C25/30 (schodki, monolit)", "m³", "1,6", "PN-EN 206"),
        ("5", "Obrzeże betonowe 50×20×6 cm", "mb", "92", "PN-EN 1340"),
        ("6", "Ława fundamentowa — beton C12/15", "m³", "1,4", "PN-EN 206"),
        ("7", "Piasek płukany f. 0–2 mm (podsypka)", "m³", "4,0", "PN-EN 13043"),
        ("8", "Kruszywo łamane f. 0–31,5 mm (podbudowa)", "m³", "7,5", "PN-EN 13242"),
        ("9", "Tłuczeń f. 31,5–63 mm (podbudowa dolna)", "m³", "9,0", "–"),
        ("10", "Pospółka f. 0–16 mm (odsączająca)", "m³", "3,5", "–"),
        ("11", "Ziemia urodzajna (humus) gr. 20 cm", "m³", "42,0", "–"),
        ("12", "Siatka zbrojeniowa Ø6 #150 (schodki)", "m²", "11,0", "–"),
        ("13", "Korytko odwodnienia liniowego z rusztem", "mb", "7,0", "PN-EN 1433"),
        ("14", "Taśma dylatacyjna / kit trwale plastyczny", "mb", "35,0", "–"),
    ]
    T("WYKAZ I SPECYFIKACJA MATERIAŁÓW", x0, y0 + len(rows) * rh + 80, 32, MA.MIDDLE_LEFT, "OPISY")
    T("*ilości szacunkowe — do potwierdzenia obmiarem po rysunkach warsztatowych",
      x0, y0 + len(rows) * rh + 42, 20, MA.MIDDLE_LEFT, "OPISY")
    for i in range(len(rows) + 1):
        L(x0, y0 + i * rh, x0 + W, y0 + i * rh, "KONTUR")
    xx = x0
    for wi in [0] + w:
        xx += wi; L(xx, y0, xx, y0 + len(rows) * rh, "KONTUR")
    for ri, r in enumerate(reversed(rows)):
        cx_ = x0
        for ci, cell in enumerate(r):
            al = MA.MIDDLE_LEFT if ci == 1 else MA.MIDDLE_CENTER
            xoff = 16 if ci == 1 else w[ci] / 2
            T(cell, cx_ + xoff, y0 + ri * rh + rh / 2, 23, al, "OPISY")
            cx_ += w[ci]

# ============================================================ ZLOZENIE ARKUSZA
ramka(); tabelka()
plan_dzialki(650, 1250)
przekroj(4150, 5150, "A-A'", LAY_PODJAZD, LAY_TRAWNIK,
         "PODJAZD — kostka betonowa", "TRAWNIK", total_w=200.0)
przekroj_sciezka(4150, 3500, "B-B'")
przekroj_CC(4150, 1850)
wykazy(5720, 4680)
opis_techniczny(5720, 4560)
bilans(5720, 3500)
detal_styk(6750, 2200)
legenda(2850, 470)

import datetime
TS = datetime.datetime.now().strftime("%y%m%d-%H%M")   # yyMMdd-hhmm na koncu nazwy
_dxf = "outputs/nawierzchnia_v2_%s.dxf" % TS
_png = "outputs/podgląd_nawierzchnia_v2_%s.png" % TS

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
_mpl.qsave(msp, _png, size_inches=(33.1, 33.1 * SHH / SHW), dpi=170, bg="#FFFFFF")
print("OK podglad", _png)

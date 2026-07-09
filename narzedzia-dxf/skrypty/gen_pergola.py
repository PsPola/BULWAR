# -*- coding: utf-8 -*-
"""
PERGOLA DREWNIANA Z TREJAŻEM — projekt wykonawczy, arkusz A1 (1:25 i 1:2.5)
Model w cm, 1:1. Ramka A1 przeskalowana x25 (841x594 mm -> 2102.5x1485 cm).
Detale rysowane x10 (na wydruku 1:25 daje 1:2.5), wymiary stylem WYMDET (dimlfac=0.1).
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

# --- WARSTWY (szablon prowadzącej) ---
for name, color, lt, lw in [
    ("PRZEKROJ",     7, "Continuous", 50),
    ("WIDOK",        7, "Continuous", 25),
    ("SZRAF",        8, "Continuous", 13),
    ("WYMIARY",      8, "Continuous", 13),
    ("CIECIA",       7, "DASHDOT",    50),
    ("NIEWIDOCZNE",  8, "DASHED",     18),
    ("OPISY",        7, "Continuous", 18),
    ("RAMKA",        7, "Continuous", 50),
    ("OSIE",         8, "DASHDOT",    13),
]:
    doc.layers.add(name, color=color, linetype=lt, lineweight=lw)

# --- STYLE WYMIAROWANIA ---
dst = doc.dimstyles.duplicate_entry("EZDXF", "WYM")
for k, v in dict(dimtxt=8, dimasz=5, dimtsz=4, dimexo=3, dimexe=4, dimgap=2,
                 dimdec=1, dimzin=8, dimtad=1, dimscale=1, dimlfac=1).items():
    dst.set_dxf_attrib(k, v)
dst.dxf.dimtxsty = "ARIAL"
dsd = doc.dimstyles.duplicate_entry("WYM", "WYMDET")
dsd.dxf.dimlfac = 0.1
dsd.dxf.dimexo = 6; dsd.dxf.dimexe = 6

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

def kratka(x0, y0, w, h, step=15.0, layer="WIDOK", ox=0, oy=0):
    rect(x0, y0, w, h, layer, ox, oy)
    x = x0+step
    while x < x0+w-1:
        line(x, y0, x, y0+h, layer, ox, oy); x += step
    y = y0+step
    while y < y0+h-1:
        line(x0, y, x0+w, y, layer, ox, oy); y += step

def beam_side(x0, x1, y0, y1, ch, layer, ox=0, oy=0):
    poly([(x0, y0+ch), (x0+ch, y0), (x1-ch, y0), (x1, y0+ch), (x1, y1), (x0, y1)],
         layer, ox, oy)

def wavy(x0, y0, x1, y1, n=6, amp=3, layer="PRZEKROJ", ox=0, oy=0):
    pts = []
    for i in range(n*4+1):
        t = i/(n*4)
        px = x0+(x1-x0)*t; py = y0+(y1-y0)*t
        dx = x1-x0; dy = y1-y0; L = math.hypot(dx, dy) or 1
        o = amp*math.sin(t*math.pi*n)
        pts.append((px - dy/L*o, py + dx/L*o))
    msp.add_lwpolyline([(ox+p[0], oy+p[1]) for p in pts], dxfattribs={"layer": layer})

# ================= GEOMETRIA (cm) =================
AX = 300.0
P  = 15.0
BW, BH = 15.0, 25.0
RW, RH = 10.0, 15.0
OV = 30.0
NR = 13; SP = 30.0
CLR = 250.0
B0, B1 = 250.0, 275.0
R0, R1 = 275.0, 290.0
FOOT, FH = 40.0, 50.0
CHW, CHH = 50.0, 10.0
PB0, PB1 = 5.0, 245.0
CH = 5.0
RAFX = [-OV+5 + i*SP for i in range(NR)]

# szrafy: drewno gęsto, beton rzadziej
W_SC, B_SC, CH_SC = 3.0, 6.0, 4.0

# ============================================================
def v_fundamenty(ox, oy):
    for cx in (0, AX):
        for cy in (0, AX):
            rect(cx-CHW/2, cy-CHW/2, CHW, CHW, "NIEWIDOCZNE", ox, oy)
            rect(cx-FOOT/2, cy-FOOT/2, FOOT, FOOT, "WIDOK", ox, oy)
            rect(cx-5, cy-5, 10, 10, "WIDOK", ox, oy)
            line(cx-3, cy, cx+3, cy, "WIDOK", ox, oy)
            line(cx, cy-3, cx, cy+3, "WIDOK", ox, oy)
    for c in (0, AX):
        line(c, -55, c, AX+55, "OSIE", ox, oy)
        line(-55, c, AX+55, c, "OSIE", ox, oy)
    hdim(-FOOT/2, FOOT/2, -FOOT/2, -25, ox, oy)
    hdim(0, AX, -FOOT/2, -50, ox, oy)
    hdim(-FOOT/2, AX+FOOT/2, -FOOT/2, -75, ox, oy)
    vdim(0, AX, -FOOT/2, -55, ox, oy)
    vdim(-FOOT/2, FOOT/2, -FOOT/2, -25, ox, oy)
    leader([(-3, AX+4), (-55, AX+48)], "kotwa slupowa regulowana M20", 7, ox, oy)
    leader([(20, AX+16), (78, AX+40)], "stopa betonowa 40x40x50, C16/20", 7, ox, oy)
    leader([(25, AX-25), (98, AX-62)], "chudy beton 50x50x10", 7, ox, oy)
    title("Rzut fundamentów   skala 1:25", -50, AX+90, ox, oy)

# ============================================================
def v_rzut_ciety(ox, oy):
    for cx in (0, AX):
        for cy in (0, AX):
            rect(cx-P/2, cy-P/2, P, P, "PRZEKROJ", ox, oy)
            hrect(cx-P/2, cy-P/2, P, P, "ANSI31", W_SC, 45, ox, oy)
    for c in (0, AX):
        line(c, -45, c, AX+45, "OSIE", ox, oy)
        line(-45, c, AX+45, c, "OSIE", ox, oy)
    y0 = AX-2
    for xx in (P/2, AX-P/2-6):
        rect(xx, y0, 6, 4, "PRZEKROJ", ox, oy)
        hrect(xx, y0, 6, 4, "ANSI31", 1.2, 45, ox, oy)
    x = 22.5
    while x < AX-P/2-6:
        rect(x-1, y0, 2, 4, "PRZEKROJ", ox, oy)
        x += 15
    line(P/2, y0, AX-P/2, y0, "WIDOK", ox, oy)
    line(P/2, y0+4, AX-P/2, y0+4, "WIDOK", ox, oy)
    x0 = AX-2
    for yy in (P/2, P/2+60-6):
        rect(x0, yy, 4, 6, "PRZEKROJ", ox, oy)
        hrect(x0, yy, 4, 6, "ANSI31", 1.2, 45, ox, oy)
    y = P/2+15
    while y < P/2+60-6:
        rect(x0, y-1, 4, 2, "PRZEKROJ", ox, oy)
        y += 15
    line(x0, P/2, x0, P/2+60, "WIDOK", ox, oy)
    line(x0+4, P/2, x0+4, P/2+60, "WIDOK", ox, oy)
    hdim(0, AX, -P/2, -40, ox, oy)
    hdim(-P/2, P/2, -P/2, -15, ox, oy)
    vdim(0, AX, -P/2, -40, ox, oy)
    vdim(P/2, P/2+60, AX+2+4, 30, ox, oy)
    leader([(150, AX+2), (102, AX+48)], "kratka trejazowa: listwy 2x4 co 15 cm, rama 4x6", 7, ox, oy)
    leader([(AX+4, 45), (AX+50, 74)], "panel boczny szer. 60", 7, ox, oy)
    title("Rzut cięty na wysokości 1 m   skala 1:25", -50, AX+85, ox, oy)

# ============================================================
def v_rzut_gory(ox, oy):
    for yc in (0, AX):
        line(-OV, yc-BW/2, AX+OV, yc-BW/2, "WIDOK", ox, oy)
        line(-OV, yc+BW/2, AX+OV, yc+BW/2, "WIDOK", ox, oy)
    for cx in (0, AX):
        for cy in (0, AX):
            rect(cx-P/2, cy-P/2, P, P, "NIEWIDOCZNE", ox, oy)
    for xc in RAFX:
        rect(xc-RW/2, -OV, RW, AX+2*OV, "WIDOK", ox, oy)
    # linie cięcia
    line(-75, 0, AX+75, 0, "CIECIA", ox, oy)
    arrow(-60, 14, 90, ox=ox, oy=oy); arrow(AX+60, 14, 90, ox=ox, oy=oy)
    line(-60, 0, -60, 14, "CIECIA", ox, oy); line(AX+60, 0, AX+60, 14, "CIECIA", ox, oy)
    text("A", -75, 20, 14, "OPISY", TA.CENTER, ox=ox, oy=oy)
    text("A'", AX+78, 20, 14, "OPISY", TA.CENTER, ox=ox, oy=oy)
    line(0, -75, 0, AX+75, "CIECIA", ox, oy)
    arrow(14, -60, 0, ox=ox, oy=oy); arrow(14, AX+60, 0, ox=ox, oy=oy)
    line(0, -60, 14, -60, "CIECIA", ox, oy); line(0, AX+60, 14, AX+60, "CIECIA", ox, oy)
    text("B", -16, -66, 14, "OPISY", TA.CENTER, ox=ox, oy=oy)
    text("B'", -16, AX+58, 14, "OPISY", TA.CENTER, ox=ox, oy=oy)
    hdim(RAFX[0], RAFX[1], AX+OV, 26, ox, oy)
    hdim(-OV, AX+OV, -OV, -100, ox, oy)
    hdim(-OV, 0, -OV, -80, ox, oy)
    hdim(0, AX, -OV, -80, ox, oy)
    hdim(AX, AX+OV, -OV, -80, ox, oy)
    vdim(-OV, AX+OV, AX+OV, 85, ox, oy)
    vdim(0, AX, AX+OV, 60, ox, oy)
    leader([(RAFX[5]+2, 160), (RAFX[5]+40, 195)], "poprzeczki 10x15 co 30 - 13 szt.", 7, ox, oy, TA.RIGHT)
    leader([(200, AX+BW/2-2), (238, AX+88)], "platew 15x25", 7, ox, oy)
    title("Rzut z góry   skala 1:25", -50, AX+110, ox, oy)

# ============================================================
def fundament_przekroj(cx, ox, oy):
    rect(cx-FOOT/2, -FH, FOOT, FH, "PRZEKROJ", ox, oy)
    hrect(cx-FOOT/2, -FH, FOOT, FH, "ANSI31", B_SC, 45, ox, oy)
    rect(cx-CHW/2, -FH-CHH, CHW, CHH, "PRZEKROJ", ox, oy)
    hrect(cx-CHW/2, -FH-CHH, CHW, CHH, "ANSI31", CH_SC, 0, ox, oy)

def slup_przekroj(cx, ox, oy):
    rect(cx-P/2, PB0, P, CLR-PB0, "PRZEKROJ", ox, oy)
    hrect(cx-P/2, PB0, P, CLR-PB0, "ANSI31", W_SC, 45, ox, oy)
    rect(cx-P/2-0.5, PB0, 0.5, 12, "PRZEKROJ", ox, oy)
    rect(cx+P/2, PB0, 0.5, 12, "PRZEKROJ", ox, oy)
    rect(cx-10, 4, 20, 1, "PRZEKROJ", ox, oy)
    line(cx-1, 0, cx-1, 4, "WIDOK", ox, oy); line(cx+1, 0, cx+1, 4, "WIDOK", ox, oy)

def teren(x0, x1, ox, oy):
    line(x0, 0, x1, 0, "PRZEKROJ", ox, oy)
    text("poz. terenu +/-0,00", x0+2, 5, 6, "OPISY", TA.LEFT, ox=ox, oy=oy)

def detal_circle(cx, cy, r, nr, ox=0, oy=0, tx=None, ty=None):
    msp.add_circle((ox+cx, oy+cy), r, dxfattribs={"layer": "OPISY"})
    tx = tx if tx is not None else cx+r+6
    ty = ty if ty is not None else cy+r
    line(cx+r*0.7071, cy+r*0.7071, tx, ty, "OPISY", ox, oy)
    text("Detal %d" % nr, tx+2, ty+2, 10, "OPISY", TA.LEFT, ox=ox, oy=oy)

# ============================================================
def v_przekroj_AA(ox, oy):
    teren(-80, AX+80, ox, oy)
    kratka(P/2, PB0, AX-P, PB1-PB0, 15, "WIDOK", ox, oy)
    for cx in (0, AX):
        slup_przekroj(cx, ox, oy)
        fundament_przekroj(cx, ox, oy)
    beam_side(-OV, AX+OV, B0, B1, CH, "WIDOK", ox, oy)
    for xc in RAFX:
        rect(xc-RW/2, R0, RW, RH, "PRZEKROJ", ox, oy)
        hrect(xc-RW/2, R0, RW, RH, "ANSI31", 2.0, 45, ox, oy)
    vdim(0, B0, AX+OV, 50, ox, oy)
    vdim(B0, B1, AX+OV, 50, ox, oy)
    vdim(R0, R1, AX+OV, 50, ox, oy)
    vdim(0, R1, AX+OV, 80, ox, oy)
    vdim(-FH-CHH, 0, -OV-10, -35, ox, oy)
    hdim(0, AX, 0, -85, ox, oy)
    hdim(-OV, 0, B1, 40, ox, oy)
    leader([(160, B1-5), (196, B1+52)], "platew 15x25", 7, ox, oy)
    leader([(RAFX[3], R1), (RAFX[3]+40, R1+40)], "poprzeczki 10x15 co 30", 7, ox, oy)
    leader([(AX+P/2-2, 150), (AX+52, 174)], "slup 15x15, fazowany 1x1", 7, ox, oy)
    leader([(150, 120), (98, 160)], "kratka trejazowa, oczko 15x15", 7, ox, oy, TA.RIGHT)
    detal_circle(0, 12, 26, 1, ox, oy, tx=-95, ty=52)
    detal_circle(RAFX[10], B1, 26, 2, ox, oy, tx=RAFX[10]+56, ty=B1+58)
    title("Przekrój A-A'   skala 1:25", -60, R1+95, ox, oy)

# ============================================================
def v_przekroj_BB(ox, oy):
    teren(-80, AX+80, ox, oy)
    kratka(P/2, PB0, 60, PB1-PB0, 15, "WIDOK", ox, oy)
    for cx in (0, AX):
        slup_przekroj(cx, ox, oy)
        fundament_przekroj(cx, ox, oy)
    for yc in (0, AX):
        rect(yc-BW/2, B0, BW, BH, "PRZEKROJ", ox, oy)
        hrect(yc-BW/2, B0, BW, BH, "ANSI31", W_SC, 45, ox, oy)
    beam_side(-OV, AX+OV, R0, R1, CH, "WIDOK", ox, oy)
    vdim(0, B0, AX+OV, 50, ox, oy)
    vdim(B0, B1, AX+OV, 50, ox, oy)
    vdim(R0, R1, AX+OV, 50, ox, oy)
    vdim(0, R1, AX+OV, 80, ox, oy)
    vdim(PB0, PB1, -OV-10, -35, ox, oy)
    hdim(0, AX, 0, -85, ox, oy)
    hdim(AX, AX+OV, R0, 40, ox, oy)
    leader([(200, R1-4), (238, R1+42)], "poprzeczka 10x15", 7, ox, oy)
    leader([(AX-4, B1-6), (AX+52, B1+48)], "platew 15x25 (cieta)", 7, ox, oy)
    leader([(40, 190), (92, 216)], "panel boczny - kratka 60x240", 7, ox, oy)
    detal_circle(AX, B0+BH/2, 30, 3, ox, oy, tx=AX+68, ty=B0+82)
    detal_circle(P/2+4, 130, 24, 4, ox, oy, tx=86, ty=92)
    title("Przekrój B-B'   skala 1:25", -60, R1+95, ox, oy)

# ============================================================
def v_widok_boku(ox, oy):
    line(-70, 0, AX+70, 0, "WIDOK", ox, oy)
    kratka(P/2, PB0, 60, PB1-PB0, 15, "WIDOK", ox, oy)
    for cy in (0, AX):
        rect(cy-P/2, PB0, P, CLR-PB0, "WIDOK", ox, oy)
        rect(cy-P/2-0.5, PB0, P+1, 12, "WIDOK", ox, oy)
    for cy in (0, AX):
        rect(cy-BW/2, B0, BW, BH, "WIDOK", ox, oy)
    beam_side(-OV, AX+OV, R0, R1, CH, "WIDOK", ox, oy)
    hdim(0, AX, 0, -30, ox, oy)
    hdim(-OV, AX+OV, R0, 40, ox, oy)
    vdim(0, B0, AX+OV+10, 35, ox, oy)
    vdim(0, R1, AX+OV+10, 65, ox, oy)
    title("Widok z boku   skala 1:25", -60, R1+70, ox, oy)

# ============================================================
def v_widok_front(ox, oy):
    line(-70, 0, AX+70, 0, "WIDOK", ox, oy)
    kratka(P/2, PB0, AX-P, PB1-PB0, 15, "WIDOK", ox, oy)
    for cx in (0, AX):
        rect(cx-P/2, PB0, P, CLR-PB0, "WIDOK", ox, oy)
        rect(cx-P/2-0.5, PB0, P+1, 12, "WIDOK", ox, oy)
    beam_side(-OV, AX+OV, B0, B1, CH, "WIDOK", ox, oy)
    for xc in RAFX:
        rect(xc-RW/2, R0, RW, RH, "WIDOK", ox, oy)
    hdim(0, AX, 0, -30, ox, oy)
    hdim(-OV, AX+OV, R0, 40, ox, oy)
    vdim(0, B0, AX+OV+10, 35, ox, oy)
    vdim(0, R1, AX+OV+10, 65, ox, oy)
    title("Widok od frontu   skala 1:25", -60, R1+70, ox, oy)

# ============================================================
# DETALE (x10)
# ============================================================
S = 10.0
DW_SC, DB_SC = 12.0, 20.0   # szraf drewna / betonu w detalach

def dr(cx, cy, x, y, w, h, layer):  rect(cx+x*S, cy+y*S, w*S, h*S, layer)
def dh(cx, cy, x, y, w, h, pat, sc, ang=45): hrect(cx+x*S, cy+y*S, w*S, h*S, pat, sc, ang)
def dl(cx, cy, x1, y1, x2, y2, layer): line(cx+x1*S, cy+y1*S, cx+x2*S, cy+y2*S, layer)

def detal1(cx, cy, r):
    """Posadowienie słupa: kotwa regulowana M20, podkładka, stopa. y=0 -> wierzch stopy."""
    o = cy - 60
    dl(cx, o, -14, 0, 14, 0, "PRZEKROJ")
    dl(cx, o, -14, 0, -14, -9, "PRZEKROJ"); dl(cx, o, 14, 0, 14, -9, "PRZEKROJ")
    wavy(cx-14*S, o-9*S, cx+14*S, o-9*S, 4, 4, "PRZEKROJ")
    hpoly([(cx-14*S, o), (cx+14*S, o), (cx+14*S, o-9*S), (cx-14*S, o-9*S)], "ANSI31", DB_SC, 45)
    dr(cx, o, -1, -8, 2, 12, "PRZEKROJ"); dh(cx, o, -1, -8, 2, 12, "SOLID", 1)
    dr(cx, o, -2, 2.6, 4, 1.4, "PRZEKROJ")
    dr(cx, o, -10, 4.0, 20, 0.6, "PRZEKROJ"); dh(cx, o, -10, 4.0, 20, 0.6, "SOLID", 1)
    dr(cx, o, -7.5, 4.6, 15, 1.0, "PRZEKROJ"); dh(cx, o, -7.5, 4.6, 15, 1.0, "ANSI37", 6)
    dr(cx, o, -7.5, 5.6, 15, 16, "PRZEKROJ")
    dh(cx, o, -7.5, 5.6, 15, 16, "ANSI31", DW_SC, 45)
    wavy(cx-7.5*S, o+21.6*S, cx+7.5*S, o+21.6*S, 4, 4, "PRZEKROJ")
    dr(cx, o, -8.0, 4.6, 0.5, 13, "PRZEKROJ"); dh(cx, o, -8.0, 4.6, 0.5, 13, "SOLID", 1)
    dr(cx, o,  7.5, 4.6, 0.5, 13, "PRZEKROJ"); dh(cx, o,  7.5, 4.6, 0.5, 13, "SOLID", 1)
    for yy in (9.5, 14.5):
        dl(cx, o, -8, yy, 8, yy, "WIDOK")
        dl(cx, o, -8, yy+0.6, 8, yy+0.6, "NIEWIDOCZNE")
        dl(cx, o, -8, yy-0.6, 8, yy-0.6, "NIEWIDOCZNE")
    ddim((cx-7.5*S, o+21.6*S), (cx+7.5*S, o+21.6*S), (cx-7.5*S, o+24*S))
    ddim((cx+10*S, o+4.6*S), (cx+10*S, o+5.6*S), (cx+12.5*S, o+4.6*S), 90)
    ddim((cx+10*S, o), (cx+10*S, o+4.6*S), (cx+12.5*S, o), 90)
    ddim((cx-8*S, o+9.5*S), (cx-8*S, o+14.5*S), (cx-12*S, o+9.5*S), 90)
    leader([(cx+8*S, o+12*S), (cx+11*S, o+16.5*S)], "2x sruba M10,", 6.5)
    text("otwor sr. 12 wiercony", cx+11*S+3, o+16.5*S-8, 6.5)
    leader([(cx+7.5*S, o+5.1*S), (cx+13*S, o+8.2*S)], "podkladka guma/teflon", 6.5)
    text("gr. 10 mm", cx+13*S+3, o+8.2*S-8, 6.5)
    leader([(cx-10*S, o+4.3*S), (cx-13*S, o+8.5*S)], "kotwa regulowana M20,", 6.5, talign=TA.RIGHT)
    text("blacha gr. 6 mm", cx-13*S-3, o+8.5*S-8, 6.5, align=TA.RIGHT)
    leader([(cx+1*S, o-6*S), (cx+8*S, o-11*S)], "stopa betonowa C16/20", 6.5)
    text("Detal 1   skala 1:2.5", cx-r, cy+r+10, 12, "OPISY")

def detal2(cx, cy, r):
    """Poprzeczka na płatwi, wkręt podfrezowany. y=0 -> styk poprzeczka/płatew."""
    o = cy - 30
    # płatew (przekrój poprzeczny, urwana dołem)
    dl(cx, o, -7.5, -12, -7.5, -1, "PRZEKROJ"); dl(cx, o, 7.5, -12, 7.5, -1, "PRZEKROJ")
    dl(cx, o, -7.5, -1, -6.5, 0, "PRZEKROJ"); dl(cx, o, 7.5, -1, 6.5, 0, "PRZEKROJ")  # fazy 1x1
    dl(cx, o, -6.5, 0, 6.5, 0, "PRZEKROJ")
    wavy(cx-7.5*S, o-12*S, cx+7.5*S, o-12*S, 4, 4, "PRZEKROJ")
    hpoly([(cx-7.5*S, o-12*S), (cx+7.5*S, o-12*S), (cx+7.5*S, o-1*S), (cx+6.5*S, o),
           (cx-6.5*S, o), (cx-7.5*S, o-1*S)], "ANSI31", DW_SC, 45)
    # poprzeczka (wzdłuż, urwana z obu stron)
    dl(cx, o, -12, 0, 12, 0, "PRZEKROJ")
    dl(cx, o, -12, 15, 12, 15, "PRZEKROJ")
    wavy(cx-12*S, o, cx-12*S, o+15*S, 3, 4, "PRZEKROJ")
    wavy(cx+12*S, o, cx+12*S, o+15*S, 3, 4, "PRZEKROJ")
    hpoly([(cx-12*S, o), (cx+12*S, o), (cx+12*S, o+15*S), (cx-12*S, o+15*S)],
          "ANSI31", DW_SC, 135)
    # podfrezowanie + wkręt 8x220 (trzon w drewnie = linie przerywane)
    dr(cx, o, -0.75, 13, 1.5, 2, "WIDOK")
    dr(cx, o, -0.75, 12.4, 1.5, 0.6, "WIDOK"); dh(cx, o, -0.75, 12.4, 1.5, 0.6, "SOLID", 1)
    dl(cx, o, -0.4, 12.4, -0.4, -6, "NIEWIDOCZNE"); dl(cx, o, 0.4, 12.4, 0.4, -6, "NIEWIDOCZNE")
    dl(cx, o, -0.4, -6, 0, -7.5, "NIEWIDOCZNE"); dl(cx, o, 0.4, -6, 0, -7.5, "NIEWIDOCZNE")
    ddim((cx+12*S, o), (cx+12*S, o+15*S), (cx+15*S, o), 90)
    ddim((cx-7.5*S, o-12*S), (cx+7.5*S, o-12*S), (cx-7.5*S, o-15.5*S))
    ddim((cx-0.75*S, o+13*S), (cx-0.75*S, o+15*S), (cx-5*S, o+13*S), 90)
    leader([(cx+0.7*S, o+13.5*S), (cx+5*S, o+18*S)], "wkret ciesielski 8x220,", 6.5)
    text("leb podfrezowany 20 mm pod lico", cx+5*S+3, o+18*S-8, 6.5)
    leader([(cx-6.9*S, o-0.6*S), (cx-11*S, o-5*S)], "faza 1x1 cm", 6.5, talign=TA.RIGHT)
    text("Detal 2   skala 1:2.5", cx-r, cy+r+10, 12, "OPISY")

def detal3(cx, cy, r):
    """Płatew na słupie: 2 wkręty 8x320 od góry, podfrezowane. y=0 -> wierzch słupa."""
    o = cy - 110
    dr(cx, o, -7.5, -8, 15, 8, "PRZEKROJ"); dh(cx, o, -7.5, -8, 15, 8, "ANSI31", DW_SC, 45)
    wavy(cx-7.5*S, o-8*S, cx+7.5*S, o-8*S, 4, 4, "PRZEKROJ")
    dr(cx, o, -7.5, 0, 15, 25, "PRZEKROJ"); dh(cx, o, -7.5, 0, 15, 25, "ANSI31", DW_SC, 135)
    for xx in (-3.5, 3.5):
        dl(cx, o, xx-0.4, 22.4, xx-0.4, -6, "NIEWIDOCZNE")
        dl(cx, o, xx+0.4, 22.4, xx+0.4, -6, "NIEWIDOCZNE")
        dl(cx, o, xx-0.4, -6, xx, -7.5, "NIEWIDOCZNE"); dl(cx, o, xx+0.4, -6, xx, -7.5, "NIEWIDOCZNE")
        dr(cx, o, xx-0.75, 22.4, 1.5, 0.6, "WIDOK"); dh(cx, o, xx-0.75, 22.4, 1.5, 0.6, "SOLID", 1)
        dr(cx, o, xx-0.75, 23, 1.5, 2, "WIDOK")
    dl(cx, o, -7.5, -1, -6.5, 0, "PRZEKROJ"); dl(cx, o, 7.5, -1, 6.5, 0, "PRZEKROJ")
    ddim((cx-3.5*S, o+25*S), (cx+3.5*S, o+25*S), (cx-3.5*S, o+28*S))
    ddim((cx+7.5*S, o), (cx+7.5*S, o+25*S), (cx+11*S, o), 90)
    ddim((cx-7.5*S, o-4*S), (cx+7.5*S, o-4*S), (cx-7.5*S, o-7*S))
    leader([(cx+4.2*S, o+24*S), (cx+8*S, o+29*S)], "2x wkret ciesielski 8x320,", 6.5)
    text("otwory nawiercone sr. 5, leb podfrezowany", cx+8*S+3, o+29*S-8, 6.5)
    leader([(cx-6.9*S, o-0.6*S), (cx-11*S, o+4*S)], "faza 1x1 cm", 6.5, talign=TA.RIGHT)
    text("Detal 3   skala 1:2.5", cx-r, cy+r+12, 12, "OPISY")

def detal4(cx, cy, r):
    """Mocowanie ramy kratki do słupa (rzut poziomy, cięty)."""
    o = cy - 20
    dr(cx, o, -7.5, -7.5, 15, 15, "PRZEKROJ"); dh(cx, o, -7.5, -7.5, 15, 15, "ANSI31", DW_SC, 45)
    dr(cx, o, 7.5, -3, 1, 6, "PRZEKROJ"); dh(cx, o, 7.5, -3, 1, 6, "SOLID", 1)
    dr(cx, o, 8.5, -2, 4, 6.0, "PRZEKROJ"); dh(cx, o, 8.5, -2, 4, 6.0, "ANSI31", DW_SC*0.7, 135)
    dr(cx, o, 12.5, -1, 2, 4, "PRZEKROJ"); dh(cx, o, 12.5, -1, 2, 4, "ANSI31", DW_SC*0.6, 45)
    dl(cx, o, 12.5, 1, -2, 1, "WIDOK")
    dl(cx, o, 12.5, 1.35, 0, 1.35, "NIEWIDOCZNE"); dl(cx, o, 12.5, 0.65, 0, 0.65, "NIEWIDOCZNE")
    ddim((cx-7.5*S, o-7.5*S), (cx+7.5*S, o-7.5*S), (cx-7.5*S, o-11*S))
    ddim((cx+7.5*S, o-7.5*S), (cx+8.5*S, o-7.5*S), (cx+7.5*S, o-9.5*S))
    ddim((cx+12.5*S, o-2*S), (cx+12.5*S, o+4*S), (cx+16*S, o-2*S), 90)
    leader([(cx+2*S, o+1*S), (cx-2*S, o+10*S)], "wkret 6x120,", 6.5, talign=TA.RIGHT)
    text("otwor nawiercony sr. 4", cx-2*S-3, o+10*S-8, 6.5, align=TA.RIGHT)
    leader([(cx+8*S, o-2.8*S), (cx+5*S, o-13*S)], "podkladka dystansowa 10 mm", 6.5, talign=TA.RIGHT)
    leader([(cx+10.5*S, o+4*S), (cx+12*S, o+9*S)], "rama kratki 4x6", 6.5)
    leader([(cx+14.5*S, o+2.8*S), (cx+16*S, o+6*S)], "listwa 2x4", 6.5)
    text("Detal 4   skala 1:2.5", cx-r, cy+r+12, 12, "OPISY")

# ============================================================
# RAMKA, TABELKA, WYKAZY
# ============================================================
SHW, SHH = 2102.5, 1485.0
def ramka():
    rect(0, 0, SHW, SHH, "RAMKA")
    rect(50, 25, SHW-50-25, SHH-25-25, "RAMKA")

def tabelka():
    x0, y0, x1, y1 = SHW-25-450, 25, SHW-25, 165
    rect(x0, y0, x1-x0, y1-y0, "RAMKA")
    line(x0, y0+60, x1, y0+60, "RAMKA")
    line(x0+225, y0+60, x0+225, y1, "RAMKA")
    line(x0+110, y0, x0+110, y0+60, "RAMKA")
    line(x0+225, y0, x0+225, y0+60, "RAMKA")
    line(x0+340, y0, x0+340, y0+60, "RAMKA")
    line(x0, y0+30, x0+225, y0+30, "RAMKA")
    t = 6.5
    text("Kierunek: Architektura krajobrazu", x0+8, y1-16, t)
    text("WBiIŚ SGGW", x0+8, y1-28, t)
    text("Rok II, sem. 4, rok akad. 2025/2026", x0+8, y1-40, t)
    text("Przedmiot: Budowa obiektów", x0+8, y1-52, t)
    text("architektury krajobrazu 2", x0+8, y1-64, t)
    text("Temat: projekt wykonawczy pergoli", x0+233, y1-20, t)
    text("z trejażem", x0+233, y1-32, t)
    text("Arkusz: rzuty, przekroje i detale", x0+233, y1-48, t)
    text("Wykonał: Pola Organiszczak", x0+8, y0+38, t)
    text("Sprawdził:", x0+233, y0+38, t)
    text("Skala:", x0+8, y0+20, t)
    text("1:25 i 1:2.5", x0+8, y0+8, t)
    text("Data:", x0+118, y0+20, t)
    text("Ocena:", x0+233, y0+20, t)
    text("Uwagi:", x0+348, y0+20, t)

def wykazy(x0, y0):
    rh = 22.0
    w = [28, 150, 70, 62, 40]
    W = sum(w)
    rows = [
        ("Nr", "Element", "Przekrój [cm]", "Dług. [cm]", "szt."),
        ("1", "Słup", "15x15", "245", "4"),
        ("2", "Płatew", "15x25", "360", "2"),
        ("3", "Poprzeczka", "10x15", "360", "13"),
        ("4", "Rama kratki - łata", "4x6", "wg rys.", "kpl."),
        ("5", "Listwa kratki", "2x4", "wg rys.", "kpl."),
    ]
    text("WYKAZ ELEMENTÓW DREWNIANYCH", x0, y0+len(rows)*rh+34, 9)
    text("(drewno klejone GL24h, impregnowane ciśnieniowo)", x0, y0+len(rows)*rh+20, 6.5)
    for i in range(len(rows)+1):
        line(x0, y0+i*rh, x0+W, y0+i*rh, "OPISY")
    xx = x0
    for wi in [0]+w:
        xx += wi; line(xx, y0, xx, y0+len(rows)*rh, "OPISY")
    for ri, r in enumerate(reversed(rows)):
        cx_ = x0
        for ci, cell in enumerate(r):
            text(cell, cx_+5, y0+ri*rh+7, 6.5)
            cx_ += w[ci]
    y2 = y0 - 40
    rows2 = [
        "ELEMENTY STALOWE I ZŁĄCZNE:",
        "- kotwa słupowa regulowana M20, ocynk - 4 szt.",
        "- wkręt ciesielski 8x220 (poprzeczki) - 26 szt.",
        "- wkręt ciesielski 8x320 (płatwie) - 8 szt.",
        "- śruba M10 z nakrętką (kotwy) - 8 szt.",
        "- podkładka guma/teflon 15x15x1 - 4 szt.",
        "- wkręt 6x120 (kratki) - 24 szt.",
        "Wszystkie otwory nawiercane (pre-drilling).",
    ]
    for i, s in enumerate(rows2):
        text(s, x0, y2-i*15, 6.5 if i else 8)

# ============================================================
# ZŁOŻENIE ARKUSZA
# ============================================================
ramka()
tabelka()

v_fundamenty(170, 1050)
v_rzut_ciety(170, 585)
v_rzut_gory(170, 135)

v_przekroj_AA(720, 1010)
v_widok_boku(720, 490)

v_przekroj_BB(1280, 1010)
v_widok_front(1280, 490)

D1 = (880, 235, 195)
D2 = (1440, 235, 195)
D3 = (1900, 1200, 210)
D4 = (1900, 770, 195)
detal1(*D1); detal2(*D2); detal3(*D3); detal4(*D4)
for cx, cy, r in (D1, D2, D3, D4):
    msp.add_circle((cx, cy), r, dxfattribs={"layer": "OPISY"})

wykazy(1690, 385)

doc.set_modelspace_vport(height=1600, center=(SHW/2, SHH/2))
doc.saveas("outputs/pergola.dxf")
print("OK, zapisano DXF")

from ezdxf.addons.drawing import matplotlib as mpl_draw
mpl_draw.qsave(msp, "outputs/pergola_preview.png",
               size_inches=(33.1, 23.4), dpi=180, bg="#FFFFFF")
print("OK, podgląd")

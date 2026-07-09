# -*- coding: utf-8 -*-
"""
PERGOLA — projekt wykonawczy, wg standardu wytyczne/WYTYCZNE_DXF.md
- DXF R2013 ASCII, model 1:1 w MILIMETRACH (wymiar 3000 = 3000 mm)
- rzeczywiste encje: LINE / LWPOLYLINE / CIRCLE / ARC / MTEXT / DIMENSION / MULTILEADER
- BEZ bloków, BEZ proxy, BEZ HATCH (kreskowanie liniami na KRESKOWANIE),
  BEZ grotów OBLIQUE (groty ISO closed-filled)
- warstwy: KONTUR / OSIE / WYMIARY / OPISY / KRESKOWANIE
- font Arial (polskie znaki), teksty 2.5/3.5/5.0 mm (na wydruku), druk 1:20
"""
import math
import ezdxf
from ezdxf.math import Vec2
from ezdxf.enums import MTextEntityAlignment
from ezdxf.render import mleader

PS = 20  # skala druku 1:20 -> mnoznik anotacji, by tekst mial nominalne mm na papierze

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

# dimstyle ISO — groty closed-filled (dimtsz=0 => bez kreskowych/OBLIQUE), skala 20
ds = doc.dimstyles.add("ISO")
for k, v in dict(dimtxt=3.5, dimasz=3.5, dimexe=1.25, dimexo=2.0, dimgap=1.0,
                 dimtad=1, dimtsz=0.0, dimdec=0, dimlfac=1.0, dimscale=PS,
                 dimclrt=3, dimtxsty="ARIAL", dimblk="").items():
    ds.set_dxf_attrib(k, v)

# ------------------------------------------------------------------ helpers
def L(x1, y1, x2, y2, layer="KONTUR"):
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": layer})

def R(x, y, w, h, layer="KONTUR"):
    msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
                       close=True, dxfattribs={"layer": layer})

def T(s, x, y, mm=3.5, align=MTextEntityAlignment.MIDDLE_LEFT, layer="OPISY", rot=0):
    m = msp.add_mtext(s, dxfattribs={"layer": layer, "style": "ARIAL",
                                     "char_height": mm * PS, "rotation": rot})
    m.set_location((x, y), attachment_point=align)
    return m

def DIMH(x1, x2, y, p1y, p2y=None, off=0):
    """poziomy wymiar miedzy x1,x2; linia wymiarowa na wys. y."""
    p2y = p1y if p2y is None else p2y
    d = msp.add_linear_dim(base=(0, y), p1=(x1, p1y), p2=(x2, p2y),
                           angle=0, dimstyle="ISO", dxfattribs={"layer": "WYMIARY"})
    d.render()

def DIMV(y1, y2, x, p1x, p2x=None):
    p2x = p1x if p2x is None else p2x
    d = msp.add_linear_dim(base=(x, 0), p1=(p1x, y1), p2=(p2x, y2),
                           angle=90, dimstyle="ISO", dxfattribs={"layer": "WYMIARY"})
    d.render()

def LEAD(text, target, insert, side=mleader.ConnectionSide.left, mm=3.0):
    ml = msp.add_multileader_mtext("Standard")
    ml.multileader.dxf.layer = "OPISY"
    ml.set_content(text, style="ARIAL", char_height=mm,
                   alignment=mleader.TextAlignment.left)
    ml.set_overall_scaling(PS)
    ml.add_leader_line(side, [Vec2(target)])
    ml.build(insert=Vec2(insert))

def hatch_lines(x, y, w, h, spacing, ang_deg, layer="KRESKOWANIE"):
    """wypelnia prostokat rownoleglymi LINIAMI pod katem (zamiast encji HATCH)."""
    a = math.radians(ang_deg)
    dx, dy = math.cos(a), math.sin(a)          # kierunek linii
    nx, ny = -dy, dx                           # normalna
    cx, cy = x + w / 2, y + h / 2
    corners = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    proj = [ (px - cx) * nx + (py - cy) * ny for px, py in corners]
    s0, s1 = min(proj), max(proj)
    s = s0 + spacing / 2
    while s < s1:
        px, py = cx + s * nx, cy + s * ny
        seg = _clip(px, py, dx, dy, x, x + w, y, y + h)
        if seg:
            t0, t1 = seg
            L(px + t0 * dx, py + t0 * dy, px + t1 * dx, py + t1 * dy, layer)
        s += spacing

def _clip(px, py, dx, dy, xmin, xmax, ymin, ymax):
    t0, t1 = -1e18, 1e18
    for p, d, lo, hi in ((px, dx, xmin, xmax), (py, dy, ymin, ymax)):
        if abs(d) < 1e-12:
            if p < lo or p > hi:
                return None
        else:
            ta, tb = (lo - p) / d, (hi - p) / d
            if ta > tb:
                ta, tb = tb, ta
            t0, t1 = max(t0, ta), min(t1, tb)
    return (t0, t1) if t0 < t1 else None

# ------------------------------------------------------------------ wymiary pergoli (mm)
AX, AY = 3000, 4000          # rozstaw osi slupow: szerokosc x glebokosc
SL = 140                     # slup 140 x 140
BW, BH = 100, 200            # belka nosna 100 (szer) x 200 (wys)
KW, KH = 60, 160             # krokiew 60 (szer) x 160 (wys)
OKAP = 350                   # wysieg belek i krokwi
NKROK = 10                   # liczba krokwi
Z_SD = 100                   # spod slupa (na kotwie 100 nad terenem)
HS = 2400                    # wysokosc slupa
Z_SG = Z_SD + HS             # 2500 wierzch slupa = spod belki
Z_BG = Z_SG + BH             # 2700 wierzch belki
Z_KG = Z_BG + KH             # 2860 wierzch krokwi
FW = 400                     # stopa 400 x 400
F_TOP, F_BOT = -400, -1000    # stopa fundamentowa; spod -1,00 m (poniżej przemarzania, strefa II/III)
CH = 100                     # chudy beton pod stopa

krok_y = [(-OKAP + i * (AY + 2 * OKAP) / (NKROK - 1)) for i in range(NKROK)]

# =================================================================== RZUT
def rzut(ox, oy):
    def rx(x): return ox + x
    def ry(y): return oy + y
    # osie slupow (OSIE) — kreska-kropka, z wysunieciem
    for ax in (0, AX):
        L(rx(ax), ry(-OKAP - 250), rx(ax), ry(AY + OKAP + 250), "OSIE")
    for ay in (0, AY):
        L(rx(-OKAP - 250), ry(ay), rx(AX + OKAP + 250), ry(ay), "OSIE")
    # belki (2) wzdluz Y na osiach X=0, X=AX
    for ax in (0, AX):
        R(rx(ax - BW / 2), ry(-OKAP), BW, AY + 2 * OKAP, "KONTUR")
    # krokwie (NKROK) wzdluz X na wierzchu belek
    for ky in krok_y:
        R(rx(-OKAP), ry(ky - KW / 2), AX + 2 * OKAP, KW, "KONTUR")
    # slupy (4) — widoczne pod krokwiami: rysujemy kontur
    for ax in (0, AX):
        for ay in (0, AY):
            R(rx(ax - SL / 2), ry(ay - SL / 2), SL, SL, "KONTUR")
    # linia ciecia A-A (przez lewa os slupow X=0), strzalki -> +X, litery
    xcut = rx(-OKAP - 550)
    L(xcut, ry(-OKAP - 100), xcut, ry(AY + OKAP + 100), "OSIE")
    for ay in (ry(-OKAP - 100), ry(AY + OKAP + 100)):
        # grot ISO otwarty (2 linie), kierunek +X
        L(xcut, ay, xcut + 260, ay, "OSIE")
        yd = -1 if ay < oy else 1
        L(xcut + 260, ay, xcut + 180, ay - 70 * yd, "OSIE")
        L(xcut + 260, ay, xcut + 180, ay + 70 * yd, "OSIE")
        T("A", xcut - 40, ay, 5.0, MTextEntityAlignment.MIDDLE_RIGHT)
    # wymiary
    DIMH(rx(0), rx(AX), ry(-OKAP - 900), ry(-OKAP - 900))
    DIMV(ry(0), ry(AY), rx(-OKAP - 900), rx(-OKAP - 900))
    DIMH(rx(-OKAP), rx(AX + OKAP), ry(AY + OKAP + 700), ry(AY + OKAP + 700))
    # opis krokwi (MLEADER) — wskazuje na 2 krokwie wspolnym opisem
    ml = msp.add_multileader_mtext("Standard")
    ml.multileader.dxf.layer = "OPISY"
    ml.set_content("krokwie 60×160 mm\nrozstaw ~500 mm", style="ARIAL",
                   char_height=3.0, alignment=mleader.TextAlignment.left)
    ml.set_overall_scaling(PS)
    ml.add_leader_line(mleader.ConnectionSide.right, [Vec2(rx(AX + OKAP - 200), ry(krok_y[2]))])
    ml.add_leader_line(mleader.ConnectionSide.right, [Vec2(rx(AX + OKAP - 200), ry(krok_y[6]))])
    ml.build(insert=Vec2(rx(AX + OKAP + 1400), ry(AY / 2)))
    LEAD("belka nośna\n100×200 mm", (rx(AX / 2), ry(-OKAP + 60)),
         (rx(AX / 2 + 900), ry(-OKAP - 300)), mleader.ConnectionSide.left)
    LEAD("słup 140×140 mm", (rx(0), ry(0)), (rx(-1900), ry(AY / 2)),
         mleader.ConnectionSide.right)
    T("RZUT   1:20", rx(AX / 2), ry(AY + OKAP + 1300), 5.0,
      MTextEntityAlignment.MIDDLE_CENTER, "OPISY")

# =================================================================== WIDOK OD PRZODU
def widok_przod(ox, oy):
    def rx(x): return ox + x
    def rz(z): return oy + z
    # teren
    L(rx(-OKAP - 400), rz(0), rx(AX + OKAP + 400), rz(0), "KONTUR")
    hatch_lines(rx(-OKAP - 400), rz(-160), (AX + 2 * OKAP + 800), 160, 130, 45, "KRESKOWANIE")
    # cokoly (2)
    for ax in (0, AX):
        R(rx(ax - 150), rz(0), 300, Z_SD, "KONTUR")
    # slupy (2)
    for ax in (0, AX):
        R(rx(ax - SL / 2), rz(Z_SD), SL, HS, "KONTUR")
    # belki widziane na czolo (2) — 100 szer x 200 wys
    for ax in (0, AX):
        R(rx(ax - BW / 2), rz(Z_SG), BW, BH, "KONTUR")
    # krokwie: pasmo na wierzchu (widziane z boku jako jeden gabaryt) + wysiegi
    R(rx(-OKAP), rz(Z_BG), AX + 2 * OKAP, KH, "KONTUR")
    # wymiary wysokosciowe
    DIMV(rz(0), rz(Z_SG), rx(-OKAP - 700), rx(-OKAP - 700))
    DIMV(rz(Z_SG), rz(Z_KG), rx(-OKAP - 700), rx(-OKAP - 700))
    DIMV(rz(0), rz(Z_KG), rx(-OKAP - 1400), rx(-OKAP - 1400))
    DIMH(rx(0), rx(AX), rz(-700), rz(-700))
    T("WIDOK OD PRZODU   1:20", rx(AX / 2), rz(Z_KG + 700), 5.0,
      MTextEntityAlignment.MIDDLE_CENTER)

# =================================================================== PRZEKROJ A-A (kierunek Y, z fundamentem)
def przekroj(ox, oy):
    def ry(y): return ox + y      # os pozioma = glebokosc Y
    def rz(z): return oy + z
    # teren
    L(ry(-OKAP - 400), rz(0), ry(AY + OKAP + 400), rz(0), "KONTUR")
    hatch_lines(ry(-OKAP - 400), rz(-180), (AY + 2 * OKAP + 800), 180, 130, 45, "KRESKOWANIE")
    for ay in (0, AY):
        # --- fundament (przeciety => kreskowanie) ---
        R(ry(ay - CH * 1.5), rz(F_BOT - CH), FW + CH, CH, "KONTUR")            # chudy beton
        hatch_lines(ry(ay - CH * 1.5), rz(F_BOT - CH), FW + CH, CH, 90, 45, "KRESKOWANIE")
        R(ry(ay - FW / 2), rz(F_BOT), FW, F_TOP - F_BOT, "KONTUR")            # stopa
        hatch_lines(ry(ay - FW / 2), rz(F_BOT), FW, F_TOP - F_BOT, 70, 45, "KRESKOWANIE")
        R(ry(ay - 150), rz(F_TOP), 300, -F_TOP + Z_SD, "KONTUR")              # cokol do +Z_SD
        hatch_lines(ry(ay - 150), rz(F_TOP), 300, -F_TOP + Z_SD, 70, 45, "KRESKOWANIE")
        # kotwa stalowa (marka) — schematycznie
        L(ry(ay), rz(-150), ry(ay), rz(Z_SD + 120), "KONTUR")
        # --- slup drewniany (przeciety => kreskowanie gestsze) ---
        R(ry(ay - SL / 2), rz(Z_SD), SL, HS, "KONTUR")
        hatch_lines(ry(ay - SL / 2), rz(Z_SD), SL, HS, 45, 45, "KRESKOWANIE")
    # belka nosna wzdluz Y (przecieta) na obu slupach — jedna ciagla
    R(ry(-OKAP), rz(Z_SG), AY + 2 * OKAP, BH, "KONTUR")
    hatch_lines(ry(-OKAP), rz(Z_SG), AY + 2 * OKAP, BH, 55, 45, "KRESKOWANIE")
    # krokwie na czolo (widok, bez kreskowania) — rzad prostokatow
    for ky in krok_y:
        R(ry(ky - KW / 2), rz(Z_BG), KW, KH, "KONTUR")
    # wymiary
    DIMH(ry(0), ry(AY), rz(Z_KG + 700), rz(Z_KG + 700))
    DIMV(rz(F_BOT), rz(0), ry(-OKAP - 700), ry(-OKAP - 700))
    DIMV(rz(0), rz(Z_SG), ry(-OKAP - 700), ry(-OKAP - 700))
    DIMV(rz(F_BOT - CH), rz(Z_KG), ry(-OKAP - 1400), ry(-OKAP - 1400))
    # opisy warstw (MLEADER)
    LEAD("słup drewniany C24\n140×140 mm", (ry(0), rz(Z_SD + HS / 2)),
         (ry(AY / 2 - 400), rz(HS)), mleader.ConnectionSide.left)
    LEAD("belka nośna\n100×200 mm", (ry(AY / 2), rz(Z_SG + BH / 2)),
         (ry(AY + OKAP + 300), rz(Z_SG + 300)), mleader.ConnectionSide.left)
    LEAD("stopa fundamentowa\nbeton C20/25  400×400×600\nposad. −1,00 m (poniżej przemarzania)",
         (ry(AY), rz((F_TOP + F_BOT) / 2)),
         (ry(AY + OKAP + 300), rz(F_BOT + 100)), mleader.ConnectionSide.left)
    LEAD("chudy beton C8/10 gr. 100", (ry(0), rz(F_BOT - CH / 2)),
         (ry(-OKAP - 300), rz(F_BOT - 400)), mleader.ConnectionSide.right)
    LEAD("kotwa/podstawa słupa\nstalowa ocynk., +0,10 m", (ry(AY), rz(Z_SD)),
         (ry(AY + OKAP + 300), rz(Z_SD - 500)), mleader.ConnectionSide.left)
    T("PRZEKRÓJ A-A   1:20", ry(AY / 2), rz(Z_KG + 1300), 5.0,
      MTextEntityAlignment.MIDDLE_CENTER)

# =================================================================== DETAL podstawy slupa
def detal(ox, oy):
    def ry(y): return ox + y
    def rz(z): return oy + z
    ay = 0
    L(ry(-500), rz(0), ry(500), rz(0), "KONTUR")                    # teren
    hatch_lines(ry(-500), rz(-120), 1000, 120, 90, 45, "KRESKOWANIE")
    R(ry(ay - 150), rz(F_TOP), 300, -F_TOP + Z_SD, "KONTUR")        # cokol
    hatch_lines(ry(ay - 150), rz(F_TOP), 300, -F_TOP + Z_SD, 50, 45, "KRESKOWANIE")
    R(ry(ay - SL / 2), rz(Z_SD), SL, 500, "KONTUR")                 # dolny fragment slupa
    hatch_lines(ry(ay - SL / 2), rz(Z_SD), SL, 500, 35, 45, "KRESKOWANIE")
    # podstawa stalowa U + kotwa
    L(ry(ay - SL / 2 - 10), rz(Z_SD), ry(ay - SL / 2 - 10), rz(Z_SD + 180), "KONTUR")
    L(ry(ay + SL / 2 + 10), rz(Z_SD), ry(ay + SL / 2 + 10), rz(Z_SD + 180), "KONTUR")
    L(ry(ay - SL / 2 - 10), rz(Z_SD), ry(ay + SL / 2 + 10), rz(Z_SD), "KONTUR")
    L(ry(ay), rz(-150), ry(ay), rz(Z_SD + 180), "OSIE")            # trzpien kotwy
    # sruby (otwory) — okregi
    for dxs in (-40, 40):
        msp.add_circle((ry(ay + dxs), rz(Z_SD + 90)), 12, dxfattribs={"layer": "KONTUR"})
    DIMV(rz(0), rz(Z_SD), ry(650), ry(650))
    DIMV(rz(F_TOP), rz(0), ry(650), ry(650))
    LEAD("podstawa słupa — stal ocynk.\nmocowanie 2× śruba M12", (ry(SL / 2), rz(Z_SD + 90)),
         (ry(900), rz(Z_SD + 400)), mleader.ConnectionSide.left)
    LEAD("słup drewniany 140×140", (ry(0), rz(Z_SD + 350)),
         (ry(-1100), rz(Z_SD + 500)), mleader.ConnectionSide.right)
    T("DETAL 1 — podstawa słupa   1:5", ry(0), rz(Z_SD + 900), 5.0,
      MTextEntityAlignment.MIDDLE_CENTER)

# ------------------------------------------------------------------ rozmieszczenie widokow
# Uklad 2-rzedowy (zamiast dlugiego pasa), by arkusz mial proporcje A1 landscape:
#   gora:  RZUT (lewo)   |  PRZEKROJ A-A (prawo)
#   dol:   WIDOK (lewo)  |  DETAL (srodek)  |  WYKAZ + TABELKA (prawo)
rzut(0, 5600)
przekroj(8200, 5900)
widok_przod(0, 0)
detal(5200, 400)

# wykaz materialow (dolny pas, miedzy detalem a tabelka rysunkowa)
wx0, wy0, wdy = 7000, 1350, 285
rows = [
    "WYKAZ MATERIAŁÓW",
    "1. Słupy drewniane C24  140×140 mm — 4 szt.",
    "2. Belki nośne  100×200 mm — 2 szt.",
    "3. Krokwie  60×160 mm — 10 szt., rozstaw ~500 mm",
    "4. Podstawy słupów stalowe ocynk. + śruby M12 — 4 kpl.",
    "5. Stopy fundamentowe beton C20/25  400×400×600 mm — 4 szt.",
    "6. Chudy beton C8/10 gr. 100 mm pod stopami",
    "7. Impregnacja drewna ciśnieniowa; łączniki ocynk./nierdz.",
]
for i, s in enumerate(rows):
    T(s, wx0, wy0 + (len(rows) - i) * wdy, 3.5 if i == 0 else 2.5)

# ------------------------------------------------------------------ ramka A1 + tabelka
from ezdxf import bbox
ext = bbox.extents(msp)
xmin, ymin = ext.extmin.x, ext.extmin.y
xmax, ymax = ext.extmax.x, ext.extmax.y
PAD = 500
xmin -= PAD; ymin -= PAD; xmax += PAD; ymax += PAD
w, h = xmax - xmin, ymax - ymin
R_A1 = 841.0 / 594.0                       # proporcja arkusza A1 poziomo ~1.416
if w / h > R_A1:                           # za szeroko -> dodaj wysokosc
    dy = (w / R_A1 - h) / 2; ymin -= dy; ymax += dy
else:                                      # za wysoko -> dodaj szerokosc
    dx = (h * R_A1 - w) / 2; xmin -= dx; xmax += dx
fw, fh = xmax - xmin, ymax - ymin
R(xmin, ymin, fw, fh, "KONTUR")                        # obwiednia arkusza
mI = 300
R(xmin + mI, ymin + mI, fw - 2 * mI, fh - 2 * mI, "KONTUR")   # ramka wewn.

# tabelka rysunkowa (prawy dolny rog, przy ramce wewn.)
tw, th = 5200, 1600
tx0, ty0 = xmax - mI - 80 - tw, ymin + mI + 80
R(tx0, ty0, tw, th, "KONTUR")
L(tx0, ty0 + th * 0.66, tx0 + tw, ty0 + th * 0.66, "KONTUR")
L(tx0, ty0 + th * 0.33, tx0 + tw, ty0 + th * 0.33, "KONTUR")
L(tx0 + tw * 0.66, ty0, tx0 + tw * 0.66, ty0 + th, "KONTUR")
T("PERGOLA OGRODOWA — PROJEKT WYKONAWCZY", tx0 + 150, ty0 + th * 0.83, 3.5)
T("Wykonał: Pola Organiszczak    SGGW, Architektura krajobrazu", tx0 + 150, ty0 + th * 0.50, 2.5)
T("Rysunek: rzut, widok, przekrój A-A, detal", tx0 + 150, ty0 + th * 0.17, 2.5)
T("Skala: 1:20 / 1:5", tx0 + tw * 0.66 + 150, ty0 + th * 0.50, 3.5)
T("Jedn.: mm", tx0 + tw * 0.66 + 150, ty0 + th * 0.17, 2.5)

# ------------------------------------------------------------------ zapis + podglad
import datetime
TS = datetime.datetime.now().strftime("%y%m%d-%H%M")   # yyMMdd-hhmm na koncu nazwy
_dxf = "outputs/pergola_v2_%s.dxf" % TS
_png = "outputs/podgląd_pergola_v2_%s.png" % TS

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
_ar = fw / fh
_mpl.qsave(msp, _png, size_inches=(16.5 * _ar / 1.416, 16.5), dpi=150, bg="#FFFFFF")
print("OK podglad", _png)

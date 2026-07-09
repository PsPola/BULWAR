# -*- coding: utf-8 -*-
"""
POGLADOWY PLAN DZIALKI 33 x 12 m  (na podstawie recznego szkicu IMG_2393)
Cel: potwierdzic wspolne rozumienie ukladu (strefy + nawierzchnie) zanim
przejdziemy do rysunku wykonawczego. Rysunek do skali, kolory jak na szkicu.

UKLAD WSPOLRZEDNYCH: metry, origin (0,0) w lewym-dolnym rogu (przy ulicy).
Dzialka: x 0..12 (front/szerokosc), y 0..33 (glebokosc).

ZALOZENIA (do potwierdzenia) oznaczone [?] w etykietach i opisane w konsoli.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import matplotlib.patheffects as pe

PW, PH = 12.0, 33.0

fig, ax = plt.subplots(figsize=(8.0, 17.5))
ax.set_xlim(-3.5, 15.5)
ax.set_ylim(-4.0, 36.0)
ax.set_aspect("equal")
ax.axis("off")

HALO = [pe.withStroke(linewidth=3, foreground="white")]

def zona(x, y, w, h, fc, ec, lw=1.6, alpha=1.0, hatch=None, z=2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                           lw=lw, alpha=alpha, hatch=hatch, zorder=z))

def txt(s, x, y, fs=11, w="bold", c="black", rot=0, ha="center", va="center",
        halo="white"):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=c, weight=w,
            rotation=rot, zorder=6,
            path_effects=[pe.withStroke(linewidth=3, foreground=halo)])

def dim(p1, p2, s, fs=10):
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="<->", color="#333", lw=1.1), zorder=5)
    mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
    rot = 90 if abs(p2[1]-p1[1]) > abs(p2[0]-p1[0]) else 0
    txt(s, mx, my, fs, "normal", "#222", rot)

# --- ULICA ---
ax.add_patch(Rectangle((-3.5, -4.0), 19.0, 4.0, facecolor="#E2E2E2",
                       edgecolor="none", hatch="////", zorder=0))
txt("ul. Ogrodowa", 6, -2.2, 13, "bold", "#555")

# --- TRAWNIK (tlo strefy zielonej) ---
ax.add_patch(Rectangle((0, 3), 12, 30, facecolor="#E9F4DC", edgecolor="none", zorder=1))

# --- PODJAZD (rozowy) 12 x 3 m ---
zona(0, 0, 12, 3, "#F6C4DB", "#D81B8C")
txt("PODJAZD  12 × 3 m", 6, 1.5, 11)
# furtka + brama na linii ulicy
ax.plot([1.0, 2.4], [0, 0], color="#8B5E00", lw=5, zorder=7)
ax.plot([6.5, 11.0], [0, 0], color="#8B5E00", lw=5, zorder=7)
txt("furtka", 1.7, 0.5, 8.5, "normal")
txt("brama", 8.7, 0.5, 8.5, "normal")

# --- DOM (szary) 7 x 15 m, przy prawej granicy ---
zona(5, 3, 7, 15, "#D6D6D6", "#4D4D4D", lw=2.0)
txt("DOM\n7 × 15 m", 8.5, 11.5, 13)
# garaz (ciemniejszy) w dolnej-prawej czesci domu
zona(8, 3, 4, 3, "#BBBBBB", "#4D4D4D", lw=1.2, z=3)
txt("GARAŻ", 10, 4.5, 9)
# wejscie glowne (od strony podjazdu / sciezki)
txt("wejście\ngłówne", 6.2, 4.4, 8, "normal", "#222")
ax.annotate("", xy=(5.0, 4.2), xytext=(6.0, 4.2),
            arrowprops=dict(arrowstyle="->", color="#c00", lw=1.6), zorder=7)

# --- SCIEZKI 1 m (uklad L): zielona pionowa + niebieska pozioma ---
zona(4, 3, 1, 16, "#8FD14F", "#4E8A1E", z=4)          # boczna, wzdluz domu -> do y=19
zona(5, 18, 7, 1, "#59C4E6", "#1E7EA0", z=4)          # gorna, nad domem -> do prawej granicy
txt("ścieżka 1 m", 4.5, 11, 9, "bold", "#1a4d00", 90)
txt("ścieżka 1 m", 8.5, 18.5, 9, "bold", "#0a3b52")

# --- PODEST 3 x 4 m (fioletowy) prawy-gorny rog ---
zona(8, 30, 4, 3, "#C724B1", "#7A1470", z=4)
txt("PODEST\n4 × 3 m", 10, 31.5, 10, "bold", "white", halo="#7A1470")

# --- SCHODKI 1 m (pomaranczowy) laczace podest ze sciezka ---
zona(11, 19, 1, 11, "#FF7A33", "#B84A00", z=4)
txt("schodki 1 m", 11.5, 24.5, 9, "bold", "#5c2400", 90)

# --- DRZEWO w trawniku [? polozenie] ---
ax.add_patch(Circle((3.0, 27.0), 1.3, facecolor="#7BB661", edgecolor="#3f6b2f",
                    lw=1.4, zorder=4))
ax.add_patch(Circle((3.0, 27.0), 0.25, facecolor="#3f6b2f", edgecolor="none", zorder=5))
txt("drzewo [?]", 3.0, 24.8, 9, "normal", "#2f5020")
txt("TRAWNIK", 3.0, 21.5, 12, "bold", "#3f6b2f")

# --- WYMIARY GABARYTOWE ---
dim((0, -3.2), (12, -3.2), "12,0 m")            # front
dim((13.6, 0), (13.6, 33), "33,0 m")            # bok
dim((-1.4, 0), (-1.4, 3), "3 m")                # glebokosc podjazdu
dim((-1.4, 3), (-1.4, 18), "15 m")              # wysokosc domu
dim((0, 19.6), (5, 19.6), "5 m")                # korytarz od zachodu

# --- TYTUL + PN ---
txt("PLAN DZIAŁKI  33 × 12 m  —  układ poglądowy (wg szkicu)", 5.5, 35.4, 13)
ax.annotate("", xy=(-2.4, 35.3), xytext=(-2.4, 33.6),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.8), zorder=7)
txt("N", -2.4, 35.7, 12)

plt.savefig("outputs/dzialka_poglad.png", dpi=150, bbox_inches="tight",
            facecolor="white")
print("OK, zapisano outputs/dzialka_poglad.png")

print("""
ZALOZENIA DO POTWIERDZENIA:
 - drzewo: dokladne polozenie ('10 m do drzewa') - przyjete orientacyjnie
 - schodki 1 m: przyjete jako pionowy ciag przy prawej granicy (podest -> sciezka)
 - garaz 4x3 m w bryle domu; wejscie glowne od strony sciezki/podjazdu
 - sciezka 1 m (nie 3 m jak w obecnym gen_nawierzchnia.py)
 - podjazd 12x3 m na calej szerokosci frontu
""")

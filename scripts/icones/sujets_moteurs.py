"""Icônes des moteurs (29) et des configurations de motorisation (51)."""
import math

import numpy as np

from dessin import Canvas, cyl, sphere, flat, plane_lit, ROMAN


# ---------------------------------------------------------------- moteurs à pistons
def _bank(c, x0, x1, y_top, y_bot, n, dark=0.0, slant=2.0):
    """Rangée de cylindres en ligne (vue de côté), culasses en haut."""
    c.poly([(x0 + slant, y_top), (x1 + slant, y_top), (x1, y_bot), (x0, y_bot)],
           cyl((x0, (y_top + y_bot) / 2), (x1, (y_top + y_bot) / 2), (y_bot - y_top) / 2, base=0.42 - dark, amp=0.48 - dark))
    step = (x1 - x0) / n
    for i in range(n):
        x = x0 + slant + i * step + 0.6
        c.rrect((x, y_top - 0.8, x + step - 1.2, y_top + 2.6), 0.8, cyl((x, y_top), (x + step, y_top), 1.6, base=0.5 - dark), outline=False)
        c.line([(x - 0.3, y_bot - 1.2), (x + step - 1.5, y_bot - 1.2)], 0.35, 0.3)


def _prop_shaft(c, y=23.6, x1=5):
    c.rrect((0.5, y - 2.4, x1, y + 2.4), 1, cyl((0, y), (x1, y), 2.4, base=0.5))


def engine_v():
    c = Canvas()
    _bank(c, 19, 52, 3.5, 12, 6, dark=0.12, slant=4)              # rangée arrière, bien visible : le « V »
    c.rrect((12, 17, 51, 31), 3, cyl((12, 24), (51, 24), 7))
    _bank(c, 13, 45, 11, 19, 6)
    for i in range(6):
        c.ellipse((17.5 + i * 5.3, 18.6, 19.9 + i * 5.3, 20.6), 0.12, outline=False)
    c.rrect((17, 30, 46, 35), 2, cyl((17, 32.5), (46, 32.5), 3, base=0.25, amp=0.4))
    c.poly([(4, 18), (13, 15), (13, 32), (4, 29)], cyl((4, 23.5), (13, 23.5), 8))
    _prop_shaft(c)
    c.circle(50.5, 23.5, 5, sphere(50.5, 23.5, 5))
    c.circle(50.5, 23.5, 2, 0.2, outline=False)
    return c


def engine_inline():
    c = Canvas()
    c.rrect((12, 18, 50, 31), 3, cyl((12, 24.5), (50, 24.5), 6.5))
    _bank(c, 13, 47, 9, 19, 6)
    for i in range(6):
        c.ellipse((17 + i * 5.6, 19.2, 19.4 + i * 5.6, 21.2), 0.12, outline=False)
    c.rrect((17, 30, 45, 35), 2, cyl((17, 32.5), (45, 32.5), 3, base=0.25, amp=0.4))
    c.poly([(4, 19), (13, 16), (13, 31), (4, 28)], cyl((4, 23.5), (13, 23.5), 7.5))
    _prop_shaft(c)
    c.rrect((48, 20, 54, 29), 2, cyl((48, 24.5), (54, 24.5), 4.5, base=0.35))
    return c


def engine_diesel():
    """Diesel à pistons opposés (type Jumo 205) : haut bloc, deux vilebrequins."""
    c = Canvas()
    c.rrect((12, 9, 50, 34), 2.5, cyl((12, 21.5), (50, 21.5), 12.5, base=0.36))
    c.rrect((11, 6.5, 51, 11.5), 2, cyl((11, 9), (51, 9), 2.5, base=0.5))
    c.rrect((11, 31.5, 51, 36.5), 2, cyl((11, 34), (51, 34), 2.5, base=0.3))
    for i in range(6):
        x = 15 + i * 5.8
        c.line([(x, 13), (x, 30)], 0.45, 0.35)
        c.ellipse((x + 1, 20.5, x + 3.8, 23), 0.12, outline=False)
    c.poly([(4, 17), (12, 14), (12, 30), (4, 27)], cyl((4, 22), (12, 22), 7.5))
    _prop_shaft(c, 22)
    return c


def _radial_face(c, cx, cy, R, n, r_cyl, hub, base=0.32):
    for i in range(n):
        th = 2 * math.pi * i / n - math.pi / 2
        u, v = math.cos(th), math.sin(th)

        def P(rr, w):
            return (cx + u * rr - v * w, cy + v * rr + u * w)
        rin = hub * 0.85
        c.poly([P(rin, -r_cyl), P(R - 1.5, -r_cyl), P(R, -r_cyl * 0.6), P(R, r_cyl * 0.6), P(R - 1.5, r_cyl), P(rin, r_cyl)],
               cyl(P(rin, 0), P(R, 0), r_cyl, base=base))
        for rr in np.arange(rin + 1.5, R - 1.5, max(1.1, (R - rin) / 7)):
            c.line([P(rr, -r_cyl + 0.2), P(rr, r_cyl - 0.2)], 0.35, 0.4)
    c.circle(cx, cy, hub, sphere(cx, cy, hub, base=0.28, amp=0.55))
    c.circle(cx, cy, hub * 0.5, sphere(cx, cy, hub * 0.5, base=0.42))


def engine_radial():
    c = Canvas()
    c.rrect((24, 14, 50, 33), 4, cyl((24, 23.5), (50, 23.5), 9.5, base=0.3, amp=0.4))   # carter arrière
    c.rrect((44, 17, 54, 30), 3, cyl((44, 23.5), (54, 23.5), 6.5, base=0.35))
    _radial_face(c, 20, 21, 18, 9, 3.2, 7)
    return c


def engine_rotary():
    c = Canvas()
    _radial_face(c, 26, 21, 18, 7, 3.6, 7, base=0.36)
    c.arc((5, 0.5, 47, 41.5), 200, 250, 0.6, 0.2)               # flèches de rotation
    c.arc((5, 0.5, 47, 41.5), 20, 70, 0.6, 0.2)
    c.rrect((44, 18, 53, 25), 2, cyl((44, 21.5), (53, 21.5), 3.5, base=0.4))
    return c


def engine_flat():
    """Moteur à plat (cylindres opposés, vu de dessus), hélice vers le haut."""
    c = Canvas()
    c.rrect((24, 9, 32, 36), 3, cyl((24, 22), (32, 22), 4, base=0.4))
    for y in (14, 25):
        for side in (-1, 1):
            x0 = 28 + side * 4
            x1 = 28 + side * 21
            c.bar((x0, y + 2.5), (x1, y + 2.5), 3.4, cyl((x0, y + 2.5), (x1, y + 2.5), 3.4, base=0.4))
            for k in range(6):
                xx = x0 + side * (3 + k * 2.6)
                c.line([(xx, y - 0.6), (xx, y + 5.6)], 0.4, 0.45)
    c.rrect((25.5, 2, 30.5, 9.5), 1.5, cyl((25.5, 6), (30.5, 6), 2.5, base=0.5))
    return c


# ---------------------------------------------------------------- réaction
def engine_pulsejet():
    c = Canvas()
    c.bar((3, 21), (16, 21), 6.5, cyl((3, 21), (16, 21), 6.5))
    c.poly([(16, 14.5), (26, 17.5), (26, 24.5), (16, 27.5)], cyl((16, 21), (26, 21), 6))
    c.bar((26, 21), (53, 21), 3.4, cyl((26, 21), (53, 21), 3.4, base=0.45))
    for x in (5, 8, 11):
        c.line([(x, 15.5), (x, 26.5)], 0.4, 0.45)                 # grille de clapets
    c.line([(40, 17.8), (40, 24.2)], 0.35, 0.3)
    return c


def engine_centrifugal():
    c = Canvas()
    c.circle(15, 21, 12, sphere(15, 21, 12, base=0.3, amp=0.55))   # carter du compresseur
    c.circle(15, 21, 5, sphere(15, 21, 5, base=0.45))
    for k in range(5):                                             # chambres de combustion
        y = 11 + k * 5
        c.bar((22, y), (38, 21 + (y - 21) * 0.4), 2.1, cyl((22, y), (38, 21), 2.1, base=0.42))
    c.poly([(36, 15), (44, 17), (44, 25), (36, 27)], cyl((36, 21), (44, 21), 6))
    c.bar((44, 21), (54, 21), 3.6, cyl((44, 21), (54, 21), 3.6, base=0.4))
    return c


def engine_axial():
    c = Canvas()
    c.poly([(2, 21), (8, 15.5), (8, 26.5)], sphere(6, 21, 6, base=0.45))              # cône d'entrée
    c.bar((7, 21), (44, 21), 6.2, cyl((7, 21), (44, 21), 6.2))
    for x in range(12, 31, 3):
        c.line([(x, 15.2), (x, 26.8)], 0.35, 0.35)                 # étages du compresseur
    c.poly([(44, 15), (53, 17.5), (53, 24.5), (44, 27)], cyl((44, 21), (53, 21), 5))
    c.poly([(49, 18.8), (55, 21), (49, 23.2)], 0.2, outline=False)
    return c


def engine_turboprop():
    c = Canvas()
    c.bar((14, 23), (52, 23), 5.6, cyl((14, 23), (52, 23), 5.6))
    for x in range(20, 36, 3):
        c.line([(x, 17.8), (x, 28.2)], 0.35, 0.35)
    c.rrect((8, 17, 16, 29), 2.5, cyl((8, 23), (16, 23), 6, base=0.38))
    c.poly([(1, 23), (8, 19), (8, 27)], sphere(5, 23, 4.5, base=0.5))               # cône d'hélice
    c.bar((6, 21), (6.5, 3), 1.4, cyl((6, 21), (6.5, 3), 1.4, base=0.5))             # pales
    c.bar((6, 25), (6.5, 41), 1.4, cyl((6, 25), (6.5, 41), 1.4, base=0.4))
    return c


def engine_rocket():
    c = Canvas()
    c.bar((4, 15), (30, 15), 5, cyl((4, 15), (30, 15), 5, base=0.4))                 # réservoirs
    c.bar((4, 28), (30, 28), 4.2, cyl((4, 28), (30, 28), 4.2, base=0.35))
    c.line([(30, 15), (38, 20)], 0.8, 0.2)
    c.line([(30, 28), (38, 23)], 0.8, 0.2)
    c.circle(39, 21.5, 4.5, sphere(39, 21.5, 4.5, base=0.4))       # chambre de combustion
    c.poly([(42, 19), (55, 13), (55, 30), (42, 24)], cyl((42, 21.5), (55, 21.5), 8, base=0.3))   # tuyère
    c.poly([(52, 16), (55, 14), (55, 29), (52, 27)], 0.15, outline=False)
    return c


ENGINES = {
    "v": engine_v, "inline": engine_inline, "radial": engine_radial, "rotary": engine_rotary,
    "flat": engine_flat, "diesel": engine_diesel, "pulsejet": engine_pulsejet, "centrifugal": engine_centrifugal,
    "axial": engine_axial, "turboprop": engine_turboprop, "rocket": engine_rocket,
}


def engine(mid):
    """zv_engine_<famille>[_<n>] : dessin de la famille, palier n en chiffre romain."""
    rest = mid[len("zv_engine_"):]
    fam, _, n = rest.rpartition("_") if rest[-1].isdigit() else (rest, "", "")
    c = ENGINES[fam]()
    if n:
        c.badge = (ROMAN[int(n)], "tier")
    return c


# ---------------------------------------------------------------- configurations
def silhouette(c, span=50, chord=7, wy=17, fus=(25.5, 3, 30.5, 39), tail=(19, 34, 37, 37.5), lit=0.46):
    """Avion vu de dessus, en retrait (la pièce mise en valeur est dessinée par-dessus)."""
    x0, y0, x1, y1 = fus
    c.rrect(fus, 2.2, plane_lit(lit, 0.25, y0, y1))
    cx = (x0 + x1) / 2
    c.poly([(cx - span / 2, wy + 1.5), (cx - 3, wy - 1), (cx + 3, wy - 1), (cx + span / 2, wy + 1.5),
            (cx + span / 2, wy + chord - 1), (cx - span / 2, wy + chord - 1)], plane_lit(lit + 0.05, 0.3, wy, wy + chord))
    c.poly([(tail[0], tail[1] + 1), (tail[2], tail[1] + 1), (tail[2], tail[3]), (tail[0], tail[3])], plane_lit(lit, 0.2, tail[1], tail[3]))


def nacelle(c, x, y, ln=9, r=2.3, prop=True, rear=False):
    c.rrect((x - r, y, x + r, y + ln), r, cyl((x - r, y + ln / 2), (x + r, y + ln / 2), r, base=0.55), accent=1.0)
    if prop:
        py = y + ln + 0.6 if rear else y - 1.2
        c.ellipse((x - r - 1.6, py - 0.7, x + r + 1.6, py + 0.7), 0.85, accent=1.0, outline=False)


LAYOUTS = {
    "nose": lambda c: (silhouette(c, span=40), nacelle(c, 28, 3.5, 8, 2.8)),
    "twin_nose": lambda c: (silhouette(c, span=40), nacelle(c, 28, 3.5, 10, 3.2),
                            c.ellipse((22.5, 1.0, 33.5, 2.2), 0.85, accent=1.0, outline=False)),
    "tandem": lambda c: (silhouette(c, span=40, tail=(19, 30, 37, 33.5)), nacelle(c, 28, 3.5, 7, 2.8),
                         nacelle(c, 28, 33, 6, 2.6, rear=True)),
    "tail": lambda c: (silhouette(c, span=40, fus=(25.5, 3, 30.5, 36), tail=(19, 29, 37, 32.5)),
                       nacelle(c, 28, 32, 6, 2.8, rear=True)),
    "twin_wing": lambda c: (silhouette(c), nacelle(c, 15, 12), nacelle(c, 41, 12)),
    "tri": lambda c: (silhouette(c), nacelle(c, 28, 3.5, 7, 2.6), nacelle(c, 15, 12), nacelle(c, 41, 12)),
    "quad": lambda c: (silhouette(c, span=54), [nacelle(c, x, 12.5, 8, 2.1) for x in (9, 18.5, 37.5, 47)]),
    "quad_tandem": lambda c: (silhouette(c, span=54), [nacelle(c, x, 11, 12, 2.3) for x in (14, 42)],
                              [c.ellipse((x - 3.6, 23.4, x + 3.6, 24.6), 0.85, accent=1.0, outline=False) for x in (14, 42)]),
    "quint": lambda c: (silhouette(c, span=54), nacelle(c, 28, 3.5, 7, 2.6),
                        [nacelle(c, x, 12.5, 8, 2.1) for x in (9, 18.5, 37.5, 47)]),
    "hexa": lambda c: (silhouette(c, span=55), [nacelle(c, x, 12.5, 7.5, 1.9) for x in (5.5, 13, 20.5, 35.5, 43, 50.5)]),
}


def config(mid):
    """zv_engine_config_<disposition>_<classe> : silhouette, moteurs en valeur, classe A à D en orangé."""
    rest = mid[len("zv_engine_config_"):]
    layout, cls = rest.rsplit("_", 1)
    c = Canvas()
    LAYOUTS[layout](c)
    c.badge = (cls.upper(), "class")
    return c

"""Icônes des slots vides (GFX_EMSI_<slot>) : pictogramme vert pâle en relief, comme le seul slot vide
du vanilla (plane_role_module.dds, 76×42). Un « + » à gauche, puis soit un petit avion dont l'emplacement
du slot ressort, soit la pièce que le slot accepte."""
import math

from dessin import Canvas, cyl, sphere, flat, plane_lit

W, H = 76, 42
HI = 1.0            # mise en valeur (vert plus clair)


def _plus(c):
    c.poly([(6, 19.5), (14, 19.5), (14, 22.5), (6, 22.5)], 0.7)
    c.poly([(8.5, 17), (11.5, 17), (11.5, 25), (8.5, 25)], 0.7)


def _side(c, lit=0.5):
    """Avion vu de côté, nez à gauche, dans la zone x 18 à 74."""
    c.poly([(18, 21), (24, 17.5), (60, 18.5), (72, 17), (72, 21.5), (60, 23.5), (24, 25.5), (18, 23.5)], flat(lit, 0.25))
    c.poly([(64, 18), (70, 8), (73, 8), (72.5, 18.5)], flat(lit, 0.2))          # dérive
    c.poly([(34, 22), (52, 22), (50, 25), (36, 25)], flat(lit - 0.08, 0.2))     # aile vue de côté
    c.ellipse((30, 14.5, 40, 19), flat(lit + 0.1, 0.2))                        # verrière


def _top(c, lit=0.5):
    """Avion vu de dessus, dans la zone x 18 à 74."""
    cx = 46
    c.rrect((cx - 2.5, 4, cx + 2.5, 38), 2, flat(lit, 0.25))
    c.poly([(cx - 27, 18), (cx + 27, 18), (cx + 27, 23), (cx - 27, 23)], flat(lit + 0.05, 0.25))
    c.poly([(cx - 9, 34), (cx + 9, 34), (cx + 9, 37), (cx - 9, 37)], flat(lit, 0.2))


def _spot(c, x, y, r=3.2):
    c.circle(x, y, r, 0.85, accent=HI)


def _num(c, n):
    c.badge = (str(n), "count")


def slot(sid):
    c = Canvas(W, H)
    c.slot = True
    _plus(c)
    k = sid.replace("fixed_zv_", "").replace("zv_", "")
    if k.startswith("wing_") and k != "wing_type":
        n = int(k[-1])
        _top(c)
        x = {1: 24, 2: 68, 3: 33, 4: 59, 5: 46}[n]
        _spot(c, x, 20.5)
        _num(c, n)
    elif k.startswith("internal_"):
        _side(c)
        c.rrect((40, 18.5, 58, 23.5), 1, 0.85, accent=HI)
        _num(c, int(k[-1]))
    else:
        side_spots = {"nose": (19.5, 22), "rear_cockpit": (44, 17.5), "belly_front": (30, 25.5), "belly_middle": (43, 26),
                      "belly_rear": (56, 24.5), "tail_position": (73, 19.5), "dorsal": (52, 16.5)}
        if k in side_spots:
            _side(c)
            _spot(c, *side_spots[k])
        elif k == "propeller":
            for i in range(3):
                th = 2 * math.pi * i / 3 - math.pi / 2
                u, v = math.cos(th), math.sin(th)
                c.poly([(46 + u * 3 - v * 2, 21 + v * 3 + u * 2), (46 + u * 17, 21 + v * 17), (46 + u * 3 + v * 2, 21 + v * 3 - u * 2)], 0.65)
            c.circle(46, 21, 3.5, 0.8, accent=HI)
        elif k == "propeller_module":
            c.poly([(44, 4), (48, 4), (49, 21), (43, 21)], 0.62)
            c.circle(46, 24, 4, 0.8, accent=HI)
            c.arc((36, 8, 56, 20), 200, 340, 0.8, 0)
        elif k == "engine":
            c.rrect((26, 16, 66, 30), 3, flat(0.6, 0.3))
            for i in range(6):
                c.rrect((29 + i * 6, 9, 33 + i * 6, 16), 1, 0.7)
            c.poly([(18, 19), (26, 17), (26, 29), (18, 27)], 0.65)
        elif k == "engine_config":
            _top(c)
            for x in (32, 60):
                c.rrect((x - 2, 13, x + 2, 23), 2, 0.85, accent=HI)
        elif k in ("engine_module_1", "engine_module_2"):
            c.circle(40, 21, 11, 0.62)
            c.poly([(40, 10), (62, 10), (62, 16), (46, 16)], 0.62)
            c.circle(40, 21, 4, 0.8, accent=HI)
            _num(c, int(k[-1]))
        elif k == "materials":
            for j, y in enumerate((26, 19, 12)):
                c.poly([(24 + j * 3, y), (60 + j * 3, y), (64 + j * 3, y + 6), (28 + j * 3, y + 6)], 0.55 + 0.07 * j)
        elif k == "construction":
            c.poly([(20, 15), (72, 15), (72, 27), (20, 27)], 0.6)
            for x in range(26, 70, 8):
                c.circle(x, 21, 2.4, 0.2, outline=False)
        elif k == "landing_gear":
            c.poly([(18, 8), (72, 8), (72, 12), (18, 12)], 0.5)
            c.poly([(44, 12), (47, 12), (47, 26), (44, 26)], 0.62)
            c.circle(45.5, 30, 7, 0.8, accent=HI)
        elif k == "fuselage":
            c.poly([(18, 21), (26, 14), (60, 15.5), (72, 18), (72, 22), (60, 26), (26, 28), (18, 24)], 0.62)
            c.ellipse((30, 10, 42, 17), 0.82, accent=HI)
        elif k == "wing_type":
            a, cx, cy = 26, 46, 22
            le = [(cx + x, cy - 5 * math.sqrt(max(0, 1 - (x / a) ** 2))) for x in [i * a / 15 - a for i in range(31)]]
            te = [(cx + x, cy + 6 * math.sqrt(max(0, 1 - (x / a) ** 2))) for x in [a - i * a / 15 for i in range(31)]]
            c.poly(le + te, 0.85, accent=HI)
            c.poly([(44.5, 6), (47.5, 6), (48, 38), (44, 38)], 0.55)
        elif k == "tail":
            c.circle(46, 27, 4, 0.6)
            c.poly([(26, 26), (66, 26), (65, 29), (27, 29)], 0.85, accent=HI)
            c.poly([(44.5, 6), (47.5, 6), (48, 24), (44, 24)], 0.85, accent=HI)
        elif k == "cockpit":
            c.poly([(18, 25), (26, 22), (72, 21), (72, 31), (26, 31), (18, 29)], 0.55)
            c.poly([(32, 21.5), (38, 13), (52, 12.5), (58, 21)], 0.85, accent=HI)
        elif k == "role":
            _top(c, 0.62)
    return c

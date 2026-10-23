"""Icônes des pièces de structure : ailes (61), fuselages, empennages, trains, hélices, cockpits, matériaux,
construction. Vues de dessus ou de côté, lisibles à 56×42 : c'est la forme qui renseigne le joueur."""
import math

import numpy as np

from dessin import Canvas, cyl, sphere, flat, plane_lit

SIZE_OF = {"s": "S", "m": "M", "l": "L"}


def _size_badge(c, mid):
    suf = mid.rsplit("_", 1)[-1]
    if suf in SIZE_OF:
        c.badge = (SIZE_OF[suf], "size")


# ---------------------------------------------------------------- ailes
def planform(shape, a=24.0):
    """Demi-aile droite (bord d'attaque puis bord de fuite), x de 0 (emplanture) à a (saumon), y vers l'arrière."""
    n = 30
    xs = np.linspace(0, a, n)
    if shape == "elliptique":
        le = [(x, -6.0 * math.sqrt(max(0, 1 - (x / a) ** 2))) for x in xs]
        te = [(x, 7.0 * math.sqrt(max(0, 1 - (x / a) ** 2))) for x in xs]
    elif shape == "discoide":
        r = 14.0
        xs = np.linspace(0, r, n)
        le = [(x, -math.sqrt(max(0, r * r - x * x))) for x in xs]
        te = [(x, math.sqrt(max(0, r * r - x * x))) for x in xs]
    elif shape == "delta":
        le = [(x, -9 + 17 * x / a) for x in xs]
        te = [(x, 9) for x in xs]
    elif shape == "mixte":                                        # partie centrale droite, extrémités effilées
        le = [(x, -5 if x < a * 0.45 else -5 + 2.5 * (x - a * 0.45) / (a * 0.55)) for x in xs]
        te = [(x, 6 if x < a * 0.45 else 6 - 4 * (x - a * 0.45) / (a * 0.55)) for x in xs]
    else:
        cr, ct, sw = {"rectangulaire": (11, 10, 0), "trapezoidale": (12, 6, 2), "effilee": (11, 3.5, 2.5),
                      "laminaire": (12, 5, 0.5), "fleche_legere": (11, 6, 7), "fleche_prononcee": (11, 5, 14),
                      "fleche_inversee": (11, 6, -7), "mouette": (12, 6, 2), "mouette_inversee": (12, 6, 2),
                      "forme_unique": (9, 8, 0)}[shape]
        le = [(x, -cr * 0.45 + sw * x / a + (cr - ct) * 0.2 * x / a) for x in xs]
        te = [(x, cr * 0.55 + sw * x / a - (cr - ct) * 0.8 * x / a) for x in xs]
    return le, te


def _draw_wing(c, shape, cx, cy, a=24.0, lit=0.62, accent=0.0):
    le, te = planform(shape, a)
    right = [(cx + x, cy + y) for x, y in le] + [(cx + x, cy + y) for x, y in te[::-1]]
    left = [(cx - x, cy + y) for x, y in le] + [(cx - x, cy + y) for x, y in te[::-1]]
    ys = [p[1] for p in right]
    sh = plane_lit(lit, 0.4, min(ys), max(ys))
    c.poly(right, sh, accent=accent)
    c.poly(left, sh, accent=accent)
    c.line([(cx - a * 0.95, cy + 0.2), (cx + a * 0.95, cy + 0.2)], 0.3, 0.15) if shape not in ("discoide",) else None
    for s in (-1, 1):                                             # ailerons
        p = [(cx + s * x, cy + y - 1.8) for x, y in te if a * 0.5 < x < a * 0.92]
        if len(p) > 1:
            c.line(p, 0.4, 0.35)


def _ghost_fuselage(c, cx, y0=2.5, y1=39.5, tail=True):
    pts = [(cx, y0), (cx + 1.8, y0 + 2), (cx + 2.4, y0 + 7.5), (cx + 2.4, y1 - 9.5), (cx + 1.2, y1 - 3.5)]
    if tail:
        pts += [(cx + 6.5, y1 - 2.5), (cx + 6.5, y1), (cx - 6.5, y1), (cx - 6.5, y1 - 2.5)]
    pts += [(cx - 1.2, y1 - 3.5), (cx - 2.4, y1 - 9.5), (cx - 2.4, y0 + 7.5), (cx - 1.8, y0 + 2)]
    c.poly(pts, 0.3, a=0.4)


def _front_glyph(c, pos, x0=43, y0=33):
    """Petit repère vu de face, en bas à droite : la position de l'aile sur le fuselage."""
    w, cx, cy = 12, x0 + 6, y0 + 4
    g = 0.78
    if pos != "sans_queue":
        c.circle(cx, cy, 1.9, g)
    if pos in ("basse", "mediane", "haute", "canard"):
        y = {"basse": cy + 1.3, "mediane": cy, "haute": cy - 1.3, "canard": cy}[pos]
        c.poly([(x0, y - 0.45), (x0 + w, y - 0.45), (x0 + w, y + 0.45), (x0, y + 0.45)], g)
    elif pos == "parasol":
        c.poly([(x0, cy - 3.8), (x0 + w, cy - 3.8), (x0 + w, cy - 2.9), (x0, cy - 2.9)], g)
        c.bar((cx - 1.2, cy - 1.5), (cx - 2.4, cy - 3.0), 0.3, g)        # mâts du parasol
        c.bar((cx + 1.2, cy - 1.5), (cx + 2.4, cy - 3.0), 0.3, g)
    elif pos in ("biplan", "sesquiplan", "triplan"):
        levels = {"biplan": [(-3.4, 1), (2.0, 1)], "sesquiplan": [(-3.4, 1), (2.0, 0.6)],
                  "triplan": [(-3.6, 1), (-0.2, 1), (3.0, 1)]}[pos]
        for dy, k in levels:
            hw = w / 2 * k
            c.poly([(cx - hw, cy + dy - 0.4), (cx + hw, cy + dy - 0.4), (cx + hw, cy + dy + 0.4), (cx - hw, cy + dy + 0.4)], g)
    elif pos in ("mouette", "mouette_inversee"):
        k = -1 if pos == "mouette" else 1                          # aile cassée : vers le haut ou vers le bas
        for s in (-1, 1):
            c.bar((cx + s * 1.6, cy + k * 1.0), (cx + s * 3.2, cy + k * 2.8), 0.45, g)
            c.bar((cx + s * 3.2, cy + k * 2.8), (cx + s * 6.2, cy + k * 0.4), 0.45, g)
    elif pos == "sans_queue":
        c.poly([(x0, cy - 0.2), (cx, cy - 1.4), (x0 + w, cy - 0.2), (cx, cy + 1.0)], g)


def wing(mid):
    """zv_wing_<position>_<forme>."""
    rest = mid[len("zv_wing_"):]
    for pos in ("sans_queue", "mediane", "basse", "haute", "parasol", "biplan", "sesquiplan", "triplan", "canard"):
        if rest.startswith(pos + "_"):
            shape = rest[len(pos) + 1:]
            break
    c = Canvas()
    cx = 26
    if pos == "sans_queue":
        _draw_wing(c, shape, cx, 17 if shape != "discoide" else 18, a=24)
        c.ellipse((cx - 2, 9, cx + 2, 15), sphere(cx, 12, 2.4, base=0.5))          # verrière
    elif pos == "canard":
        _ghost_fuselage(c, cx, tail=False)
        _draw_wing(c, shape, cx, 27, a=22)
        c.poly([(cx - 8, 9), (cx + 8, 9), (cx + 7, 12), (cx - 7, 12)], plane_lit(0.6, 0.3, 9, 12))   # plan canard
    elif pos in ("biplan", "sesquiplan", "triplan"):
        _ghost_fuselage(c, cx)
        if pos == "triplan":
            for k, dy in enumerate((22, 18, 14)):
                _draw_wing(c, "rectangulaire", cx, dy, a=19, lit=0.45 + 0.1 * k)
        else:
            _draw_wing(c, shape if shape != "forme_unique" else "rectangulaire", cx, 21,
                       a=24 if pos == "biplan" else 17, lit=0.45)
            _draw_wing(c, shape if shape != "forme_unique" else "rectangulaire", cx, 16, a=24, lit=0.62)
    else:
        mouette = shape.startswith("mouette")
        _ghost_fuselage(c, cx)
        _draw_wing(c, "trapezoidale" if mouette else shape, cx, 17, a=24)
        if mouette:
            for s in (-1, 1):                                       # cassure de l'aile en mouette
                c.line([(cx + s * 7, 13.5), (cx + s * 7, 22)], 0.45, 0.45)
        pos = shape if mouette else pos
    _front_glyph(c, pos)
    return c


# ---------------------------------------------------------------- fuselages (vue de côté, nez à gauche)
def _fuselage_side(c, pts, canopy, lit=0.42):
    ys = [p[1] for p in pts]
    c.poly(pts, cyl((0, (min(ys) + max(ys)) / 2), (56, (min(ys) + max(ys)) / 2), (max(ys) - min(ys)) / 2, base=lit))
    c.ellipse(canopy, sphere((canopy[0] + canopy[2]) / 2, (canopy[1] + canopy[3]) / 2, 3, base=0.55))


def fuselage(mid):
    kind = mid[len("zv_fuselage_"):].rsplit("_", 1)[0]
    c = Canvas()
    if kind == "classic":
        _fuselage_side(c, [(3, 19), (12, 15), (40, 17), (53, 19), (53, 21), (40, 23.5), (12, 26), (3, 23)], (16, 12.5, 26, 17.5))
        c.poly([(46, 18), (52, 8), (54.5, 8), (53, 19)], flat(0.45))
    elif kind == "jug":
        _fuselage_side(c, [(3, 17), (12, 12), (36, 14), (53, 19), (53, 22), (36, 28), (12, 31), (3, 26)], (17, 9.5, 27, 15))
        c.poly([(45, 17), (51, 7), (54, 7), (53, 19)], flat(0.45))
    elif kind == "teardrop":
        _fuselage_side(c, [(3, 20), (14, 14), (30, 15), (53, 20), (53, 21.5), (30, 25), (14, 27), (3, 23)], (17, 8.5, 31, 17))
        c.poly([(46, 19), (51, 9), (54, 9), (53.5, 20.5)], flat(0.45))
    elif kind == "flying_boat":
        _fuselage_side(c, [(3, 18), (14, 13), (42, 15), (53, 17), (53, 20), (34, 24), (30, 30), (12, 31), (3, 25)], (12, 11, 20, 15.5))
        c.line([(30, 24.5), (30, 30)], 0.5, 0.5)                    # redan de la coque
        c.poly([(44, 16), (51, 6), (54, 6), (53, 17.5)], flat(0.45))
        c.bar((22, 33), (34, 33), 1.5)                              # flotteur
    elif kind == "twin_boom":                                       # vue de dessus
        c.rrect((23, 6, 33, 28), 4, cyl((23, 17), (33, 17), 5, base=0.45))
        for x in (12, 44):
            c.bar((x, 10), (x, 37), 2.2)
        c.poly([(4, 15), (52, 15), (52, 21), (4, 21)], plane_lit(0.6, 0.3, 15, 21))
        c.poly([(10, 35), (46, 35), (46, 38), (10, 38)], plane_lit(0.55, 0.2, 35, 38))
    elif kind == "flying_wing":                                     # vue de dessus
        c.poly([(28, 6), (54, 24), (52, 28), (40, 24), (28, 28), (16, 24), (4, 28), (2, 24)], plane_lit(0.6, 0.35, 6, 28))
        c.ellipse((25.5, 9, 30.5, 17), sphere(28, 13, 2.6, base=0.5))
    _size_badge(c, mid)
    return c


# ---------------------------------------------------------------- empennages (vue de l'arrière)
def tail(mid):
    kind = mid[len("zv_tail_"):]
    c = Canvas()
    cx, cy = 28, 26
    stab = lambda y, w=22: c.poly([(cx - w, y - 1.2), (cx + w, y - 1.2), (cx + w - 1, y + 1.2), (cx - w + 1, y + 1.2)], flat(0.55))
    fin = lambda x, y0, y1, w=1.6: c.poly([(x - w, y1), (x - w * 0.5, y0), (x + w * 0.5, y0), (x + w, y1)], cyl((x - w, 0), (x + w, 0), w, base=0.45))
    if kind == "twin_boom":
        for x in (14, 42):
            c.circle(x, cy, 3, sphere(x, cy, 3))
            fin(x, 8, cy)
        stab(cy - 1, 15)
    else:
        c.circle(cx, cy, 4.5, sphere(cx, cy, 4.5))
        if kind == "classic":
            stab(cy)
            fin(cx, 6, cy - 3)
        elif kind == "t":
            fin(cx, 8, cy - 3)
            stab(8.5, 18)
        elif kind == "twin":
            stab(cy)
            for x in (cx - 21, cx + 21):
                fin(x, 12, cy + 7)
        elif kind == "v":
            c.bar((cx - 2, cy - 2), (cx - 19, 8), 1.4, cyl((cx - 2, cy - 2), (cx - 19, 8), 1.4, base=0.5))
            c.bar((cx + 2, cy - 2), (cx + 19, 8), 1.4, cyl((cx + 2, cy - 2), (cx + 19, 8), 1.4, base=0.5))
        elif kind == "cruciform":
            stab(cy)
            fin(cx, 6, cy - 3)
            fin(cx, cy + 3, cy + 15)
    return c


# ---------------------------------------------------------------- trains (vue de côté)
def _belly(c, y=12):
    c.poly([(2, y - 3), (14, y - 6), (42, y - 5), (54, y - 3), (54, y), (42, y + 1.5), (14, y + 2.5), (2, y + 1)], 0.32, a=0.45)


def _wheel(c, x, y, r):
    c.circle(x, y, r, sphere(x, y, r, base=0.25, amp=0.5))
    c.circle(x, y, r * 0.4, sphere(x, y, r * 0.4, base=0.5))


def gear(mid):
    kind = mid[len("zv_"):]
    c = Canvas()
    _belly(c)
    if kind in ("gear_fixed_taildragger", "gear_retractable_taildragger"):
        c.bar((18, 14), (17, 29), 1.0)
        _wheel(c, 17, 31, 5.5)
        if kind == "gear_fixed_taildragger":
            c.poly([(12, 27), (17, 24), (22, 27), (22, 33), (12, 33)], flat(0.55))   # carénage de roue
        c.bar((47, 13), (49, 19), 0.6)
        _wheel(c, 49, 20.5, 2.2)
    elif kind in ("gear_fixed_tricycle", "gear_retractable_tricycle"):
        c.bar((10, 14), (10, 29), 0.9)
        _wheel(c, 10, 31, 4)
        c.bar((34, 14), (34, 28), 1.0)
        _wheel(c, 34, 31, 5.5)
    elif kind == "floats":
        for x0 in (8,):
            c.bar((26, 14), (24, 27), 0.7)
            c.bar((14, 14), (14, 27), 0.7)
            c.poly([(3, 29), (8, 26.5), (44, 27), (50, 30), (44, 33), (8, 33)], cyl((3, 30), (50, 30), 3.5, base=0.4))
    elif kind == "skis":
        c.bar((18, 14), (18, 28), 1.0)
        c.poly([(4, 31), (8, 28.5), (34, 29), (34, 31.5), (8, 32)], flat(0.6))
        c.bar((47, 13), (48, 25), 0.6)
        c.poly([(42, 26), (53, 26), (53, 27.5), (43, 27.5)], flat(0.55))
    elif kind == "takeoff_trolley":
        c.poly([(8, 22), (48, 22), (48, 25), (8, 25)], flat(0.5))
        for x in (12, 44):
            _wheel(c, x, 30, 4.5)
        c.line([(28, 15), (28, 21)], 0.6, 0.3)
    if "retractable" in kind:                                    # flèche de rétraction
        x = 17 if "taildragger" in kind else 34
        c.arc((x - 9, 14, x + 9, 34), 200, 300, 0.7, 0.1)
    return c


# ---------------------------------------------------------------- hélices (vue de face)
def prop(mid):
    rest = mid[len("zv_prop_"):]
    parts = rest.split("_")
    n = int(parts[0])
    wood = rest.endswith("wood")
    c = Canvas()
    cx, cy = 28, 21
    for i in range(n):
        th = 2 * math.pi * i / n - math.pi / 2 + 0.25
        u, v = math.cos(th), math.sin(th)
        w0, w1 = (2.6, 1.6) if not wood else (3.2, 2.4)
        P = lambda r, w: (cx + u * r - v * w, cy + v * r + u * w)
        c.poly([P(3, -w0), P(17, -w1), P(19, 0), P(17, w1), P(3, w0)], cyl(P(3, 0), P(19, 0), w0, base=0.45 if not wood else 0.35))
        if wood:
            c.line([P(5, 0.4), P(17, 0.2)], 0.3, 0.3)
    c.circle(cx, cy, 4, sphere(cx, cy, 4, base=0.45))
    return c


def prop_module(mid):
    c = Canvas()
    cx, cy = 28, 21
    c.poly([(cx - 2, 4), (cx + 2, 4), (cx + 3, 21), (cx - 3, 21)], cyl((cx - 3, 0), (cx + 3, 0), 3, base=0.45))
    c.circle(cx, 24, 4, sphere(cx, 24, 4, base=0.45))
    if mid.endswith("variable_pitch"):
        c.arc((cx - 9, 6, cx + 9, 18), 200, 340, 0.8, 0.1)          # rotation du pas
    else:                                                         # mise en drapeau : pale de profil
        c.poly([(cx + 8, 8), (cx + 22, 9.5), (cx + 22, 10.5), (cx + 8, 12)], flat(0.6))
        c.line([(cx + 4, 10), (cx + 7, 10)], 0.5, 0)
    return c


# ---------------------------------------------------------------- cockpits (vue de côté, nez à gauche)
def cockpit(mid):
    kind = mid[len("zv_cockpit_"):]
    c = Canvas()
    if kind == "glazed_nose":
        c.poly([(16, 12), (54, 13), (54, 31), (16, 32)], cyl((16, 22), (54, 22), 10, base=0.38))
        c.poly([(2, 22), (6, 14), (16, 12), (16, 32), (6, 30)], sphere(10, 22, 10, base=0.55))
        for x in (6, 10, 14):
            c.line([(x, 13.5), (x, 30.5)], 0.35, 0.5)
        c.line([(3, 22), (16, 22)], 0.35, 0.5)
        return c
    c.poly([(2, 24), (10, 20), (54, 19), (54, 31), (10, 31), (2, 28)], cyl((2, 25), (54, 25), 6, base=0.38))
    if kind == "open":
        c.poly([(20, 19.5), (23, 14), (25, 14), (24, 19.5)], flat(0.75), a=0.8)
        c.circle(30, 16.5, 2.6, sphere(30, 16.5, 2.6, base=0.3))   # tête du pilote
    elif kind == "closed":
        c.poly([(18, 19.5), (23, 13), (36, 12.5), (42, 19)], sphere(30, 16, 8, base=0.55))
        for x in (24, 31):
            c.line([(x, 13), (x + 1, 19)], 0.35, 0.55)
    elif kind == "bubble":
        c.ellipse((18, 9, 40, 25), sphere(29, 14, 9, base=0.6))
        c.poly([(16, 19), (56, 19), (56, 26), (16, 26)], cyl((2, 25), (54, 25), 6, base=0.38))
    elif kind == "pressurized":
        c.poly([(18, 19.5), (23, 15), (34, 14.5), (40, 19)], sphere(30, 17, 7, base=0.5))
        for x in (40, 45, 50):
            c.circle(x, 24, 1.5, 0.75, outline=False)
    return c


# ---------------------------------------------------------------- matériaux et construction
def material(mid):
    c = Canvas()
    kind = mid[len("zv_"):]
    if kind == "tube_and_fabric":
        c.poly([(4, 10), (52, 10), (52, 32), (4, 32)], flat(0.35), a=0.55)
        for x in range(4, 53, 8):
            c.line([(x, 10), (x, 32)], 0.7, 0)
            if x < 52:
                c.line([(x, 10), (x + 8, 32)], 0.5, 0)
        c.line([(4, 10), (52, 10)], 0.8, 0)
        c.line([(4, 32), (52, 32)], 0.8, 0)
    elif kind == "wooden_monocoque":
        c.rrect((4, 9, 52, 33), 6, cyl((4, 21), (52, 21), 12, base=0.36))
        for y in range(12, 32, 3):
            c.line([(6, y), (50, y + 0.6)], 0.3, 0.3)
    else:                                                          # matériaux non stratégiques : tôles d'acier
        for k, y in enumerate((24, 18, 12)):
            c.poly([(8 + k * 2, y), (46 + k * 2, y), (50 + k * 2, y + 6), (12 + k * 2, y + 6)], flat(0.4 + 0.08 * k))
        _size_badge(c, mid)
    return c


def construction(mid):
    c = Canvas()
    light = "lightweight" in mid
    c.poly([(3, 15), (53, 15), (53, 27), (3, 27)], cyl((3, 21), (53, 21), 6, base=0.4))     # longeron
    if light:
        for x in range(9, 50, 7):
            c.circle(x, 21, 2.6, 0.08, outline=True)                   # trous d'allègement
    else:
        for x in range(7, 52, 5):
            c.line([(x, 15.5), (x, 26.5)], 0.7, 0.45)                   # nervures doublées
        c.poly([(3, 13), (53, 13), (53, 15.5), (3, 15.5)], flat(0.6))
        c.poly([(3, 26.5), (53, 26.5), (53, 29), (3, 29)], flat(0.5))
    _size_badge(c, mid)
    return c


FAMILY = [
    ("zv_wing_", "ailes", wing), ("zv_fuselage_", "fuselages", fuselage), ("zv_tail_", "empennages", tail),
    ("zv_gear_", "trains", gear), ("zv_floats", "trains", gear), ("zv_skis", "trains", gear),
    ("zv_takeoff_trolley", "trains", gear), ("zv_prop_variable", "hélices", prop_module),
    ("zv_prop_feathering", "hélices", prop_module), ("zv_prop_", "hélices", prop),
    ("zv_cockpit_", "cockpits", cockpit), ("zv_tube_and_fabric", "matériaux", material),
    ("zv_wooden_monocoque", "matériaux", material), ("zv_non_strategic", "matériaux", material),
    ("zv_lightweight_construction", "matériaux", construction), ("zv_reinforced_construction", "matériaux", construction),
]

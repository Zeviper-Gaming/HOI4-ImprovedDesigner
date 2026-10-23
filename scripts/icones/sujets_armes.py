"""Icônes des armes : mitrailleuses, canons, canons AT, roquettes, bombes (attaches et soutes), armes
navales et guidées, armes spéciales, tourelles et armes à main."""
import math

import numpy as np

from dessin import Canvas, cyl, sphere, flat, ROMAN


# ---------------------------------------------------------------- armes de tir
def _gun(c, ox, oy, ang, length, r_barrel, r_body, body_len, drum=False, jacket=False, brake=0.0):
    """Une arme vue de côté, orientée selon `ang` (degrés), culasse en (ox, oy)."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    P = lambda u, v=0: (ox + u * ca - v * sa, oy + u * sa + v * ca)
    c.bar(P(0), P(body_len), r_body)
    if drum:
        q = P(body_len * 0.45, -r_body - 2.4)
        c.circle(*q, 2.6, sphere(*q, 2.6, base=0.3))
    c.bar(P(body_len - 0.5), P(length), r_barrel, cyl(P(body_len), P(length), r_barrel, base=0.5))
    if jacket:                                                     # manchon de refroidissement percé
        c.bar(P(body_len), P(body_len + (length - body_len) * 0.55), r_barrel * 1.9, cyl(P(body_len), P(length), r_barrel * 1.9, base=0.4))
        for k in range(4):
            u = body_len + 1.5 + k * (length - body_len) * 0.12
            c.circle(*P(u), 0.35, 0.1, outline=False)
    if brake:
        c.bar(P(length - brake), P(length + 0.4), r_barrel * 1.8, cyl(P(length - brake), P(length), r_barrel * 1.8, base=0.35))
    c.line([P(1), P(body_len - 1)], 0.3, 0.3)


def _stack(c, n, horizontal, draw):
    """n armes côte à côte (diagonale montante, ou à l'horizontale pour le nez)."""
    if horizontal:
        ys = {1: [21], 2: [16, 26], 3: [12, 21, 30], 4: [9, 16.5, 24, 31.5]}[n]
        for y in ys:
            draw(52, y, 180)
    else:
        offs = {1: [(6, 33)], 2: [(4, 28), (10, 37)], 3: [(3, 25), (7, 32), (11, 39)], 4: [(2, 22), (5, 28), (8, 34), (11, 40)]}[n]
        for x, y in offs:
            draw(x, y, -24)


def machine_gun(mid):
    nose = "_nose_" in mid
    rest = mid.replace("zv_nose_", "zv_")[3:]                      # light_mg_2x, heavy_imp_mg_1x…
    heavy = rest.startswith("heavy")
    imp = "_imp_" in rest
    n = int(rest.rsplit("_", 1)[1][0])
    c = Canvas()
    rb, rbody = (0.75, 1.7) if heavy else (0.55, 1.3)
    L = 38 if not nose else 40
    _stack(c, n, nose, lambda x, y, ang: _gun(c, x, y, ang, L, rb, rbody, 12, jacket=not imp and not heavy, brake=1.6 if heavy else 0))
    c.badge = ("II" if imp else "I", "tier")
    return c


def cannon(mid):
    nose = "_nose_" in mid
    rest = mid.replace("zv_nose_", "zv_")[3:]                      # cannon_20mm_1_2x, cannon_30mm_1x
    parts = rest.split("_")
    n = int(parts[-1][0])
    c = Canvas()
    if parts[1] == "30mm":
        _stack(c, n, nose, lambda x, y, ang: _gun(c, x, y, ang, 30, 1.2, 2.3, 13, brake=2.5))
        c.badge = ("30", "count")
    else:
        gen = int(parts[2])
        _stack(c, n, nose, lambda x, y, ang: _gun(c, x, y, ang, 42, 0.8, 1.8, 14, drum=gen == 1, brake=2.2))
        c.badge = (ROMAN[gen], "tier")
    return c


def at_cannon(mid):
    nose = "_nose_" in mid
    cal = int(mid.rsplit("_", 1)[1])
    c = Canvas()
    k = {37: 0.8, 40: 0.85, 57: 1.0, 75: 1.15}[cal]
    if nose:
        _gun(c, 52, 22, 180, 50, 1.0 * k, 3.2 * k, 16, brake=4)
    else:
        c.rrect((8, 22, 34, 31), 4, cyl((8, 26.5), (34, 26.5), 4.5, base=0.38))     # nacelle sous l'aile
        c.bar((20, 21), (20, 17), 1.0)
        c.bar((30, 26.5), (54, 26.5), 1.1 * k, cyl((30, 26.5), (54, 26.5), 1.1 * k, base=0.5))
        c.bar((50, 26.5), (55, 26.5), 2.0 * k, cyl((50, 26.5), (55, 26.5), 2.0 * k, base=0.35))
        c.poly([(4, 16), (52, 16), (52, 18), (4, 18)], flat(0.4), a=0.5)          # aile en filigrane
    c.badge = (f"{cal}", "count")
    return c


def rocket(mid):
    kind = mid[len("zv_rockets_"):]
    c = Canvas()
    c.poly([(3, 11), (53, 11), (53, 13.5), (3, 13.5)], flat(0.38), a=0.55)         # aile en filigrane
    def rk(x, y, ln=20, r=1.4, ap=False, big=False):
        r = r * (1.4 if big else 1)
        c.bar((x, y), (x + ln, y), r, cyl((x, y), (x + ln, y), r, base=0.48))
        c.poly([(x + ln, y - r), (x + ln + 3 + (2 if ap else 0), y), (x + ln, y + r)], sphere(x + ln + 1, y, r + 0.5, base=0.5))
        c.poly([(x - 1, y - r - 1.8), (x + 3, y - r), (x + 3, y + r), (x - 1, y + r + 1.8)], flat(0.5))
    if kind in ("rails_1", "rails_2", "at_1", "at_2"):
        for k, y in enumerate((19, 27, 35)):
            c.bar((6 + k * 2, y - 2.6), (36 + k * 2, y - 2.6), 0.5, flat(0.55))       # rail
            rk(8 + k * 2, y, 24, ap=kind.startswith("at"), big=kind.endswith("2"))
        c.badge = ("II" if kind.endswith("2") else "I", "tier")
    elif kind == "r4m":
        for row in range(3):
            for col in range(4):
                rk(6 + col * 12, 18 + row * 7, 8, 0.8)
    elif kind == "wgr21":
        c.bar((10, 25), (48, 25), 5, cyl((10, 25), (48, 25), 5, base=0.36))         # tube lance-roquettes
        c.circle(48, 25, 4.2, 0.12, outline=True)
        c.bar((22, 20), (22, 13.5), 0.9)
        c.bar((38, 20), (38, 13.5), 0.9)
    return c


# ---------------------------------------------------------------- bombes
def _bomb(c, x, y, ln, r, fins=True, pointed=False, base=0.42):
    c.bar((x + r, y), (x + ln - r, y), r, cyl((x, y), (x + ln, y), r, base=base))
    c.circle(x + ln - r, y, r, sphere(x + ln - r, y, r, base=base))
    if pointed:
        c.poly([(x + ln - r, y - r), (x + ln + r * 1.4, y), (x + ln - r, y + r)], sphere(x + ln, y, r, base=base + 0.05))
    if fins:                                                       # cône arrière puis ailettes fines
        c.poly([(x + r, y - r), (x - r * 0.6, y - r * 0.45), (x - r * 0.6, y + r * 0.45), (x + r, y + r)], cyl((x, y), (x + r, y), r * 0.7, base=base))
        fl = min(3.2, r)
        c.poly([(x - r * 0.6 - fl * 0.4, y - r * 1.15), (x - r * 0.6 + fl, y - r * 1.15), (x - r * 0.1 + fl, y - r * 0.35),
                (x - r * 0.1 + fl, y + r * 0.35), (x - r * 0.6 + fl, y + r * 1.15), (x - r * 0.6 - fl * 0.4, y + r * 1.15)], flat(0.55))


def bomb_locks(mid):
    kind = mid[len("zv_bomb_locks_"):]
    c = Canvas()
    c.poly([(3, 7), (53, 7), (53, 9.5), (3, 9.5)], flat(0.38), a=0.55)
    if kind == "light":
        for x in (8, 32):
            c.bar((x + 8, 10), (x + 8, 15), 0.7)
            _bomb(c, x, 19, 16, 3.2)
    elif kind == "frag":
        for x in (7, 19, 31, 43):
            for y in (17, 27):
                _bomb(c, x, y, 8, 1.8)
    elif kind == "ap":
        c.bar((22, 10), (22, 15), 0.8)
        _bomb(c, 10, 22, 30, 4.2, pointed=True, base=0.36)
    elif kind == "heavy":
        c.bar((24, 10), (24, 14), 1.0)
        _bomb(c, 6, 23, 40, 7.5, base=0.34)
    elif kind == "incendiary":
        for x in (8, 32):
            _bomb(c, x, 20, 15, 3.4, base=0.38)
            c.poly([(x + 4, 28), (x + 7, 33), (x + 9, 29), (x + 11, 35), (x + 13, 28)], flat(0.85), accent=1.0)
    elif kind == "napalm":
        c.bar((24, 10), (24, 14), 0.8)
        c.rrect((6, 15, 50, 27), 6, cyl((6, 21), (50, 21), 6, base=0.4))
        c.poly([(14, 31), (18, 37), (22, 32), (27, 39), (32, 32), (37, 37), (40, 31)], flat(0.85), accent=1.0)
    elif kind == "earthquake":
        c.bar((24, 10), (24, 13), 1.2)
        _bomb(c, 3, 25, 49, 9, base=0.32)
    return c


def bomb_bay(mid):
    kind = mid[len("zv_bomb_bay_"):]
    c = Canvas()
    c.poly([(3, 5), (53, 5), (53, 30), (3, 30)], flat(0.28), a=0.55)            # soute ouverte
    c.poly([(3, 30), (12, 30), (5, 39), (1, 39)], flat(0.5))                     # portes
    c.poly([(44, 30), (53, 30), (55, 39), (51, 39)], flat(0.5))
    rows = {"light": (3, 2, 2.4), "medium": (2, 2, 3.2), "medium_frag": (3, 3, 2.2), "large": (2, 1, 4.8),
            "large_frag": (3, 4, 2.2), "incendiary": (3, 2, 2.8), "earthquake": (1, 1, 9.0)}[kind]
    nr, nc, r = rows
    for i in range(nr):
        for j in range(nc):
            y = 9 + (i + 0.5) * 20 / nr
            w = 44 / nc
            _bomb(c, 6 + j * w, y, w - 4, r, base=0.4)
    if kind == "incendiary":
        c.poly([(18, 32), (22, 38), (26, 33), (30, 39), (34, 32)], flat(0.85), accent=1.0)
    return c


# ---------------------------------------------------------------- armes navales, guidées, spéciales
def naval(mid):
    c = Canvas()
    if mid == "zv_depth_charges":
        for x in (8, 26, 44):
            c.rrect((x - 6, 12, x + 6, 30), 2.5, cyl((x - 6, 21), (x + 6, 21), 6, base=0.4))
            c.line([(x - 6, 16), (x + 6, 16)], 0.4, 0.4)
            c.line([(x - 6, 26), (x + 6, 26)], 0.4, 0.4)
    else:                                                          # FIDO : torpille acoustique
        _bomb(c, 6, 21, 44, 4.2, base=0.42)
        c.poly([(3, 14), (9, 18), (9, 24), (3, 28)], flat(0.55))
        c.arc((44, 12, 56, 30), 300, 60, 0.6, 0.1)
        c.arc((41, 8, 59, 34), 300, 60, 0.6, 0.1)
    return c


def guided(mid):
    c = Canvas()
    if mid == "zv_fritz_x":
        _bomb(c, 12, 21, 36, 4.6, fins=False, pointed=True, base=0.38)
        c.poly([(8, 12), (18, 16), (18, 26), (8, 30)], flat(0.5))                 # empennage en anneau
        c.poly([(24, 17), (32, 9), (34, 9), (30, 18)], flat(0.6))
        c.poly([(24, 25), (32, 33), (34, 33), (30, 24)], flat(0.5))
    else:                                                          # Hs 293 : bombe planante à ailes
        _bomb(c, 8, 22, 40, 3.2, fins=True, base=0.42)
        c.poly([(22, 22), (30, 6), (34, 6), (32, 22)], flat(0.62))
        c.poly([(22, 22), (30, 38), (34, 38), (32, 22)], flat(0.5))
        c.bar((14, 27), (24, 27), 1.6, cyl((14, 27), (24, 27), 1.6, base=0.35))  # fusée d'appoint
    return c


def schraege_musik(mid):
    c = Canvas()
    c.poly([(2, 30), (14, 26), (54, 27), (54, 32), (14, 34), (2, 33)], cyl((2, 30), (54, 30), 4, base=0.38), a=0.8)
    for x in (22, 30):
        _gun(c, x, 27, -62, 22, 0.8, 1.8, 7, brake=1.8)
    return c


# ---------------------------------------------------------------- tourelles
def turret(mid):
    """lmg/hmg/cannon_defense_turret_4x (mod), ball_turret_*, remote_turret_*."""
    m = mid[3:]
    if m.startswith("ball_turret_"):
        kind, gun, n = "ball", *m[len("ball_turret_"):].split("_")
    elif m.startswith("remote_turret_"):
        kind, gun, n = "remote", *m[len("remote_turret_"):].split("_")
    else:
        kind, gun, n = "dome", m.split("_")[0], m.rsplit("_", 1)[1]
    n = int(n[0])
    c = Canvas()
    rb = {"lmg": 0.45, "hmg": 0.65, "cannon": 0.85}[gun]
    if kind == "dome":
        c.poly([(4, 33), (52, 33), (52, 37), (4, 37)], flat(0.35), a=0.6)
        c.ellipse((10, 14, 34, 38), sphere(22, 24, 12, base=0.4))
        c.line([(14, 22), (30, 22)], 0.35, 0.4)
        ys = np.linspace(22, 30, n) if n > 1 else [26]
        for y in ys:
            c.bar((26, y), (53, y - 7), rb, cyl((26, y), (53, y - 7), rb, base=0.5))
    elif kind == "ball":
        c.poly([(4, 4), (52, 4), (52, 8), (4, 8)], flat(0.35), a=0.6)
        c.bar((22, 8), (22, 13), 1.2)
        c.circle(22, 23, 11, sphere(22, 23, 11, base=0.34))
        c.circle(19, 21, 3.2, sphere(19, 21, 3.2, base=0.65))                   # hublot
        ys = np.linspace(19, 27, n) if n > 1 else [23]
        for y in ys:
            c.bar((30, y), (54, y + 6), rb, cyl((30, y), (54, y + 6), rb, base=0.5))
    else:                                                          # télécommandée : barbette basse
        c.poly([(3, 30), (53, 30), (53, 34), (3, 34)], flat(0.35), a=0.6)
        c.ellipse((10, 22, 34, 34), sphere(22, 30, 12, base=0.4))
        c.rrect((16, 18, 28, 26), 3, cyl((16, 22), (28, 22), 4, base=0.45))
        ys = np.linspace(19, 25, n) if n > 1 else [22]
        for y in ys:
            c.bar((26, y), (54, y - 4), rb, cyl((26, y), (54, y - 4), rb, base=0.5))
        c.circle(8, 26, 2.2, sphere(8, 26, 2.2, base=0.6))                      # viseur déporté
    c.badge = ({"lmg": "I", "hmg": "II", "cannon": "III"}[gun], "tier")
    return c


def hand_mg(mid):
    heavy = mid.endswith("heavy")
    c = Canvas()
    c.arc((8, 22, 30, 42), 180, 360, 0.9, 0.1)                        # rail circulaire
    c.bar((19, 32), (21, 22), 0.8)
    _gun(c, 12, 24, -18, 40, 0.6 if heavy else 0.45, 1.6 if heavy else 1.2, 12, jacket=not heavy, brake=1.6 if heavy else 0)
    c.badge = ("II" if heavy else "I", "tier")
    return c


FAMILY = [
    ("zv_nose_at_cannon_", "armes", at_cannon), ("zv_at_cannon_", "armes", at_cannon),
    ("zv_nose_cannon_", "armes", cannon), ("zv_cannon_", "armes", cannon),
    ("zv_nose_light", "armes", machine_gun), ("zv_nose_heavy", "armes", machine_gun),
    ("zv_light_", "armes", machine_gun), ("zv_heavy_", "armes", machine_gun),
    ("zv_rockets_", "armes", rocket), ("zv_bomb_locks_", "bombes", bomb_locks), ("zv_bomb_bay_tank", None, None),
    ("zv_bomb_bay_", "bombes", bomb_bay), ("zv_depth_charges", "bombes", naval), ("zv_fido", "bombes", naval),
    ("zv_fritz_x", "bombes", guided), ("zv_hs293", "bombes", guided),
    ("guided_anti_ship_missile", "bombes", guided),   # module vanilla : dessin pour l'icône de sa tech seulement ("zv_schraege_musik", "armes", schraege_musik),
    ("zv_lmg_defense_turret", "tourelles", turret), ("zv_hmg_defense_turret", "tourelles", turret),
    ("zv_ball_turret_", "tourelles", turret), ("zv_remote_turret_", "tourelles", turret),
    ("zv_hand_mg_", "tourelles", hand_mg),
]

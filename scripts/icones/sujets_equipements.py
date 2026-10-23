"""Icônes des équipements (alimentation, refroidissement, réservoirs, blindage, électronique, viseurs,
aérodynamique, transport…) et des rôles."""
import math

import numpy as np

from dessin import Canvas, cyl, sphere, flat, plane_lit, ROMAN
from sujets_structure import _size_badge
from sujets_moteurs import silhouette, nacelle


def _tank(c, x0, y0, x1, y1, base=0.4):
    r = (y1 - y0) / 2
    c.rrect((x0, y0, x1, y1), r, cyl((x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2), r, base=base))


def _snail(c, cx, cy, r, base=0.38):
    """Carter en colimaçon d'un compresseur, avec sa roue."""
    c.circle(cx, cy, r, sphere(cx, cy, r, base=base))
    c.poly([(cx, cy - r), (cx + r * 1.6, cy - r), (cx + r * 1.6, cy - r * 0.35), (cx + r * 0.6, cy - r * 0.35)], flat(base + 0.1))
    for k in range(8):
        th = 2 * math.pi * k / 8
        c.line([(cx + math.cos(th) * r * 0.25, cy + math.sin(th) * r * 0.25), (cx + math.cos(th + 0.5) * r * 0.75, cy + math.sin(th + 0.5) * r * 0.75)], 0.35, 0.4)


def _drop(c, x, y, s=1.0):
    c.poly([(x, y - 4 * s), (x + 2.6 * s, y + 0.5 * s), (x, y + 2.6 * s), (x - 2.6 * s, y + 0.5 * s)], flat(0.85), accent=1.0)
    c.circle(x, y + 0.6 * s, 2.5 * s, flat(0.85), accent=1.0)


def supercharger(m):
    c = Canvas()
    turbo = "turbo" in m
    if turbo:
        _snail(c, 18, 22, 10)
        _snail(c, 38, 22, 8, base=0.3)
        c.bar((24, 22), (32, 22), 1.6)
        c.bar((44, 28), (54, 36), 2.2, cyl((44, 28), (54, 36), 2.2, base=0.3))   # gaz d'échappement
    elif m == "zv_two_stage_supercharger":
        _snail(c, 16, 22, 9)
        _snail(c, 36, 22, 9)
        c.bar((22, 22), (30, 22), 1.4)
    else:
        _snail(c, 22, 22, 12)
        if m == "zv_improved_supercharger":                           # refroidisseur intermédiaire
            c.rrect((40, 12, 54, 32), 2, flat(0.45))
            for y in range(14, 31, 2):
                c.line([(41, y), (53, y)], 0.35, 0.45)
        elif m == "zv_supercharger":
            c.circle(44, 26, 6, sphere(44, 26, 6, base=0.4))           # boîte à deux vitesses
            for k in range(10):
                th = 2 * math.pi * k / 10
                c.line([(44 + 5 * math.cos(th), 26 + 5 * math.sin(th)), (44 + 6.5 * math.cos(th), 26 + 6.5 * math.sin(th))], 0.5, 0)
    tier = {"zv_early_supercharger": 1, "zv_early_turbocharger": 1, "zv_supercharger": 2, "zv_turbocharger": 2,
            "zv_improved_supercharger": 3, "zv_improved_turbocharger": 3, "zv_two_stage_supercharger": 3}[m]
    c.badge = (ROMAN[tier], "tier")
    return c


def feed(m):
    """Alimentation : essence à haut indice, injections, carburateur anti-g, GM-1, régime d'urgence."""
    c = Canvas()
    if m.startswith("zv_high_octane"):
        c.rrect((12, 8, 40, 36), 3, cyl((12, 22), (40, 22), 14, base=0.38))       # fût
        for y in (14, 30):
            c.line([(12, y), (40, y)], 0.5, 0.45)
        c.poly([(42, 14), (52, 14), (49, 22), (52, 22), (44, 34), (46, 25), (42, 25)], flat(0.85), accent=1.0)  # éclair
        _size_badge(c, m)
    elif m.startswith("zv_water_injection"):
        _tank(c, 6, 12, 38, 30)
        _drop(c, 46, 20, 1.6)
        _size_badge(c, m)
    elif m == "zv_gm1":
        for x in (12, 24, 36):
            c.rrect((x - 4, 10, x + 4, 36), 4, cyl((x - 4, 23), (x + 4, 23), 4, base=0.4))
            c.rrect((x - 1.5, 6, x + 1.5, 10), 0.5, flat(0.6))
    elif m == "zv_direct_injection":
        c.bar((6, 21), (36, 21), 2.6)
        c.poly([(36, 17), (42, 19.5), (42, 22.5), (36, 25)], flat(0.6))
        for k in range(5):
            c.line([(43, 21), (54, 14 + k * 3.5)], 0.4, 0)
        c.arc((43, 10, 56, 32), 300, 60, 0.5, 0)
    elif m == "zv_anti_g_carburettor":
        c.rrect((12, 12, 34, 34), 3, cyl((12, 23), (34, 23), 11, base=0.38))
        c.circle(23, 23, 5, 0.15)
        c.poly([(44, 8), (48, 8), (48, 26), (52, 26), (46, 34), (40, 26), (44, 26)], flat(0.85), accent=1.0)   # flèche g
    elif m.startswith("zv_wep"):
        c.poly([(14, 32), (40, 32), (40, 36), (14, 36)], flat(0.45))
        c.bar((22, 33), (34, 10), 1.6)
        c.circle(34, 10, 3.2, sphere(34, 10, 3.2, base=0.5))
        c.arc((10, 6, 46, 42), 200, 290, 0.7, 0)
        c.poly([(44, 8), (52, 8), (48, 16), (53, 16), (44, 28), (46, 19), (42, 19)], flat(0.85), accent=1.0)
        _size_badge(c, m)
    return c


def cooling(m):
    c = Canvas()
    if m == "zv_naca_cowling":
        c.ellipse((10, 4, 40, 38), sphere(25, 21, 15, base=0.4))
        c.ellipse((16, 10, 34, 32), 0.15)
        c.poly([(38, 10), (52, 14), (52, 28), (38, 32)], cyl((38, 21), (52, 21), 9, base=0.35))
    elif m == "zv_air_intake":
        c.poly([(4, 12), (20, 16), (52, 18), (52, 26), (20, 28), (4, 32)], cyl((4, 22), (52, 22), 9, base=0.4))
        c.ellipse((2, 12, 8, 32), 0.15)
        for x in (24, 36):
            c.line([(x, 17), (x, 27)], 0.35, 0.3)
    elif m == "zv_radiator_annular":
        c.circle(28, 21, 16, sphere(28, 21, 16, base=0.38))
        c.circle(28, 21, 9, 0.15)
        for k in range(24):
            th = 2 * math.pi * k / 24
            c.line([(28 + 10 * math.cos(th), 21 + 10 * math.sin(th)), (28 + 15 * math.cos(th), 21 + 15 * math.sin(th))], 0.35, 0.45)
    else:                                                            # ventral ou d'aile : bloc à ailettes
        c.poly([(3, 9), (53, 9), (53, 13), (3, 13)], flat(0.38), a=0.55)
        x0, x1 = (16, 40) if m == "zv_radiator_ventral" else (6, 50)
        c.rrect((x0, 14, x1, 30), 2, flat(0.42))
        for x in np.arange(x0 + 2, x1 - 1, 2):
            c.line([(x, 15), (x, 29)], 0.3, 0.45)
        if m == "zv_radiator_ventral":
            c.poly([(x0, 30), (x1 + 6, 30), (x1, 34), (x0 + 2, 34)], flat(0.5))       # écope
    return c


def jet_upgrade(m):
    c = Canvas()
    if m == "zv_afterburner":
        c.bar((4, 21), (34, 21), 6)
        c.poly([(34, 15), (42, 16.5), (42, 25.5), (34, 27)], cyl((34, 21), (42, 21), 6, base=0.35))
        c.poly([(42, 17), (55, 21), (42, 25)], flat(0.9), accent=1.0)
        c.badge = ("II", "tier")
    elif m == "zv_supersonic_intake":
        c.poly([(16, 12), (52, 14), (52, 30), (16, 32)], cyl((16, 22), (52, 22), 10, base=0.38))
        c.poly([(3, 22), (18, 16), (18, 28)], sphere(12, 22, 6, base=0.5))
    else:                                                            # compresseur amélioré
        c.circle(22, 21, 15, sphere(22, 21, 15, base=0.36))
        for k in range(18):
            th = 2 * math.pi * k / 18
            c.line([(22 + 4 * math.cos(th), 21 + 4 * math.sin(th)), (22 + 14 * math.cos(th + 0.35), 21 + 14 * math.sin(th + 0.35))], 0.4, 0.45)
        c.circle(22, 21, 4, sphere(22, 21, 4, base=0.5))
        c.poly([(40, 14), (54, 17), (54, 25), (40, 28)], cyl((40, 21), (54, 21), 7, base=0.4))
    return c


def tanks(m):
    c = Canvas()
    if m.startswith("zv_self_sealing"):
        _tank(c, 6, 9, 50, 33)
        for x in (16, 28, 40):
            c.poly([(x - 1.5, 9.5), (x + 1.5, 9.5), (x + 1.5, 32.5), (x - 1.5, 32.5)], flat(0.6), outline=True)
        _size_badge(c, m)
    elif m.startswith("zv_fuel_tanks"):
        _tank(c, 6, 9, 50, 33)
        c.rrect((24, 5, 32, 10), 1, flat(0.55))
        _size_badge(c, m)
    elif m.startswith("zv_drop_tanks"):
        c.poly([(3, 7), (53, 7), (53, 9.5), (3, 9.5)], flat(0.38), a=0.55)
        c.bar((28, 9.5), (28, 14), 0.9)
        c.poly([(4, 22), (14, 15), (42, 15), (54, 22), (42, 29), (14, 29)], cyl((4, 22), (54, 22), 7, base=0.42))
        c.poly([(50, 18), (56, 13), (56, 31), (50, 26)], flat(0.5))
        _size_badge(c, m)
    elif m == "zv_bomb_bay_tank":
        c.poly([(3, 5), (53, 5), (53, 30), (3, 30)], flat(0.28), a=0.55)
        c.poly([(3, 30), (12, 30), (5, 39), (1, 39)], flat(0.5))
        c.poly([(44, 30), (53, 30), (55, 39), (51, 39)], flat(0.5))
        _tank(c, 8, 9, 48, 27)
    elif m == "zv_ferry_tank":
        _tank(c, 2, 12, 54, 32, base=0.38)
        for x in (12, 22, 32, 42):
            c.line([(x, 12.5), (x, 31.5)], 0.35, 0.35)
    return c


def armour(m):
    c = Canvas()
    if m == "zv_armored_cockpit" or m == "zv_ejection_seat":
        c.poly([(18, 34), (36, 34), (38, 26), (22, 26)], flat(0.45))            # assise
        c.poly([(30, 26), (38, 26), (40, 6), (33, 5)], cyl((30, 15), (40, 15), 4, base=0.45))   # dossier
        if m == "zv_armored_cockpit":
            c.poly([(37, 4), (46, 6), (46, 30), (38, 28)], flat(0.58))          # plaque de blindage
            for y in (9, 16, 23):
                c.circle(42, y, 0.8, 0.2, outline=False)
        else:
            c.poly([(10, 14), (14, 6), (18, 14), (16, 14), (16, 26), (12, 26), (12, 14)], flat(0.85), accent=1.0)  # flèche
            c.bar((40, 28), (46, 2), 0.8)                                   # rails d'éjection
    else:                                                              # plaques S, M, L
        n = {"s": 1, "m": 2, "l": 3}[m[-1]]
        for k in range(n):
            o = k * 3.5
            c.poly([(10 + o, 8 + o), (40 + o, 8 + o), (44 + o, 12 + o), (44 + o, 30 + o), (14 + o, 30 + o), (10 + o, 26 + o)], flat(0.42 + 0.06 * k))
            for x, y in ((14 + o, 12 + o), (40 + o, 12 + o), (14 + o, 26 + o), (40 + o, 26 + o)):
                c.circle(x, y, 0.9, 0.2, outline=False)
        _size_badge(c, m)
    return c


def safety(m):
    c = Canvas()
    if m.startswith("zv_auto_extinguisher"):
        c.rrect((20, 9, 34, 38), 6, cyl((20, 23), (34, 23), 7, base=0.42))
        c.rrect((24, 4, 30, 9), 1, flat(0.55))
        c.bar((30, 6), (44, 10), 0.8)
        c.poly([(44, 8), (52, 12), (44, 14)], flat(0.6))
        _size_badge(c, m)
    elif m in ("zv_deicing_boots", "zv_heated_leading_edges"):
        c.poly([(4, 24), (10, 16), (50, 16), (54, 24), (50, 28), (10, 28)], plane_lit(0.6, 0.35, 16, 28))
        if m == "zv_deicing_boots":
            for y in (18, 20.5, 23):
                c.line([(8, y), (48, y)], 0.5, 0.5)
        else:
            for x in (14, 26, 38):
                c.line([(x, 13), (x + 2, 10), (x, 7), (x + 2, 4)], 0.6, 0)
        c.badge = ("II" if m == "zv_heated_leading_edges" else "I", "tier")
    return c


def _box(c, x0, y0, x1, y1, base=0.38):
    c.rrect((x0, y0, x1, y1), 2, flat(base, 0.2))


def avionics(m):
    c = Canvas()
    k = m[3:]
    if k == "radio_telephone":
        _box(c, 8, 12, 40, 36)
        for x, y in ((16, 20), (28, 20)):
            c.circle(x, y, 3, sphere(x, y, 3, base=0.5))
        c.line([(12, 30), (36, 30)], 0.5, 0.5)
        c.arc((32, 2, 54, 22), 180, 360, 0.8, 0)                            # casque
        c.circle(33, 12, 2.6, flat(0.5))
        c.circle(53, 12, 2.6, flat(0.5))
    elif k == "iff":
        _box(c, 6, 16, 32, 36)
        c.bar((19, 16), (19, 6), 0.6)
        for r in (6, 10, 14):
            c.arc((40 - r, 20 - r, 40 + r, 20 + r), 300, 60, 0.6, 0)
        c.circle(40, 20, 2, flat(0.85), accent=1.0)
    elif k == "monica":
        _box(c, 4, 14, 26, 34)
        for r in (5, 9, 13):
            c.arc((40 - r, 24 - r, 40 + r, 24 + r), 120, 240, 0.6, 0)          # ondes vers l'arrière
        c.circle(40, 24, 2.2, flat(0.85), accent=1.0)
    elif k == "naxos":
        c.ellipse((10, 10, 46, 30), sphere(28, 20, 15, base=0.45))
        c.poly([(8, 30), (48, 30), (48, 34), (8, 34)], flat(0.4))
        for r in (6, 11):
            c.arc((28 - r, 10 - r, 28 + r, 10 + r), 200, 340, 0.5, 0)
    elif k == "window":
        for i in range(9):
            x, y = 8 + (i * 13) % 40, 6 + (i * 7) % 28
            c.poly([(x, y), (x + 2, y), (x + 6, y + 9), (x + 4, y + 9)], flat(0.75), accent=0.6)
    elif k == "asv_radar":
        c.poly([(4, 24), (52, 24), (52, 27), (4, 27)], flat(0.38), a=0.55)
        for x in (12, 26, 40):
            c.bar((x, 24), (x, 12), 0.7)
            for y in (13, 16, 19):
                c.bar((x - 4, y), (x + 4, y), 0.45)
        c.circle(48, 12, 2, flat(0.85), accent=1.0)
    elif k == "leigh_light":
        c.rrect((8, 12, 34, 32), 6, cyl((8, 22), (34, 22), 10, base=0.38))
        c.ellipse((30, 12, 38, 32), flat(0.85), accent=1.0)
        c.poly([(38, 14), (56, 6), (56, 38), (38, 30)], flat(0.85), a=0.35, accent=1.0)
    elif k == "sonobuoys":
        for x in (14, 34):
            c.rrect((x - 5, 8, x + 5, 34), 4, cyl((x - 5, 21), (x + 5, 21), 5, base=0.42))
            c.bar((x, 8), (x, 2), 0.4)
        c.arc((6, 30, 46, 46), 200, 340, 0.5, 0)
    elif k == "mad":
        c.poly([(2, 18), (30, 18), (30, 24), (2, 24)], flat(0.38), a=0.55)
        c.bar((30, 21), (52, 21), 1.8)
        c.circle(52, 21, 2.6, sphere(52, 21, 2.6, base=0.5))
        for r in (5, 9):
            c.arc((52 - r, 21 - r, 52 + r, 21 + r), 60, 120, 0.5, 0)
    elif k == "night_photo":
        _box(c, 8, 12, 38, 34)
        c.circle(23, 23, 7, sphere(23, 23, 7, base=0.3))
        c.circle(23, 23, 3, 0.12)
        c.poly([(42, 8), (50, 8), (46, 16), (52, 16), (42, 30), (45, 19), (40, 19)], flat(0.9), accent=1.0)
    elif k in ("autopilot", "radar_altimeter"):
        _box(c, 8, 10, 40, 36)
        c.circle(24, 23, 9, sphere(24, 23, 9, base=0.3))
        if k == "autopilot":
            c.line([(15, 23), (33, 23)], 0.6, 0)
            c.line([(24, 14), (24, 32)], 0.4, 0)
        else:
            c.line([(24, 23), (30, 16)], 0.6, 0)
            for r in (5, 9):
                c.arc((48 - r, 38 - r, 48 + r, 38 + r), 200, 340, 0.5, 0)
        c.badge = ("II" if k == "radar_altimeter" else "I", "tier")
    return c


def gunsight(m):
    c = Canvas()
    k = m[3:]
    gen = int(k[-1])
    c.rrect((10, 26, 34, 36), 2, flat(0.38))                            # boîtier
    c.poly([(16, 26), (24, 8), (27, 8), (21, 26)], flat(0.75), a=0.55)     # glace réflectrice
    c.circle(42, 17, 7, 0.2, a=0.0)
    c.arc((35, 10, 49, 24), 0, 360, 0.6, 0)                             # réticule
    c.line([(42, 12), (42, 22)], 0.4, 0)
    c.line([(37, 17), (47, 17)], 0.4, 0)
    if k.startswith("gyro"):
        c.circle(22, 31, 4, sphere(22, 31, 4, base=0.5))
        c.arc((15, 24, 29, 38), 200, 340, 0.6, 0)
    elif k.startswith("attack"):
        c.poly([(40, 30), (44, 30), (44, 36), (46, 36), (42, 40), (38, 36), (40, 36)], flat(0.85), accent=1.0)
    c.badge = (ROMAN[gen], "tier")
    return c


def aero(m):
    """Volets, becs, aérofreins, pylônes, crosse d'appontage."""
    c = Canvas()
    k = m[3:]
    wing = lambda: c.poly([(3, 16), (8, 12), (40, 12), (44, 16), (44, 24), (3, 24)], plane_lit(0.55, 0.3, 12, 24))
    if k == "leading_edge_slats":
        c.poly([(10, 14), (48, 14), (52, 18), (52, 26), (10, 26)], plane_lit(0.55, 0.3, 14, 26))
        c.poly([(2, 18), (6, 12), (8, 12), (5, 20)], flat(0.75), accent=1.0)
    elif k.startswith("combat_flaps") or k == "fowler_flaps":
        wing()
        if k == "fowler_flaps":
            c.poly([(46, 20), (54, 24), (52, 30), (44, 26)], flat(0.75), accent=1.0)
        else:
            c.poly([(44, 20), (52, 26), (50, 28), (43, 23)], flat(0.75), accent=1.0)
        _size_badge(c, m)
    elif k.startswith("dive_brakes"):
        c.poly([(3, 6), (53, 6), (53, 10), (3, 10)], flat(0.38), a=0.55)
        for x in (10, 30):
            c.poly([(x, 10), (x + 14, 10), (x + 14, 34), (x, 34)], flat(0.5))
            for yy in range(14, 32, 5):
                for xx in range(x + 3, x + 13, 5):
                    c.circle(xx, yy, 1.2, 0.12, outline=False)
        _size_badge(c, m)
    elif k.startswith("aerodynamic_pylons"):
        c.poly([(3, 6), (53, 6), (53, 10), (3, 10)], flat(0.38), a=0.55)
        c.poly([(18, 10), (36, 10), (32, 20), (22, 20)], plane_lit(0.6, 0.3, 10, 20))
        c.poly([(8, 26), (16, 21), (40, 21), (50, 26), (40, 31), (16, 31)], cyl((8, 26), (50, 26), 5, base=0.4))
        _size_badge(c, m)
    elif k == "carrier_equipment":
        c.poly([(2, 12), (40, 14), (40, 20), (2, 20)], cyl((2, 16), (40, 16), 4, base=0.4), a=0.8)
        c.bar((36, 19), (50, 33), 0.8)                                    # crosse d'appontage
        c.poly([(48, 31), (54, 33), (53, 36), (47, 34)], flat(0.6))
        c.poly([(8, 24), (20, 24), (22, 38), (10, 38)], flat(0.5))         # aile repliée
        c.arc((4, 18, 26, 40), 180, 270, 0.6, 0)
    return c


def payload(m):
    c = Canvas()
    k = m[3:]
    if k == "cargo_bay":
        for x, y, w, h in ((6, 20, 16, 16), (24, 20, 14, 16), (40, 24, 12, 12), (14, 6, 16, 14)):
            c.rrect((x, y, x + w, y + h), 1, flat(0.42 + 0.03 * (x % 3)))
            c.line([(x, y + h / 2), (x + w, y + h / 2)], 0.4, 0.4)
    elif k == "troop_compartment":
        for i, x in enumerate((10, 22, 34, 46)):
            c.circle(x, 13, 3, sphere(x, 13, 3, base=0.45))
            c.rrect((x - 4, 17, x + 4, 32), 2.5, cyl((x - 4, 24), (x + 4, 24), 4, base=0.4))
    elif k == "supply_drop":
        c.ellipse((10, 2, 46, 22), sphere(28, 12, 18, base=0.5))
        c.poly([(10, 12), (46, 12), (46, 14), (10, 14)], 0.15, outline=False)
        for x in (12, 28, 44):
            c.line([(x, 13), (28, 28)], 0.35, 0)
        c.rrect((22, 27, 34, 40), 2, flat(0.42))
    elif k == "rato":
        c.poly([(4, 10), (52, 10), (52, 13), (4, 13)], flat(0.38), a=0.55)
        for y in (20, 31):
            c.rrect((10, y - 4, 40, y + 4), 4, cyl((10, y), (40, y), 4, base=0.42))
            c.poly([(40, y - 3), (46, y - 4.5), (46, y + 4.5), (40, y + 3)], flat(0.4))
            c.poly([(46, y - 3), (55, y), (46, y + 3)], flat(0.9), accent=1.0)
    return c


# ---------------------------------------------------------------- rôles
ROLE_MARK = {
    "fighter": "cross", "interceptor": "arrow_up", "heavy_fighter": "cross", "cas": "bomb", "suicide": "burst",
    "tac_bomber": "bomb", "naval_bomber": "torpedo", "recon": "eye", "maritime_patrol": "wave",
    "strat_bomber": "bombs", "transport": "crate",
}


def role(m):
    rest = m[len("zv_role_"):]
    kind, size = rest.rsplit("_", 1)
    c = Canvas()
    layout = {"small": "nose", "medium": "twin_wing", "large": "quad"}[size]
    if layout == "nose":
        silhouette(c, span=36, chord=6, wy=16, fus=(19.5, 4, 23.5, 34), tail=(15, 30, 28, 32.5), lit=0.5)
        x_mark = 41
    elif layout == "twin_wing":
        silhouette(c, span=40, chord=6, wy=15, fus=(19.5, 4, 24.5, 36), tail=(14, 31, 30, 34), lit=0.5)
        for x in (12, 32):
            c.rrect((x - 1.8, 11, x + 1.8, 20), 1.8, flat(0.5))
        x_mark = 45
    else:
        silhouette(c, span=44, chord=7, wy=15, fus=(20, 3, 25, 38), tail=(14, 33, 31, 36), lit=0.5)
        for x in (5, 13, 32, 40):
            c.rrect((x - 1.6, 12, x + 1.6, 20), 1.6, flat(0.5))
        x_mark = 48
    mark = ROLE_MARK[kind]
    y = 28
    if mark == "cross":
        c.circle(x_mark, y - 6, 5.5, 0.2, a=0.0)
        c.arc((x_mark - 5.5, y - 11.5, x_mark + 5.5, y - 0.5), 0, 360, 0.6, 0)
        c.line([(x_mark, y - 12.5), (x_mark, y + 0.5)], 0.5, 0)
        c.line([(x_mark - 6.5, y - 6), (x_mark + 6.5, y - 6)], 0.5, 0)
    elif mark == "arrow_up":
        c.poly([(x_mark - 4, y - 4), (x_mark, y - 13), (x_mark + 4, y - 4), (x_mark + 1.5, y - 4), (x_mark + 1.5, y + 3), (x_mark - 1.5, y + 3), (x_mark - 1.5, y - 4)], flat(0.85), accent=1.0)
    elif mark in ("bomb", "bombs"):
        for dx in ((0,) if mark == "bomb" else (-3.5, 3.5)):
            c.rrect((x_mark + dx - 2.2, y - 10, x_mark + dx + 2.2, y + 1), 2.2, flat(0.85), accent=1.0)
            c.poly([(x_mark + dx - 2.6, y - 12), (x_mark + dx + 2.6, y - 12), (x_mark + dx + 1.5, y - 9), (x_mark + dx - 1.5, y - 9)], flat(0.85), accent=1.0)
    elif mark == "torpedo":
        c.rrect((x_mark - 7, y - 6, x_mark + 6, y - 2.5), 1.8, flat(0.85), accent=1.0)
        c.poly([(x_mark + 6, y - 7), (x_mark + 8.5, y - 7), (x_mark + 8.5, y - 1.5), (x_mark + 6, y - 1.5)], flat(0.85), accent=1.0)
    elif mark == "burst":
        pts = [(x_mark + (6 if k % 2 == 0 else 2.6) * math.cos(2 * math.pi * k / 14), y - 6 + (6 if k % 2 == 0 else 2.6) * math.sin(2 * math.pi * k / 14)) for k in range(14)]
        c.poly(pts, flat(0.9), accent=1.0)
    elif mark == "eye":
        c.ellipse((x_mark - 6.5, y - 9, x_mark + 6.5, y - 3), flat(0.85), accent=1.0)
        c.circle(x_mark, y - 6, 1.8, 0.15, outline=False)
    elif mark == "wave":
        for dy in (0, 4):
            c.line([(x_mark - 7, y - 6 + dy), (x_mark - 3.5, y - 8 + dy), (x_mark, y - 6 + dy), (x_mark + 3.5, y - 8 + dy), (x_mark + 7, y - 6 + dy)], 0.9, 0)
        c.alpha = np.maximum(c.alpha, c.lines * 0.95)
    elif mark == "crate":
        c.rrect((x_mark - 5, y - 11, x_mark + 5, y - 1), 1, flat(0.85), accent=1.0)
        c.line([(x_mark - 5, y - 6), (x_mark + 5, y - 6)], 0.4, 0.4)
    c.badge = ({"small": "S", "medium": "M", "large": "L"}[size], "size")
    return c


FAMILY = [
    ("zv_early_supercharger", "équipements", supercharger), ("zv_early_turbocharger", "équipements", supercharger),
    ("zv_supercharger", "équipements", supercharger), ("zv_turbocharger", "équipements", supercharger),
    ("zv_improved_supercharger", "équipements", supercharger), ("zv_improved_turbocharger", "équipements", supercharger),
    ("zv_two_stage_supercharger", "équipements", supercharger),
    ("zv_high_octane", "équipements", feed), ("zv_water_injection", "équipements", feed), ("zv_gm1", "équipements", feed),
    ("zv_direct_injection", "équipements", feed), ("zv_anti_g", "équipements", feed), ("zv_wep_", "équipements", feed),
    ("zv_naca_cowling", "équipements", cooling), ("zv_air_intake", "équipements", cooling), ("zv_radiator_", "équipements", cooling),
    ("zv_afterburner", "équipements", jet_upgrade), ("zv_supersonic_intake", "équipements", jet_upgrade),
    ("zv_jet_improved_compressor", "équipements", jet_upgrade),
    ("zv_self_sealing", "équipements", tanks), ("zv_fuel_tanks", "équipements", tanks), ("zv_drop_tanks", "équipements", tanks),
    ("zv_bomb_bay_tank", "équipements", tanks), ("zv_ferry_tank", "équipements", tanks),
    ("zv_armor_plate_", "équipements", armour), ("zv_armored_cockpit", "équipements", armour), ("zv_ejection_seat", "équipements", armour),
    ("zv_auto_extinguisher", "équipements", safety), ("zv_deicing_boots", "équipements", safety), ("zv_heated_leading", "équipements", safety),
    ("zv_radio_telephone", "électronique", avionics), ("zv_iff", "électronique", avionics), ("zv_monica", "électronique", avionics),
    ("zv_naxos", "électronique", avionics), ("zv_window", "électronique", avionics), ("zv_asv_radar", "électronique", avionics),
    ("zv_leigh_light", "électronique", avionics), ("zv_sonobuoys", "électronique", avionics), ("zv_mad", "électronique", avionics),
    ("zv_night_photo", "électronique", avionics), ("zv_autopilot", "électronique", avionics), ("zv_radar_altimeter", "électronique", avionics),
    ("zv_reflex_gunsight", "électronique", gunsight), ("zv_attack_gunsight", "électronique", gunsight), ("zv_gyro_gunsight", "électronique", gunsight),
    ("zv_leading_edge_slats", "équipements", aero), ("zv_combat_flaps", "équipements", aero), ("zv_fowler_flaps", "équipements", aero),
    ("zv_dive_brakes", "équipements", aero), ("zv_aerodynamic_pylons", "équipements", aero), ("zv_carrier_equipment", "équipements", aero),
    ("zv_cargo_bay", "équipements", payload), ("zv_troop_compartment", "équipements", payload), ("zv_supply_drop", "équipements", payload),
    ("zv_rato", "équipements", payload), ("zv_role_", "rôles", role),
]

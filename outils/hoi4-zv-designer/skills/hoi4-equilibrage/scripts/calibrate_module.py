#!/usr/bin/env python3
"""
calibrate_module.py - Place un module (nouveau ou modifié) sur la courbe de sa
catégorie et signale ce qui sort de la norme vanilla.

    # module écrit dans un fichier (bloc equipment_modules = { ... } ou bloc seul)
    python3 calibrate_module.py --file mon_module.txt --year 1941
    # module déjà présent dans une base (vanilla ou mod)
    python3 calibrate_module.py --name aircraft_cannon_2_2x
    python3 calibrate_module.py --db mod_air_db.json --name mon_canon_37mm

Pour chaque stat du module (permanente ou de mission), le script :
  1. ajuste une tendance linéaire stat = a + b × année sur les modules vanilla de
     la même catégorie (s'il y en a au moins 3 datés), et donne la plage
     attendue à l'année du module (tendance ± plus grand écart observé) ;
  2. compare les ratios stat/IC et stat/poids à ceux des pairs de ±3 ans ;
  3. teste la DOMINANCE : un pair d'année ≤ que le module domine-t-il le module
     (ou l'inverse) — mieux ou égal partout, pas plus cher, pas plus lourd ?
     Un nouveau module qui domine un pair contemporain sans contrepartie est le
     signe classique d'un module "cheaté".
  4. vérifie la cohérence avec son `parent` (chaîne d'amélioration) : le module
     doit apporter un gain sur au moins une stat et le payer quelque part, ou être
     plus tardif.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "scripts"))  # scripts partagés du plugin (pdx, extract_air)
import plane_calc as pc  # noqa: E402
from pdx import Block, load_file  # noqa: E402
from extract_air import parse_module  # noqa: E402

COST_STATS = {"build_cost_ic", "weight", "fuel_consumption"}           # plus = pire
NEG_GOOD = {"night_penalty"}                                              # plus = pire aussi
IGNORE = {"thrust"}  # traitée à part pour les moteurs


def flat_stats(m: dict) -> dict:
    """Stats effectives : permanentes + la mission où le module sert le plus
    (on prend la première mission listée pour chaque bloc, clé 'stat@mission')."""
    out = {}
    for k, v in m["add_stats"].items():
        out[k] = out.get(k, 0) + v
    for k, v in m["add_average_stats"].items():
        out[k + " (moy.)"] = v
    for k, v in m["multiply_stats"].items():
        out[k + " (×)"] = v
    for mt in m["mission_type_stats"]:
        tag = mt["missions"][0] if mt["missions"] else "?"
        for k, v in mt["add_stats"].items():
            out[f"{k}@{tag}"] = out.get(f"{k}@{tag}", 0) + v
        for k, v in mt["add_average_stats"].items():
            out[f"{k} (moy.)@{tag}"] = v
        for k, v in mt["multiply_stats"].items():
            out[f"{k} (×)@{tag}"] = v
    return out


def worse_is_higher(stat: str) -> bool:
    base = stat.split("@")[0].replace(" (moy.)", "").replace(" (×)", "")
    return base in COST_STATS or base in NEG_GOOD


def better_or_equal(a: dict, b: dict) -> bool:
    """a au moins aussi bon que b sur toutes les stats de l'union."""
    for k in set(a) | set(b):
        va, vb = a.get(k, 0.0), b.get(k, 0.0)
        if worse_is_higher(k):
            if va > vb + 1e-9:
                return False
        elif k.startswith("air_agility") or k.startswith("maximum_speed") or k.startswith("air_range") or k.startswith("reliability"):
            if va < vb - 1e-9:
                return False
        else:
            if va < vb - 1e-9:
                return False
    return True


def linfit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return my, 0.0
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my - b * mx, b


def load_module_from_file(path: str) -> dict:
    root = load_file(path)
    em = root.get("equipment_modules")
    blk = em if isinstance(em, Block) else root
    for name, b in blk.blocks():
        if name == "limit":
            continue
        return parse_module(name, b, path, None)
    sys.exit("aucun module trouvé dans le fichier")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", help="base contenant les pairs (défaut : vanilla)")
    ap.add_argument("--name", help="module présent dans la base")
    ap.add_argument("--file", help="fichier contenant la définition du module")
    ap.add_argument("--year", type=int, help="année visée (sinon : année de la tech qui le débloque)")
    ap.add_argument("--window", type=int, default=3, help="fenêtre ± années pour les pairs (défaut 3)")
    a = ap.parse_args(argv)
    db = pc.load_db(a.db)
    M = db["modules"]
    if a.file:
        mod = load_module_from_file(a.file)
    elif a.name:
        if a.name not in M:
            sys.exit(f"module inconnu : {a.name}")
        mod = M[a.name]
    else:
        ap.print_help()
        return 1
    year = a.year or mod.get("year")
    cat = mod["category"]
    peers = [m for n, m in M.items() if m["category"] == cat and n != mod["name"]]
    print(f"# Calibration de `{mod['name']}` — catégorie {cat}, année {year or '?'}")
    if not peers:
        print("Aucun module vanilla dans cette catégorie : comparer à la catégorie la plus proche (voir references/methode-calibration.md).")
        return 0
    fs = flat_stats(mod)
    print("\n## Stats du module")
    for k, v in fs.items():
        print(f"  {k:40} {v:g}")

    print("\n## Position sur la tendance de la catégorie")
    dated = [(p.get("year"), flat_stats(p)) for p in peers if p.get("year") and p["year"] > 1925]
    for k, v in fs.items():
        pts = [(y, s[k]) for y, s in dated if k in s]
        if len(pts) < 3 or not year:
            vals = [s.get(k) for _, s in dated if k in s]
            if vals:
                print(f"  {k:40} {v:g}  (pairs : {min(vals):g} → {max(vals):g}, trop peu de points pour une tendance)")
            continue
        aa, bb = linfit([p[0] for p in pts], [p[1] for p in pts])
        resid = max(abs(y - (aa + bb * x)) for x, y in pts)
        exp = aa + bb * year
        lo, hi = exp - resid, exp + resid
        flag = ""
        if v > hi + 1e-9:
            flag = "  ⚠ AU-DESSUS de la plage" if not worse_is_higher(k) else "  (plus cher/lourd que la plage)"
        elif v < lo - 1e-9:
            flag = "  (en dessous de la plage)" if not worse_is_higher(k) else "  ⚠ MOINS CHER/LÉGER que la plage"
        print(f"  {k:40} {v:g}   attendu ≈ {exp:.3g} [{lo:.3g} ; {hi:.3g}] (pente {bb:+.3g}/an, {len(pts)} pts){flag}")

    print(f"\n## Ratios face aux pairs de ±{a.window} ans")
    near = [p for p in peers if year and p.get("year") and abs(p["year"] - year) <= a.window] or peers
    ic = mod["add_stats"].get("build_cost_ic", 0)
    w_mod = fs.get("weight", 0) + sum(v for k, v in fs.items() if k.startswith("weight@"))
    main_stats = [k for k in fs if not worse_is_higher(k) and not k.startswith("air_agility") and "(×)" not in k and fs[k] > 0]
    for k in main_stats:
        def r(m, kk=k):
            s = flat_stats(m)
            c = m["add_stats"].get("build_cost_ic", 0)
            return (s.get(kk, 0) / c) if c else None
        mine = (fs[k] / ic) if ic else None
        others = [(p["name"], r(p)) for p in near if r(p)]
        if others and mine is not None:
            mx = max(o[1] for o in others)
            mn = min(o[1] for o in others)
            flag = "  ⚠ meilleur rapport que tous les pairs" if mine > mx * 1.05 else ""
            print(f"  {k}/IC : {mine:.2f}  (pairs {mn:.2f} → {mx:.2f}){flag}")

    print("\n## Dominance")
    found = False
    for p in near:
        sp = flat_stats(p)
        if better_or_equal(fs, sp) and fs != sp:
            print(f"  ⚠ `{mod['name']}` DOMINE `{p['name']}` ({p.get('year')}) : au moins aussi bon partout, sans surcoût")
            found = True
        elif better_or_equal(sp, fs) and fs != sp:
            print(f"  `{p['name']}` ({p.get('year')}) domine `{mod['name']}` : le nouveau module serait inutile")
            found = True
    if not found:
        print("  Aucune dominance stricte : chaque module a un compromis par rapport aux pairs proches.")

    if mod.get("parent") and mod["parent"] in M:
        par = M[mod["parent"]]
        sp = flat_stats(par)
        gains = {k: fs.get(k, 0) - sp.get(k, 0) for k in set(fs) | set(sp)}
        print(f"\n## Face au parent `{par['name']}` ({par.get('year')})")
        for k, d in sorted(gains.items()):
            if abs(d) > 1e-9:
                print(f"  {k:40} {d:+g}")
        if not any((d > 0 and not worse_is_higher(k)) or (d < 0 and worse_is_higher(k)) for k, d in gains.items()):
            print("  ⚠ aucun gain par rapport au parent")
    return 0


if __name__ == "__main__":
    try:  # sortie tronquée par | head : pas de trace d'erreur
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())

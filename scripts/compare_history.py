"""Phase 7 : compare chaque avion de départ converti (mod) à son design vanilla de même nom, stat par
stat, avec le calcul du plugin (plane_calc.compute) et les curseurs au cran 5.

  python -X utf8 scripts/compare_history.py --mod-db <mod_db.json>   (base : extract_air.py --mod mod)

Sortie : tableau Markdown des écarts (rapport/vanilla), médianes par rôle et liste des écarts > 15 % (Q17).
"""
import argparse, json, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "outils/hoi4-zv-designer"
sys.path.insert(0, str(PLUGIN / "skills/hoi4-equilibrage/scripts"))
sys.path.insert(0, str(Path(__file__).parent))
import plane_calc as P  # noqa: E402
import gen_mod_table as T  # noqa: E402

STATS = [("maximum_speed", "Vitesse"), ("air_agility", "Agilité"), ("air_attack", "Attaque air"),
         ("air_defence", "Défense"), ("air_range", "Portée"), ("air_ground_attack", "Sol"),
         ("air_bombing", "Bomb."), ("naval_strike_attack", "Naval"), ("build_cost_ic", "IC"),
         ("reliability", "Fiabilité")]
TOL = 0.15          # Q17 : tolérance de 15 %
SLIDER = "_zv_curseurs_cran_5"


def add_sliders(db):
    """Module fictif = les deux curseurs au cran d'usine (5 crans de chaque), posé dans un slot fictif."""
    add, mult = {}, {}
    for u in T.CURSEURS.values():
        for k, v in u["add"].items():
            add[k] = add.get(k, 0) + v * T.CURSEUR_USINE
        for k, v in u["mult"].items():
            mult[k] = mult.get(k, 0) + v * T.CURSEUR_USINE
    db["modules"][SLIDER] = {"category": SLIDER, "add_stats": add, "multiply_stats": mult, "add_average_stats": {},
                             "mission_type_stats": [], "forbid_module_categories": []}
    for a in db["airframes"].values():
        a["slots"][SLIDER] = {"categories": [SLIDER], "required": False}


def main_stats(db, airframe, modules):
    """Stats du designer, et celles de la mission principale pour les stats de mission (sol, bomb., naval)."""
    res = P.compute_all_missions(db, airframe, modules)
    d = dict(res["designer"]["stats"])
    for k in ("air_ground_attack", "air_bombing", "naval_strike_attack"):
        d[k] = max([r["stats"].get(k, 0) for r in res.values()] + [0])
    errs = [e for r in res.values() for e in r["errors"]]
    return d, errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mod-db", required=True)
    a = ap.parse_args()
    mod = P.load_db(a.mod_db)
    van = P.load_db(PLUGIN / "data/air_db_vanilla.json")
    add_sliders(mod)
    vh = {(h["country"], h["name"]): h for h in van["history_designs"]
          if any("By Blood Alone" in c and not c.startswith("NOT") for c in h.get("context", []))}
    rows, ratios, errors = [], {k: [] for k, _ in STATS}, []
    for h in mod["history_designs"]:
        if not any(str(v).startswith("zv_") for v in h["modules"].values()):
            continue
        v = vh.get((h["country"], h["name"]))
        if not v:
            continue
        ms, merr = main_stats(mod, h["type"], dict(h["modules"], **{SLIDER: SLIDER}))
        vs, _ = main_stats(van, v["type"], v["modules"])
        if merr:
            errors.append((h["country"], h["name"], merr))
        r = {}
        for k, _ in STATS:
            if abs(vs.get(k, 0)) > 1e-9:
                r[k] = ms.get(k, 0) / vs[k]
                ratios[k].append(r[k])
        role = h["type"].rsplit("_", 1)[0]
        rows.append((h["country"], h["name"], role, ms, vs, r))
    out = ["| Pays | Avion | Cellule | " + " | ".join(n for _, n in STATS) + " |",
           "| --- | --- | --- | " + " | ".join("---" for _ in STATS) + " |"]
    for c, n, role, ms, vs, r in rows:
        cells = []
        for k, _ in STATS:
            if k in r:
                flag = "🔴" if r[k] < 1 - TOL else "🟢" if r[k] > 1 + TOL else ""
                cells.append(f"{ms.get(k, 0):.3g} / {vs[k]:.3g} {flag}".strip())
            else:
                cells.append(f"{ms.get(k, 0):.3g} / —" if ms.get(k, 0) else "—")
        out.append(f"| {c} | {n} | {role.replace('_airframe', '').replace('plane_', '')} | " + " | ".join(cells) + " |")
    out += ["", "| Stat | Écart médian (mod / vanilla) | Hors ±15 % |", "| --- | --- | --- |"]
    for k, name in STATS:
        if ratios[k]:
            nb = sum(1 for x in ratios[k] if abs(x - 1) > TOL)
            out.append(f"| {name} | ×{statistics.median(ratios[k]):.2f} | {nb} / {len(ratios[k])} |")
    out.append(f"\n{len(rows)} avions comparés. Lecture : « mod / vanilla » ; 🔴 plus de 15 % en dessous, 🟢 plus de 15 % au-dessus.")
    if errors:
        out.append("\nAvertissements du calcul (poids > poussée dans une mission…) :")
        out += [f"- {c} « {n} » : {'; '.join(sorted(set(e)))[:200]}" for c, n, e in errors]
    print("\n".join(out))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
plane_calc.py - Calcule les statistiques d'un design d'avion HOI4 (designer BBA)
à partir de la base `air_db.json` produite par extract_air.py (skill hoi4-modding).

Exemples :
    # un design précis, stats affichées par mission
    python3 plane_calc.py --type small_plane_airframe_2 \
        fixed_main_weapon_slot=heavy_mg_4x fixed_auxiliary_weapon_slot_1=aircraft_cannon_1_2x \
        engine_type_slot=engine_3_1x special_type_slot_1=armor_plate_small

    # tous les designs historiques d'un pays, avec en dernière colonne l'avion
    # générique d'avant le designer (la référence d'équilibrage retenue)
    python3 plane_calc.py --history GER
    # un gabarit IA
    python3 plane_calc.py --ai GER_fighter

    # sortie JSON (pour d'autres scripts)
    python3 plane_calc.py --type ... --json

Base par défaut : <racine du plugin>/data/air_db_vanilla.json (générée sur la version notée dans
son champ meta.game_version). Pour un mod : --db chemin/vers/air_db.json.

MODÈLE DE CALCUL (reconstitué à partir des fichiers et des defines, PAS d'une
documentation officielle de la formule — voir references/modele-de-calcul.md) :

  1. base       = stats de la cellule (archétype + type)
  2. + Σ add_stats des modules (+ mission_type_stats.add_stats si la mission est active)
  3. + moyenne des add_average_stats des modules qui fournissent la stat
  4. × (1 + Σ multiply_stats)                       [multiplicateurs ADDITIONNÉS]
  5. agilité += THRUST_WEIGHT_AGILITY_FACTOR × max(0, poussée − poids)
  6. design INVALIDE si poids > poussée (pour la mission considérée)

Les points 3, 4 (ordre) et 5 (avant/après multiplicateurs) sont les hypothèses
à vérifier en jeu : les constantes AVERAGE_MODE, MULT_MODE et AGILITY_BONUS_STAGE
permettent de tester les variantes si une comparaison avec le designer du jeu
montre un écart.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN_ROOT = HERE.parents[2]
DEFAULT_DB = PLUGIN_ROOT / "data" / "air_db_vanilla.json"

# --- hypothèses du modèle (à confirmer en jeu, cf. modele-de-calcul.md) ------
AVERAGE_MODE = "modules_mean_plus_base"   # ou "all_mean" (base incluse dans la moyenne)
MULT_MODE = "sum"                          # ou "product" (Π(1+m))
AGILITY_BONUS_STAGE = "after_mult"         # ou "before_mult"

DISPLAY_STATS = [
    "maximum_speed", "air_agility", "air_attack", "air_defence", "air_range",
    "air_ground_attack", "air_bombing", "naval_strike_attack", "naval_strike_targetting",
    "surface_detection", "sub_detection", "night_penalty", "mines_planting", "mines_sweeping",
    "thrust", "weight", "reliability", "build_cost_ic", "fuel_consumption",
]
STAT_FR = {
    "maximum_speed": "Vitesse max", "air_agility": "Agilité", "air_attack": "Attaque air",
    "air_defence": "Défense air", "air_range": "Portée", "air_ground_attack": "Attaque sol",
    "air_bombing": "Bombardement strat.", "naval_strike_attack": "Attaque navale",
    "naval_strike_targetting": "Ciblage naval", "surface_detection": "Détection surface",
    "sub_detection": "Détection sous-marins", "night_penalty": "Pénalité de nuit",
    "mines_planting": "Pose de mines", "mines_sweeping": "Déminage", "thrust": "Poussée",
    "weight": "Poids", "reliability": "Fiabilité", "build_cost_ic": "Coût (IC)",
    "fuel_consumption": "Carburant",
}
NAVAL_MISSIONS = {"naval_bomber", "port_strike", "naval_kamikaze"}


def load_db(path: str | Path | None = None) -> dict:
    p = Path(path) if path else DEFAULT_DB
    if not p.is_file():
        sys.exit(f"Base introuvable : {p}\nGénère-la avec : python3 <racine du plugin>/scripts/extract_air.py --ref <HOI4> --out {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def define(db: dict, name: str, default: float) -> float:
    v = db.get("defines", {}).get(f"NAir.{name}", {}).get("value")
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------
def _limit_matches(lim: dict, slot: str, module: str | None, mod: dict | None) -> bool:
    for m in lim["match"]:
        if "module" in m:
            if m["module"] == "any" and module:
                return True
            if m["module"] == "empty" and not module:
                return True
            if module and m["module"] == module:
                return True
        if "category" in m:
            if m["category"] == "any" and module:
                return True
            if mod and m["category"] == mod.get("category"):
                return True
    return False


def validate(db: dict, airframe: dict, modules: dict[str, str | None]) -> list[str]:
    """Erreurs bloquantes (le jeu refuserait le design)."""
    errs = []
    M = db["modules"]
    slots = airframe["slots"]
    for s, m in modules.items():
        if s not in slots:
            errs.append(f"slot inconnu pour {airframe['name']} : {s}")
            continue
        if m and m not in M:
            errs.append(f"module inconnu : {m}")
            continue
        if m and M[m]["category"] not in slots[s].get("categories", []):
            errs.append(f"{m} ({M[m]['category']}) interdit dans {s}")
    for s, info in slots.items():
        if info.get("required") and not modules.get(s):
            errs.append(f"slot obligatoire vide : {s}")
    present = {s: m for s, m in modules.items() if m and m in M}
    cats = {M[m]["category"] for m in present.values()}
    for s, m in present.items():
        for fc in M[m].get("forbid_module_categories", []):
            if fc in cats:
                errs.append(f"{m} interdit la catégorie {fc} (présente dans le design)")
    for lim in airframe.get("module_count_limit", []):
        n = sum(1 for s in slots if _limit_matches(lim, s, modules.get(s), M.get(modules.get(s) or "")))
        c = lim.get("count")
        if c in (None, "any"):
            continue
        c = int(float(c))
        op = lim.get("op", "=")
        ok = (n < c) if op == "<" else (n > c) if op == ">" else (n == c)
        if not ok:
            what = ", ".join(f"{k}={v}" for mm in lim["match"] for k, v in mm.items())
            errs.append(f"limite non respectée : {what} -> {n} (doit être {op} {c})")
    return errs


# --------------------------------------------------------------------------
# Calcul
# --------------------------------------------------------------------------
def allowed_missions(db: dict, airframe: dict, modules: dict) -> list[str]:
    M = db["modules"]
    ms = set()
    for m in modules.values():
        if m and m in M:
            ms.update(M[m].get("allow_mission_type", []))
    ms.update(airframe.get("allow_mission_type", []))
    ms -= set(airframe.get("forbid_mission_type", []))
    return sorted(ms)


def design_types(db: dict, airframe: dict, modules: dict) -> list[str]:
    """Type(s) d'équipement du design. Avec type_override = <slot>, c'est le
    module de ce slot qui donne le type (add_equipment_type)."""
    M = db["modules"]
    slot = airframe.get("type_override")
    if slot and modules.get(slot) in M:
        t = M[modules[slot]].get("add_equipment_type", [])
        allowed = airframe.get("allowed_types") or [airframe.get("type")]
        res = [x for x in t if x in allowed] or t
        if res:
            return res
    t = airframe.get("type")
    return t if isinstance(t, list) else [t]


def _naval_armament_category(db: dict, modules: dict, mission: str) -> str | None:
    """USE_SINGLE_NAVAL_ARMAMENT_CATEGORY : seule la catégorie d'armement qui
    inflige le plus de dégâts navals compte pour les missions navales."""
    M = db["modules"]
    best, best_val = None, -1.0
    per_cat = defaultdict(float)
    for m in modules.values():
        if not m or m not in M:
            continue
        for mt in M[m]["mission_type_stats"]:
            if mission in mt["missions"]:
                atk = mt["add_stats"].get("naval_strike_attack", 0)
                has_tgt = "naval_strike_targetting" in mt["add_stats"] or "naval_strike_targetting" in mt["add_average_stats"]
                if atk and has_tgt:
                    per_cat[M[m]["category"]] += atk
    for c, v in per_cat.items():
        if v > best_val:
            best, best_val = c, v
    return best


def compute(db: dict, airframe_name: str, modules: dict[str, str | None], mission: str | None = None) -> dict:
    A = db["airframes"].get(airframe_name)
    if A is None:
        raise KeyError(f"cellule inconnue : {airframe_name}")
    M = db["modules"]
    modules = {s: (None if m in (None, "", "empty") else m) for s, m in modules.items()}
    base = defaultdict(float, A["stats"])
    add = defaultdict(float)
    mult = defaultdict(float)
    mult_list = defaultdict(list)
    avg = defaultdict(list)
    resources = defaultdict(float, A.get("resources", {}))

    naval_cat = _naval_armament_category(db, modules, mission) if mission in NAVAL_MISSIONS else None
    use_single = str(db.get("defines", {}).get("NAir.USE_SINGLE_NAVAL_ARMAMENT_CATEGORY", {}).get("value", "true")).lower() == "true"

    def apply(block_add, block_mult, block_avg):
        for k, v in block_add.items():
            add[k] += v
        for k, v in block_mult.items():
            mult[k] += v
            mult_list[k].append(v)
        for k, v in block_avg.items():
            avg[k].append(v)

    for s, m in modules.items():
        if not m or m not in M:
            continue
        mod = M[m]
        apply(mod["add_stats"], mod["multiply_stats"], mod["add_average_stats"])
        for r, v in mod.get("build_cost_resources", {}).items():
            resources[r] += v
        if mission:
            for mt in mod["mission_type_stats"]:
                if mission in mt["missions"]:
                    if use_single and naval_cat and mission in NAVAL_MISSIONS and mod["category"] != naval_cat \
                            and ("naval_strike_attack" in mt["add_stats"]):
                        continue
                    apply(mt["add_stats"], mt["multiply_stats"], mt["add_average_stats"])

    keys = set(base) | set(add) | set(avg) | set(mult)
    out = {}
    for k in keys:
        v = base[k] + add[k]
        if avg.get(k):
            if AVERAGE_MODE == "all_mean":
                vals = avg[k] + ([base[k]] if k in A["stats"] else [])
                v = add[k] + sum(vals) / len(vals)
            else:
                v += sum(avg[k]) / len(avg[k])
        if MULT_MODE == "product":
            f = 1.0
            for x in mult_list.get(k, []):
                f *= 1 + x
        else:
            f = 1 + mult[k]
        out[k] = v * f
    thrust, weight = out.get("thrust", 0.0), out.get("weight", 0.0)
    factor = define(db, "THRUST_WEIGHT_AGILITY_FACTOR", 0.5)
    bonus = factor * max(0.0, thrust - weight)
    if AGILITY_BONUS_STAGE == "after_mult":
        out["air_agility"] = out.get("air_agility", 0.0) + bonus
    else:
        out["air_agility"] = (base["air_agility"] + add["air_agility"] + bonus) * (1 + mult["air_agility"])
    errors = validate(db, A, modules)
    if weight > thrust + 1e-9:
        errors.append(f"poids ({weight:g}) > poussée ({thrust:g})" + (f" en mission {mission}" if mission else ""))
    return {
        "airframe": airframe_name,
        "mission": mission,
        "modules": modules,
        "types": design_types(db, A, modules),
        "missions": allowed_missions(db, A, modules),
        "stats": {k: round(v, 4) for k, v in sorted(out.items())},
        "agility_bonus_from_thrust": round(bonus, 3),
        "resources": {k: v for k, v in resources.items() if v},
        "valid": not errors,
        "errors": errors,
        "year": A.get("year"),
        "module_years": {s: (M[m].get("year") if m in M else None) for s, m in modules.items() if m},
    }


def compute_all_missions(db: dict, airframe_name: str, modules: dict) -> dict:
    """Stats du designer (sans mission) puis pour chaque mission permise."""
    res = {"designer": compute(db, airframe_name, modules, None)}
    for ms in res["designer"]["missions"]:
        res[ms] = compute(db, airframe_name, modules, ms)
    return res


# --------------------------------------------------------------------------
# Affichage
# --------------------------------------------------------------------------
def fmt(v: float) -> str:
    return f"{v:.3g}" if abs(v) < 10 else f"{v:.1f}".rstrip("0").rstrip(".")


def generic_of_design(db: dict, airframe: str, types: list) -> tuple[dict | None, str | None]:
    """Avion générique (ancien système) de référence pour ce design : celui que le jeu
    associe à la cellule du rôle du design (derived_variant_name / variant_name)."""
    A, G = db["airframes"], db.get("generic_planes", {})
    base = A[airframe].get("duplicate_of") or airframe
    role = types[0] if types else A[airframe].get("type")
    for a in A.values():
        if (a["name"] == base or a.get("duplicate_of") == base) and a.get("type") == role and a.get("generic_ref") in G:
            return G[a["generic_ref"]], a.get("generic_ref_how")
    return None, None


def print_design(db: dict, title: str, airframe: str, modules: dict, file=sys.stdout):
    allm = compute_all_missions(db, airframe, modules)
    d = allm["designer"]
    A = db["airframes"][airframe]
    print(f"\n### {title}", file=file)
    print(f"Cellule : {airframe} ({A.get('loc_name') or '-'}, {A.get('year')}) — type(s) : {', '.join(map(str, d['types']))}", file=file)
    for s, m in modules.items():
        if m and m not in ("empty",):
            mm = db["modules"].get(m, {})
            print(f"  {s:32} {m:34} {mm.get('loc_name') or ''} ({mm.get('year') or '?'})", file=file)
    cols = ["designer"] + [m for m in allm if m != "designer"]
    stats = [s for s in DISPLAY_STATS if any(abs(allm[c]["stats"].get(s, 0)) > 1e-9 for c in cols)]
    gen, how = generic_of_design(db, airframe, d["types"])
    head = f"{'stat':24}" + "".join(f"{c[:14]:>15}" for c in cols) + (f"{'| ' + gen['name'][:13]:>17}" if gen else "")
    print(head, file=file)
    for s in stats:
        gv = gen["stats"].get(s) if gen else None
        gcol = (f"{'| ' + fmt(gv):>17}" if gv is not None else f"{'| —':>17}") if gen else ""
        print(f"{STAT_FR.get(s, s)[:24]:24}" + "".join(f"{fmt(allm[c]['stats'].get(s, 0)):>15}" for c in cols) + gcol, file=file)
    if gen:
        print(f"référence générique : {gen['name']} ({gen.get('year')}, lien {how}) — stats de base, sans améliorations", file=file)
    print(f"bonus d'agilité dû à la poussée (designer) : +{d['agility_bonus_from_thrust']:g}", file=file)
    if d["resources"]:
        print("ressources : " + ", ".join(f"{k} {v:g}" for k, v in d["resources"].items()), file=file)
    for c in cols:
        if allm[c]["errors"]:
            print(f"  ⚠ {c} : " + " ; ".join(allm[c]["errors"]), file=file)


def parse_assignments(items: list[str]) -> dict:
    mods = {}
    for it in items:
        if "=" not in it:
            sys.exit(f"argument invalide (attendu slot=module) : {it}")
        s, m = it.split("=", 1)
        mods[s.strip()] = m.strip()
    return mods


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("assign", nargs="*", help="slot=module")
    ap.add_argument("--db", help="air_db.json (défaut : <plugin>/data/air_db_vanilla.json)")
    ap.add_argument("--type", help="cellule (type d'équipement), ex. small_plane_airframe_2")
    ap.add_argument("--mission", help="ne calculer que cette mission")
    ap.add_argument("--history", metavar="TAG", help="calcule les designs historiques d'un pays (ou ALL)")
    ap.add_argument("--ai", metavar="GROUPE", help="calcule les gabarits d'un groupe IA (modules exacts seulement)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    db = load_db(a.db)

    if a.history:
        hs = [h for h in db["history_designs"] if a.history == "ALL" or h["country"] == a.history]
        if a.json:
            print(json.dumps([dict(h, result=compute_all_missions(db, h["type"], h["modules"])) for h in hs], ensure_ascii=False, indent=1))
        else:
            for h in hs:
                ctx = " / ".join(h.get("context", [])) or "sans condition"
                print_design(db, f"{h['country']} — {h['name']} [{ctx}]", h["type"], h["modules"])
        return 0
    if a.ai:
        g = db["ai_designs"].get(a.ai)
        if not g:
            sys.exit(f"groupe IA inconnu : {a.ai}. Groupes : {', '.join(db['ai_designs'])}")
        for dn, d in g["designs"].items():
            mods = {s: v for s, v in d["modules"].items() if isinstance(v, str) and v in db["modules"] or v == "empty"}
            if d["type"] not in db["airframes"]:
                print(f"\n### {dn} : type {d['type']} hors designer (ou catégorie de slot), ignoré")
                continue
            print_design(db, f"IA {a.ai} — {dn} (modules imposés uniquement)", d["type"], mods)
        return 0
    if not a.type:
        ap.print_help()
        return 1
    mods = parse_assignments(a.assign)
    if a.json:
        res = compute(db, a.type, mods, a.mission) if a.mission else compute_all_missions(db, a.type, mods)
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print_design(db, "Design", a.type, mods)
    return 0


if __name__ == "__main__":
    try:  # sortie tronquée par | head : pas de trace d'erreur
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())

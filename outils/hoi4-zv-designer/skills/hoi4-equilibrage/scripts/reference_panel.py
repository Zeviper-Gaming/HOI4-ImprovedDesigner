#!/usr/bin/env python3
"""
reference_panel.py - Panel de référence d'équilibrage : un mélange
  1. des AVIONS GÉNÉRIQUES d'avant le designer (fighter_equipment_2…),
  2. de MODÈLES PERMIS PAR LE DESIGNER VANILLA :
       - designs historiques des pays (create_equipment_variant, faits par les développeurs),
       - gabarits de l'IA (common/ai_equipment), complétés comme l'IA le ferait,
  3. et, en option, de designs ajoutés par Florian (--extra).

Les modèles sont regroupés par RÔLE (fighter, cas, naval_bomber, heavy_fighter,
tactical_bomber, strategic_bomber…), FAMILLE de cellule (small, cv_small, medium,
large) et PALIER (0 à 5). Pour chaque groupe et chaque stat, on obtient une
fourchette vanilla (min / médiane / max) et la valeur du générique : c'est
l'« enveloppe de référence » qui dit si un design s'écarte de l'équilibre du jeu.

    python3 reference_panel.py                                  # résumé de tous les groupes
    python3 reference_panel.py --role fighter --family small --tier 2 --members
    python3 reference_panel.py --md ../references/panel-vanilla.md
    python3 reference_panel.py --extra mes_designs.txt          # ajoute des designs de Florian
    python3 reference_panel.py --db mod_db.json --json panel.json

Format de --extra : texte Paradox, un ou plusieurs blocs
    create_equipment_variant = { name = "Mon chasseur" type = small_plane_airframe_2
        modules = { fixed_main_weapon_slot = heavy_mg_4x engine_type_slot = engine_3_1x } }
(même syntaxe que dans common/history/countries).

Chaque stat est mesurée dans la mission où elle sert (attaque sol en appui
rapproché, bombardement en mission stratégique, stats navales en frappe navale,
le reste dans la mission principale du rôle), seulement si le design peut voler
cette mission.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "scripts"))  # scripts partagés du plugin
import plane_calc as pc  # noqa: E402

PANEL_STATS = ["maximum_speed", "air_agility", "air_attack", "air_defence", "air_range", "air_ground_attack",
               "air_bombing", "naval_strike_attack", "naval_strike_targetting", "reliability", "build_cost_ic"]
ROLE_MISSION = {"fighter": "air_superiority", "heavy_fighter": "air_superiority", "interceptor": "interception",
                "cas": "cas", "naval_bomber": "naval_bomber", "tactical_bomber": "cas",
                "strategic_bomber": "strategic_bomber", "maritime_patrol_plane": "naval_bomber",
                "scout_plane": "recon", "suicide": "naval_kamikaze"}
STAT_MISSION = {"air_ground_attack": "cas", "air_bombing": "strategic_bomber",
                "naval_strike_attack": "naval_bomber", "naval_strike_targetting": "naval_bomber"}
ROLE_ORDER = ["fighter", "heavy_fighter", "cas", "naval_bomber", "tactical_bomber", "strategic_bomber",
              "maritime_patrol_plane", "scout_plane", "suicide"]


# --------------------------------------------------------------------------
def family_tier(db, airframe):
    a = db["airframes"][airframe]
    base = a.get("duplicate_of") or airframe
    arch = db["airframes"].get(base, a).get("archetype") or a.get("archetype") or ""
    fam = next((f for f in ("cv_small", "small", "medium", "large") if arch.startswith(f + "_plane")), None)
    m = re.search(r"_(\d+)$", base)
    return fam, (int(m.group(1)) if m else None), base


def measure(db, airframe, modules, role):
    """Stats du design, chaque stat dans la mission où elle sert."""
    A = db["airframes"][airframe]
    allowed = pc.allowed_missions(db, A, modules)
    base_m = ROLE_MISSION.get(role)
    if base_m not in allowed:
        base_m = None
    cache, out, valid = {}, {}, True
    for k in PANEL_STATS:
        m = STAT_MISSION.get(k, base_m)
        if m and m not in allowed:
            continue
        if m not in cache:
            cache[m] = pc.compute(db, airframe, modules, m)
        r = cache[m]
        if not r["valid"]:
            valid = False
            continue
        out[k] = r["stats"].get(k, 0.0)
    return out, valid


# --------------------------------------------------------------------------
def complete_ai_design(db, d):
    """Gabarit IA -> design concret : modules imposés, puis slots restants remplis
    avec allowed_modules dans l'ordre de préférence (comme l'IA, en approximation).
    Renvoie None si une exigence n'est pas un module concret (catégorie, comparaison)."""
    M, A = db["modules"], db["airframes"]
    if d["type"] not in A:
        return None
    af = A[d["type"]]
    mods = {}
    for s, v in d["modules"].items():
        if s not in af["slots"]:
            return None
        if isinstance(v, str) and (v in M or v == "empty"):
            mods[s] = None if v == "empty" else v
        else:
            return None
    for s, info in af["slots"].items():
        if s in mods:
            continue
        mods[s] = None
        for cand in d["allowed_modules"]:
            cands = [cand] if cand in M else [m for m, mm in M.items() if mm["category"] == cand]
            placed = False
            for c in cands:
                if M[c]["category"] not in info.get("categories", []):
                    continue
                trial = dict(mods)
                trial[s] = c
                r = pc.compute(db, d["type"], trial, None)
                hard = [e for e in r["errors"] if "obligatoire" not in e]
                if not hard:
                    mods[s] = c
                    placed = True
                    break
            if placed:
                break
    return mods


def load_extra(path):
    sys.path.insert(0, str(HERE.parents[2] / "scripts"))
    from pdx import load_file  # noqa
    from extract_air import find_variants  # noqa
    root = load_file(path)
    found = []
    find_variants(root, found, [])
    for v in found:
        v["country"] = "FLORIAN"
    return found


# --------------------------------------------------------------------------
def build_panel(db, extra=None):
    members = []
    for h in db["history_designs"] + (extra or []):
        if h["type"] not in db["airframes"]:
            continue
        r = pc.compute(db, h["type"], h["modules"], None)
        role = (r["types"] or [db["airframes"][h["type"]].get("type")])[0]
        fam, tier, base = family_tier(db, h["type"])
        stats, valid = measure(db, h["type"], {s: (None if m == "empty" else m) for s, m in h["modules"].items()}, role)
        members.append({"source": "ajout Florian" if h.get("country") == "FLORIAN" else "historique",
                        "name": f"{h.get('country', '')} {h.get('name') or ''}".strip(),
                        "airframe": h["type"], "base": base, "family": fam, "tier": tier, "role": role,
                        "modules": h["modules"], "stats": stats, "valid": valid,
                        "context": " / ".join(h.get("context", []))})
    for g, grp in db["ai_designs"].items():
        for dn, d in grp["designs"].items():
            mods = complete_ai_design(db, d)
            if mods is None:
                continue
            r = pc.compute(db, d["type"], mods, None)
            role = (r["types"] or [db["airframes"][d["type"]].get("type")])[0]
            fam, tier, base = family_tier(db, d["type"])
            stats, valid = measure(db, d["type"], mods, role)
            members.append({"source": "IA", "name": f"{g}/{dn}", "airframe": d["type"], "base": base,
                            "family": fam, "tier": tier, "role": role, "modules": mods,
                            "stats": stats, "valid": valid, "context": ""})
    return members


def generic_for_group(db, fam, tier, role):
    A, G = db["airframes"], db.get("generic_planes", {})
    for a in A.values():
        if a["is_archetype"]:
            continue
        f, t, _ = family_tier(db, a["name"])
        if f == fam and t == tier and a.get("type") == role and a.get("generic_ref") in G:
            return G[a["generic_ref"]], a.get("generic_ref_how")
    return None, None


def summarise(db, members):
    groups = {}
    for m in members:
        if not m["valid"]:
            continue
        groups.setdefault((m["role"], m["family"], m["tier"]), []).append(m)
    out = {}
    for key, ms in groups.items():
        role, fam, tier = key
        gen, how = generic_for_group(db, fam, tier, role)
        st = {}
        for k in PANEL_STATS:
            vals = [m["stats"][k] for m in ms if k in m["stats"]]
            if not vals:
                continue
            gv = gen["stats"].get(k) if gen else None
            genv = gen.get("envelope", {}).get(k) if gen else None
            st[k] = {"min": min(vals), "med": statistics.median(vals), "max": max(vals), "n": len(vals),
                     "generic": gv, "generic_ceiling": genv or gv,
                     # enveloppe combinée : le plus haut entre le meilleur modèle vanilla et le générique amélioré
                     "envelope_max": max([x for x in (max(vals), genv or gv) if x is not None])}
        out[key] = {"role": role, "family": fam, "tier": tier, "n": len(ms),
                    "generic": gen["name"] if gen else None, "generic_how": how,
                    "sources": sorted({m["source"] for m in ms}), "stats": st,
                    "members": [m["name"] for m in ms]}
    return out


def group_key_for(db, airframe, role):
    fam, tier, _ = family_tier(db, airframe)
    return (role, fam, tier)


# --------------------------------------------------------------------------
def fmtv(v):
    return "—" if v is None else (f"{v:.3g}" if abs(v) < 10 else f"{v:.0f}")


def render_md(db, summary, members, version):
    order = {r: i for i, r in enumerate(ROLE_ORDER)}
    fam_order = {"small": 0, "cv_small": 1, "medium": 2, "large": 3, None: 9}
    L = [f"# Panel de référence vanilla — version {version}", "",
         "Généré par `scripts/reference_panel.py`. Décision de Florian (14/10/2026) : la référence d'équilibrage mélange "
         "les **avions génériques** d'avant le designer et des **modèles permis par le designer vanilla** "
         "(designs historiques des pays, gabarits de l'IA complétés comme l'IA le ferait). Pour chaque rôle, famille "
         "et palier : fourchette des modèles vanilla (min · médiane · max), valeur du générique (base → plafond amélioré), "
         "et **enveloppe** = le plus haut des deux maximums. Un design qui dépasse l'enveloppe s'écarte de l'équilibre du jeu.",
         "",
         f"{sum(1 for m in members if m['valid'])} modèles valides : "
         f"{sum(1 for m in members if m['valid'] and m['source'] == 'historique')} historiques, "
         f"{sum(1 for m in members if m['valid'] and m['source'] == 'IA')} gabarits IA"
         + (f", {sum(1 for m in members if m['valid'] and m['source'] == 'ajout Florian')} ajoutés par Florian" if any(m['source'] == 'ajout Florian' for m in members) else "")
         + ". Gabarits IA dont une exigence n'est pas un module précis (catégorie, comparaison `>`, `any_of`) : non retenus.", ""]
    stats_show = [k for k in PANEL_STATS if k != "reliability"]
    for key in sorted(summary, key=lambda k: (order.get(k[0], 99), fam_order.get(k[1], 9), k[2] if k[2] is not None else 9)):
        g = summary[key]
        role, fam, tier = key
        L += [f"## {role} — {fam}, palier {tier} ({g['n']} modèles : {', '.join(g['sources'])})", "",
              f"Générique : {g['generic'] or 'aucun'}" + (f" ({g['generic_how']})" if g['generic'] else ""), "",
              "| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |", "|---|---|---|---|---|---|"]
        for k in stats_show:
            s = g["stats"].get(k)
            if not s:
                continue
            gen = f"{fmtv(s['generic'])} → {fmtv(s['generic_ceiling'])}" if s["generic"] is not None else "—"
            L.append(f"| {pc.STAT_FR.get(k, k)} | {fmtv(s['min'])} | {fmtv(s['med'])} | {fmtv(s['max'])} | {gen} | **{fmtv(s['envelope_max'])}** |")
        names = g["members"]
        L += ["", "Modèles : " + ", ".join(names[:25]) + (f" … (+{len(names) - 25})" if len(names) > 25 else ""), ""]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db")
    ap.add_argument("--extra", action="append", default=[], help="fichier de designs ajoutés (create_equipment_variant)")
    ap.add_argument("--role")
    ap.add_argument("--family", choices=["small", "cv_small", "medium", "large"])
    ap.add_argument("--tier", type=int)
    ap.add_argument("--members", action="store_true", help="liste les modèles du groupe avec leurs stats")
    ap.add_argument("--md")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    db = pc.load_db(a.db)
    extra = []
    for e in a.extra:
        extra += load_extra(e)
    members = build_panel(db, extra)
    summary = summarise(db, members)
    if a.md:
        Path(a.md).write_text(render_md(db, summary, members, db["meta"].get("game_version")), encoding="utf-8")
        print(f"Écrit {a.md}")
    if a.json:
        Path(a.json).write_text(json.dumps({"summary": {"|".join(map(str, k)): v for k, v in summary.items()},
                                            "members": members}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Écrit {a.json}")
    if a.md or a.json:
        return 0
    for key, g in sorted(summary.items(), key=lambda kv: (ROLE_ORDER.index(kv[0][0]) if kv[0][0] in ROLE_ORDER else 99, str(kv[0][1]), kv[0][2] or 0)):
        role, fam, tier = key
        if (a.role and role != a.role) or (a.family and fam != a.family) or (a.tier is not None and tier != a.tier):
            continue
        print(f"\n== {role} / {fam} / palier {tier} — {g['n']} modèles ({', '.join(g['sources'])}) — générique {g['generic']}")
        for k in ["maximum_speed", "air_agility", "air_attack", "air_defence", "air_range", "air_ground_attack",
                  "air_bombing", "naval_strike_attack", "build_cost_ic"]:
            s = g["stats"].get(k)
            if s:
                print(f"  {pc.STAT_FR.get(k, k):22} {fmtv(s['min']):>6} · {fmtv(s['med']):>6} · {fmtv(s['max']):>6}"
                      f"   générique {fmtv(s['generic']):>6} → {fmtv(s['generic_ceiling']):>6}   enveloppe {fmtv(s['envelope_max'])}")
        if a.members:
            for m in members:
                if m["valid"] and (m["role"], m["family"], m["tier"]) == key:
                    mods = ", ".join(v for v in m["modules"].values() if v and v != "empty")
                    print(f"    [{m['source']}] {m['name']} ({m['airframe']}) : {mods}")
    return 0


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())

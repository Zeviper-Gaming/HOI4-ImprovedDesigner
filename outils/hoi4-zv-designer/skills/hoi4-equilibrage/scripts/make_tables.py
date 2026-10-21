#!/usr/bin/env python3
"""
make_tables.py - Génère les tableaux de référence (Markdown) des stats du
designer d'avions à partir d'une base air_db.json.

    python3 make_tables.py                          # vanilla -> stdout
    python3 make_tables.py --out ../references/tables-vanilla.md
    python3 make_tables.py --db mod_air_db.json --out tables-mod.md

Tableaux produits :
  1. Cellules par famille et palier (stats de base, coût, poids, slots)
  2. Moteurs : poussée, coût, carburant, multiplicateurs, par palier
  3. Modules par catégorie : stats permanentes et stats de mission, coût, poids,
     année et technologie
  4. Ratios d'efficacité par catégorie (stat principale par IC et par poids)
  5. Avions génériques d'avant le designer (référence) et correspondance cellule → générique
  6. Designs historiques BBA rapportés à leur générique (changements d'échelle)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plane_calc as pc  # noqa: E402

FAMILY_ORDER = ["small_plane_airframe", "cv_small_plane_airframe", "medium_plane_airframe", "large_plane_airframe"]
PRIMARY = {  # stat principale par catégorie (pour les ratios)
    "fighter_weapon": ("air_attack", None),
    "cas_weapon": ("air_ground_attack", "cas"),
    "tac_weapon": ("air_ground_attack", "cas"),
    "strat_weapon": ("air_bombing", "strategic_bomber"),
    "nav_bomber_weapon": ("naval_strike_attack", "naval_bomber"),
    "plane_special_module_defense_turret": ("air_defence", None),
    "plane_special_module_defense_turret_x2": ("air_defence", None),
}


def f(v):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


def stat_str(d: dict, pct=False) -> str:
    if not d:
        return ""
    return ", ".join(f"{k} {'+' if v > 0 else ''}{v * 100:g}%" if pct else f"{k} {v:+g}" for k, v in d.items())


def mission_str(m: dict) -> str:
    parts = []
    for mt in m.get("mission_type_stats", []):
        bits = []
        if mt["add_stats"]:
            bits.append(stat_str(mt["add_stats"]))
        if mt["multiply_stats"]:
            bits.append(stat_str(mt["multiply_stats"], pct=True))
        if mt["add_average_stats"]:
            bits.append("moy. " + stat_str(mt["add_average_stats"]))
        parts.append(f"[{'/'.join(mt['missions'])}] " + "; ".join(bits))
    return " · ".join(parts)


def airframe_table(db) -> list[str]:
    A = db["airframes"]
    out = ["## 1. Cellules (stats de base)", "",
           "Stats de la cellule seule, avant modules. Les doublons (CAS, naval, chasseur lourd, reconnaissance, "
           "patrouille maritime) reprennent les stats de la cellule source.", ""]
    cols = ["year", "maximum_speed", "air_agility", "air_defence", "air_range", "weight", "build_cost_ic", "reliability"]
    out.append("| Cellule | Nom | " + " | ".join(["Année", "Vitesse", "Agilité", "Défense", "Portée", "Poids", "IC", "Fiab."]) + " | Slots (fixes+libres) | Tech |")
    out.append("|---" * (len(cols) + 4) + "|")
    fams = FAMILY_ORDER + sorted({a["archetype"] for a in A.values() if not a["duplicate_of"]} - set(FAMILY_ORDER))
    for fam in fams:
        for n, a in sorted(A.items(), key=lambda x: (x[1].get("year") or 0, x[0])):
            if a["archetype"] != fam or a["is_archetype"] or a["duplicate_of"]:
                continue
            s = a["stats"]
            fixed = sum(1 for x in a["slots"].values() if x["kind"] == "fixed")
            vals = [f(a.get("year"))] + [f(s.get(c)) for c in cols[1:]]
            out.append(f"| `{n}` | {a.get('loc_name') or ''} | " + " | ".join(vals) +
                       f" | {fixed}+{len(a['slots']) - fixed} | {', '.join(a.get('techs', [])) or '—'} |")
    return out


def engine_table(db) -> list[str]:
    M = db["modules"]
    out = ["", "## 2. Moteurs", "",
           "Poussée et coût additionnés ; `maximum_speed` multiplicatif (additionné aux autres multiplicateurs).", "",
           "| Module | Nom | Catégorie | Année | Poussée | IC | Carburant | Multiplicateurs | Ressources | Poussée/IC |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    engines = [m for m in M.values() if "engine" in (m["category"] or "")]
    engines.sort(key=lambda m: (m["category"], m.get("year") or 0, m["name"]))
    for m in engines:
        a = m["add_stats"]
        thr, ic = a.get("thrust", 0), a.get("build_cost_ic", 0)
        out.append(f"| `{m['name']}` | {m.get('loc_name') or ''} | {m['category']} | {f(m.get('year'))} | {f(thr)} | {f(ic)} | "
                   f"{f(a.get('fuel_consumption'))} | {stat_str(m['multiply_stats'], pct=True)} | {stat_str(m['build_cost_resources'])} | "
                   f"{thr / ic:.2f} |" if ic else f"| `{m['name']}` | | {m['category']} | | {f(thr)} | 0 | | | | — |")
    return out


def module_tables(db) -> list[str]:
    M = db["modules"]
    C = db["categories"]
    out = ["", "## 3. Modules par catégorie", "",
           "Colonnes : stats permanentes (toujours actives), stats de mission (actives seulement pendant la mission indiquée, "
           "y compris le POIDS), coût en IC, année de la tech la plus précoce.", ""]
    for cat in sorted(C):
        mods = [m for m in M.values() if m["category"] == cat and "engine" not in cat]
        if not mods:
            continue
        mods.sort(key=lambda m: (m.get("year") or 0, m["name"]))
        out += [f"### {cat} — {C[cat].get('loc_name') or ''}", "",
                f"Slots qui l'acceptent : {', '.join(C[cat]['slots'])}", "",
                "| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |",
                "|---|---|---|---|---|---|---|---|---|"]
        for m in mods:
            out.append(f"| `{m['name']}` | {m.get('loc_name') or ''} | {f(m.get('year'))} | {', '.join(m.get('techs', [])) or '—'} | "
                       f"{stat_str(m['add_stats'])} | {stat_str(m['multiply_stats'], pct=True)} {('moy. ' + stat_str(m['add_average_stats'])) if m['add_average_stats'] else ''} | "
                       f"{mission_str(m)} | {', '.join(m['allow_mission_type'])} | {stat_str(m['build_cost_resources'])} |")
        out.append("")
    return out


def primary_value(m, stat, mission):
    v = m["add_stats"].get(stat, 0.0)
    w = m["add_stats"].get("weight", 0.0)
    ag = m["add_stats"].get("air_agility", 0.0)
    if mission:
        for mt in m["mission_type_stats"]:
            if mission in mt["missions"]:
                v += mt["add_stats"].get(stat, 0.0)
                w += mt["add_stats"].get("weight", 0.0)
                ag += mt["add_stats"].get("air_agility", 0.0)
    return v, w, ag


def ratio_tables(db) -> list[str]:
    M = db["modules"]
    out = ["", "## 4. Ratios d'efficacité", "",
           "Stat principale de la catégorie rapportée au coût (IC) et au poids, pour repérer un module hors courbe. "
           "Le poids et la pénalité d'agilité sont ceux de la mission où la stat compte.", ""]
    for cat, (stat, mission) in PRIMARY.items():
        mods = [m for m in M.values() if m["category"] == cat]
        rows = []
        for m in mods:
            v, w, ag = primary_value(m, stat, mission)
            if not v:
                continue
            ic = m["add_stats"].get("build_cost_ic", 0.0)
            rows.append((m.get("year") or 0, m["name"], v, ic, w, ag))
        if not rows:
            continue
        rows.sort()
        out += [f"### {cat} — {stat}" + (f" (mission {mission})" if mission else ""), "",
                "| Module | Année | Stat | IC | Poids | Agilité | Stat/IC | Stat/poids |", "|---|---|---|---|---|---|---|---|"]
        for y, n, v, ic, w, ag in rows:
            out.append(f"| `{n}` | {y or '—'} | {v:g} | {ic:g} | {w:g} | {ag:+g} | {v / ic:.2f} | " + (f"{v / w:.2f}" if w else "—") + " |" if ic else
                       f"| `{n}` | {y or '—'} | {v:g} | 0 | {w:g} | {ag:+g} | — | " + (f"{v / w:.2f}" if w else "—") + " |")
        out.append("")
    return out


GEN_COLS = [("year", "Année"), ("maximum_speed", "Vitesse"), ("air_agility", "Agilité"), ("air_attack", "Att. air"),
            ("air_defence", "Déf."), ("air_range", "Portée"), ("air_ground_attack", "Att. sol"),
            ("air_bombing", "Bomb."), ("naval_strike_attack", "Att. nav."), ("naval_strike_targetting", "Cibl. nav."),
            ("reliability", "Fiab."), ("build_cost_ic", "IC")]
ROLE_ORDER = ["fighter", "heavy_fighter", "cas", "naval_bomber", "tactical_bomber", "strategic_bomber",
              "scout_plane", "interceptor", "suicide"]
STAT_MISSION = {"air_ground_attack": "cas", "air_bombing": "strategic_bomber",
                "naval_strike_attack": "naval_bomber", "naval_strike_targetting": "naval_bomber"}
ROLE_MISSION = {"fighter": "air_superiority", "heavy_fighter": "air_superiority", "cas": "cas",
                "naval_bomber": "naval_bomber", "tactical_bomber": "cas", "strategic_bomber": "strategic_bomber"}


def generic_tables(db) -> list[str]:
    G = db.get("generic_planes", {})
    if not G:
        return []
    out = ["", "## 5. Avions génériques d'avant le designer (RÉFÉRENCE d'équilibrage)", "",
           "Décision de Florian (14/10/2026) : les valeurs de référence sont celles des avions génériques de l'ancien "
           "système (utilisés sans By Blood Alone), définis dans `x_plane_airframes.txt` et `intercontinental_bomber.txt`. "
           "Valeurs de base, sans améliorations. « Plafond amélioré » = toutes les améliorations qui augmentent la stat "
           "au niveau 5 (hypothèse : pourcentages additionnés).", "",
           "| Avion | Rôle | " + " | ".join(c[1] for c in GEN_COLS) + " | Plafond amélioré | Améliorations |",
           "|---|---|" + "---|" * len(GEN_COLS) + "---|---|"]
    order = {r: i for i, r in enumerate(ROLE_ORDER)}
    for g in sorted(G.values(), key=lambda g: (order.get(g.get("type"), 99), g["name"].startswith("cv_"), g.get("year") or 0, g["name"])):
        st = g["stats"]
        vals = [f(g.get("year")) if k == "year" else f(st.get(k)) for k, _ in GEN_COLS]
        env = ", ".join(f"{k} {v:g}" for k, v in g.get("envelope", {}).items())
        out.append(f"| `{g['name']}` | {g.get('type')} | " + " | ".join(vals) + f" | {env or '—'} | {', '.join(g.get('upgrades_resolved', [])) or '—'} |")
    out += ["", "Correspondance cellule → avion générique (officielle = donnée par le jeu dans `derived_variant_name` "
            "ou `variant_name` ; approchée = même rôle, année la plus proche) :", "",
            "| Cellule | Année | Rôle | Générique | Lien |", "|---|---|---|---|---|"]
    for n, a in sorted(db["airframes"].items(), key=lambda x: x[0]):
        if a["is_archetype"]:
            continue
        out.append(f"| `{n}` | {f(a.get('year'))} | {a.get('type')} | {a.get('generic_ref') or '—'} | {a.get('generic_ref_how') or 'aucun générique de ce rôle'} |")
    return out


def history_vs_generic(db) -> list[str]:
    import statistics
    A, G = db["airframes"], db.get("generic_planes", {})
    stats = ["maximum_speed", "air_agility", "air_attack", "air_defence", "air_range", "air_ground_attack",
             "air_bombing", "naval_strike_attack", "naval_strike_targetting", "build_cost_ic"]
    agg: dict = {}
    for h in db["history_designs"]:
        a = A.get(h["type"])
        if not a or "officielle" not in (a.get("generic_ref_how") or ""):
            continue
        g = G[a["generic_ref"]]
        base_m = ROLE_MISSION.get(a.get("type"))
        allowed = pc.allowed_missions(db, a, h["modules"])
        for k in stats:
            # chaque stat est mesurée dans la mission où elle sert, si le design la permet
            m = STAT_MISSION.get(k, base_m)
            if m and m not in allowed:
                continue
            r = pc.compute(db, h["type"], h["modules"], m)
            if not r["valid"] or not g["stats"].get(k):
                continue
            agg.setdefault(a["type"], {}).setdefault(k, []).append(r["stats"].get(k, 0) / g["stats"][k])
    if not agg:
        return []
    out = ["", "## 6. Designs historiques BBA rapportés à leur avion générique", "",
           "Médiane, par rôle, du rapport « stat du design historique / stat du générique officiellement associé à sa "
           "cellule », chaque stat étant mesurée dans la mission où elle sert (attaque sol en appui rapproché, bombardement en mission stratégique, stats navales en frappe navale), seulement pour les designs capables de cette mission. 1,00 = même niveau. Montre où le designer BBA a "
           "**changé d'échelle** par rapport à l'ancien système : sur ces stats, la référence générique ne peut pas "
           "être prise en valeur absolue sans recalibrer les modules.", "",
           "| Rôle | Designs | " + " | ".join(pc.STAT_FR.get(k, k) for k in stats) + " |",
           "|---|---|" + "---|" * len(stats)]
    order = {r: i for i, r in enumerate(ROLE_ORDER)}
    for role in sorted(agg, key=lambda r: order.get(r, 99)):
        d = agg[role]
        n = max(len(v) for v in d.values())
        cells = []
        for k in stats:
            v = d.get(k)
            cells.append(f"{statistics.median(v):.2f}" if v else "—")
        out.append(f"| {role} | {n} | " + " | ".join(cells) + " |")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    db = pc.load_db(a.db)
    lines = [f"# Tableaux de référence du designer d'avions — version {db['meta'].get('game_version')}", "",
             "Généré par `scripts/make_tables.py` à partir des fichiers du jeu. Ne pas éditer à la main : "
             "relancer le script après une mise à jour du jeu.", ""]
    lines += airframe_table(db) + engine_table(db) + module_tables(db) + ratio_tables(db) + generic_tables(db) + history_vs_generic(db)
    txt = "\n".join(lines) + "\n"
    if a.out:
        Path(a.out).write_text(txt, encoding="utf-8")
        print(f"Écrit {a.out} ({len(lines)} lignes)")
    else:
        print(txt)


if __name__ == "__main__":
    try:  # sortie tronquée par | head : pas de trace d'erreur
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    main()

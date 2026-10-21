#!/usr/bin/env python3
"""
balance_audit.py - Test "anti-cheat" du designer d'avions (décision de Florian :
garde-fous A « compromis explicites » + B « plafonds », les paliers de tech
bornant naturellement les modules disponibles par année).

    python3 balance_audit.py                       # toutes les cellules de base, rapport texte
    python3 balance_audit.py --airframe small_plane_airframe_2 --stat air_attack
    python3 balance_audit.py --db mod_air_db.json --compare <plugin>/data/audit_vanilla.json
    python3 balance_audit.py --md rapport.md       # rapport Markdown

Principe :
  - Pour chaque cellule et chaque stat-cible, une recherche en faisceau construit
    le design qui MAXIMISE la stat, avec les modules disponibles à l'année de la
    cellule (+ --grace), en respectant slots, limites et poussée ≥ poids.
  - RÉFÉRENCE PRINCIPALE = l'avion GÉNÉRIQUE d'avant le designer, du même rôle que
    le design obtenu (fighter_equipment_2, CAS_equipment_2…), relié à la cellule
    par le jeu lui-même (derived_variant_name / variant_name) ou, à défaut, par
    l'année la plus proche. Deux niveaux : sa valeur de base, et son « plafond
    amélioré » (toutes les améliorations qui augmentent la stat au niveau 5).
  - Le PANEL DE RÉFÉRENCE mêle ces génériques et des modèles permis par le designer
    vanilla (designs historiques, gabarits IA complétés, designs ajoutés via --extra).
  - Le meilleur design historique de la cellule reste affiché (référence secondaire).

Drapeaux :
  ⚠ SANS-CONTREPARTIE (garde-fou A) : la stat-cible dépasse le générique de plus
               de --tolerance (défaut 15 %) alors qu'aucune autre stat suivie du rôle
               n'est inférieure au générique de plus de --compensation (défaut 10 %)
               et que le coût en IC ne le dépasse pas de plus de --compensation.
  ⚠ HORS-ENVELOPPE (garde-fou B) : la stat-cible dépasse de plus de --tolerance
               l'ENVELOPPE DE RÉFÉRENCE du rôle, de la famille et du palier :
               max(meilleur modèle vanilla — designs historiques et gabarits IA —,
               générique au plafond amélioré). Panel : reference_panel.py.
  ⓘ PLAFOND-GÉNÉRIQUE : dépasse le seul générique amélioré (information : le
               designer vanilla le fait souvent, cf. tables-vanilla.md §6).
  ⓘ ENVELOPPE-COMME-VANILLA : (avec --compare) hors enveloppe, mais le designer
               vanilla permet déjà le même dépassement et le mod ne l'aggrave pas
               de plus de --tolerance. À traiter seulement si Florian veut
               resserrer le vanilla (plafonds sur les EMPILEMENTS).
  ⓘ EMPILEMENT (garde-fou B) : le design maximisé répète un module qui sert la
               stat-cible : candidat à un module_count_limit.
  ⚠ DOMINANT   : le design maximisé égale ou bat le meilleur design historique de
               la cellule sur toutes les stats suivies, pour un coût ≤.
  ⚠ VANILLA+   : (avec --compare) la valeur max du mod dépasse celle du vanilla sur
               la même cellule de plus de --tolerance. L'audit vanilla est fourni
               pré-calculé : --compare <plugin>/data/audit_vanilla.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plane_calc as pc  # noqa: E402
import reference_panel as rp  # noqa: E402

# stat-cible -> mission dans laquelle on la mesure
TARGETS = {
    "air_attack": "air_superiority",
    "air_agility": "air_superiority",
    "maximum_speed": "air_superiority",
    "air_defence": None,
    "air_range": None,
    "air_ground_attack": "cas",
    "naval_strike_attack": "naval_bomber",
    "air_bombing": "strategic_bomber",
}
# stats suivies pour le test de dominance, par mission
TRACKED = {
    "air_superiority": ["air_attack", "air_agility", "maximum_speed", "air_defence", "air_range", "reliability"],
    "cas": ["air_ground_attack", "air_agility", "maximum_speed", "air_defence", "air_range", "reliability"],
    "naval_bomber": ["naval_strike_attack", "naval_strike_targetting", "air_agility", "maximum_speed", "air_defence", "air_range"],
    "strategic_bomber": ["air_bombing", "air_defence", "maximum_speed", "air_range", "air_agility"],
    None: ["air_attack", "air_agility", "maximum_speed", "air_defence", "air_range"],
}


def available_modules(db, airframe, year_max):
    """slot -> [modules utilisables] (+ None si le slot n'est pas obligatoire)."""
    M = db["modules"]
    res = {}
    for s, info in airframe["slots"].items():
        opts = [m for m, mod in M.items()
                if mod["category"] in info.get("categories", [])
                and (mod.get("year") is None and mod.get("techs") or (mod.get("year") or 9999) <= year_max)]
        if not info.get("required"):
            opts.append(None)
        res[s] = opts
    return res


def _score(db, airframe_name, d, stat, mission, cost_weight, engine_slots):
    r = pc.compute(db, airframe_name, d, mission)
    hard = [e for e in r["errors"] if "obligatoire" not in e and "poids" not in e]
    if hard:
        return None, r
    st = r["stats"]
    score = st.get(stat, 0.0) - cost_weight * st.get("build_cost_ic", 0.0)
    # la contrainte poussée >= poids n'a de sens qu'une fois le moteur choisi
    if any(d.get(s) for s in engine_slots):
        over = max(0.0, st.get("weight", 0) - st.get("thrust", 0))
        score -= 1000 * over
    # le design doit pouvoir voler la mission où la stat est mesurée
    A = db["airframes"][airframe_name]
    if mission and all(d.get(s) for s, i in A["slots"].items() if i.get("required")) \
            and mission not in r["missions"]:
        score -= 1e6
    return score, r


def beam_search(db, airframe_name, stat, mission, year_max, width=120, cost_weight=1e-3, seeds=()):
    """Recherche en faisceau slot par slot (moteur d'abord), puis amélioration
    locale (échange d'un module à la fois) à partir des meilleurs designs
    trouvés ET des designs de référence fournis en `seeds`."""
    A = db["airframes"][airframe_name]
    opts = available_modules(db, A, year_max)
    engine_slots = [s for s, info in A["slots"].items()
                    if any("engine" in c for c in info.get("categories", []))]
    slots = engine_slots + sorted([s for s in opts if s not in engine_slots], key=lambda s: len(opts[s]))
    beam = [dict()]
    for s in slots:
        scored, seen = [], set()
        for partial in beam:
            for m in opts[s]:
                d = dict(partial)
                d[s] = m
                sig = tuple(sorted((k, v or "") for k, v in d.items()))
                if sig in seen:
                    continue
                seen.add(sig)
                sc, _ = _score(db, airframe_name, d, stat, mission, cost_weight, engine_slots)
                if sc is not None:
                    scored.append((sc, d))
        scored.sort(key=lambda x: -x[0])
        beam = [d for _, d in scored[:width]] or beam

    def full(d):
        return {s: d.get(s) for s in A["slots"]}

    starts = [full(d) for d in beam[:5]]
    for sd in seeds:
        if all(s in A["slots"] for s in sd):
            starts.append(full({s: (None if m in ("empty", None) else m) for s, m in sd.items()}))

    def valid_score(d):
        sc, r = _score(db, airframe_name, d, stat, mission, cost_weight, engine_slots)
        if sc is None or not r["valid"]:
            return None, r
        return sc, r

    best, best_sc = None, None
    for d in starts:
        sc, r = valid_score(d)
        cur = dict(d)
        improved = True
        while improved:
            improved = False
            for s in A["slots"]:
                for m in opts[s]:
                    if m == cur.get(s):
                        continue
                    t = dict(cur)
                    t[s] = m
                    sc2, r2 = valid_score(t)
                    if sc2 is not None and (sc is None or sc2 > sc + 1e-9):
                        cur, sc, r, improved = t, sc2, r2, True
        if sc is not None and (best_sc is None or sc > best_sc):
            best, best_sc = r, sc
    return best


def reference_designs(db, airframe_name):
    """Designs historiques sur cette cellule, ou sur la cellule source si c'est un doublon."""
    A = db["airframes"][airframe_name]
    names = {airframe_name}
    for n, a in db["airframes"].items():
        if a.get("duplicate_of") == airframe_name:
            names.add(n)
    return [h for h in db["history_designs"] if h["type"] in names]


def best_reference(db, airframe_name, stat, mission):
    best = None
    for h in reference_designs(db, airframe_name):
        A = db["airframes"].get(h["type"])
        ms = pc.allowed_missions(db, A, h["modules"])
        if mission and mission not in ms:
            continue
        r = pc.compute(db, h["type"], h["modules"], mission)
        if not r["valid"]:
            continue
        r["ref_name"] = f"{h['country']} {h['name']}"
        if best is None or r["stats"].get(stat, 0) > best["stats"].get(stat, 0):
            best = r
    return best


def dominates(maxd, ref, mission):
    if not maxd or not ref:
        return False
    tr = TRACKED.get(mission, TRACKED[None])
    s1, s2 = maxd["stats"], ref["stats"]
    if s1.get("build_cost_ic", 0) > s2.get("build_cost_ic", 0) + 1e-9:
        return False
    if not all(s1.get(k, 0) >= s2.get(k, 0) - 1e-9 for k in tr):
        return False
    # au moins une amélioration stricte (sinon c'est le design de référence lui-même)
    strictly = any(s1.get(k, 0) > s2.get(k, 0) + 1e-6 for k in tr) or \
        s1.get("build_cost_ic", 0) < s2.get("build_cost_ic", 0) - 1e-6
    return strictly


# rôle de référence selon la famille de cellule et la mission où la stat est mesurée
MISSION_ROLE = {
    ("small", "air_superiority"): "fighter", ("small", "cas"): "cas", ("small", "naval_bomber"): "naval_bomber",
    ("cv_small", "air_superiority"): "fighter", ("cv_small", "cas"): "cas", ("cv_small", "naval_bomber"): "naval_bomber",
    ("medium", "air_superiority"): "heavy_fighter", ("medium", "cas"): "tactical_bomber",
    ("medium", "naval_bomber"): "tactical_bomber", ("medium", "strategic_bomber"): "tactical_bomber",
    ("large", "strategic_bomber"): "strategic_bomber", ("large", "naval_bomber"): "maritime_patrol_plane",
    ("large", "cas"): "strategic_bomber", ("large", "air_superiority"): "strategic_bomber",
}


def family(db, airframe_name):
    arch = db["airframes"][airframe_name].get("archetype") or ""
    for f in ("cv_small", "small", "medium", "large"):
        if arch.startswith(f + "_plane"):
            return f
    return None


def reference_role(db, airframe_name, mission, maxd):
    """Rôle de l'avion générique servant de référence : fixé par la mission de la
    stat-cible (une stat navale se compare à un bombardier naval, pas au chasseur
    lourd que serait le design s'il garde une mitrailleuse en slot principal)."""
    r = MISSION_ROLE.get((family(db, airframe_name), mission))
    if r:
        return r
    return (maxd.get("types") or [db["airframes"][airframe_name].get("type")])[0]


def generic_for(db, airframe_name, role):
    """Avion générique de référence pour un design de rôle `role` sur cette cellule."""
    A = db["airframes"]
    G = db.get("generic_planes", {})
    for a in A.values():
        if (a["name"] == airframe_name or a.get("duplicate_of") == airframe_name) \
                and a.get("type") == role and a.get("generic_ref") in G:
            return G[a["generic_ref"]], a.get("generic_ref_how")
    year = A[airframe_name].get("year") or 1936
    cands = [g for g in G.values() if g.get("type") == role and g.get("year")]
    if not cands:
        return None, None
    cands.sort(key=lambda g: (abs(g["year"] - year) + (0.5 if g["year"] > year else 0)))
    return cands[0], f"approchée (rôle {role}, année la plus proche)"


def compare_generic(maxd, gen, stat, mission, tol, comp):
    """Bilan du design maximisé face au générique : écarts relatifs par stat suivie."""
    tr = TRACKED.get(mission, TRACKED[None])
    gs, ms = gen["stats"], maxd["stats"]
    deltas = {}
    for k in set(tr) | {stat, "build_cost_ic"}:
        if gs.get(k):
            deltas[k] = ms.get(k, 0.0) / gs[k] - 1
    gain = deltas.get(stat)
    losses = {k: d for k, d in deltas.items() if k not in (stat, "build_cost_ic") and d < -comp}
    dearer = deltas.get("build_cost_ic", 0) > comp
    flags = []
    if gain is not None and gain > tol and not losses and not dearer:
        flags.append("SANS-CONTREPARTIE")
    ceiling = gen.get("envelope", {}).get(stat) or gs.get(stat)
    if ceiling and ms.get(stat, 0) > ceiling * (1 + tol) + 1e-9:
        flags.append("PLAFOND-GÉNÉRIQUE")
    return deltas, losses, ceiling, flags


def stacking(db, maxd, stat, mission):
    """Modules répétés qui servent la stat-cible (candidats à un plafond)."""
    M = db["modules"]
    counts = {}
    for m in maxd["modules"].values():
        if m:
            counts[m] = counts.get(m, 0) + 1
    out = []
    for m, n in counts.items():
        if n < 2 or m not in M:
            continue
        mod = M[m]
        contrib = mod["add_stats"].get(stat, 0) + mod["multiply_stats"].get(stat, 0)
        for mt in mod["mission_type_stats"]:
            if mission in mt["missions"]:
                contrib += mt["add_stats"].get(stat, 0) + mt["multiply_stats"].get(stat, 0)
        if contrib > 0:
            out.append(f"{m}×{n}")
    return out


def audit(db, airframes, stats, grace, width, ratio_max, tol=0.15, comp=0.10, panel=None):
    rows = []
    for an in airframes:
        A = db["airframes"][an]
        year = A.get("year") or 1936
        for stat in stats:
            mission = TARGETS[stat]
            seeds = [h["modules"] for h in reference_designs(db, an)]
            maxd = beam_search(db, an, stat, mission, year + grace, width, seeds=seeds)
            if maxd is None:
                continue
            if mission and mission not in maxd["missions"]:
                continue
            role = reference_role(db, an, mission, maxd)
            gen, how = generic_for(db, an, role)
            ref = best_reference(db, an, stat, mission)
            vmax = maxd["stats"].get(stat, 0)
            vref = ref["stats"].get(stat, 0) if ref else None
            ratio = (vmax / vref) if vref else None
            flags = []
            deltas, losses, ceiling, gflags = ({}, {}, None, [])
            if gen:
                deltas, losses, ceiling, gflags = compare_generic(maxd, gen, stat, mission, tol, comp)
                flags += gflags
            stack = stacking(db, maxd, stat, mission)
            if stack:
                flags.append("EMPILEMENT")
            if dominates(maxd, ref, mission):
                flags.append("DOMINANT")
            env = None
            if panel is not None:
                g = panel.get(rp.group_key_for(db, an, role))
                env = g["stats"].get(stat) if g else None
                if env is None and ceiling:
                    # aucun modèle vanilla dans ce groupe : l'enveloppe se réduit au générique amélioré
                    env = {"min": None, "med": None, "max": None, "n": 0, "generic": gen["stats"].get(stat) if gen else None,
                           "generic_ceiling": ceiling, "envelope_max": ceiling}
                if env and vmax > env["envelope_max"] * (1 + tol) + 1e-9:
                    flags.append("HORS-ENVELOPPE")
            gbase = gen["stats"].get(stat) if gen else None
            rows.append({
                "airframe": an, "year": year, "stat": stat, "mission": mission, "role": role,
                "max": vmax, "ref": vref, "ratio": ratio, "ref_name": ref.get("ref_name") if ref else None,
                "generic": gen["name"] if gen else None, "generic_how": how,
                "generic_base": gbase, "generic_ceiling": ceiling,
                "vanilla_panel": env,
                "ratio_generic": (vmax / gbase) if gbase else None,
                "deltas_vs_generic": deltas, "losses_vs_generic": losses, "stacking": stack,
                "max_design": maxd["modules"], "max_stats": maxd["stats"],
                "ref_stats": ref["stats"] if ref else None, "flags": flags,
            })
    return rows


def base_airframes(db):
    return [n for n, a in db["airframes"].items() if not a["is_archetype"] and not a.get("duplicate_of")
            and a.get("techs")]


def flag_vs_vanilla(rows, compare_rows, tol):
    """VANILLA+ si le mod dépasse le maximum atteignable en vanilla. Un HORS-ENVELOPPE
    que le vanilla présente déjà (et que le mod n'aggrave pas) devient une simple
    information : ENVELOPPE-COMME-VANILLA."""
    cmp = {(r["airframe"], r["stat"]): r for r in (compare_rows or [])}
    for r in rows:
        c = cmp.get((r["airframe"], r["stat"]))
        if c and c.get("max") and r["max"] > c["max"] * tol + 1e-9:
            r["flags"].append("VANILLA+")
            r["vanilla_max"] = c["max"]
        if c and "HORS-ENVELOPPE" in r["flags"] and "HORS-ENVELOPPE" in c.get("flags", []) \
                and "VANILLA+" not in r["flags"]:
            r["flags"] = [("ENVELOPPE-COMME-VANILLA" if f == "HORS-ENVELOPPE" else f) for f in r["flags"]]


def _pct(d):
    return f"{d * 100:+.0f} %"


def render(rows, db, compare_rows=None, md=False):
    out = []
    cmp = {(r["airframe"], r["stat"]): r for r in (compare_rows or [])}
    P = out.append
    cur = None
    for r in rows:
        if r["airframe"] != cur:
            cur = r["airframe"]
            A = db["airframes"][cur]
            P(f"\n## {cur} — {A.get('loc_name') or ''} ({r['year']})" if md else f"\n=== {cur} ({r['year']}) ===")
            if md:
                P("| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |")
                P("|---|---|---|---|---|---|---|---|---|")
        mods = ", ".join(f"{m}" for m in r["max_design"].values() if m)
        gen = (f"{r['generic']} {r['generic_base']:.4g} → {r['generic_ceiling']:.4g}"
               if r.get("generic") and r.get("generic_base") is not None and r.get("generic_ceiling") else
               (f"{r['generic']} (stat absente)" if r.get("generic") else "—"))
        rg = f"{r['ratio_generic']:.2f}" if r.get("ratio_generic") else "—"
        hist = f"{r['ref']:.4g} ({r['ratio']:.2f})" if r["ref"] is not None and r["ratio"] else "—"
        c = cmp.get((r["airframe"], r["stat"]))
        van = f"{c['max']:.4g}" if c and c.get("max") is not None else "—"
        flags = " ".join(("ⓘ" if f in ("EMPILEMENT", "PLAFOND-GÉNÉRIQUE", "DOMINANT", "ENVELOPPE-COMME-VANILLA") else "⚠") + f for f in r["flags"])
        if r.get("stacking"):
            flags += " (" + ", ".join(r["stacking"]) + ")"
        losses = ", ".join(f"{pc.STAT_FR.get(k, k)} {_pct(d)}" for k, d in sorted(r.get("losses_vs_generic", {}).items())) or "aucune"
        vp = r.get("vanilla_panel")
        vps = (f"{vp['min']:.4g} · {vp['med']:.4g} · {vp['max']:.4g} ({vp['n']})" if vp and vp.get("n")
               else ("aucun modèle (générique seul)" if vp else "—"))
        envs = f"{vp['envelope_max']:.4g}" if vp else "—"
        if md:
            P(f"| {pc.STAT_FR.get(r['stat'], r['stat'])} | {r.get('role') or '—'} | {r['max']:.4g} | {vps} | {gen} | **{envs}** | {flags} | {losses} | {mods} |")
        else:
            P(f"{pc.STAT_FR.get(r['stat'], r['stat']):22} [{r.get('role')}] max {r['max']:.4g}   enveloppe {envs}"
              f"   modèles vanilla {vps}   générique {gen}"
              + (f"   max vanilla audité {van}" if c else "") + (f"   {flags}" if flags else ""))
            P(f"    design : {mods}")
            P(f"    pertes vs générique (> seuil) : {losses}")
            d = r.get("deltas_vs_generic") or {}
            if d:
                P("    écarts vs générique : " + ", ".join(f"{pc.STAT_FR.get(k, k)} {_pct(v)}" for k, v in sorted(d.items())))
            if r["ref_name"]:
                P(f"    meilleur design historique : {r['ref_name']} ({hist})")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db")
    ap.add_argument("--compare", help="référence : une base air_db (audit recalculé) ou un audit JSON déjà calculé, ex. <plugin>/data/audit_vanilla.json (instantané)")
    ap.add_argument("--airframe", action="append", help="cellule(s) à auditer (défaut : toutes les cellules de base)")
    ap.add_argument("--stat", action="append", choices=list(TARGETS), help="stat(s)-cible(s)")
    ap.add_argument("--grace", type=int, default=0, help="années d'avance tolérées sur les modules (défaut 0)")
    ap.add_argument("--width", type=int, default=120, help="largeur du faisceau (défaut 120)")
    ap.add_argument("--ratio-max", type=float, default=2.0, help="(information) ratio max / historique jugé élevé")
    ap.add_argument("--tolerance", type=float, default=0.15,
                    help="dépassement toléré du générique (A, B) et du vanilla (VANILLA+), en fraction (défaut 0.15)")
    ap.add_argument("--compensation", type=float, default=0.10,
                    help="perte minimale (fraction) sur une autre stat, ou surcoût IC, pour compter comme contrepartie (défaut 0.10)")
    ap.add_argument("--panel-db", help="base servant au panel de référence (défaut : vanilla du plugin)")
    ap.add_argument("--extra", action="append", default=[], help="designs de référence ajoutés au panel (create_equipment_variant)")
    ap.add_argument("--md", help="écrit un rapport Markdown")
    ap.add_argument("--json", help="écrit les résultats bruts en JSON")
    a = ap.parse_args(argv)
    db = pc.load_db(a.db)
    afs = a.airframe or base_airframes(db)
    stats = a.stat or list(TARGETS)
    vdb = pc.load_db(a.panel_db) if a.panel_db else pc.load_db(None)
    extra = []
    for e in a.extra:
        extra += rp.load_extra(e)
    panel = rp.summarise(vdb, rp.build_panel(vdb, extra))
    rows = audit(db, afs, stats, a.grace, a.width, a.ratio_max, a.tolerance, a.compensation, panel)
    crow = None
    if a.compare:
        raw = json.loads(Path(a.compare).read_text(encoding="utf-8"))
        if isinstance(raw, list):
            crow = raw  # résultats d'audit déjà calculés (ex. data/audit_vanilla.json)
        else:
            crow = audit(raw, [x for x in afs if x in raw["airframes"]], stats, a.grace, a.width, a.ratio_max, a.tolerance, a.compensation, panel)
    if crow:
        flag_vs_vanilla(rows, crow, 1 + a.tolerance)
    txt = render(rows, db, crow, md=bool(a.md))
    if a.md:
        head = f"# Audit d'équilibrage — version {db['meta'].get('game_version')}\n\n" \
               f"Modules disponibles jusqu'à l'année de la cellule + {a.grace} an(s), plus ceux des designs historiques " \
               f"de la cellule (servent d'amorces). Faisceau {a.width}.\n\n" \
               f"Référence (décision de Florian) : mélange des avions génériques d'avant le designer et des modèles vanilla " \
               f"(designs historiques, gabarits IA) du même rôle, famille et palier. Enveloppe = max(meilleur modèle vanilla, " \
               f"générique amélioré). Tolérance {a.tolerance:.0%}, contrepartie minimale {a.compensation:.0%}.\n"
        Path(a.md).write_text(head + txt + "\n", encoding="utf-8")
        print(f"Rapport écrit : {a.md}")
    else:
        print(txt)
    if a.json:
        Path(a.json).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    flagged = [r for r in rows if r["flags"]]
    print(f"\n{len(rows)} combinaisons auditées, {len(flagged)} drapeau(x).")
    return 0


if __name__ == "__main__":
    try:  # sortie tronquée par | head : pas de trace d'erreur
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())

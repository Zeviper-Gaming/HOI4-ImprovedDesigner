#!/usr/bin/env python3
"""
extract_air.py - Extrait du jeu (ou d'un mod) toute la matière du designer d'avions
dans une base JSON unique, réutilisée par les autres scripts (et par le skill
hoi4-equilibrage).

    python3 extract_air.py --ref "<dossier HOI4 ou HOI4-ref>" --out air_db.json
    python3 extract_air.py --ref <vanilla> --mod <dossier du mod> --out air_db.json

Avec --mod, les fichiers du mod sont chargés APRÈS ceux du jeu, comme le fait
HOI4 : un fichier du mod de même chemin relatif remplace celui du jeu, un objet
de même nom dans un autre fichier écrase la définition précédente (et c'est
signalé dans `warnings`).

Contenu de la base :
  modules      : chaque module d'avion (stats, catégorie, missions, coûts,
                 conversions, tech qui le débloque, année, nom localisé)
  categories   : catégories de modules -> modules, slots qui les acceptent
  airframes    : cellules (archétypes et types), stats de base RÉSOLUES
                 (archétype + type), slots, limites, modules par défaut
  techs        : technologies (année, coût, équipements et modules débloqués)
  ai_designs   : gabarits IA (common/ai_equipment/*planes*)
  history_designs : designs historiques (create_equipment_variant)
  generic_planes : avions génériques de l'ancien système (référence d'équilibrage)
                 + plane_upgrades (leurs améliorations) ; chaque cellule porte
                 generic_ref / generic_ref_how
  defines      : constantes NAir utiles au designer
  warnings     : incohérences relevées pendant l'extraction
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdx import Block, Entry, load_defines, load_file, load_localisation, num  # noqa: E402

STAT_BLOCKS = ("add_stats", "multiply_stats", "add_average_stats")
PLANE_MODULE_FILE_HINT = "plane"
AIRFRAME_FILES = (
    "plane_airframes.txt",
    "x_plane_airframes.txt",
    "quad_engine_airframe.txt",
    "single_engine_airframe.txt",
    "twin_engine_airframe.txt",
    "intercontinental_bomber.txt",
)
NON_STAT_KEYS = {
    "year", "is_archetype", "is_buildable", "priority", "archetype", "parent", "is_frame",
    "type", "ai_type", "upgrades", "can_be_produced", "can_be_lend_leased", "module_slots",
    "module_count_limit", "default_modules", "resources", "is_convertable", "picture",
    "allowed_types", "allow_mission_type", "forbid_mission_type", "group_by", "sprite",
    "air_map_icon_frame", "interface_category", "substitute", "interface_overview_category_index",
    "abbreviation", "derived_variant_name", "type_override", "variant_name", "only_duplicate_archetype",
    "for_each", "alias", "default_carrier_composition_weight", "max_military_factories",
    "lend_lease_cost", "manpower", "build_cost_ic", "fuel_consumption", "can_convert_from",
    "reliability",
}
# lend_lease_cost/manpower/build_cost_ic/fuel_consumption/reliability sont des stats
# "de production" : on les garde dans `base` mais on les liste à part.
PRODUCTION_KEYS = ("build_cost_ic", "fuel_consumption", "reliability", "manpower", "lend_lease_cost")


# --------------------------------------------------------------------------
# Fichiers : superposition jeu + mod
# --------------------------------------------------------------------------
def layered_files(roots: list[Path], rel_dir: str, pattern: str = "*.txt") -> list[tuple[Path, str]]:
    """Fichiers de `rel_dir` pour chaque racine. Un fichier d'une racine plus
    tardive (le mod) de même nom remplace celui d'une racine antérieure.
    Retourne [(chemin, origine)] triés par nom de fichier (ordre de chargement)."""
    chosen: dict[str, tuple[Path, str]] = {}
    for i, root in enumerate(roots):
        d = root / rel_dir
        if not d.is_dir():
            continue
        origin = "vanilla" if i == 0 else "mod"
        for f in d.glob(pattern):
            chosen[f.name] = (f, origin)
    return [chosen[k] for k in sorted(chosen)]


def rel(path: Path, roots: list[Path]) -> str:
    for r in roots:
        try:
            return str(path.relative_to(r)).replace("\\", "/")
        except ValueError:
            pass
    return str(path)


def stats_of(b) -> dict:
    if not isinstance(b, Block):
        return {}
    return {k: num(v) for k, v in b.items() if isinstance(v, str)}


# --------------------------------------------------------------------------
# Modules
# --------------------------------------------------------------------------
def parse_module(name: str, b: Block, src: str, dlc: str | None) -> dict:
    m: dict = {
        "name": name,
        "file": src,
        "line": b.line,
        "dlc_limit": dlc,
        "category": b.get("category"),
        "parent": b.get("parent"),
        "abbreviation": b.get("abbreviation"),
        "gui_category": b.get("gui_category"),
        "xp_cost": num(b.get("xp_cost"), None) if b.get("xp_cost") else None,
        "dismantle_cost_ic": num(b.get("dismantle_cost_ic"), None) if b.get("dismantle_cost_ic") else None,
    }
    for sb in STAT_BLOCKS:
        m[sb] = stats_of(b.get(sb))
    m["build_cost_resources"] = stats_of(b.get("build_cost_resources"))
    m["dismantle_cost_resources"] = stats_of(b.get("dismantle_cost_resources"))
    am = b.get("allow_mission_type")
    m["allow_mission_type"] = am.values() if isinstance(am, Block) else ([am] if am else [])
    aet = b.get("add_equipment_type")
    m["add_equipment_type"] = aet.values() if isinstance(aet, Block) else ([aet] if aet else [])
    fmc = b.get("forbid_module_categories")
    m["forbid_module_categories"] = fmc.values() if isinstance(fmc, Block) else []
    fet = b.get("forbid_equipment_type_exact_match_for_category")
    m["forbid_equipment_type_exact_match_for_category"] = dict(fet.items()) if isinstance(fet, Block) else {}
    mts = []
    for blk in b.get_all("mission_type_stats"):
        if not isinstance(blk, Block):
            continue
        lim = blk.get("limit")
        entry = {"missions": lim.values() if isinstance(lim, Block) else []}
        for sb in STAT_BLOCKS:
            entry[sb] = stats_of(blk.get(sb))
        mts.append(entry)
    m["mission_type_stats"] = mts
    convs = []
    for blk in b.get_all("can_convert_from"):
        if isinstance(blk, Block):
            convs.append({
                "module": blk.get("module"),
                "module_category": blk.get("module_category"),
                "convert_cost_ic": num(blk.get("convert_cost_ic"), None) if blk.get("convert_cost_ic") else None,
            })
    m["can_convert_from"] = convs
    known = {"category", "parent", "abbreviation", "gui_category", "xp_cost", "dismantle_cost_ic", "sfx",
             "allow_mission_type", "add_equipment_type", "forbid_module_categories",
             "forbid_equipment_type_exact_match_for_category", "mission_type_stats", "can_convert_from",
             "build_cost_resources", "dismantle_cost_resources", *STAT_BLOCKS}
    m["other_keys"] = sorted(set(b.keys()) - known)
    return m


def load_modules(roots, warnings) -> dict[str, dict]:
    mods: dict[str, dict] = {}
    for f, origin in layered_files(roots, "common/units/equipment/modules"):
        root = load_file(f)
        for w in getattr(root, "warnings", []):
            warnings.append(w)
        for em in root.get_all("equipment_modules"):
            if not isinstance(em, Block):
                continue
            dlc = None
            lim = em.get("limit")
            if isinstance(lim, Block):
                dlc = lim.get("has_dlc")
            for name, b in em.blocks():
                if name == "limit":
                    continue
                cat = b.get("category") or ""
                # on ne garde que les modules d'avion : catégorie qui contient plane/fighter/bomb/...
                m = parse_module(name, b, rel(f, roots), dlc)
                m["origin"] = origin
                if name in mods:
                    warnings.append(f"module '{name}' redéfini dans {m['file']} (déjà dans {mods[name]['file']}) : la dernière définition gagne")
                mods[name] = m
    return mods


# --------------------------------------------------------------------------
# Équipements (cellules)
# --------------------------------------------------------------------------
def parse_slots(b) -> dict | str | None:
    if b is None:
        return None
    if isinstance(b, str):
        return b  # 'inherit' ou 'none'
    slots = {}
    for e in b.entries:
        if e.key is None:
            continue
        if isinstance(e.value, Block):
            cats = e.value.get("allowed_module_categories")
            slots[e.key] = {
                "required": e.value.get("required") == "yes",
                "categories": cats.values() if isinstance(cats, Block) else [],
                "kind": "fixed" if e.key.startswith("fixed_") else "custom",
            }
        else:
            slots[e.key] = {"same_as": e.value, "kind": "fixed" if e.key.startswith("fixed_") else "custom"}
    return slots


def parse_limits(b: Block) -> list[dict]:
    out = []
    for blk in b.get_all("module_count_limit"):
        if not isinstance(blk, Block):
            continue
        lim: dict = {"match": []}
        for e in blk.entries:
            if e.key in ("module", "category"):
                lim["match"].append({e.key: e.value})
            elif e.key == "count":
                lim["op"], lim["count"] = e.op, e.value
            elif e.key == "title":
                lim["title"] = e.value
        out.append(lim)
    return out


def parse_equipment(name: str, b: Block, src: str) -> dict:
    eq: dict = {"name": name, "file": src, "line": b.line}
    for k in ("year", "archetype", "parent", "type", "ai_type", "type_override", "abbreviation",
              "derived_variant_name", "sprite", "picture", "substitute", "alias", "group_by"):
        v = b.get(k)
        if v is not None:
            eq[k] = v.values() if isinstance(v, Block) else v
    eq["is_archetype"] = b.get("is_archetype") == "yes"
    eq["is_buildable"] = b.get("is_buildable") != "no"
    eq["module_slots"] = parse_slots(b.get("module_slots"))
    eq["module_count_limit"] = parse_limits(b)
    dm = b.get("default_modules")
    eq["default_modules"] = dict(dm.items()) if isinstance(dm, Block) else {}
    at = b.get("allowed_types")
    eq["allowed_types"] = at.values() if isinstance(at, Block) else []
    am = b.get("allow_mission_type")
    eq["allow_mission_type"] = am.values() if isinstance(am, Block) else ([am] if am else [])
    fm = b.get("forbid_mission_type")
    eq["forbid_mission_type"] = fm.values() if isinstance(fm, Block) else ([fm] if fm else [])
    eq["resources"] = stats_of(b.get("resources"))
    up = b.get("upgrades")
    eq["upgrades"] = up.values() if isinstance(up, Block) else []
    base = {}
    for k, v in b.items():
        if isinstance(v, str) and (k not in NON_STAT_KEYS or k in PRODUCTION_KEYS):
            try:
                base[k] = float(v)
            except ValueError:
                pass
    eq["stats"] = base
    fe = b.get("for_each")
    if isinstance(fe, Block):
        eq["for_each"] = {k: dict(v.items()) for k, v in fe.blocks()}
    vn = b.get("variant_name")
    if isinstance(vn, Block):
        eq["variant_name"] = dict(vn.items())
    return eq


def load_equipment(roots, warnings):
    """Charge toutes les définitions d'équipement des fichiers d'avions,
    plus duplicate_archetypes. Retourne (equipments, duplicates)."""
    equipments: dict[str, dict] = {}
    duplicates: dict[str, dict] = {}
    for f, origin in layered_files(roots, "common/units/equipment"):
        root = load_file(f)
        for w in getattr(root, "warnings", []):
            warnings.append(w)
        src = rel(f, roots)
        for eqs in root.get_all("equipments"):
            if not isinstance(eqs, Block):
                continue
            for name, b in eqs.blocks():
                eq = parse_equipment(name, b, src)
                eq["origin"] = origin
                if name in equipments:
                    warnings.append(f"équipement '{name}' redéfini dans {src} (déjà dans {equipments[name]['file']})")
                equipments[name] = eq
        for dup in root.get_all("duplicate_archetypes"):
            if not isinstance(dup, Block):
                continue
            for name, b in dup.blocks():
                d = parse_equipment(name, b, src)
                d["origin"] = origin
                d["only_duplicate_archetype"] = b.get("only_duplicate_archetype") == "yes"
                d["module_slots_none"] = b.get("module_slots") == "none"
                duplicates[name] = d
    return equipments, duplicates


def is_plane_equipment(eq: dict, equipments: dict) -> bool:
    arch = eq["name"] if eq.get("is_archetype") else eq.get("archetype")
    if not arch:
        return False
    a = equipments.get(arch, {})
    return "plane" in arch or a.get("sprite", "").endswith("plane") or "airframe" in arch


def resolve_airframes(equipments: dict, duplicates: dict, warnings: list) -> dict[str, dict]:
    """Construit les cellules du designer : types avec module_slots (directs ou
    hérités), stats = archétype puis type (le type écrase l'archétype).
    Ajoute les types générés par duplicate_archetypes."""
    out: dict[str, dict] = {}

    def slots_of(name, seen=()):
        eq = equipments.get(name)
        if eq is None or name in seen:
            return None
        s = eq["module_slots"]
        if isinstance(s, dict):
            # résoudre les alias "slot = autre_slot" et "slot = inherit"
            res = {}
            for k, v in s.items():
                if "same_as" in v:
                    if v["same_as"] == "inherit":
                        src = eq.get("parent") or eq.get("archetype")
                        ps = slots_of(src, seen + (name,)) or {}
                        if k in ps:
                            res[k] = dict(ps[k])
                    elif v["same_as"] in res:
                        res[k] = dict(res[v["same_as"]], kind="fixed" if k.startswith("fixed_") else "custom")
                else:
                    res[k] = v
            return res
        if s == "inherit":
            return slots_of(eq.get("parent") or eq.get("archetype"), seen + (name,))
        return None

    def limits_of(name, seen=()):
        eq = equipments.get(name)
        if eq is None or name in seen:
            return []
        inherited = []
        for src in (eq.get("archetype"), eq.get("parent")):
            if src and src != name:
                inherited = merge_limits(inherited, limits_of(src, seen + (name,)))
        return merge_limits(inherited, eq["module_count_limit"])

    for name, eq in equipments.items():
        if not is_plane_equipment(eq, equipments):
            continue
        slots = slots_of(name)
        if not slots:
            continue
        arch_name = name if eq["is_archetype"] else eq.get("archetype")
        arch = equipments.get(arch_name, {})
        stats = dict(arch.get("stats", {}))
        if not eq["is_archetype"]:
            stats.update(eq["stats"])
        out[name] = {
            "name": name,
            "file": eq["file"],
            "line": eq["line"],
            "origin": eq.get("origin"),
            "is_archetype": eq["is_archetype"],
            "archetype": arch_name,
            "duplicate_of": None,
            "parent": eq.get("parent"),
            "year": int(num(eq.get("year") or arch.get("year"), 0)) or None,
            "type": eq.get("type") or arch.get("type"),
            "allowed_types": arch.get("allowed_types", []),
            "type_override": arch.get("type_override"),
            "derived_variant_name": eq.get("derived_variant_name"),
            "stats": stats,
            "resources": eq["resources"] or arch.get("resources", {}),
            "slots": slots,
            "module_count_limit": limits_of(name),
            "default_modules": eq["default_modules"] or arch.get("default_modules", {}),
            "allow_mission_type": arch.get("allow_mission_type", []),
            "forbid_mission_type": arch.get("forbid_mission_type", []),
        }

    # types générés par duplicate_archetypes : <nouvel_arch>_<suffixe>
    for dname, d in duplicates.items():
        src_arch = d.get("archetype")
        # only_duplicate_archetype = archétypes hérités du système non-BBA : pas de types enfants
        if not src_arch or d.get("module_slots_none") or d.get("only_duplicate_archetype"):
            continue
        for tname, t in list(out.items()):
            if t["archetype"] != src_arch or t["duplicate_of"]:
                continue
            if t["is_archetype"]:
                new_name = dname
            elif tname.startswith(src_arch + "_"):
                new_name = dname + tname[len(src_arch):]
            else:
                continue
            if new_name in out:
                continue
            nt = json.loads(json.dumps(t))
            nt.update({
                "name": new_name,
                "archetype": dname,
                "duplicate_of": tname,
                "type": d.get("type") or t["type"],
                "file": d["file"],
                "line": d["line"],
                "origin": d.get("origin"),
                "forbid_mission_type": d.get("forbid_mission_type") or t["forbid_mission_type"],
            })
            if d.get("ai_type"):
                nt["ai_type"] = d["ai_type"]
            for stat, op in d.get("for_each", {}).items():
                if "set" in op:
                    nt["stats"][stat] = num(op["set"])
            out[new_name] = nt
    return out


def merge_limits(parent: list[dict], child: list[dict]) -> list[dict]:
    """Une limite héritée est remplacée par une limite de l'enfant ayant
    exactement les mêmes conditions (doc officielle)."""
    key = lambda l: json.dumps(sorted(json.dumps(m, sort_keys=True) for m in l["match"]))
    res = {key(l): l for l in parent}
    for l in child:
        res[key(l)] = l
    return list(res.values())


# --------------------------------------------------------------------------
# Avions génériques d'avant le designer (référence d'équilibrage)
# --------------------------------------------------------------------------
GENERIC_STATS = ("maximum_speed", "air_range", "air_agility", "air_attack", "air_defence", "air_ground_attack",
                 "air_bombing", "naval_strike_attack", "naval_strike_targetting", "surface_detection",
                 "sub_detection", "reliability", "build_cost_ic", "fuel_consumption", "air_superiority", "manpower")


def load_generic_planes(equipments: dict, duplicates: dict, airframes: dict) -> dict[str, dict]:
    """Avions « fixes » de l'ancien système (fighter_equipment_1, CAS_equipment_2…),
    utilisés sans le DLC By Blood Alone. Stats propres de l'équipement, sans les
    améliorations (upgrades)."""
    plane_arches = {a["archetype"] for a in airframes.values()} | set(duplicates)
    out = {}
    for n, eq in equipments.items():
        if n in airframes or eq["is_archetype"] or not eq.get("archetype"):
            continue
        arch = eq["archetype"]
        if arch not in plane_arches:
            continue
        typ = eq.get("type") or duplicates.get(arch, {}).get("type") or equipments.get(arch, {}).get("type")
        out[n] = {
            "name": n, "file": eq["file"], "line": eq["line"], "origin": eq.get("origin"),
            "year": int(num(eq.get("year"), 0)) or None, "archetype": arch,
            "type": typ if isinstance(typ, str) else (typ[0] if typ else None),
            "stats": {k: v for k, v in eq["stats"].items() if k in GENERIC_STATS},
            "resources": eq["resources"], "upgrades": eq.get("upgrades", []),
            "parent": eq.get("parent"),
        }
    return out


def link_generic(airframes: dict, duplicates: dict, generic: dict) -> None:
    """Associe chaque cellule à son avion générique : correspondance OFFICIELLE
    (derived_variant_name de la cellule, variant_name du doublon) ou, à défaut,
    APPROCHÉE (même type, année la plus proche, de préférence antérieure)."""
    for n, a in airframes.items():
        if a["is_archetype"]:
            continue
        ref, how = None, None
        if a.get("duplicate_of"):
            vn = duplicates.get(a["archetype"], {}).get("variant_name", {})
            if vn.get(n) in generic:
                ref, how = vn[n], "officielle (variant_name du doublon)"
        elif a.get("derived_variant_name") in generic:
            ref, how = a["derived_variant_name"], "officielle (derived_variant_name)"
        if ref is None:
            cands = [g for g in generic.values() if g["type"] == a.get("type") and g["year"]]
            if cands and a.get("year"):
                cands.sort(key=lambda g: (abs(g["year"] - a["year"]) + (0.5 if g["year"] > a["year"] else 0)))
                ref, how = cands[0]["name"], f"approchée (même type {a.get('type')}, année la plus proche)"
        a["generic_ref"] = ref
        a["generic_ref_how"] = how


def resolve_generic_upgrades(generic: dict, upgrades: dict) -> None:
    """Améliorations de chaque avion générique (héritées de la chaîne `parent`)
    et « enveloppe » par stat : valeur atteinte en poussant au niveau max
    TOUTES les améliorations qui augmentent cette stat (sans tenir compte de
    leurs malus sur d'autres stats). Hypothèse [reconstitué] : les niveaux
    d'amélioration s'additionnent en pourcentage de la valeur de base."""
    for g in generic.values():
        cur, seen = g, set()
        ups = g["upgrades"]
        while not ups and cur.get("parent") in generic and cur["parent"] not in seen:
            seen.add(cur["parent"])
            cur = generic[cur["parent"]]
            ups = cur["upgrades"]
        g["upgrades_resolved"] = ups
        env = {}
        for stat, base in g["stats"].items():
            if stat in ("reliability", "build_cost_ic", "fuel_consumption", "manpower"):
                continue
            bonus = sum(upgrades[u]["max_level"] * upgrades[u]["per_level"].get(stat, 0)
                        for u in ups if u in upgrades and upgrades[u]["per_level"].get(stat, 0) > 0)
            if bonus:
                env[stat] = round(base * (1 + bonus), 4)
        g["envelope"] = env


def load_upgrades(roots) -> dict[str, dict]:
    out = {}
    for f, origin in layered_files(roots, "common/units/equipment/upgrades"):
        root = load_file(f)
        up = root.get("upgrades")
        if not isinstance(up, Block):
            continue
        for n, b in up.blocks():
            if "plane" not in n:
                continue
            out[n] = {"max_level": int(num(b.get("max_level"), 0)),
                      "per_level": {k: num(v) for k, v in b.items() if isinstance(v, str) and k not in ("max_level", "cost")},
                      "cost": b.get("cost")}
    return out


# --------------------------------------------------------------------------
# Technologies
# --------------------------------------------------------------------------
def load_techs(roots, warnings) -> dict[str, dict]:
    techs: dict[str, dict] = {}
    for f, origin in layered_files(roots, "common/technologies"):
        root = load_file(f)
        src = rel(f, roots)
        tb = root.get("technologies")
        if not isinstance(tb, Block):
            continue
        for name, b in tb.blocks():
            if name.startswith("@"):
                continue
            ee = b.get("enable_equipments")
            em = b.get("enable_equipment_modules")
            path = [p.get("leads_to_tech") for p in b.get_all("path") if isinstance(p, Block)]
            cats = b.get("categories")
            folder = b.get("folder")
            techs[name] = {
                "name": name,
                "file": src,
                "line": b.line,
                "origin": origin,
                "start_year": int(num(b.get("start_year"), 0)) or None,
                "research_cost": num(b.get("research_cost"), None) if b.get("research_cost") else None,
                "enable_equipments": ee.values() if isinstance(ee, Block) else [],
                "enable_equipment_modules": em.values() if isinstance(em, Block) else [],
                "leads_to": [p for p in path if p],
                "categories": cats.values() if isinstance(cats, Block) else [],
                "folder": folder.get("name") if isinstance(folder, Block) else None,
                "has_allow": b.get("allow") is not None,
                "has_allow_branch": b.get("allow_branch") is not None,
                "is_special_project_tech": b.get("is_special_project_tech") == "yes",
            }
    return techs


# --------------------------------------------------------------------------
# IA et designs historiques
# --------------------------------------------------------------------------
def slot_requirements(mb: Block) -> dict:
    out = {}
    for e in mb.entries:
        if e.key is None:
            continue
        if isinstance(e.value, Block):
            out[e.key] = e.value.to_dict()
        else:
            out[e.key] = e.value if e.op == "=" else f"{e.op} {e.value}"
    return out


def load_ai_designs(roots, warnings) -> dict[str, dict]:
    groups = {}
    for f, origin in layered_files(roots, "common/ai_equipment"):
        root = load_file(f)
        src = rel(f, roots)
        for gname, g in root.blocks():
            if g.get("category") != "air":
                continue
            roles = g.get("roles")
            grp = {"file": src, "line": g.line, "origin": origin,
                   "roles": roles.values() if isinstance(roles, Block) else [],
                   "available_for": (g.get("available_for").values() if isinstance(g.get("available_for"), Block) else []),
                   "blocked_for": (g.get("blocked_for").values() if isinstance(g.get("blocked_for"), Block) else []),
                   "designs": {}}
            for dname, d in g.blocks():
                tv = d.get("target_variant")
                if not isinstance(tv, Block):
                    continue
                mods = tv.get("modules")
                allowed = d.get("allowed_modules")
                grp["designs"][dname] = {
                    "line": d.line,
                    "type": tv.get("type"),
                    "match_value": num(tv.get("match_value"), None) if tv.get("match_value") else None,
                    "modules": slot_requirements(mods) if isinstance(mods, Block) else {},
                    "allowed_modules": allowed.values() if isinstance(allowed, Block) else [],
                    "has_enable": d.get("enable") is not None,
                }
            groups[gname] = grp
    return groups


def find_variants(b: Block, out: list, ctx: list):
    for e in b.entries:
        if not isinstance(e.value, Block):
            continue
        if e.key == "create_equipment_variant":
            v = e.value
            mods = v.get("modules")
            out.append({
                "name": v.get("name"),
                "type": v.get("type"),
                "modules": dict(mods.items()) if isinstance(mods, Block) else {},
                "design_team": v.get("design_team"),
                "line": e.line,
                "context": list(ctx),
            })
        else:
            lim = e.value.get("limit") if e.key in ("if", "else_if") else None
            label = None
            if isinstance(lim, Block):
                dl = [x.value for x in lim.entries if x.key == "has_dlc"]
                nots = [x.value for x in lim.entries if x.key in ("NOT", "not") and isinstance(x.value, Block)]
                for n in nots:
                    dl += ["NOT " + y.value for y in n.entries if y.key == "has_dlc"]
                label = " & ".join(dl) if dl else None
            find_variants(e.value, out, ctx + ([label] if label else []) + (["else"] if e.key == "else" else []))


def load_history_designs(roots, airframes, warnings) -> list[dict]:
    out = []
    # Le jeu lit history/countries/ (racine du jeu) ; la copie HOI4-ref les range dans common/history/
    # (piège 16) : on lit les deux, le fichier d'une racine plus tardive (le mod) remplaçant l'autre.
    chosen: dict = {}
    for i, root in enumerate(roots):
        for d in ("common/history/countries", "history/countries"):
            for f in sorted((root / d).glob("*.txt")) if (root / d).is_dir() else []:
                chosen[f.name] = (f, "vanilla" if i == 0 else "mod")
    for f, origin in [chosen[k] for k in sorted(chosen)]:
        root = load_file(f)
        tag = f.name.split(" ")[0].split("-")[0].strip()
        found: list = []
        find_variants(root, found, [])
        for v in found:
            if v["type"] in airframes:
                v["country"] = tag
                v["file"] = rel(f, roots)
                out.append(v)
    return out


# --------------------------------------------------------------------------
# Assemblage
# --------------------------------------------------------------------------
def build(roots: list[Path], lang: str = "french") -> dict:
    warnings: list[str] = []
    all_modules = load_modules(roots, warnings)
    equipments, duplicates = load_equipment(roots, warnings)
    airframes = resolve_airframes(equipments, duplicates, warnings)
    generic = load_generic_planes(equipments, duplicates, airframes)
    link_generic(airframes, duplicates, generic)
    upgrades = load_upgrades(roots)
    resolve_generic_upgrades(generic, upgrades)
    techs = load_techs(roots, warnings)

    # modules utilisables par les cellules d'avion
    plane_cats = set()
    for a in airframes.values():
        for s in a["slots"].values():
            plane_cats.update(s.get("categories", []))
    modules = {k: v for k, v in all_modules.items() if v["category"] in plane_cats}
    # modules hors designer d'avions (chars, navires, ou catégorie qu'aucun slot n'accepte)
    other_modules = {k: {"category": v["category"], "origin": v.get("origin"), "file": v["file"], "line": v["line"]}
                     for k, v in all_modules.items() if k not in modules}

    # localisation
    loc: dict[str, str] = {}
    for root in roots:
        d = root / "localisation" / lang
        if d.is_dir():
            for f in sorted(d.rglob("*.yml")):
                loc.update(load_localisation(f))
        d2 = root / "localisation"
        if d2.is_dir():
            for f in sorted(d2.glob(f"*_l_{lang}.yml")):
                loc.update(load_localisation(f))

    def L(key):
        v = loc.get(key)
        # résolution simple des renvois $clé$
        for _ in range(3):
            if v and re.fullmatch(r"\$[A-Za-z0-9_.]+\$", v):
                v = loc.get(v.strip("$"), v)
        return v

    # techs -> modules / cellules
    mod_tech: dict[str, list] = {}
    eq_tech: dict[str, list] = {}
    for t in techs.values():
        for m in t["enable_equipment_modules"]:
            mod_tech.setdefault(m, []).append(t["name"])
        for e in t["enable_equipments"]:
            eq_tech.setdefault(e, []).append(t["name"])

    for name, m in modules.items():
        m["techs"] = mod_tech.get(name, [])
        years = [techs[t]["start_year"] for t in m["techs"] if techs[t]["start_year"]]
        m["year"] = min(years) if years else None
        m["loc_name"] = L(name)
        if not m["techs"]:
            warnings.append(f"module '{name}' ({m.get('origin')}) : aucune technologie lue ne le débloque (projet spécial, effet de focus, ou fichier manquant)")
    for name, a in airframes.items():
        a["techs"] = eq_tech.get(name, [])
        a["loc_name"] = L(name)

    categories: dict[str, dict] = {}
    for name, m in modules.items():
        c = categories.setdefault(m["category"], {"modules": [], "slots": set(), "loc_name": L(f"EQ_MOD_CAT_{m['category']}_TITLE")})
        c["modules"].append(name)
    for a in airframes.values():
        for sname, s in a["slots"].items():
            for c in s.get("categories", []):
                if c in categories:
                    categories[c]["slots"].add(sname)
                else:
                    categories.setdefault(c, {"modules": [], "slots": set(), "loc_name": L(f"EQ_MOD_CAT_{c}_TITLE")})["slots"].add(sname)
    for c in categories.values():
        c["slots"] = sorted(c["slots"])
        if not c["modules"]:
            pass

    plane_techs = {k: v for k, v in techs.items()
                   if v["enable_equipment_modules"] and any(m in modules for m in v["enable_equipment_modules"])
                   or any(e in airframes for e in v["enable_equipments"])}

    defines = {}
    for root in roots:
        p = root / "common" / "defines"
        if p.is_dir():
            for f in sorted(p.glob("*.lua")):
                for k, v in load_defines(f).items():
                    if k.startswith("NAir."):
                        defines[k] = v

    ai = load_ai_designs(roots, warnings)
    hist = load_history_designs(roots, airframes, warnings)

    return {
        "meta": {
            "roots": [str(r) for r in roots],
            "language": lang,
            "counts": {
                "modules": len(modules), "categories": len(categories), "airframes": len(airframes),
                "plane_techs": len(plane_techs), "ai_design_groups": len(ai), "history_designs": len(hist),
                "generic_planes": len(generic),
            },
        },
        "modules": modules,
        "other_modules": other_modules,
        "categories": categories,
        "airframes": airframes,
        "techs": plane_techs,
        "ai_designs": ai,
        "history_designs": hist,
        "generic_planes": generic,
        "plane_upgrades": upgrades,
        "defines": defines,
        "loc_slots": {k[len("EQ_MOD_SLOT_"):-len("_TITLE")]: L(k) for k in loc if k.startswith("EQ_MOD_SLOT_")},
        "warnings": warnings,
    }


def find_version(roots: list[Path]) -> str | None:
    for r in roots:
        for cand in (r / "launcher-settings.json", r / "launcher" / "launcher-settings.json"):
            if cand.is_file():
                try:
                    return json.loads(cand.read_text(encoding="utf-8-sig")).get("rawVersion")
                except Exception:
                    pass
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", required=True, help="dossier du jeu (ou copie HOI4-ref)")
    ap.add_argument("--mod", action="append", default=[], help="dossier de mod à superposer (répétable, dans l'ordre)")
    ap.add_argument("--lang", default="french")
    ap.add_argument("--out", default="air_db.json")
    a = ap.parse_args(argv)
    roots = [Path(a.ref)] + [Path(m) for m in a.mod]
    db = build(roots, a.lang)
    db["meta"]["game_version"] = find_version(roots)
    Path(a.out).write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    c = db["meta"]["counts"]
    print(f"Écrit {a.out} - version {db['meta']['game_version']} - " + ", ".join(f"{k}: {v}" for k, v in c.items()))
    if db["warnings"]:
        print(f"{len(db['warnings'])} avertissement(s) :")
        for w in db["warnings"][:40]:
            print("  -", w)
    return 0


if __name__ == "__main__":
    try:  # sortie tronquée par | head : pas de trace d'erreur
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())

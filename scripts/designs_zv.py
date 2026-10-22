"""Briques communes aux gabarits d'IA (gen_ai.py) et aux designs de départ (gen_history.py).

Une « recette » donne, pour chaque slot, soit un module précis, soit une catégorie (zv_cat_…),
soit une liste de modules par ordre de préférence. `build` en tire un design concret : pour une
catégorie ou une liste, le meilleur module débloqué par les techs données qui garde le design valide.
"""
import json
from pathlib import Path

import check_designs as C

ROOT = Path(__file__).resolve().parent.parent
RULES = C.Rules()
TECH_YEAR = {t["id"]: t["year"] for t in json.loads((ROOT / "data/techs.json").read_text(encoding="utf-8"))}


def year(mid):
    """Année du module (année de sa tech ; vanilla hors arbre du mod : 1936)."""
    return TECH_YEAR.get(RULES.module_tech.get(mid), 1936)


def members(item):
    """Modules possibles pour un élément de recette, du meilleur au moins bon."""
    if isinstance(item, (list, tuple)):
        return list(item)
    if item.startswith("zv_cat_"):
        mods = [m for m, v in RULES.modules.items() if v["category"] == item]
        return sorted(mods, key=lambda m: (-year(m), m))
    return [item]


def available(mid, techs):
    t = RULES.module_tech.get(mid)
    return techs is None or (t is not None and t in techs)


def build(eq_type, recipe, techs=None, unresearched=None):
    """Design concret {slot: module} ; ValueError si un slot ne trouve aucun module valide.
    Les slots sont remplis dans l'ordre de la recette : chaque choix est contrôlé avec les précédents.
    Si `unresearched` est une liste, un slot sans module débloqué prend quand même le meilleur module
    valide, et le slot est noté dans la liste (au lieu de l'erreur)."""
    design = {}
    for slot, item in recipe.items():
        for pass_techs in ([techs, None] if unresearched is not None else [techs]):
            for mid in members(item):
                if not available(mid, pass_techs):
                    continue
                trial = dict(design, **{slot: mid})
                errs = [e for e in RULES.check(eq_type, trial) if not e.startswith("slot obligatoire")
                        and "count > 0" not in e]
                if not errs:
                    design[slot] = mid
                    if pass_techs is None and techs is not None:
                        unresearched.append(mid)
                    break
            if slot in design:
                break
        else:
            raise ValueError(f"{eq_type} : aucun module valide pour {slot} = {item}")
    return design


def valid_members(eq_type, design, slot, item):
    """Modules d'un élément de recette que le designer accepterait dans `slot`, le reste du design
    étant fixé (pour savoir si une catégorie entière est sûre pour l'IA)."""
    ok = []
    for mid in members(item):
        trial = dict(design, **{slot: mid})
        if not RULES.check(eq_type, trial):
            ok.append(mid)
    return ok


def techs_for(design, eq_type):
    """Techs nécessaires à un design (modules et cellule) ; None pour un module de projet spécial."""
    need = {RULES.equipment_tech.get(RULES.resolve(eq_type)[1])}
    for m in design.values():
        need.add(RULES.module_tech.get(m))
    return need

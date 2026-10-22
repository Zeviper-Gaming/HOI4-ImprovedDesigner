"""Contrôle d'un design d'avion selon les règles du mod, lues dans les fichiers générés (mod/).

Ce que le designer vérifie, et que ce script refait avant d'aller en jeu :
  - chaque module est posé dans un slot de la cellule qui accepte sa catégorie ;
  - les slots obligatoires (required = yes) sont remplis ;
  - aucun module n'est d'une catégorie interdite par un autre (forbid_module_categories) ;
  - les limites module_count_limit de l'archétype, du palier et du doublon de rôle sont tenues
    (un palier ou un doublon remplace une limite de l'archétype qui porte les mêmes conditions) ;
  - le rôle posé correspond au type de la cellule (sinon le jeu range le design ailleurs).
Et, si on lui donne les techs d'un pays : chaque module et la cellule sont débloqués.

Utilisé par gen_history.py (designs de départ) et gen_ai.py (gabarits d'IA). En ligne de commande :
  python -X utf8 scripts/check_designs.py small_plane_airframe_1 zv_engine_v_1 zv_engine_config_nose_a …
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "outils/hoi4-zv-designer/scripts"))
from pdx import Block, load_file, num  # noqa: E402

MOD = ROOT / "mod"
EQ = MOD / "common/units/equipment"


def _limits(block):
    """module_count_limit d'un bloc : (conditions, opérateur, nombre)."""
    out = []
    for lim in block.get_all("module_count_limit"):
        conds = frozenset(f"{e.key}={e.value}" for e in lim if e.key in ("module", "category"))
        cnt = lim.get_entry("count")
        out.append((conds, cnt.op, int(num(cnt.value))))
    return out


def _merge(*levels):
    """Limites cumulées : un niveau plus précis remplace celle qui porte les mêmes conditions."""
    merged = {}
    for level in levels:
        for conds, op, n in level:
            merged[(conds, op)] = (conds, op, n)
    return list(merged.values())


class Rules:
    def __init__(self, ref=Path("F:/Github Local/HOI4-ref")):
        root = load_file(EQ / "plane_airframes.txt").get("equipments")
        self.archetypes, self.tiers = {}, {}
        for name, b in root.blocks():
            if b.get("is_archetype") == "yes":
                slots = {}
                for sname, s in b.get("module_slots").blocks():
                    slots[sname] = (s.get("required") == "yes", set(s.get("allowed_module_categories").values()))
                self.archetypes[name] = dict(type=b.get("type"), slots=slots, limits=_limits(b))
            else:
                self.tiers[name] = dict(archetype=b.get("archetype"), limits=_limits(b))
        self.duplicates = {}
        dup = load_file(EQ / "x_plane_airframes.txt").get("duplicate_archetypes")
        for name, b in dup.blocks():
            if b.get("archetype") in self.archetypes:
                self.duplicates[name] = dict(archetype=b.get("archetype"), type=b.get("type"), limits=_limits(b))
        self.modules = {}
        mods = load_file(EQ / "modules/00_plane_modules.txt").get("equipment_modules")
        for name, b in mods.blocks():
            forbid = b.get("forbid_module_categories")
            role = b.get("add_equipment_type")
            self.modules[name] = dict(category=b.get("category"),
                                      forbid=set(forbid.values()) if isinstance(forbid, Block) else set(),
                                      role=role.values()[0] if isinstance(role, Block) else None)
        # Techs : celles du mod, plus les fichiers vanilla que le mod n'écrase pas (radars, viseurs…).
        self.module_tech, self.equipment_tech, self.prereqs = {}, {}, {}
        files = {f.name: f for f in (ref / "common/technologies").glob("*.txt")}
        files.update({f.name: f for f in (MOD / "common/technologies").glob("*.txt")})
        for f in files.values():
            techs = load_file(f).get("technologies")
            if not isinstance(techs, Block):
                continue
            for tid, t in techs.blocks():
                if tid.startswith("@"):
                    continue
                for key, store in (("enable_equipment_modules", self.module_tech), ("enable_equipments", self.equipment_tech)):
                    for e in self._all(t, key):
                        for v in e.values():
                            store.setdefault(v, tid)
                for p in t.get_all("path"):
                    if isinstance(p, Block) and p.get("leads_to_tech"):
                        self.prereqs.setdefault(p.get("leads_to_tech"), set()).add(tid)

    def closure(self, techs):
        """Les techs données et tous leurs prérequis (chemins leads_to_tech)."""
        out, todo = set(), list(techs)
        while todo:
            t = todo.pop()
            if t not in out:
                out.add(t)
                todo += self.prereqs.get(t, ())
        return out

    @staticmethod
    def _all(block, key):
        """Toutes les listes `key`, y compris dans les blocs imbriqués (if/limit de DLC)."""
        found = []
        for e in block:
            if isinstance(e.value, Block):
                if e.key == key:
                    found.append(e.value)
                else:
                    found += Rules._all(e.value, key)
        return found

    # ------------------------------------------------------------------ type de cellule
    def resolve(self, eq_type):
        """small_plane_cas_airframe_1 → (archétype, palier, doublon, type)."""
        m = re.fullmatch(r"(\w+)_(\d)", eq_type)
        if not m:
            raise KeyError(f"type de cellule inconnu : {eq_type}")
        base, n = m[1], m[2]
        if base in self.archetypes:
            return base, f"{base}_{n}", None, self.archetypes[base]["type"]
        if base in self.duplicates:
            d = self.duplicates[base]
            return d["archetype"], f"{d['archetype']}_{n}", base, d["type"]
        raise KeyError(f"type de cellule inconnu : {eq_type}")

    # ------------------------------------------------------------------ placement
    def place(self, eq_type, modules, fixed=None):
        """Range une liste de modules dans les slots de la cellule (premier slot libre qui accepte
        la catégorie, dans l'ordre de l'écran). `fixed` : {slot: module} imposés."""
        arch = self.resolve(eq_type)[0]
        slots = self.archetypes[arch]["slots"]
        design = dict(fixed or {})
        for mid in modules:
            if mid not in self.modules:
                raise KeyError(f"module inconnu : {mid}")
            cat = self.modules[mid]["category"]
            free = [s for s, (_, cats) in slots.items() if cat in cats and s not in design]
            if not free:
                raise ValueError(f"{eq_type} : pas de slot libre pour {mid} ({cat})")
            design[free[0]] = mid
        return {s: design[s] for s in slots if s in design}

    # ------------------------------------------------------------------ contrôle
    def check(self, eq_type, design, techs=None):
        """Liste des raisons pour lesquelles le designer refuserait le design (vide = accepté)."""
        errors = []
        try:
            arch, tier, dup, typ = self.resolve(eq_type)
        except KeyError as e:
            return [str(e)]
        if tier not in self.tiers:
            return [f"palier inexistant : {tier}"]
        slots = self.archetypes[arch]["slots"]
        mods = {s: m for s, m in design.items() if m != "empty"}
        for s, m in mods.items():
            if s not in slots:
                errors.append(f"slot {s} absent de {arch}")
            elif m not in self.modules:
                errors.append(f"module inconnu : {m}")
            elif self.modules[m]["category"] not in slots[s][1]:
                errors.append(f"{m} ({self.modules[m]['category']}) refusé dans {s}")
        if errors:
            return errors
        for s, (req, _) in slots.items():
            if req and s not in mods:
                errors.append(f"slot obligatoire vide : {s}")
        cats = {m: self.modules[m]["category"] for m in mods.values()}
        for m in mods.values():
            for other, c in cats.items():
                if c in self.modules[m]["forbid"]:
                    errors.append(f"{m} interdit la catégorie de {other} ({c})")
        dup_limits = self.duplicates[dup]["limits"] if dup else []
        for conds, op, n in _merge(self.archetypes[arch]["limits"], self.tiers[tier]["limits"], dup_limits):
            count = sum(1 for m in mods.values() if f"module={m}" in conds or f"category={cats[m]}" in conds)
            ok = count < n if op == "<" else count > n if op == ">" else count == n
            if not ok:
                errors.append(f"limite non tenue : {sorted(conds)} count {op} {n} (il y en a {count})")
        roles = [self.modules[m]["role"] for m in mods.values() if self.modules[m]["role"]]
        if roles and roles[0] != typ:
            errors.append(f"rôle {roles[0]} sur une cellule de type {typ} ({eq_type})")
        if techs is not None:
            t = self.equipment_tech.get(tier)
            if t and t not in techs:
                errors.append(f"cellule {tier} : tech {t} manquante")
            for m in mods.values():
                t = self.module_tech.get(m)
                if t is None:
                    errors.append(f"{m} : débloqué par aucune tech (projet spécial ?)")
                elif t not in techs:
                    errors.append(f"{m} : tech {t} manquante")
        return errors


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    r = Rules()
    design = r.place(argv[0], argv[1:])
    for s, m in design.items():
        print(f"  {s} = {m}")
    errs = r.check(argv[0], design)
    print("accepté" if not errs else "\n".join("REFUSÉ : " + e for e in errs))


if __name__ == "__main__":
    main(sys.argv[1:])

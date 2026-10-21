#!/usr/bin/env python3
"""
validate_mod.py - Contrôle statique d'un mod HOI4 centré sur le designer
d'avions, AVANT de lancer le jeu. Ne remplace pas error.log, mais attrape la
plupart des erreurs qui y finiraient.

    python3 validate_mod.py --mod <dossier du mod> --ref <HOI4 ou HOI4-ref>
    python3 validate_mod.py --mod <mod> --ref <ref> --lang french --lang english
    python3 validate_mod.py --mod <mod> --ref <ref> --json rapport.json

Contrôles :
  [syntaxe]   accolades équilibrées dans .txt/.gui/.gfx, jeton isolé suspect
  [encodage]  .yml en UTF-8 AVEC BOM, en-tête l_<langue>: cohérent avec le nom
              du fichier, clés dupliquées
  [descriptor] descriptor.mod présent, champs name/version/supported_version,
              replace_path signalés
  [écrasement] fichiers du mod qui remplacent un fichier vanilla de même chemin
              (remplacement TOTAL du fichier) et objets redéfinis ailleurs
  [modules]   catégorie connue d'au moins un slot, nom localisé, description,
              icône GFX_EMI_<module> (ou gfx), tech qui le débloque,
              can_convert_from/parent vers des modules existants
  [cellules]  catégories de slot existantes, default_modules valides, conteneur
              equipment_designer_<type|archétype> dans un .gui, nombre de slots
              fixes/libres compatible avec plane_designer_view.gui, sprite du plan
  [techs]     enable_equipments / enable_equipment_modules vers des objets connus
  [IA]        gabarits ai_equipment (catégorie air) : types, slots et modules connus
Sévérités : ERREUR (le jeu cassera ou ignorera), ALERTE (probable oubli), INFO.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))  # scripts partagés du plugin (pdx, extract_air)
from pdx import Block, check_braces, load_file, read_text  # noqa: E402
import extract_air as ea  # noqa: E402

TEXT_EXT = {".txt", ".gui", ".gfx"}


class Report:
    def __init__(self):
        self.items = []

    def add(self, sev, cat, msg, where=""):
        self.items.append({"severity": sev, "check": cat, "message": msg, "where": where})

    def print(self):
        order = {"ERREUR": 0, "ALERTE": 1, "INFO": 2}
        by = defaultdict(list)
        for it in sorted(self.items, key=lambda x: (order[x["severity"]], x["check"])):
            by[it["severity"]].append(it)
        for sev in ("ERREUR", "ALERTE", "INFO"):
            if by[sev]:
                print(f"\n== {sev} ({len(by[sev])}) ==")
                for it in by[sev]:
                    w = f"  [{it['where']}]" if it["where"] else ""
                    print(f"- [{it['check']}] {it['message']}{w}")
        n = {s: len(by[s]) for s in order}
        print(f"\nBilan : {n['ERREUR']} erreur(s), {n['ALERTE']} alerte(s), {n['INFO']} info(s).")
        return n["ERREUR"]


def check_syntax(mod: Path, rep: Report):
    for f in mod.rglob("*"):
        if f.suffix.lower() in TEXT_EXT and f.is_file():
            try:
                txt = read_text(f)
            except Exception as e:  # pragma: no cover
                rep.add("ERREUR", "syntaxe", f"lecture impossible : {e}", str(f.relative_to(mod)))
                continue
            for p in check_braces(txt):
                rep.add("ERREUR", "syntaxe", p, str(f.relative_to(mod)))
            raw = f.read_bytes()
            if raw.startswith(b"\xef\xbb\xbf") and f.suffix.lower() == ".txt":
                rep.add("INFO", "encodage", "BOM UTF-8 dans un .txt (accepté par le jeu, inutile)", str(f.relative_to(mod)))


def check_localisation(mod: Path, rep: Report, langs: list[str]):
    seen = defaultdict(list)
    for f in mod.rglob("*.yml"):
        relp = str(f.relative_to(mod))
        raw = f.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            rep.add("ERREUR", "encodage", "fichier de localisation sans BOM UTF-8 : le jeu l'ignorera", relp)
        try:
            txt = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            rep.add("ERREUR", "encodage", "fichier de localisation non UTF-8", relp)
            continue
        m = re.search(r"_l_([a-z_]+)\.yml$", f.name)
        if not m:
            rep.add("ERREUR", "localisation", "nom de fichier sans suffixe _l_<langue>.yml", relp)
            continue
        lang = m.group(1)
        first = next((l for l in txt.splitlines() if l.strip() and not l.strip().startswith("#")), "")
        if first.strip() != f"l_{lang}:":
            rep.add("ERREUR", "localisation", f"première ligne '{first.strip()}' au lieu de 'l_{lang}:'", relp)
        for i, line in enumerate(txt.splitlines(), 1):
            mm = re.match(r'^\s*([^\s:#]+):\d*\s*"', line)
            if mm:
                seen[(lang, mm.group(1))].append(f"{relp}:{i}")
            elif line.strip() and not line.strip().startswith("#") and not line.strip().startswith("l_"):
                if re.match(r"^\s*[^\s:#]+:\d*\s*[^\"\s]", line):
                    rep.add("ERREUR", "localisation", f"ligne {i} : texte sans guillemets", relp)
            if "\t" in line[:len(line) - len(line.lstrip())]:
                rep.add("ALERTE", "localisation", f"ligne {i} : indentation par tabulation (préférer un espace)", relp)
    for (lang, k), where in seen.items():
        if len(where) > 1:
            rep.add("ALERTE", "localisation", f"clé '{k}' ({lang}) définie {len(where)} fois : {', '.join(where[:3])}")
    return {(l, k) for (l, k) in seen}


def check_descriptor(mod: Path, rep: Report):
    d = mod / "descriptor.mod"
    if not d.is_file():
        rep.add("ALERTE", "descriptor", "descriptor.mod absent à la racine du mod")
        return
    root = load_file(d)
    for k in ("name", "version", "supported_version"):
        if root.get(k) is None:
            rep.add("ALERTE", "descriptor", f"champ '{k}' absent")
    for rp in root.get_all("replace_path"):
        rep.add("INFO", "descriptor", f"replace_path = {rp} : TOUT le dossier vanilla est ignoré")


def check_overrides(mod: Path, ref: Path, rep: Report):
    for f in mod.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in TEXT_EXT | {".yml"}:
            continue
        r = f.relative_to(mod)
        if (ref / r).is_file():
            if f.suffix.lower() == ".yml" and "replace" not in r.parts:
                rep.add("ALERTE", "écrasement", "même nom qu'un fichier de localisation vanilla : mettre les surcharges dans localisation/<langue>/replace/", str(r))
            else:
                rep.add("INFO", "écrasement", "remplace INTÉGRALEMENT le fichier vanilla de même chemin", str(r))


def gui_names(roots: list[Path]) -> tuple[set, set, dict]:
    """noms de containerWindowType et de spriteType dans tous les .gui/.gfx, + positions du designer."""
    windows, sprites = set(), set()
    pos = {"fixed": 0, "custom": 0}
    for root in roots:
        for f in list((root / "interface").rglob("*.gui")) if (root / "interface").is_dir() else []:
            txt = read_text(f)
            windows.update(re.findall(r'name\s*=\s*"([^"]+)"', txt))
            if f.name == "plane_designer_view.gui":
                pos["fixed"] = len(set(re.findall(r'"pos_fixed_module_slot_window_(\d+)"', txt)))
                pos["custom"] = len(set(re.findall(r'"pos_custom_module_slot_window_(\d+)"', txt)))
        for f in list((root / "interface").rglob("*.gfx")) if (root / "interface").is_dir() else []:
            sprites.update(re.findall(r'name\s*=\s*"([^"]+)"', read_text(f)))
    return windows, sprites, pos


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mod", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--lang", action="append", help="langue(s) à exiger pour les noms (défaut : french)")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    mod, ref = Path(a.mod), Path(a.ref)
    langs = a.lang or ["french"]
    rep = Report()

    check_syntax(mod, rep)
    check_localisation(mod, rep, langs)
    check_descriptor(mod, rep)
    check_overrides(mod, ref, rep)

    db = ea.build([ref, mod], langs[0])
    for w in db["warnings"]:
        if "aucune technologie" in w:
            continue  # traité module par module ci-dessous (mod seulement)
        sev = "ALERTE" if "redéfini" in w else "INFO"
        rep.add(sev, "extraction", w)
    for n, om in db.get("other_modules", {}).items():
        if om.get("origin") == "mod" and not any(k in (om["category"] or "") for k in ("tank", "ship", "naval")):
            rep.add("ALERTE", "modules", f"'{n}' : catégorie '{om['category']}' acceptée par aucun slot d'avion "
                    "(normal pour un module de char/navire, sinon ajouter la catégorie à un slot)", f"{om['file']}:{om['line']}")

    # localisation fusionnée (toutes langues demandées)
    loc = {}
    for lang in langs:
        d = {}
        for root in (ref, mod):
            p = root / "localisation"
            if p.is_dir():
                for f in sorted(p.rglob(f"*_l_{lang}.yml")):
                    d.update(ea.load_localisation(f))
        loc[lang] = d

    windows, sprites, pos = gui_names([ref, mod])
    M, A, T = db["modules"], db["airframes"], db["techs"]
    all_cats = set(db["categories"])
    slot_cats = {c for a_ in A.values() for s in a_["slots"].values() for c in s.get("categories", [])}

    # --- modules du mod
    for n, m in M.items():
        if m.get("origin") != "mod":
            continue
        w = f"{m['file']}:{m['line']}"
        if m["category"] not in slot_cats:
            rep.add("ERREUR", "modules", f"'{n}' : catégorie '{m['category']}' acceptée par aucun slot", w)
        for lang in langs:
            if n not in loc[lang]:
                rep.add("ALERTE", "modules", f"'{n}' : pas de nom localisé ({lang})", w)
            if f"{n}_desc" not in loc[lang]:
                rep.add("INFO", "modules", f"'{n}' : pas de description '{n}_desc' ({lang})", w)
        if f"GFX_EMI_{n}" not in sprites:
            rep.add("ALERTE", "modules", f"'{n}' : aucune icône GFX_EMI_{n} (le jeu affichera une icône vide)", w)
        if not m.get("techs"):
            rep.add("ALERTE", "modules", f"'{n}' : aucune tech (enable_equipment_modules) ne le débloque", w)
        if m.get("parent") and m["parent"] not in M:
            rep.add("ERREUR", "modules", f"'{n}' : parent '{m['parent']}' inconnu", w)
        for c in m.get("can_convert_from", []):
            if c.get("module") and c["module"] not in M:
                rep.add("ERREUR", "modules", f"'{n}' : can_convert_from vers module inconnu '{c['module']}'", w)
            if c.get("module_category") and c["module_category"] not in all_cats:
                rep.add("ERREUR", "modules", f"'{n}' : can_convert_from vers catégorie inconnue '{c['module_category']}'", w)
        if not m.get("abbreviation"):
            rep.add("INFO", "modules", f"'{n}' : pas d'abbreviation (utilisée dans le nom auto des designs)", w)
        if m["add_stats"].get("build_cost_ic") is None:
            rep.add("ALERTE", "modules", f"'{n}' : pas de build_cost_ic", w)

    # --- catégories nouvelles sans nom
    for c in all_cats:
        if not any(M.get(x, {}).get("origin") == "mod" for x in db["categories"][c]["modules"]):
            continue
        for lang in langs:
            if f"EQ_MOD_CAT_{c}_TITLE" not in loc[lang]:
                rep.add("ALERTE", "localisation", f"catégorie '{c}' sans EQ_MOD_CAT_{c}_TITLE ({lang})")

    # --- cellules du mod
    for n, af in A.items():
        if af.get("origin") != "mod" or af["is_archetype"]:
            continue
        w = f"{af['file']}:{af['line']}"
        for s, info in af["slots"].items():
            for c in info.get("categories", []):
                if c not in all_cats:
                    rep.add("ERREUR", "cellules", f"'{n}' slot {s} : catégorie '{c}' sans aucun module", w)
            for lang in langs:
                if f"EQ_MOD_SLOT_{s}_TITLE" not in loc[lang]:
                    rep.add("ALERTE", "localisation", f"slot '{s}' sans EQ_MOD_SLOT_{s}_TITLE ({lang})", w)
        for s, mname in af["default_modules"].items():
            if s not in af["slots"]:
                rep.add("ERREUR", "cellules", f"'{n}' default_modules : slot inconnu '{s}'", w)
            elif mname not in ("empty",) and mname not in M:
                rep.add("ERREUR", "cellules", f"'{n}' default_modules : module inconnu '{mname}'", w)
        nfix = sum(1 for s in af["slots"].values() if s["kind"] == "fixed")
        ncus = len(af["slots"]) - nfix
        if pos["fixed"] and nfix > pos["fixed"]:
            rep.add("ERREUR", "cellules", f"'{n}' : {nfix} slots fixes mais plane_designer_view.gui n'a que {pos['fixed']} positions fixes", w)
        if pos["custom"] and ncus > pos["custom"]:
            rep.add("ERREUR", "cellules", f"'{n}' : {ncus} slots libres mais plane_designer_view.gui n'a que {pos['custom']} positions", w)
        cands = [f"equipment_designer_{n}", f"equipment_designer_{af['archetype']}"]
        if af.get("duplicate_of"):
            cands.append(f"equipment_designer_{af['duplicate_of']}")
        if not any(c in windows for c in cands):
            rep.add("ALERTE", "cellules", f"'{n}' : aucun conteneur {cands[0]} dans les .gui (plan absent du designer)", w)
        for lang in langs:
            if n not in loc[lang]:
                rep.add("ALERTE", "localisation", f"cellule '{n}' sans nom ({lang})", w)
        if not af.get("techs") and not af.get("duplicate_of"):
            rep.add("ALERTE", "cellules", f"'{n}' : aucune tech (enable_equipments) ne la débloque", w)

    # --- techs du mod
    known_eq = set(A) | {e for t in T.values() for e in t["enable_equipments"]}
    for n, t in T.items():
        if t.get("origin") != "mod":
            continue
        for m in t["enable_equipment_modules"]:
            if m not in M:
                rep.add("ERREUR", "techs", f"tech '{n}' débloque un module inconnu '{m}'", f"{t['file']}:{t['line']}")

    # --- IA
    for g, grp in db["ai_designs"].items():
        if grp.get("origin") != "mod":
            continue
        for dn, d in grp["designs"].items():
            w = f"{grp['file']}:{d['line']}"
            if d["type"] and d["type"] not in A:
                rep.add("ALERTE", "IA", f"{g}/{dn} : type '{d['type']}' inconnu des cellules du designer", w)
                continue
            slots = A.get(d["type"], {}).get("slots", {})
            for s, req in d["modules"].items():
                if s not in slots:
                    rep.add("ERREUR", "IA", f"{g}/{dn} : slot inconnu '{s}' pour {d['type']}", w)
                if isinstance(req, str):
                    tok = req.split()[-1]
                    if tok not in M and tok not in all_cats and tok != "empty":
                        rep.add("ERREUR", "IA", f"{g}/{dn} : '{tok}' n'est ni un module ni une catégorie", w)
            for x in d["allowed_modules"]:
                if x not in M and x not in all_cats:
                    rep.add("ERREUR", "IA", f"{g}/{dn} allowed_modules : '{x}' inconnu", w)

    nerr = rep.print()
    if a.json:
        Path(a.json).write_text(json.dumps(rep.items, ensure_ascii=False, indent=1), encoding="utf-8")
    return 1 if nerr else 0


if __name__ == "__main__":
    try:  # sortie tronquée par | head : pas de trace d'erreur
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())

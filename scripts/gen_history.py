"""Convertit les avions de départ (create_equipment_variant des cellules BBA) des pays au designer du mod
(phase 6, Q14 : les 15 pays qui en ont).

Lancer depuis la racine (après gen_mod.py et gen_techs.py) :
  python -X utf8 scripts/gen_history.py [--ref "F:/Github Local/HOI4-ref"]

Le jeu lit ces fichiers dans history/countries/ (racine du jeu, confirmé par Florian le 22/10) ; la copie
HOI4-ref les range dans common/history/countries/. Le mod les écrit donc dans mod/history/countries/.
Chaque fichier est la copie du vanilla où seuls les blocs modules = { } des avions BBA sont réécrits
(nom, cellule, MIO, icône et le reste du fichier inchangés, pour que les escadrilles de départ
retrouvent leurs avions par leur nom). Chaque design est contrôlé par check_designs.py avec les techs
que le pays a à cette date (1936, ou 1939 pour les blocs 1939.1.1).
"""
import argparse, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import designs_zv as Z
import designs_depart as D
import gen_ai as A

MOD = Z.ROOT / "mod"
DATE = re.compile(r"\b(\d{4})\.\d+\.\d+\s*=\s*\{")


def match_brace(t, i):
    """Position de l'accolade fermante de celle ouverte en t[i] (commentaires et chaînes ignorés)."""
    depth, n = 0, len(t)
    while i < n:
        c = t[i]
        if c == "#":
            i = t.find("\n", i)
            if i < 0:
                return n
            continue
        if c == '"':
            i = t.find('"', i + 1) + 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("accolade non fermée")


def strip_comments(t):
    return re.sub(r"#[^\n]*", "", t)


def blocks(t, key):
    """(début, fin) des blocs `key = { … }` hors commentaires."""
    out = []
    for m in re.finditer(rf"(?m)^[^#\n]*?\b{key}\s*=\s*\{{", t):
        b = m.end() - 1
        out.append((m.start(), match_brace(t, b)))
    return out


def techs_in(seg):
    return set(re.findall(r"(\w+)\s*=\s*1\b", " ".join(strip_comments(t[a:b]) for t, (a, b) in
                                                    [(seg, s) for s in blocks(seg, "set_technology")])))


def country_techs(t):
    """Techs du pays au départ (hors blocs datés) et par bloc daté {année: (début, fin, techs)}."""
    dates = []
    for m in DATE.finditer(t):
        if "#" in t[t.rfind("\n", 0, m.start()) + 1:m.start()]:
            continue
        b = match_brace(t, m.end() - 1)
        dates.append((int(m[1]), m.start(), b))
    root = t
    for _, a, b in sorted(dates, key=lambda d: -d[1]):
        root = root[:a] + root[b + 1:]
    return techs_in(root), [(y, a, b, techs_in(t[a:b])) for y, a, b in dates]


def family(tag, name):
    return "liquid" if (tag, name) in D.LIQUID else "radial"


ENGINE = re.compile(r"engine_(\d)_(\d)x")
LAYOUT = {1: "nose", 2: "twin_wing", 3: "tri", 4: "quad"}


def recipe(tag, name, eq_type, vanilla):
    """Recette du design converti : cellule et moteur, puis les armes du design vanilla."""
    arch, tier_name, dup, _ = Z.RULES.resolve(eq_type)
    tier = int(tier_name[-1])
    size = "cv" if arch.startswith("cv_") else arch.split("_")[0]
    sz = A.SIZE[size]
    fam = family(tag, name)
    k = {}
    eng = next((v for v in vanilla.values() if ENGINE.fullmatch(v)), "engine_1_1x")
    gen, count = (int(x) for x in ENGINE.fullmatch(eng).groups())
    ladder = A.LIQUID if fam == "liquid" else A.RADIAL
    k["E"] = list(reversed(ladder[:gen]))                    # le moteur vanilla, sinon le précédent
    layout = LAYOUT[count]
    k["EC"] = [f"zv_engine_config_{layout}_{c}" for c in "cba"]  # la classe qui va avec le moteur
    k["EM1"] = "zv_naca_cowling" if fam == "radial" else ["zv_radiator_ventral"] if gen >= 2 else None
    k["P"] = "zv_prop_2_metal" if tier == 0 else "zv_prop_3_metal"
    bomber = arch in ("medium_plane_airframe", "large_plane_airframe") and dup is None or \
        dup == "large_plane_maritime_patrol_plane_airframe"
    fus = next((D.VANILLA_TO_ZV[v] for v in vanilla.values() if v.startswith("flying_boat")), None)
    k["F"] = fus or f"zv_fuselage_classic_{sz}"
    if tier == 0:
        k["WT"] = "zv_wing_biplan_rectangulaire" if sz == "s" else "zv_wing_mediane_rectangulaire"
    else:
        k["WT"] = "zv_wing_mediane_trapezoidale" if sz == "l" else "zv_wing_basse_trapezoidale"
    k["T"] = "zv_tail_classic"
    if "floats" in vanilla.values():
        k["G"] = "zv_floats"
    elif not fus:
        k["G"] = "zv_gear_fixed_taildragger" if tier == 0 else ["zv_gear_retractable_taildragger", "zv_gear_fixed_taildragger"]
    k["CP"] = (["zv_cockpit_glazed_nose", "zv_cockpit_closed"] if bomber and tier >= 1   # trimoteur : pas de nez vitré
               else "zv_cockpit_open" if tier == 0 else "zv_cockpit_closed")
    k["R"] = D.ROLE_OF_TYPE[dup or arch]
    rec = {A.S[s]: v for s, v in k.items() if v}
    if size == "cv":
        rec[A.S["I1"]] = "zv_carrier_equipment"
    if dup == "large_plane_maritime_patrol_plane_airframe":   # obligation du rôle (05) : une arme anti-sous-marine
        rec[A.S["BM"]] = "zv_depth_charges"
    weapons = []
    for v in vanilla.values():
        if v == "empty" or ENGINE.fullmatch(v) or v.startswith("flying_boat") or v == "floats":
            continue
        if sz == "s" and v in D.SMALL_TURRET:
            weapons.append(D.SMALL_TURRET[v])
        else:
            weapons.append(D.VANILLA_TO_ZV.get(v, v))
    return rec, weapons


def convert(tag, name, eq_type, vanilla, techs):
    """Design converti {slot: module} et liste des écarts (modules absents ou refusés)."""
    rec, weapons = recipe(tag, name, eq_type, vanilla)
    notes, missing = [], []
    design = Z.build(eq_type, rec, techs, missing)
    notes += [f"⚠ {m} imposé sans sa tech ({Z.RULES.module_tech.get(m)}) : aucun autre module possible" for m in missing]
    slots = Z.RULES.archetypes[Z.RULES.resolve(eq_type)[0]]["slots"]
    room = lambda m: sum(1 for _, cats in slots.values() if Z.RULES.modules[m]["category"] in cats)
    for w in sorted(weapons, key=room):         # les modules qui ont le moins de places d'abord (phase 7)
        # Le module vanilla, sinon un plus ancien de la même catégorie (Florian, 23/10 : « remplace-les par
        # des modules de niveau 1 quand c'est possible »), le plus récent d'abord.
        cat = Z.RULES.modules[w]["category"]
        older = [m for m in Z.members(cat) if m != w and Z.year(m) <= Z.year(w)]
        placed, why = None, f"tech {Z.RULES.module_tech.get(w)} pas encore recherchée"
        for cand in [w] + older:
            if not Z.available(cand, techs):
                continue
            try:
                trial = Z.RULES.place(eq_type, [cand], fixed=design)
            except ValueError:
                why = "plus de slot libre"
                break
            errs = [e for e in Z.RULES.check(eq_type, trial) if not e.startswith("slot obligatoire") and "count > 0" not in e]
            if not errs:
                placed, design = cand, trial
                break
            why = errs[0]
        if placed is None:
            notes.append(f"{w} retiré : {why}")
        elif placed != w:
            notes.append(f"{w} remplacé par {placed} (tech {Z.RULES.module_tech.get(w)} pas encore recherchée)")
    return design, notes


def add_start_techs(t, tag, report_techs):
    """Ajoute au fichier pays les techs de départ de designs_depart.py (bloc set_technology à la racine
    pour 1936, au début du premier bloc 1939.1.1 pour 1939)."""
    root, dated = country_techs(t)
    d39 = set().union(*[d[3] for d in dated]) if dated else set()
    give = {1936: list(D.START_TECHS.get((tag, 1936), [])), 1939: list(D.START_TECHS.get((tag, 1939), []))}
    why = "moteur en étoile II : le vanilla le donnait avec engines_2"
    if D.RADIAL_2_WITH in root:
        give[1936].append(("zv_radial_engines_2", why))
    elif D.RADIAL_2_WITH in d39:
        give[1939].append(("zv_radial_engines_2", why))
    give[1939] = [(x, r) for x, r in give[1939] if x not in dict(give[1936])]   # déjà donnée en 1936
    for year, items in ((1939, give[1939]), (1936, give[1936])):     # 1939 d'abord : il est plus bas
        have = root | (d39 if year == 1939 else set())
        items = [(tech, r) for tech, r in dict(items).items() if tech not in have]
        if not items:
            continue
        for tech, r in items:
            miss = sorted(p for p in Z.RULES.prereqs.get(tech, ()) if p not in have | {x for x, _ in items})
            report_techs.append((tag, year, tech, r, miss))
        tab = "\t\t" if year == 1939 else "\t"
        lines = "".join(f"{tab}{tech} = 1\t# ZV: {r}\n" for tech, r in items)
        if year == 1939:
            first = min(dated, key=lambda d: d[1])
            pos = t.index("{", first[1]) + 1
            t = t[:pos] + f"\n\tset_technology = {{\t# ZV Designer : techs de départ (phase 6)\n{lines}\t}}" + t[pos:]
        else:
            m = re.search(r"(?m)^set_technology\s*=\s*\{", t)
            pos = m.start() if m else 0
            t = t[:pos] + f"set_technology = {{\t# ZV Designer : techs de départ (phase 6)\n{lines}}}\n" + t[pos:]
    return t


def modules_text(design, ind):
    t = "\t" * ind
    return "\n".join([f"{t}modules = {{"] + [f"{t}\t{s} = {m}" for s, m in design.items()] + [f"{t}}}"])


def convert_file(path, report, report_techs):
    raw = path.read_bytes()
    t = raw.decode("utf-8-sig")
    tag = path.name[:3]
    t = add_start_techs(t, tag, report_techs)
    root_techs, dated = country_techs(t)
    rep = []
    for a, b in blocks(t, "create_equipment_variant"):
        seg = t[a:b + 1]
        ty = re.search(r"\btype\s*=\s*(\w*plane\w*airframe_\d)\b", strip_comments(seg))
        if not ty:
            continue
        name = re.search(r'name\s*=\s*"([^"]+)"', seg)[1]
        mb = blocks(seg, "modules")
        if not mb:
            continue
        ma, mz = mb[0]
        vanilla = dict(re.findall(r"(\w+)\s*=\s*(\w+)", strip_comments(seg[ma:mz + 1])[len("modules"):]))
        techs = set(root_techs)
        year = 1936
        for y, da, db, dt in dated:
            if da < a < db:
                year = y
        for y, da, db, dt in dated:          # un pays peut avoir plusieurs blocs de la même date
            if y <= year:
                techs |= dt
        techs = Z.RULES.closure(techs)
        design, notes = convert(tag, name, ty[1], vanilla, techs)
        forced = {Z.RULES.module_tech.get(m) for m in design.values() if any(m in n for n in notes if n.startswith("⚠"))}
        errs = Z.RULES.check(ty[1], design, techs | forced)
        if errs:
            raise A.Fail(f"{tag} « {name} » ({ty[1]}, {year}) refusé : {errs}")
        ind = len(seg[ma:]) - len(seg[ma:].lstrip("\t"))     # le bloc commence en début de ligne
        new = modules_text(design, ind)
        up = "\t" * ind + "upgrades = {\t# ZV: curseurs au cran 5 (réglage d'usine)\n" + "\t" * ind + \
             f"\tzv_engine_power_upgrade = 5\n" + "\t" * ind + "\tzv_reliability_upgrade = 5\n" + "\t" * ind + "}"
        rep.append((a + ma, a + mz + 1, new + "\n" + up))
        report.append((tag, year, name, ty[1], notes))
    for s, e, txt in sorted(rep, reverse=True):
        t = t[:s] + txt + t[e:]
    head = ("# ZV Designer : copie du fichier vanilla 1.19.3.0 générée par scripts/gen_history.py ; seuls les\n"
            "# modules des avions BBA sont réécrits pour le designer du mod (phase 6).\n")
    return (head + t).encode("utf-8"), len(rep)        # .txt du mod : UTF-8 sans BOM (CLAUDE.md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="F:/Github Local/HOI4-ref")
    ref = Path(ap.parse_args().ref)
    src = ref / "common/history/countries"
    out = MOD / "history/countries"
    out.mkdir(parents=True, exist_ok=True)
    report, report_techs, total = [], [], 0
    try:
        for f in sorted(src.glob("*.txt")):
            if "plane_airframe" not in f.read_text(encoding="utf-8-sig"):
                continue
            data, n = convert_file(f, report, report_techs)
            (out / f.name).write_bytes(data)
            total += n
            print(f"écrit : mod/history/countries/{f.name} ({n} avions)")
    except (A.Fail, ValueError) as e:
        sys.exit(f"ERREUR : {e}")
    print(f"{total} avions de départ convertis, tous acceptés par check_designs")
    for tag, year, tech, r, miss in report_techs:
        print(f"  + {tag} {year} : {tech} ({r})" + (f" ⚠ prérequis absents : {miss}" if miss else ""))
    for tag, year, name, ty, notes in report:
        for n in notes:
            print(f"  · {tag} {year} « {name} » : {n}")


if __name__ == "__main__":
    main()

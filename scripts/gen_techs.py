"""Génère les techs du mod (phase 4) et l'écran de l'onglet Aviation, à partir de data/techs.json,
de data/modules.json (la tech de chaque module), de la table gen_mod_table.py et des fichiers
vanilla de HOI4-ref (lus, jamais modifiés).

Lancer depuis la racine (après gen_mod.py) :
  python -X utf8 scripts/gen_techs.py [--ref "F:/Github Local/HOI4-ref"]

Fichiers écrits :
  mod/common/technologies/zv_propulsion_techs.txt     (nouveau : Propulsion)
  mod/common/technologies/zv_construction_techs.txt   (nouveau : Cellule et équipements)
  mod/common/technologies/bba_air_techs.txt           (écrase le vanilla : Armement et missions + cellules)
  mod/common/special_projects/projects/air_projects.txt, rocket_projects.txt (écrasent le vanilla)
  mod/interface/countrytechtreeview.gui               (écrase le vanilla : onglet Aviation)
  mod/localisation/<langue>/zv_techs_l_<langue>.yml   (noms et descriptions des techs nouvelles)
  mod/interface/zv_technologies_icons.gfx             (icônes provisoires des techs nouvelles)
"""
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import gen_mod as G
import gen_mod_table as T

TECHS = {t["id"]: t for t in json.loads((G.DATA / "techs.json").read_text(encoding="utf-8"))}
OTHER_FOLDER = {"airdrop_mines_bba", "airsweep_mines_bba"}      # dossier Soutien naval, inchangées
MANAGED = {k: v for k, v in TECHS.items() if k not in OTHER_FOLDER}
SP_PROJECTS = {"sp_air_jet_engine", "sp_air_axial_jet_engine", "sp_rocket_interceptor"}

COLUMN_OF = {t: c for c, ts in T.TECH_COLUMNS.items() for t in ts}


def group_of(t):
    line = t["line"]
    return "Propulsion" if line < 100 else "Cellule et équipements" if line < 150 else "Armement et missions"


def modules_of(tech):
    """Modules du mod débloqués par la tech (colonne « Tech » du 05)."""
    return [m for m in G.MODULE_IDS if G.MODS[m]["tech"] == tech]


def children():
    ch = {}
    for t in MANAGED.values():
        for p in t["prereqs"]:
            ch.setdefault(p, []).append(t["id"])
    return ch


def position(tech, year):
    if tech not in COLUMN_OF:
        raise G.GenError(f"{tech} : pas de colonne dans TECH_COLUMNS")
    if year not in T.TECH_ROWS:
        raise G.GenError(f"{tech} : année {year} sans ligne dans TECH_ROWS")
    return COLUMN_OF[tech], T.TECH_ROWS[year]


def cost_text(t):
    if t["id"] in T.KEEP_COST_TECHS:
        return None
    return T.COEF_CONSTANTS[t["coef"]]


def is_sp_suite(t):
    return any(a in SP_PROJECTS for a in t["allow"])


def allow_text(t, ind):
    s = "\t" * ind
    if not t["allow"]:
        return []
    conds = []
    for a in t["allow"]:
        if a in SP_PROJECTS:
            conds.append(f"ROOT = {{ is_special_project_completed = sp:{a} }}")
        else:
            conds.append(f"has_tech = {a}")
    return [f"{s}allow = {{"] + [f"{s}\t{c}" for c in conds] + [f"{s}}}"]


def list_block(key, values, ind):
    s = "\t" * ind
    return [f"{s}{key} = {{"] + [f"{s}\t{v}" for v in values] + [f"{s}}}"]


def path_lines(kids, ind):
    s = "\t" * ind
    out = []
    for k in kids:
        out += [f"{s}path = {{", f"{s}\tleads_to_tech = {k}", f"{s}\tresearch_cost_coeff = 1", f"{s}}}"]
    return out


def folder_lines(tech, year, ind):
    s = "\t" * ind
    x, y = position(tech, year)
    return [f"{s}folder = {{", f"{s}\tname = bba_air_techs_folder", f"{s}\tposition = {{ x = {x} y = {y} }}", f"{s}}}"]


# ---------------------------------------------------------------- techs vanilla réécrites

def vanilla_blocks(ref):
    src = (ref / "common/technologies/bba_air_techs.txt").read_text(encoding="utf-8-sig")
    top = [e for e in G.entries(src, 0, len(src)) if e[0] == "technologies"][0]
    return src, top, [e for e in G.entries(src, *G.inner(top[2], top[3])) if e[4]]


def new_dup_types(enabled):
    """Doublons du mod à ajouter à côté des cellules vanilla d'une tech (palier repris)."""
    add = []
    for e in enabled:
        m = re.fullmatch(r"(cv_small|small|medium|large)_plane_airframe_(\d)", e)
        if not m:
            continue
        arch = f"{m[1]}_plane_airframe"
        add += [f"{d}_{m[2]}" for d, info in T.NEW_DUPLICATES.items() if info["archetype"] == arch]
    return add


def rewrite_vanilla(src, key, v0, v1, kids):
    """Texte de la tech vanilla `key` réécrite : modules, coût, position, chemins, doublons."""
    t = MANAGED.get(key)
    sub = G.entries(src, *G.inner(v0, v1))
    rep, done_modules = [], False
    mods = modules_of(key) if t else None
    year = t["year"] if t else None
    for k, s0, a, b, blk in sub:
        if k == "start_year" and year is None:
            year = int(src[a:b])
        if t and k == "enable_equipment_modules":
            if done_modules or not mods:
                rep.append((s0, b, "# ZV: modules vanilla retirés"))
            else:
                rep.append((s0, b, "\n".join(list_block("enable_equipment_modules", mods, 2)).lstrip("\t")
                            + "\t# ZV: modules du mod (05)"))
            done_modules = True
        elif t and k == "research_cost" and cost_text(t):
            rep.append((a, b, f"{cost_text(t)}\t# ZV: coefficient {G.fmt(t['coef'])} × {T.COEF_BASE} (arbre)"))
        elif k == "folder":
            rep.append((s0, b, "\n".join(folder_lines(key, year, 2)).lstrip("\t") + "\t# ZV: placement de l'arbre"))
        elif k == "path" and t:
            target = re.search(r"leads_to_tech\s*=\s*(\w+)", src[a:b])
            if target and target.group(1) in MANAGED:
                rep.append((s0, b, ""))           # remplacé par les chemins de l'arbre
        elif k == "enable_equipments" and "limit" not in src[a:b]:
            vals = [e[0] or src[e[1]:e[3]] for e in G.entries(src, *G.inner(a, b))]
            vals = [src[e[1]:e[3]] for e in G.entries(src, *G.inner(a, b)) if e[0] is None]
            extra = new_dup_types(vals)
            if extra:
                rep.append((b - 1, b - 1, "".join(f"\t{x}\t# ZV: doublon du mod\n\t\t" for x in extra)))
    extra_lines = []
    if t and mods and not done_modules:
        extra_lines += list_block("enable_equipment_modules", mods, 2)
    if t:
        managed_kids = [k for k in kids.get(key, [])]
        extra_lines += path_lines(managed_kids, 2)
    if extra_lines:
        rep.append((v1 - 1, v1 - 1, "\t" + "\n".join(extra_lines).lstrip("\t") + "\n\t"))
    text = src[G.inner(v0, v1)[0] - 1:v1]
    base = v0
    for a, b, s in sorted(rep, reverse=True):
        text = text[:a - base] + s + text[b - base:]
    return re.sub(r"\n(?:[ \t]*\n){2,}", "\n\n", text)


# ---------------------------------------------------------------- nouvelles techs

def category_model(tech):
    col = COLUMN_OF[tech]
    for model, cols in T.TECH_CATEGORY_MODEL.items():
        if col in cols:
            return model
    return T.TECH_GROUPS[group_of(MANAGED[tech])][1]


def new_tech_text(t, kids, categories):
    tid = t["id"]
    L = [f"\t{tid} = {{\t# {t['name']} (04-arbre, ligne {t['line']})"]
    L += [f"\t\tresearch_cost = {cost_text(t)}", f"\t\tstart_year = {t['year']}"]
    L += folder_lines(tid, t["year"], 2)
    L += allow_text(t, 2)
    if is_sp_suite(t):
        L.append("\t\tis_special_project_tech = yes")
    mods = modules_of(tid)
    if mods:
        L += list_block("enable_equipment_modules", mods, 2)
    L += path_lines(kids.get(tid, []), 2)
    L += list_block("categories", categories, 2)
    L.append("\t\tspecial_project_specialization = { specialization_air }")
    factor = T.OPTIONAL_AI_FACTOR if "optionnelle" in t["name"] else 1
    L += ["\t\tai_will_do = {", f"\t\t\tfactor = {G.fmt(factor)}", "\t\t\tmodifier = {",
          "\t\t\t\tfactor = 2", "\t\t\t\tis_major = yes", "\t\t\t}", "\t\t}"]
    L.append("\t}")
    return "\n".join(L)


def constants():
    return "\n".join(f"\t{name} = {G.fmt(coef * T.COEF_BASE)}" for coef, name in T.COEF_CONSTANTS.items())


def gen_tech_files(ref):
    src, top, blocks = vanilla_blocks(ref)
    kids = children()
    vanilla_text, categories = {}, {}
    for key, k0, v0, v1, blk in blocks:
        vanilla_text[key] = f"\t{key} = " + rewrite_vanilla(src, key, v0, v1, kids)
        cats = [e for e in G.entries(src, *G.inner(v0, v1)) if e[0] == "categories"]
        if cats:
            c = cats[0]
            categories[key] = [src[e[1]:e[3]] for e in G.entries(src, *G.inner(c[2], c[3]))]
    missing = [t for t in MANAGED if t not in vanilla_text and not t.startswith("zv_")]
    if missing:
        raise G.GenError(f"techs vanilla introuvables dans bba_air_techs.txt : {missing}")
    files = {f: [] for f, _ in T.TECH_GROUPS.values()}
    for gname, (fname, _) in T.TECH_GROUPS.items():
        for tid, t in MANAGED.items():
            if group_of(t) != gname:
                continue
            if tid in vanilla_text:
                if tid in T.MOVED_VANILLA_TECHS or fname == "bba_air_techs.txt":
                    files[fname].append((tid, vanilla_text[tid]))
            else:
                files[fname].append((tid, new_tech_text(t, kids, categories[category_model(tid)])))
    # Techs vanilla non gérées par l'arbre (cellules _1 à _5, projets spéciaux…) : réécrites pour le
    # placement et les doublons, gardées dans bba_air_techs.txt.
    for key in vanilla_text:
        if key not in MANAGED:
            files["bba_air_techs.txt"].append((key, vanilla_text[key]))
    out = {}
    for fname, items in files.items():
        if fname == "bba_air_techs.txt":
            items = [i for i in items if i[0] not in T.MOVED_VANILLA_TECHS]
        head = ("# ZV Designer : fichier généré par scripts/gen_techs.py (arbre : docs/04-arbre-technologique.md).\n"
                "# Ne pas modifier à la main.\n")
        if fname == "bba_air_techs.txt":
            head += "# Écrase le bba_air_techs.txt vanilla 1.19.3.0 (techs vanilla réécrites, marquées « ZV: »).\n"
        body = "\n\n".join(text for _, text in items)
        out[fname] = head + "technologies = {\n" + constants() + "\n\n" + body + "\n}\n"
    return out


# ---------------------------------------------------------------- projets spéciaux

def gen_projects(ref):
    jet = ["zv_engine_centrifugal_1"]
    axial = ["zv_engine_axial_1"]
    rocket = [m for m in G.MODULE_IDS if G.MODS[m]["tech"] == "sp_rocket_interceptor"]
    out = {}
    p = ref / "common/special_projects/projects/air_projects.txt"
    t = p.read_text(encoding="utf-8-sig")

    def swap(text, olds, news):
        block = re.compile(r"(enable_equipment_modules\s*=\s*\{\s*limit\s*=\s*\{\s*has_dlc\s*=\s*\"By Blood Alone\"\s*\})"
                           r"(\s*)((?:%s)\b[^{}]*?)\}" % "|".join(olds))
        m = block.search(text)
        if not m:
            raise G.GenError(f"bloc de modules introuvable : {olds}")
        if news:
            body = "".join(f"\n\t\t\t{n}" for n in news) + "\t# ZV: modules du mod (arbre, projets spéciaux)\n\t\t"
            return text[:m.start()] + m.group(1) + body + "}" + text[m.end():]
        return text[:m.start()] + "# ZV: earthshaker_bomb_release retiré (bombes sismiques du mod : zv_earthquake_bombs)" + text[m.end():]

    t = swap(t, ["jet_engine_1x"], jet)
    t = swap(t, ["jet_engine_axial_1x"], axial)
    t = swap(t, ["earthshaker_bomb_release"], [])
    old = """				has_tech = engines_2
				OR = {
					has_tech = improved_small_airframe
					has_tech = improved_medium_airframe
				}"""
    if old not in t:
        raise G.GenError("condition vanilla de sp_air_jet_engine introuvable")
    t = t.replace(old, "\t\t\t\thas_tech = engines_3\t# ZV: arbre (« Disponible si »)\n\t\t\t\thas_tech = zv_superchargers_2", 1)
    out["air_projects.txt"] = "# ZV Designer : généré par scripts/gen_techs.py à partir du vanilla 1.19.3.0.\n" + t
    p = ref / "common/special_projects/projects/rocket_projects.txt"
    t = p.read_text(encoding="utf-8-sig")
    t = swap(t, ["rocket_engine_1"], rocket)
    out["rocket_projects.txt"] = "# ZV Designer : généré par scripts/gen_techs.py à partir du vanilla 1.19.3.0.\n" + t
    return out


# ---------------------------------------------------------------- onglet Aviation

def roots():
    """Techs de l'onglet sans tech parente : chacune a besoin d'un gridbox <tech>_tree."""
    led = {k for kids in children().values() for k in kids}
    src_kept = {"basic_small_airframe", "improved_small_airframe", "advanced_small_airframe",
                "modern_small_airframe", "basic_medium_airframe", "improved_medium_airframe",
                "advanced_medium_airframe", "modern_medium_airframe", "basic_large_airframe",
                "improved_large_airframe", "advanced_large_airframe", "modern_large_airframe",
                "miniature_fighters", "aerial_hangars", "bba_strategic_airlifter", "sp_centrifugal_jet_tech"}
    out = []
    for col in sorted(T.TECH_COLUMNS):
        for tech in T.TECH_COLUMNS[col]:
            if tech in led or tech in src_kept or tech == "suicide_charge":
                continue
            if tech == "reinforced_wings_mothership" or tech == "supersonic_small_airframe":
                continue                          # vanilla : ouvertes par une autre tech
            out.append(tech)
    return out


def gen_treeview(ref):
    p = ref / "interface/countrytechtreeview.gui"
    t = p.read_text(encoding="utf-8-sig")
    folder = t.index('name = "bba_air_techs_folder"')
    end = t.index('name = "industry_folder"', folder)
    seg = t[folder:end]
    seg = re.sub(r"\n\t*gridboxtype = \{\s*name = \"(?!experimental_rockets_tree)\w+_tree\"[^{}]*?(?:\{[^{}]*\}[^{}]*?)*\}", "", seg)
    x0, y0 = T.TECH_ORIGIN
    width = (T.TECH_LAST_COLUMN + 1) * 70
    boxes = "".join(
        f"\n\t\t\tgridboxtype = {{\t# ZV: même origine pour tous les arbres (positions absolues)\n"
        f"\t\t\t\tname = \"{r}_tree\"\n\t\t\t\tposition = {{ x = {x0} y = {y0} }}\n"
        f"\t\t\t\tsize = {{ width = {width} height = 1150 }}\n\t\t\t\tslotsize = {{ width = 70 height = 70 }}\n"
        f"\t\t\t\tformat = \"UP\"\n\t\t\t}}\n" for r in roots())
    anchor = seg.rindex("\n\t\t}")
    seg = seg[:anchor] + boxes + seg[anchor:]
    seg = seg.replace("width = 2240 height = 1300", f"width = {width + x0 + 200} height = 1300", 1)
    years = sorted({y: r for y, r in T.TECH_ROWS.items()}.items(), key=lambda a: a[1])
    seen, labels = set(), []
    for year, row in years:
        if row in seen:
            continue
        seen.add(row)
        labels.append((year if year != 1922 else "1922-1926", row))

    def year_box(cont, xpos, fmtside):
        items = "".join(
            f"\t\t\t\tinstantTextBoxType = {{\n\t\t\t\t\tname = \"zv_airtech_year_{i}\"\n"
            f"\t\t\t\t\tposition = {{ x = {xpos} y = {70 * row + 20} }}\n\t\t\t\t\ttextureFile = \"\"\n"
            f"\t\t\t\t\tfont = \"hoi_36header\"\n\t\t\t\t\tborderSize = {{x = 0 y = 4}}\n\t\t\t\t\ttext = \"{y}\"\n"
            f"\t\t\t\t\tmaxWidth = 170\n\t\t\t\t\tmaxHeight = 32\n\t\t\t\t\tformat = {fmtside}\n"
            f"\t\t\t\t\tOrientation = \"UPPER_LEFT\"\n\t\t\t\t}}\n" for i, (y, row) in enumerate(labels))
        return items

    for cont, xpos, side in (("airtech_year_left", 30, "left"), ("airtech_year_right", 60, "right")):
        i0 = seg.index(f'name = "{cont}"')
        b0 = seg.index("instantTextBoxType", i0)
        close = seg.index("\n\t\t\t}", b0)
        seg = seg[:b0] + "# ZV: années de l'arbre du mod\n" + year_box(cont, xpos, side).lstrip("\t") + seg[close:]
    seg = seg.replace('name = "airtech_year_right"\n\t\t\t\tposition = { x=2000 y=25 }',
                      f'name = "airtech_year_right"\n\t\t\t\tposition = {{ x={width + x0} y=25 }}', 1)
    # Titres des groupes, centrés sur leurs colonnes (format center, 300 px de large).
    def center(c0, c1):
        return x0 + (c0 + c1 + 1) * 35 - 150
    titles = {"airtech_subtitle_airframe": center(0, 8), "airtech_subtitle_transport": center(10, 12),
              "airtech_subtitle_engines": center(13, 24), "airtech_subtitle_weapons": center(36, 49)}
    for name, xpos in titles.items():
        seg, n = re.subn(r'(name = "%s"\s*position = \{ x = )\d+' % name, r"\g<1>%d" % xpos, seg)
        if n != 1:
            raise G.GenError(f"titre {name} introuvable")
    i = seg.index('name = "airtech_subtitle_weapons"')
    start = seg.rindex("instantTextBoxType", 0, i)
    stop = seg.index("\n\t\t\t}", i) + len("\n\t\t\t}")
    block = seg[start:stop]
    block = block.replace("airtech_subtitle_weapons", "zv_airtech_subtitle_construction")
    block = block.replace('"AIR_TITLE_WEAPONS"', '"ZV_AIR_TITLE_CONSTRUCTION"')
    block = re.sub(r"position = \{ x = \d+", f"position = {{ x = {center(25, 35)}", block)
    seg = seg[:stop] + "\n\n\t\t\t# ZV: titre du groupe « Cellule et équipements »\n\t\t\t" + block + seg[stop:]
    t = t[:folder] + seg + t[end:]
    return "# ZV Designer : onglet Aviation généré par scripts/gen_techs.py (vanilla 1.19.3.0).\n" + t


# ---------------------------------------------------------------- icônes provisoires (phase 5)

def gen_tech_icons(ref):
    """Icône GFX_<tech>_medium de chaque tech nouvelle : celle de la tech vanilla la plus proche en
    remontant les prérequis, sinon celle du modèle du groupe. Provisoire, en attendant des .dds du mod."""
    gfx = (ref / "interface/Technologies.gfx").read_text(encoding="utf-8-sig")
    tex = dict(re.findall(r'name\s*=\s*"GFX_(\w+)_medium"\s*texturefile\s*=\s*"([^"]+)"', gfx, re.I))
    L = ["# ZV Designer : icônes provisoires des techs nouvelles, générées par scripts/gen_techs.py.",
         "# Chaque icône reprend une image vanilla (tech vanilla parente, ou modèle du groupe).", "spriteTypes = {"]
    for tid, t in MANAGED.items():
        if not tid.startswith("zv_"):
            continue
        todo, seen, src = list(t["prereqs"]), set(), None
        while todo and src is None:
            p = todo.pop(0)
            if p in seen:
                continue
            seen.add(p)
            if not p.startswith("zv_") and p in tex:
                src = p
            elif p in TECHS:
                todo += TECHS[p]["prereqs"]
        src = src or T.TECH_GROUPS[group_of(t)][1]
        L += ["\tSpriteType = {", f'\t\tname = "GFX_{tid}_medium"\t# image de {src}',
              f'\t\ttexturefile = "{tex[src]}"', "\t}"]
    return "\n".join(L + ["}"]) + "\n"


# ---------------------------------------------------------------- textes (phase 5)

def gen_tech_loc(lang):
    """Noms et descriptions des techs nouvelles (zv_) et titre du groupe Cellule et équipements."""
    en = lang == "english"
    k = 1 if en else 0
    E = G.E
    L = [f"l_{lang}:", f' ZV_AIR_TITLE_CONSTRUCTION:0 "{E.TEXTS["ZV_AIR_TITLE_CONSTRUCTION"][k]}"']
    for tid, t in MANAGED.items():
        if not tid.startswith("zv_") or tid in G.MODULE_IDS:   # même identifiant qu'un module : son texte sert aux deux
            continue
        name = E.TECH_EN[tid] if en else t["name"].replace(" (optionnelle)", "")
        mods = [E.name_en(m, G.MODS[m]["nom"]) if en else G.MODS[m]["nom"] for m in modules_of(tid)]
        desc = [E.TEXTS["unlocks"][k].format(", ".join(mods))] if mods else []
        if "optionnelle" in t["name"]:
            desc.append(E.TEXTS["optional"][k])
        L.append(f' {tid}:0 "{G.q(name)}"')
        L.append(f' {tid}_desc:0 "{G.q(" ".join(desc))}"')
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="F:/Github Local/HOI4-ref")
    ref = Path(ap.parse_args().ref)
    try:
        for f, text in gen_tech_files(ref).items():
            G.write(f"common/technologies/{f}", text)
        for f, text in gen_projects(ref).items():
            G.write(f"common/special_projects/projects/{f}", text)
        G.write("interface/countrytechtreeview.gui", gen_treeview(ref))
        G.write("interface/zv_technologies_icons.gfx", gen_tech_icons(ref))
        for lang in ("french", "english"):
            G.write(f"localisation/{lang}/zv_techs_l_{lang}.yml", gen_tech_loc(lang), bom=True)
    except G.GenError as e:
        sys.exit(f"ERREUR : {e}")
    print(f"arbres (gridbox) : {len(roots())}")


if __name__ == "__main__":
    main()

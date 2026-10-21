"""Contrôles du graphe tech <-> module et recomptages (§1, §3, §10.2-10.5 de la liste de contrôle)."""
import json, re, collections
from pathlib import Path

import sys
D = Path("data")
ARBRE = sys.argv[1] if len(sys.argv) > 1 else "docs/04-arbre-technologique.md"
mods = json.load(open(D / "modules_05.json"))
techs = json.load(open(D / "techs_arbre.json"))
arbre_txt = Path(ARBRE).read_text().splitlines()

# dossier de chaque tech d'après le titre de section précédant sa ligne
sections = []
for i, l in enumerate(arbre_txt, 1):
    if l.startswith("## "):
        sections.append((i, l[3:].strip()))
def section_of(line):
    s = None
    for i, name in sections:
        if i < line: s = name
    return s
for t in techs:
    t["folder"] = section_of(t["line"])

# 7 techs vanilla hors aviation (tableau à 3 colonnes)
VANILLA_HORS = {}
for l in arbre_txt:
    m = re.match(r"\| `([a-z_]+)` \| (\d{4}|—) \| (.+) \|$", l)
    if m:
        VANILLA_HORS[m.group(1)] = dict(year=int(m.group(2)) if m.group(2).isdigit() else None, modules_txt=m.group(3))

T = {t["id"]: t for t in techs}
PROJ = set(re.findall(r"^\| `(sp_[a-z_]+)` \|", "\n".join(arbre_txt), re.M))
ALL_T = set(T) | set(VANILLA_HORS) | PROJ
out = collections.OrderedDict()
R = lambda k, v: out.__setitem__(k, v)

R("techs_tableaux_principaux", len(techs))
R("techs_vanilla_hors_aviation", len(VANILLA_HORS))
R("techs_total", len(ALL_T))
outside = [t["id"] for t in techs if "autre dossier" in t["statut"] or "dossier" in t["name"].lower() and "(" in t["name"]]
R("techs_hors_dossiers_mod_dans_tableaux", outside)
by_folder = collections.Counter(t["folder"] for t in techs if t["id"] not in outside)
R("techs_par_section", dict(by_folder))
new = [t for t in techs if t["statut"].startswith("nouvelle")]
R("nouvelles", len(new))
R("vanilla_dans_tableaux", len(techs) - len(new))
R("nouvelles_par_section", dict(collections.Counter(t["folder"] for t in new)))
opt = [t["id"] for t in techs if "(optionnelle)" in t["name"]]
R("optionnelles", len(opt))
R("optionnelles_par_section", dict(collections.Counter(T[i]["folder"] for i in opt)))

# coefficients : 94 techs de modules = 99 gérées - cellules iw_ (3) - transports (2)
managed = [t for t in techs if t["id"] not in outside]
coef_scope = [t for t in managed if not t["id"].startswith("iw_") and not t["id"].startswith("bba_")]
R("perimetre_coefficients", len(coef_scope))
R("repartition_coefficients", dict(sorted(collections.Counter(t["coef"] for t in coef_scope).items())))
early_new = [t["id"] for t in new if t["year"] and t["year"] <= 1936]
R("nouvelles_1936_ou_avant", early_new)

# graphe module -> tech
mod_by_tech = collections.defaultdict(list)
for m in mods:
    mod_by_tech[m["tech"]].append(m["id"])
R("techs_citees_par_05_inexistantes", sorted(set(mod_by_tech) - ALL_T))
R("techs_sans_module_dans_05", sorted(ALL_T - set(mod_by_tech)))
year_mismatch = []
for m in mods:
    if m["tech"] in PROJ: continue
    ty = T[m["tech"]]["year"] if m["tech"] in T else VANILLA_HORS.get(m["tech"], {}).get("year")
    if ty != m["year"]:
        year_mismatch.append((m["id"], m["tech"], m["year"], ty))
R("annees_05_differentes_de_l_arbre", year_mismatch)

# prérequis
bad_pre, missing_pre = [], []
yr = {k: v["year"] for k, v in T.items()}
yr.update({k: v["year"] for k, v in VANILLA_HORS.items()})
for t in techs:
    for p in t["prereqs"]:
        if p not in yr:
            missing_pre.append((t["id"], p))
        elif yr[p] and t["year"] and yr[p] > t["year"]:
            bad_pre.append((t["id"], t["year"], p, yr[p]))
R("prerequis_inconnus", missing_pre)
R("tech_datee_avant_prerequis", bad_pre)
R("techs_a_deux_prerequis_ou_plus", [t["id"] for t in techs if len(t["prereqs"]) >= 2])
R("techs_avec_allow", {t["id"]: t["allow"] for t in techs if t["allow"]})

# nombre de modules par tech : 05 vs texte de l'arbre (estimation)
def estimate(txt):
    n = 0
    txt = re.sub(r"\(([^)]*)\)", lambda m: "(" + m.group(1).replace(",", ";") + ")", txt)
    for part in [p.strip() for p in txt.split(",") if p.strip()]:
        k = 1
        m = re.search(r"\((\d+)\)\s*$", part)
        if m: k = int(m.group(1))
        m2 = re.search(r"\(([SML](?:; [SML])*)\)", part)
        if m2: k = len(m2.group(1).split(";"))
        m3 = re.search(r"x1 à x4", part)
        if m3: k = 4
        m4 = re.search(r"x1; x2(; x4)?$|x1, x2(, x4)?$", part)
        n += k
    return n
cmp = []
for t in techs:
    est = estimate(t["modules_txt"])
    real = len(mod_by_tech.get(t["id"], []))
    if est != real:
        cmp.append((t["id"], real, est, t["modules_txt"][:120]))
R("ecarts_estimes_nb_modules_par_tech(a_revoir_a_la_main)", cmp)
R("modules_par_tech_05", {k: len(v) for k, v in sorted(mod_by_tech.items(), key=lambda x: -len(x[1]))})
Path("out").mkdir(exist_ok=True)
Path("out/check_graph.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
for k, v in out.items():
    if k == "modules_par_tech_05": continue
    print(f"- {k}: {v}")

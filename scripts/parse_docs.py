"""Extrait les tableaux des documents du projet ZV designer en JSON.

Sorties (dans data/) :
  modules_05.json  : un enregistrement par module de 05-stats-modules.md
  techs_arbre.json : un enregistrement par tech de 04-arbre-technologique.md
  inventaire.json  : lignes des tableaux de 04-inventaire-modules-avion.md
"""
import json, re, sys
from pathlib import Path

DOCS = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
OUT = Path("data"); OUT.mkdir(exist_ok=True)

def cells(line):
    line = line.strip()
    if not line.startswith("|"):
        return None
    parts = [c.strip() for c in line.strip("|").split("|")]
    return parts

# ---------- 05 ----------
mods = []
section = None
for ln, line in enumerate((DOCS / "05-stats-modules.md").read_text().splitlines(), 1):
    if line.startswith("## ") or line.startswith("### "):
        section = line.lstrip("#").strip()
        continue
    c = cells(line)
    if not c or not c[0].startswith("**"):
        continue
    m = re.match(r"\*\*(.+?)\*\*<br>`([^`]+)`", c[0])
    if not m:
        continue
    name, mid = m.group(1), m.group(2)
    # colonne tech : la cellule qui contient `tech` (année)
    tech, year = None, None
    for cell in c[1:]:
        t = re.fullmatch(r"`([^`]+)` \((\d{4}|projet)\)", cell)
        if t:
            tech, year = t.group(1), (int(t.group(2)) if t.group(2).isdigit() else "projet")
    rec = dict(line=ln, section=section, name=name, id=mid, tech=tech, year=year,
               gains=c[1] if len(c) > 1 else "", prix=c[2] if len(c) > 2 else "",
               regles=c[3] if len(c) > 3 else "", raw=c)
    rec["default"] = "— défaut" in name or "Aucun effet (module" in rec["gains"] and "défaut" in name
    rec["forbid"] = []
    fm = re.search(r"⛔ interdit : ([^|]+?)(?:<br>|$)", rec["regles"])
    if fm:
        rec["forbid_txt"] = fm.group(1).strip()
    mods.append(rec)
(OUT / "modules_05.json").write_text(json.dumps(mods, ensure_ascii=False, indent=1))

# ---------- 04-arbre ----------
techs = []
for ln, line in enumerate((DOCS / "04-arbre-technologique.md").read_text().splitlines(), 1):
    c = cells(line)
    if not c or len(c) != 7 or not c[0].startswith("`"):
        continue
    tid = c[0].strip("`")
    year = int(c[2]) if c[2].isdigit() else None
    coef = c[3].replace(",", ".")
    prereq_txt = c[4]
    allow = re.findall(r"si `([^`]+)`", prereq_txt)
    pre_part = prereq_txt.split(";")[0]
    prereqs = re.findall(r"`([^`]+)`", pre_part)
    techs.append(dict(line=ln, id=tid, name=c[1], year=year, coef=float(coef) if re.fullmatch(r"[\d.]+", coef) else coef,
                      prereqs=prereqs, allow=allow, modules_txt=c[5], statut=c[6]))
(OUT / "techs_arbre.json").write_text(json.dumps(techs, ensure_ascii=False, indent=1))

# ---------- 04-inventaire ----------
inv = []
section = None
header = None
for ln, line in enumerate((DOCS / "04-inventaire-modules-avion.md").read_text().splitlines(), 1):
    if line.startswith("#"):
        section = line.lstrip("#").strip(); header = None
        continue
    c = cells(line)
    if not c:
        continue
    if set("".join(c)) <= set("-: "):
        continue
    if header is None:
        header = c; continue
    inv.append(dict(line=ln, section=section, **{h: (c[i] if i < len(c) else "") for i, h in enumerate(header)}))
(OUT / "inventaire.json").write_text(json.dumps(inv, ensure_ascii=False, indent=1))

print(f"05 : {len(mods)} modules ; arbre : {len(techs)} techs ; inventaire : {len(inv)} lignes")

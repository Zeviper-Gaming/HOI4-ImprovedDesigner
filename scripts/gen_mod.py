"""Génère les fichiers du mod (mod/) à partir des données (data/*.json), de la table tenue à la
main (gen_mod_table.py) et des fichiers vanilla de HOI4-ref (lus, jamais modifiés).

Lancer depuis la racine :
  python -X utf8 scripts/gen_mod.py [--ref "F:/Github Local/HOI4-ref"]

Fichiers écrits :
  mod/common/units/equipment/plane_airframes.txt          (écrase le vanilla : cellules)
  mod/common/units/equipment/modules/00_plane_modules.txt (écrase le vanilla : modules)
  mod/common/technologies/zv_test_kit.txt                 (tech temporaire, phase 1)
  mod/localisation/french/zv_designer_l_french.yml        (UTF-8 avec BOM)

Le script s'arrête sur tout effet qu'il ne sait pas convertir sans ambiguïté : on complète
alors la table, on ne devine pas.
"""
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import gen_mod_table as T
import conversions
import traductions_en as E

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SLOTS = load("slots.json")["slots"]
CATS = load("categories.json")["categories_jeu"]          # nom de catégorie de jeu -> infos
MODS = {m["id"]: m for m in load("modules.json")}
PHANTOMS = load("modules_fantomes.json")["modules"]
CAT_ID = {name: c["id_propose"] for name, c in CATS.items()}

# Modules générés : le kit, puis tous les modules des catégories des phases déjà codées (ordre du 05).
MODULE_IDS = list(dict.fromkeys(T.KIT_PHASE_1 + [m for m, x in MODS.items()
                                                 if (T.PHASES_CATEGORIES is None
                                                     and x["categorie"] not in T.EXCLUDED_CATEGORIES)
                                                 or (T.PHASES_CATEGORIES and x["categorie"] in T.PHASES_CATEGORIES)]))


class GenError(Exception):
    pass


# ---------------------------------------------------------------- lecture du texte Paradox
# Découpe d'un bloc en entrées de premier niveau, avec leurs positions dans le texte, pour
# remplacer des morceaux du fichier vanilla sans toucher au reste (commentaires compris).

def _skip(text, i):
    while i < len(text):
        if text[i].isspace():
            i += 1
        elif text[i] == "#":
            while i < len(text) and text[i] != "\n":
                i += 1
        else:
            break
    return i


def _token_end(text, i):
    if text[i] == '"':
        return text.index('"', i + 1) + 1
    while i < len(text) and not text[i].isspace() and text[i] not in "{}=<>#":
        i += 1
    return i


def _block_end(text, i):
    """i pointe sur '{' ; renvoie l'indice qui suit l'accolade fermante."""
    depth = 0
    while i < len(text):
        c = text[i]
        if c == "#":
            while i < len(text) and text[i] != "\n":
                i += 1
            continue
        if c == '"':
            i = text.index('"', i + 1)
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise GenError("accolade non fermée")


def entries(text, lo, hi):
    """Entrées de premier niveau entre lo et hi : (clé, début, début_valeur, fin, est_bloc)."""
    out, i = [], _skip(text, lo)
    while i < hi:
        if text[i] == "}":
            break
        k_end = _token_end(text, i)
        key = text[i:k_end]
        j = _skip(text, k_end)
        if j < hi and text[j] in "=<>":
            j = _skip(text, j + (2 if text[j + 1] == "=" else 1))
            if text[j] == "{":
                end = _block_end(text, j)
                out.append((key, i, j, end, True))
            else:
                end = _token_end(text, j)
                out.append((key, i, j, end, False))
        else:                      # valeur nue dans une liste
            out.append((None, i, i, k_end, False))
            end = k_end
        i = _skip(text, end)
    return out


def inner(start_value, end):
    return start_value + 1, end - 1


# ---------------------------------------------------------------- catégories et slots

def game_cats(grouped, size):
    """Catégories de jeu (ids) d'une catégorie regroupée de la table des slots."""
    if grouped == "Rôle":
        return [CAT_ID[T.ROLE_CATEGORY[size]]]
    ids = [CAT_ID[n] for n, c in CATS.items() if c["categorie"] == grouped]
    if not ids:
        raise GenError(f"catégorie inconnue dans data/slots.json : {grouped}")
    return ids


def slots_for(size):
    res = []
    for s in SLOTS:                         # l'ordre de data/slots.json = ordre imposé (02 §1.9)
        if size not in s["tailles"]:
            continue
        grouped = list(s["categories"]) + [c for c, sizes in s["categories_selon_taille"].items()
                                           if size in sizes]
        cats = []
        for g in grouped:
            for c in game_cats(g, size):
                if c not in cats:
                    cats.append(c)
        res.append((s["id_propose"], s["id_propose"] in T.REQUIRED, cats, s["slot"]))
    return res


def module_slots_text(size, ind):
    t = "\t" * ind
    lines = [f"{t}module_slots = {{\t# ZV: slots du mod, dans l'ordre imposé par l'écran (02 §1.9)"]
    for sid, req, cats, name in slots_for(size):
        lines.append(f"{t}\t{sid} = {{\t# {name}")
        lines.append(f"{t}\t\trequired = {'yes' if req else 'no'}")
        lines.append(f"{t}\t\tallowed_module_categories = {{")
        lines += [f"{t}\t\t\t{c}" for c in cats]
        lines.append(f"{t}\t\t}}")
        lines.append(f"{t}\t}}")
    lines.append(f"{t}}}")
    return "\n".join(lines)


# ---------------------------------------------------------------- limites de taille

def allowed_sizes(m):
    """Archétypes où le module est permis (None = tous). Suffixe S/M/L et « Cellules : … »."""
    sizes = None
    if m.get("taille_suffixe"):
        sizes = set(T.SIZE_SUFFIX[m["taille_suffixe"]])
    for lim in m.get("regles", {}).get("limites", []):
        if lim.startswith("Cellules :"):
            s = set()
            for w in re.findall(r"petite|moyenne|grande", lim):
                s |= T.CELL_WORDS[w]
            sizes = s if sizes is None else sizes & s
        elif lim in T.LIMITE_PHRASES and T.LIMITE_PHRASES[lim][0] is not None:
            s = set(T.LIMITE_PHRASES[lim][0])
            sizes = s if sizes is None else sizes & s
    if m["categorie"] == "Rôle":        # réglé par la catégorie du slot Rôles
        return None
    return sizes


def limits_text(size, ind):
    """Limites du mod pour un archétype : tailles, limites partagées, une par design (09, 05)."""
    t = "\t" * ind
    out, seen = [], set()

    def limit(comment, conds, count, op="<"):
        key = (frozenset(conds), op)
        if key in seen:                          # deux limites aux mêmes conditions : le jeu n'en garderait qu'une
            return
        seen.add(key)
        out.append(f"{t}module_count_limit = {{\t# ZV: {comment}")
        out.extend(f"{t}\t{c}" for c in conds)
        out.extend([f"{t}\tcount {op} {count}", f"{t}}}"])

    def forbidden_here(mid):
        sizes = allowed_sizes(MODS[mid])
        return sizes is not None and size not in sizes

    for mid in MODULE_IDS:
        if forbidden_here(mid):
            limit(f"{MODS[mid]['nom']} interdit sur cette cellule", [f"module = {mid}"], 1)
    for text, (name, count) in T.SHARED_LIMIT_TEXT.items():
        mods = [mid for mid in MODULE_IDS if text in MODS[mid].get("regles", {}).get("limites", [])]
        if mods:
            limit(f"{text} ({name})", [f"module = {mid}" for mid in mods], count)
    generated_cats = {MODS[mid]["categorie"] for mid in MODULE_IDS}
    for grouped in T.ONE_PER_DESIGN:
        if grouped in generated_cats:
            for c in game_cats(grouped, size):
                limit(f"une seule {grouped} par design (09)", [f"category = {c}"], 2)
    for grouped in T.ONE_OF_EACH:
        for mid in MODULE_IDS:
            if MODS[mid]["categorie"] == grouped and not forbidden_here(mid):
                limit(f"un seul exemplaire ({grouped}, 05)", [f"module = {mid}"], 2)
    for mid in MODULE_IDS:                       # « 1 par design », « 2 par design »… (05)
        for lim in MODS[mid].get("regles", {}).get("limites", []):
            if lim in T.LIMITE_PHRASES and T.LIMITE_PHRASES[lim][1] is not None:
                _, n, on = T.LIMITE_PHRASES[lim]
                cat = CAT_ID[MODS[mid]["categorie_jeu"]]
                cond = f"module = {mid}" if on == "module" else f"category = {cat}"
                if on == "module" and forbidden_here(mid):
                    continue                     # la limite « interdit ici » porte les mêmes conditions (phase 7)
                limit(f"{MODS[mid]['nom']} : {lim} (05)", [cond], n + 1)
    for name, grouped, mods, counts in T.SIZE_LIMITS:   # limites d'armes par taille (05)
        n = counts[0 if size in "NP" else 1 if size == "M" else 2]
        if n is not None:
            limit(f"{name} : {n} au plus (05)", size_limit_conds(grouped, mods), n + 1)
    if size == "N" and T.CV_REQUIRED_MODULE in MODULE_IDS:
        limit("crosse d'appontage obligatoire sur la cellule embarquée (Q11)",
              [f"module = {T.CV_REQUIRED_MODULE}"], 0, ">")
    return "\n".join(out)


def size_limit_conds(grouped, mods):
    conds = []
    for g in grouped:
        conds += [f"category = {CAT_ID[n]}" for n, c in CATS.items() if c["categorie"] == g]
    conds += [f"module = {m}" for m in mods]
    return list(dict.fromkeys(conds))


def tier_limits_text(size, tier, ind):
    """Limites d'un palier : elles remplacent celles de l'archétype aux mêmes conditions
    (common/units/equipment/_documentation.md, l. 82)."""
    t = "\t" * ind
    out = []
    for name, grouped, mods, counts in T.SIZE_LIMITS:
        n = T.TIER_LIMITS.get(name, {}).get(tier)
        if n is not None and size in "NP":
            out.append(f"{t}module_count_limit = {{\t# ZV: {name} : {n} au plus au palier {tier} (Q7)")
            out += [f"{t}\t{c}" for c in size_limit_conds(grouped, mods)]
            out += [f"{t}\tcount < {n + 1}", f"{t}}}"]
    return "\n".join(out)


def upgrades_list(ind):
    t = "\t" * ind
    return f"{t}upgrades = {{\t# ZV: curseurs de puissance et de fiabilité (22/10)\n" + \
        "".join(f"{t}\t{u}\n" for u in T.CURSEURS) + f"{t}}}"


# ---------------------------------------------------------------- cellules

def gen_airframes(ref):
    src = ref / "common/units/equipment/plane_airframes.txt"
    text = src.read_text(encoding="utf-8-sig")
    eq = [e for e in entries(text, 0, len(text)) if e[0] == "equipments"][0]
    rep = []                                 # (début, fin, nouveau texte)
    found = set()
    small_stats = {}                         # Q11 : stats de la petite cellule terrestre
    for key, k0, v0, v1, is_blk in entries(text, *inner(eq[2], eq[3])):
        if is_blk and key.startswith("small_plane_airframe"):
            small_stats[key] = {e[0]: text[e[2]:e[3]] for e in entries(text, *inner(v0, v1))
                                if e[0] in T.CV_COPY_STATS and not e[4]}
    for key, k0, v0, v1, is_blk in entries(text, *inner(eq[2], eq[3])):
        if not is_blk:
            continue
        sub = entries(text, *inner(v0, v1))
        if key.startswith("cv_small_plane_airframe"):
            twin = small_stats.get(key[len("cv_"):], {})
            for k, s0, a, b, blk in sub:
                if k in twin and not blk and text[a:b] != twin[k]:
                    rep.append((a, b, f"{twin[k]}\t# ZV (Q11): valeur de la petite cellule terrestre "
                                      f"(vanilla {text[a:b]}), la crosse porte la pénalité"))
        is_arch = any(e[0] == "is_archetype" and text[e[2]:e[3]] == "yes" for e in sub)
        if is_arch:
            if key not in T.ARCHETYPES:
                raise GenError(f"archétype inattendu : {key}")
            size = T.ARCHETYPES[key]
            found.add(key)
            n_limits = sum(1 for e in sub if e[0] == "module_count_limit")
            for k, s0, a, b, blk in sub:
                if k == "type_override":
                    rep.append((a, b, f"{T.TYPE_OVERRIDE_SLOT}\t# ZV: la famille vient du slot Rôles"))
                elif k == "allowed_types":
                    body = "\n".join("\t\t\t" + x for x in T.ALLOWED_TYPES[size])
                    rep.append((a, b, "{\t# ZV: rôles du mod ajoutés (audit N-07)\n" + body + "\n\t\t}"))
                elif k == "fuel_consumption":
                    rep.append((a, b, "0\t# ZV: la consommation vient des moteurs (D-07)"))
                elif k == "module_slots":
                    limits = limits_text(size, 2)
                    new = module_slots_text(size, 2) + "\n" + upgrades_list(2)
                    new += "\n\t\t# ZV: limites vanilla retirées ; limites du mod ci-dessous"
                    if limits:
                        new += "\n" + limits
                    rep.append((s0, b, new.lstrip("\t")))
                elif k == "module_count_limit":
                    first = not any(r[2].startswith("# ZV: les") for r in rep if v0 <= r[0] < v1)
                    rep.append((s0, b, f"# ZV: les {n_limits} module_count_limit vanilla sont retirés" if first else ""))
                elif k == "default_modules":
                    rep.append((s0, b, "# ZV: default_modules vanilla retiré (slots vides, D-25)"))
        else:
            arch = next((text[e[2]:e[3]] for e in sub if e[0] == "archetype"), None)
            extra = upgrades_list(2)
            if arch in T.ARCHETYPES:
                tl = tier_limits_text(T.ARCHETYPES[arch], key.rsplit("_", 1)[-1], 2)
                if tl:
                    extra += "\n" + tl
            rep.append((v1 - 1, v1 - 1, "\t" + extra.lstrip("\t") + "\n\t"))   # avant l'accolade fermante
            for k, s0, a, b, blk in sub:
                if k == "module_slots" and blk:
                    rep.append((a, b, "inherit\t# ZV: mêmes slots à tous les paliers (02 §1.4)"))
                elif k == "default_modules":
                    rep.append((s0, b, "# ZV: default_modules vanilla retiré (slots vides, D-25)"))
    if found != set(T.ARCHETYPES):
        raise GenError(f"archétypes manquants : {set(T.ARCHETYPES) - found}")
    for a, b, new in sorted(rep, reverse=True):
        text = text[:a] + new + text[b:]
    text = re.sub(r"\n(?:[ \t]*\n){2,}", "\n\n", text)   # lignes vides laissées par les retraits
    head = ("# ZV Designer : fichier généré par scripts/gen_mod.py à partir du vanilla 1.19.3.0.\n"
            "# Ne pas modifier à la main : corriger les données ou la table, puis relancer.\n")
    return head + text


# ---------------------------------------------------------------- doublons de rôle

def obligation_text(type_, ind):
    t = "\t" * ind
    grouped, mods = T.ROLE_OBLIGATIONS.get(type_, ([], []))
    conds = size_limit_conds(grouped, [m for m in mods if m in MODULE_IDS])
    if not conds:
        return ""
    return "\n".join([f"{t}module_count_limit = {{\t# ZV: rôle {type_} : au moins un de ces modules (05)"]
                      + [f"{t}\t{c}" for c in conds] + [f"{t}\tcount > 0", f"{t}}}"])


def gen_duplicates(ref):
    """x_plane_airframes.txt vanilla + obligations des rôles + doublons des rôles nouveaux."""
    src = ref / "common/units/equipment/x_plane_airframes.txt"
    text = src.read_text(encoding="utf-8-sig")
    dup = [e for e in entries(text, 0, len(text)) if e[0] == "duplicate_archetypes"][0]
    rep = []
    for key, k0, v0, v1, is_blk in entries(text, *inner(dup[2], dup[3])):
        if not is_blk:
            continue
        sub = {e[0]: text[e[2]:e[3]] for e in entries(text, *inner(v0, v1)) if not e[4]}
        if sub.get("only_duplicate_archetype") == "yes" or sub.get("archetype") not in T.ARCHETYPES:
            continue
        ob = obligation_text(sub.get("type"), 2)
        if ob:
            rep.append((v1 - 1, v1 - 1, "\t" + ob.lstrip("\t") + "\n\t"))
    new = ["", "\t# ZV Designer : doublons des rôles du mod sans équivalent vanilla (audit N-07)."]
    for name, d in T.NEW_DUPLICATES.items():
        new += [f"\t{name} = {{", f"\t\tarchetype = {d['archetype']}", f"\t\ttype = {d['type']}"]
        if d.get("picture"):
            new.append(f"\t\tpicture = {d['picture']}")
        if d.get("sprite"):
            new.append(f"\t\tsprite = {d['sprite']}")
        if d.get("sup0"):
            new += ["\t\tfor_each = {", "\t\t\tair_superiority = { set = 0 }", "\t\t}"]
        new += [f"\t\tair_map_icon_frame = {d['frame']}", f"\t\tinterface_overview_category_index = {d['index']}"]
        if d.get("substitute"):
            new.append(f"\t\tsubstitute = {d['substitute']}")
        if d.get("no_training"):
            new.append("\t\tforbid_mission_type = training")
        ob = obligation_text(d["type"], 2)
        if ob:
            new.append(ob)
        new.append("\t}")
    rep.append((dup[3] - 1, dup[3] - 1, "\n".join(new) + "\n"))
    for a, b, s in sorted(rep, reverse=True):
        text = text[:a] + s + text[b:]
    head = ("# ZV Designer : fichier généré par scripts/gen_mod.py à partir du vanilla 1.19.3.0.\n"
            "# Doublons vanilla inchangés, plus les obligations des rôles et les doublons des rôles du mod.\n")
    return head + text


def all_duplicate_types():
    """Doublons de rôle de chaque archétype du mod (vanilla + nouveaux), pour les techs (phase 4)."""
    return list(T.NEW_DUPLICATES)


# ---------------------------------------------------------------- modules

def num(v):
    v = v.replace("−", "-").replace(",", ".").replace("+", "").strip()
    return float(v)


def fmt(x):
    x = round(x, 4)
    return str(int(x)) if x == int(x) else f"{x:g}"


def interdits(m):
    """Catégories interdites (ids). Reconstruit « configurations des classes B, C et D »."""
    raw = ", ".join(m.get("regles", {}).get("interdit", []))
    out = []
    mt = re.search(r"configurations des classes ([A-D](?:, [A-D])*(?: et [A-D])?)", raw)
    if mt:
        classes = re.findall(r"[A-D]", mt.group(1))
        out += [CAT_ID[n] for n in CATS if n.startswith("Motorisation") and n[-1] in classes]
        raw = raw.replace(mt.group(0), "")
    for name in [x.strip() for x in raw.split(",") if x.strip()]:
        if name in T.INTERDIT_PHRASES:
            out += [CAT_ID[n] for n in (T.INTERDIT_PHRASES[name] or [])]
        elif name in CAT_ID:
            out.append(CAT_ID[name])
        elif name in {c["categorie"] for c in CATS.values()}:
            out += [CAT_ID[n] for n, c in CATS.items() if c["categorie"] == name]
        else:
            mo = re.fullmatch(r"(Motorisation \(.*\))", name)
            ma = re.fullmatch(r"Aile \((.*)\)", name)
            if mo:
                out += [CAT_ID[n] for n in CATS if n.startswith(mo.group(1) + " –")]
            elif ma and f"Aile — {ma.group(1)}" in CAT_ID:
                out.append(CAT_ID[f"Aile — {ma.group(1)}"])
            else:
                raise GenError(f"{m['id']} : interdiction non reconnue « {name} »")
    return list(dict.fromkeys(out))


def missions_of(phrase, mid):
    """Missions d'une formulation « en … : » du 05."""
    if phrase in T.MISSION_GROUPS:
        return list(T.MISSION_GROUPS[phrase])
    out = []
    for part in re.split(r", | et ", phrase):
        part = part.strip()
        if part in T.MISSION_GROUPS:
            out += T.MISSION_GROUPS[part]
        elif part in T.MISSIONS:
            out.append(T.MISSIONS[part])
        elif part == "stratégique" and out and out[-1] == "naval_bomber":   # « frappe navale et stratégique »
            out.append("strategic_bomber")
        else:
            raise GenError(f"{mid} : mission inconnue « {part} » dans « {phrase} »")
    return list(dict.fromkeys(out))


def _effect(block, stat, val, avg, mid, txt):
    """Range un effet (« +2 % », « 11 par moteur », « ×1,55 celle d'un moteur »…) dans un bloc."""
    if (mx := re.fullmatch(r"×([\d,]+) celle d'un moteur", val)):
        key, v = "mult", num(mx.group(1))
    elif (mp := re.fullmatch(r"([+−-]?[\d,]+) %( du coût total)?", val)):
        key, v = "mult", num(mp.group(1)) / 100
    elif (ma := re.fullmatch(r"([+−-]?[\d,]+)( par moteur| IC)?", val)):
        key, v = ("avg" if avg else "add"), num(ma.group(1))
    else:
        raise GenError(f"{mid} : valeur non convertie « {val} » ({txt})")
    block[key][stat] = block[key].get(stat, 0) + v


PART = re.compile(r"(?P<lib>[^(]+?) \(`(?P<stat>\w+)`(?P<avg>, moyenne)?\) (?P<val>.+)")


def effects(m):
    """Effets d'un module : bloc permanent, blocs par missions, ressources (texte du 05)."""
    mid = m["id"]
    perm = {"add": {}, "mult": {}, "avg": {}}
    by_mission, resources, cost_ic = {}, {}, None
    for item in m["gains"] + m["prix"]:
        txt = item["texte"]
        body = txt[2:].strip()                       # sans l'emoji 🟢 / 🔴 / ⚪
        if "Aucun effet" in body:
            continue
        if (mc := re.match(r"Coût [\d,]+ IC par moteur \(([+−-]?[\d,]+) dans le module", body)):
            cost_ic = num(mc.group(1))
            continue
        if (mt := re.match(r"Coût ([\d,]+) IC \(\d+ × \d+ \+ installation \d+\)", body)):
            cost_ic = num(mt.group(1))
            continue
        if (mr := re.fullmatch(r"(\w+) ([+−-][\d,]+)", body)) and mr.group(1) in T.RESOURCES:
            res = T.RESOURCES[mr.group(1)]
            resources[res] = resources.get(res, 0) + num(mr.group(2))
            continue
        if (mm := re.match(r"en (.+?) : (.+)$", body)):
            ms = tuple(missions_of(mm.group(1), mid))
            block = by_mission.setdefault(ms, {"add": {}, "mult": {}, "avg": {}})
            parts = re.split(r", (?=[A-ZÉÈÀ])", mm.group(2))
        else:
            block, parts = perm, [body]
        for p in parts:
            pm = PART.fullmatch(p.strip())
            if not pm:
                raise GenError(f"{mid} : effet non converti « {txt} » (ligne {m['ligne_05']} du 05)")
            _effect(block, pm["stat"], pm["val"].strip(), bool(pm["avg"]), mid, txt)
    if cost_ic:
        perm["add"]["build_cost_ic"] = perm["add"].get("build_cost_ic", 0) + cost_ic
    if m["categorie_jeu"] == "Moteur":
        # Astuce des moteurs (03) : le moteur annule sa propre poussée et sa consommation.
        perm["mult"]["thrust"] = perm["mult"].get("thrust", 0) - 1
        perm["mult"]["fuel_consumption"] = perm["mult"].get("fuel_consumption", 0) - 1
        # Curseurs (05 « Réglages ») : le cran d'usine (5) est rendu neutre ici, slot obligatoire.
        for u in T.CURSEURS.values():
            for kind, key in (("add", "add"), ("mult", "mult")):
                for stat, v in u[kind].items():
                    perm[key][stat] = perm[key].get(stat, 0) - T.CURSEUR_USINE * v
    return perm, by_mission, resources


def xp_cost(m):
    """Coût en expérience du module (règle du vanilla, références gratuites : gen_mod_table)."""
    if m.get("reference"):
        return T.XP_REFERENCE
    if m["id"] in T.XP_BY_MODULE:
        return T.XP_BY_MODULE[m["id"]]
    if m["categorie"] in T.XP_GUNS:
        return 2 if re.search(T.XP_GUNS[m["categorie"]], m["id"]) else 1
    return T.XP_BY_CATEGORY.get(m["categorie"], T.XP_DEFAULT)


def module_text(m, abbr):
    t = "\t\t"
    perm, by_mission, resources = effects(m)
    cat = CAT_ID[m["categorie_jeu"]]
    sfx = "sfx_ui_sd_module_engine" if m["categorie"] in ("Moteur", "Motorisation") else "sfx_ui_sd_module_turret"
    L = [f"\t{m['id']} = {{\t# {m['nom']} (05, ligne {m['ligne_05']})",
         f'{t}abbreviation = "{abbr}"', f"{t}category = {cat}", f"{t}sfx = {sfx}",
         f"{t}xp_cost = {xp_cost(m)}"]
    deb = m.get("regles", {}).get("debloque", [])
    types = [re.search(r"type `(\w+)`", d).group(1) for d in deb if d.startswith("type ")]
    if types:
        L.append(f"{t}add_equipment_type = {{ {' '.join(types)} }}")
    def blocks(b, ind):
        out = []
        for name, key in (("add_stats", "add"), ("multiply_stats", "mult"), ("add_average_stats", "avg")):
            if b[key]:
                out.append(f"{ind}{name} = {{")
                out += [f"{ind}\t{k} = {fmt(v)}" for k, v in b[key].items()]
                out.append(f"{ind}}}")
        return out
    L += blocks(perm, t)
    if m["categorie_jeu"] == "Moteur":
        L.append(f"{t}# ZV: les effets ci-dessus comptent −{T.CURSEUR_USINE} crans de chaque curseur "
                 f"(cran {T.CURSEUR_USINE} = usine, neutre)")
    for ms, b in by_mission.items():
        L.append(f"{t}mission_type_stats = {{")
        L.append(f"{t}\tlimit = {{ {' '.join(ms)} }}")
        L += blocks(b, t + "\t")
        L.append(f"{t}}}")
    if resources:
        L.append(f"{t}build_cost_resources = {{")
        L += [f"{t}\t{k} = {fmt(v)}" for k, v in resources.items()]
        L.append(f"{t}}}")
    for d in deb:
        if d.startswith("missions :"):
            ms = [T.MISSIONS[re.sub(r"\s*\(.*\)$", "", x).strip()] for x in d.split(":", 1)[1].split(",")]
            L.append(f"{t}allow_mission_type = {{ {' '.join(ms)} }}")
    forb = interdits(m)
    if forb:
        L.append(f"{t}forbid_module_categories = {{")
        L += [f"{t}\t{c}" for c in forb]
        L.append(f"{t}}}")
    L += conversions.text(m["id"], t)            # règles de conversion (Q28, scripts/conversions.py)
    L.append("\t}")
    return "\n".join(L)


def gen_modules():
    conversions.init(sys.modules[__name__])
    order = list(MODS)
    L = ["# ZV Designer : fichier généré par scripts/gen_mod.py (données : data/modules.json, docs/05).",
         "# Ne pas modifier à la main. Écrase le 00_plane_modules.txt vanilla.",
         "equipment_modules = {", "\tlimit = {", '\t\thas_dlc = "By Blood Alone"', "\t}", ""]
    for mid in MODULE_IDS:
        L.append(module_text(MODS[mid], "z" + format(order.index(mid), "03x")))
        L.append("")
    L.append("\t# Modules fantômes (décision D-14) : identifiants vanilla encore cités par des techs")
    L.append("\t# non écrasées ; leur catégorie n'est acceptée par aucun slot.")
    for i, p in enumerate(PHANTOMS):
        L.append(f'\t{p["id"]} = {{ abbreviation = "zf{i:02d}" category = {T.PHANTOM_CATEGORY} }}'
                 f'\t# cité par {p["cite_par"]}')
    L.append("}")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- tech temporaire, localisation

def gen_test_tech():
    mods = "\n".join("\t\t\t" + m for m in MODULE_IDS)
    # Onglet Aviation : la tech a son propre gridbox zv_test_kit_tree dans mod/interface/
    # countrytechtreeview.gui (x = 815, colonne vide en 1933-1936) ; y = 2 = ligne de 1933.
    # Coût quasi nul : recherchée en un jour ou deux, sans console.
    return ("# ZV Designer : tech TEMPORAIRE du contrôle rapide n° 1 (phase 1), retirée en phase 4.\n"
            "technologies = {\n"
            f"\t{T.TEST_TECH} = {{\n\t\tenable_equipment_modules = {{\n{mods}\n\t\t}}\n"
            "\t\tresearch_cost = 0.01\n\t\tstart_year = 1922\n"
            "\t\tfolder = {\n\t\t\tname = bba_air_techs_folder\n\t\t\tposition = { x = 0 y = 2 }\n\t\t}\n"
            "\t\tcategories = { air_equipment }\n"
            "\t\tai_will_do = { factor = 0 }\n\t}\n}\n")


def gen_icons(ref):
    src = (ref / "interface/plane_modules_icons.gfx").read_text(encoding="utf-8-sig")
    tex = dict(re.findall(r'name\s*=\s*"(GFX_EMI_\w+)"\s*\n\s*texture[Ff]ile\s*=\s*"([^"]+)"', src))
    L = ["# ZV Designer : icônes des modules, slots et catégories, générées par scripts/gen_mod.py.",
         "# Images du mod (style C3, scripts/icones/gen_icons.py) ; à défaut, image vanilla provisoire.",
         "spriteTypes = {"]
    real = "gfx/interface/equipmentdesigner/planes/modules/zv"

    def sprite(name, texture):
        L.extend(["\tspriteType = {", f'\t\tname = "{name}"', f'\t\ttextureFile = "{texture}"',
                  "\t\tlegacy_lazy_load = no", "\t}"])

    for s in SLOTS:                          # slots vides (le slot Rôles garde l'icône vanilla)
        sid = s["id_propose"]
        if (MOD / real / "slots" / f"{sid}.dds").exists():
            sprite(f"GFX_EMSI_{sid}", f"{real}/slots/{sid}.dds")
        elif sid == "fixed_zv_role":
            sprite(f"GFX_EMSI_{sid}", "gfx/interface/equipmentdesigner/planes/plane_role_module.dds")
    for name, c in CATS.items():             # catégories : l'image d'un module typique, comme le vanilla
        mods = [m for m in c["modules"] if m in MODULE_IDS and (MOD / real / f"{m}.dds").exists()]
        if mods:
            sprite(f"GFX_EMI_{c['id_propose']}", f"{real}/{mods[0]}.dds")
    for mid in MODULE_IDS:
        if not mid.startswith("zv_") and f"GFX_EMI_{mid}" in tex:
            continue                         # identifiant vanilla gardé : son icône existe déjà
        if (MOD / real / f"{mid}.dds").exists():
            sprite(f"GFX_EMI_{mid}", f"{real}/{mid}.dds")
            continue
        borrowed = T.ICONES_PROVISOIRES.get(mid)
        for pattern, sprite in ([] if borrowed else T.ICONES_REGLES):
            if (mr := re.match(pattern, mid)):
                borrowed = sprite(mr) if callable(sprite) else sprite
                break
        if borrowed is None:
            raise GenError(f"{mid} : pas d'icône provisoire dans la table")
        if borrowed not in tex:
            raise GenError(f"{mid} : sprite vanilla introuvable {borrowed}")
        L += ["\tspriteType = {", f'\t\tname = "GFX_EMI_{mid}"', f'\t\ttextureFile = "{tex[borrowed]}"',
              "\t\tlegacy_lazy_load = no", "\t}"]
    L.append("}")
    return "\n".join(L) + "\n"


def gen_upgrades():
    """Curseurs (05 « Réglages », décision du 22/10/2026) : effet égal à chaque cran."""
    L = ["# ZV Designer : curseurs de puissance et de fiabilité, générés par scripts/gen_mod.py.",
         f"# Crans 0 à {T.CURSEUR_MAX} ; le cran {T.CURSEUR_USINE} (usine) est neutralisé dans les modules de moteur.",
         "# Modèle : tank_nsb_engine_upgrade (land_upgrades.txt) ; multiplicateurs au premier niveau",
         "# comme plane_engine_upgrade (air_upgrades.txt).",
         "upgrades = {"]
    for uid, u in T.CURSEURS.items():
        L += [f"\t{uid} = {{\t# {u['nom']}", f'\t\tabbreviation = "{u["abbr"]}"',
              f"\t\tmax_level = {T.CURSEUR_MAX}", "\t\tcost = air",
              "\t\tlinear_cost = {\t# ZV: aucun coût en expérience par cran (🧪)",
              "\t\t\tcost_by_level = 0", "\t\t\tcost_by_level_for_licensed_equipment = 0", "\t\t}"]
        L += [f"\t\t{k} = {fmt(v)}" for k, v in u["mult"].items()]
        L.append("\t\tadd_stats = {")
        L += [f"\t\t\t{k} = {fmt(v)}" for k, v in u["add"].items()]
        L += ["\t\t}", "\t}"]
    L.append("}")
    return "\n".join(L) + "\n"


def q(s):
    return s.replace('"', "”")


# Phrases de la colonne « Pourquoi » qui sont des notes de conception, pas du texte de jeu.
DESC_NOTES = ("🧪", "❓", "décision", "aleurs vanilla", "aleur vanilla", "identifiant conservé",
              "Débloquée par", "Valeurs proches de", "coût ramené", "à vérifier")


def desc_text(m):
    """Description en jeu : la colonne « Pourquoi » du 05 sans les notes vanilla ni les notes de travail."""
    d = (m.get("pourquoi") or "").split("<br>")[0].strip()
    d = re.sub(r"\s*\((décision[^)]*|catégorie à part[^)]*|proposition de l'arbre)\)", "", d)
    return " ".join(p for p in re.split(r"(?<=[.!?])\s+", d) if not any(k in p for k in DESC_NOTES)).strip()


def vanilla_twin(m):
    """Module vanilla dont le module du mod reprend les valeurs (« *vanilla : X* » du 05)."""
    r = re.search(r"\*vanilla : (\w+)\*", m.get("pourquoi") or "")
    return r[1] if r else None


def vanilla_loc_keys(ref):
    """Clés des textes vanilla (localisation française de HOI4-ref : les mêmes existent en anglais)."""
    keys = set()
    for p in (ref / "localisation/french").glob("*.yml"):
        keys |= set(re.findall(r"^ ([\w.]+):\d* ", p.read_text(encoding="utf-8-sig"), re.M))
    return keys


# Paliers des cellules (plane_airframes.txt vanilla) : la petite va jusqu'au palier 5 (supersonique).
AIRFRAME_TIERS = {"small_plane_airframe": 6, "cv_small_plane_airframe": 5, "medium_plane_airframe": 5,
                  "large_plane_airframe": 5}


def gen_loc(lang, vkeys):
    """Textes du mod. Les modules vanilla gardés (sans zv_) gardent les textes du jeu ; un module du mod
    sans description reprend celle du module vanilla dont il copie les valeurs, s'il y en a un."""
    en = lang == "english"
    k = 1 if en else 0
    L = [f"l_{lang}:"]
    for uid, u in T.CURSEURS.items():
        L.append(f' {uid}:0 "{E.CURSEUR_EN[u["nom"]] if en else u["nom"]}"')
        L.append(f' {uid}_desc:0 "{q(E.CURSEUR_DESC[uid][k])}"')
    for s in SLOTS:
        L.append(f' EQ_MOD_SLOT_{s["id_propose"]}_TITLE:0 "{q(E.SLOT_EN[s["slot"]] if en else s["slot"])}"')
    for name, c in CATS.items():
        L.append(f' EQ_MOD_CAT_{c["id_propose"]}_TITLE:0 "{q(E.category_en(name) if en else name)}"')
    for mid in MODULE_IDS:
        m = MODS[mid]
        if not mid.startswith("zv_") and mid in vkeys:
            continue
        d = desc_text(m)
        d = q(E.DESC_EN[d] if en and d else d)
        if not d and f"{vanilla_twin(m)}_desc" in vkeys:
            d = f"${vanilla_twin(m)}_desc$"
        L.append(f' {mid}:0 "{q(E.name_en(mid, m["nom"]) if en else m["nom"])}"')
        L.append(f' {mid}_desc:0 "{d}"')
    for dup, d in T.NEW_DUPLICATES.items():
        arch = d["archetype"]
        role = E.DUP_ROLE[dup][k]
        for n in range(AIRFRAME_TIERS[arch]):
            if n == 5:
                L.append(f' {dup}_5:0 "${arch}_5$"')
            else:
                name = (E.TIER_EN if en else E.TIER_FR)[n].format(role)
                L.append(f' {dup}_{n}:0 "{q(name[0].upper() + name[1:])}"')
            L.append(f' {dup}_{n}_desc:0 "${arch}_{n}_desc$"')
    return "\n".join(L) + "\n"


def missing_desc_en():
    """Descriptions françaises sans traduction anglaise (contrôle de phase 5)."""
    return sorted({desc_text(MODS[m]) for m in MODULE_IDS} - set(E.DESC_EN) - {""})


# ---------------------------------------------------------------- écriture

def write(rel, content, bom=False):
    p = MOD / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes((b"\xef\xbb\xbf" if bom else b"") + content.encode("utf-8"))
    print(f"écrit : mod/{rel}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="F:/Github Local/HOI4-ref")
    ref = Path(ap.parse_args().ref)
    try:
        write("common/units/equipment/plane_airframes.txt", gen_airframes(ref))
        write("common/units/equipment/x_plane_airframes.txt", gen_duplicates(ref))
        write("common/units/equipment/modules/00_plane_modules.txt", gen_modules())
        vkeys = vanilla_loc_keys(ref)
        for lang in ("french", "english"):
            write(f"localisation/{lang}/zv_designer_l_{lang}.yml", gen_loc(lang, vkeys), bom=True)
        write("interface/zv_plane_modules_icons.gfx", gen_icons(ref))
        write("common/units/equipment/upgrades/zv_plane_upgrades.txt", gen_upgrades())
    except GenError as e:
        sys.exit(f"ERREUR : {e}")
    for a in T.ARCHETYPES:
        print(f"{a} : {len(slots_for(T.ARCHETYPES[a]))} slots")


if __name__ == "__main__":
    main()

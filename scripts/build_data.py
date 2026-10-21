"""Construit les données machine du mod à partir des documents (docs/) :

  data/modules.json    : les 392 modules du 05, avec catégorie, sous-catégorie (catégorie exacte du jeu),
                         tech, année, effets décomposés, règles (débloque, interdit, limite) et texte brut
  data/categories.json : les catégories du mod (68 regroupées ; 17 de motorisation, 6 d'aile, 3 de rôle en détail)
  data/slots.json      : les 32 slots (ordre d'écran, fixe ou libre, tailles, catégories acceptées)
  data/techs.json      : les techs de l'arbre (copie enrichie de techs_arbre.json)

Lancer depuis la racine : python3 scripts/parse_docs.py docs && python3 scripts/build_data.py
Les documents font foi : en cas d'écart, corriger le document puis relancer.
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import slots_proposal as SP  # noqa: E402

mods = json.load(open("data/modules_05.json"))

# ---------- catégorie de chaque module ----------
WING_CAT = {"basse": "Basse", "mediane": "Médiane", "haute": "Haute / Parasol", "parasol": "Haute / Parasol",
            "biplan": "Autres", "sesquiplan": "Autres", "triplan": "Autres", "sans_queue": "Avancée", "canard": "Canard"}
TUR = {"lmg_defense_turret": "Tourelle x1", "hmg_defense_turret": "Tourelle x1", "cannon_defense_turret": "Tourelle x1",
       "lmg_defense_turret_2x": "Tourelle x2", "hmg_defense_turret_2x": "Tourelle x2", "cannon_defense_turret_2x": "Tourelle x2",
       "zv_lmg_defense_turret_4x": "Tourelle x4", "zv_hmg_defense_turret_4x": "Tourelle x4"}
EXACT = {
    "zv_prop_variable_pitch": "Module d'hélice", "zv_prop_feathering": "Module d'hélice",
    "zv_naca_cowling": "Carénage moteur", "zv_air_intake": "Prise d'air", "zv_rato": "Aide au décollage",
    "zv_takeoff_trolley": "Train d'atterrissage", "zv_deicing_boots": "Dégivrage", "zv_heated_leading_edges": "Dégivrage",
    "zv_wooden_monocoque": "Matériaux", "zv_tube_and_fabric": "Matériaux",
    "zv_fowler_flaps": "Volets", "zv_leading_edge_slats": "Becs de bord d'attaque",
    "zv_floats": "Train d'atterrissage", "zv_skis": "Train d'atterrissage", "zv_carrier_equipment": "Équipement naval",
    "zv_armored_cockpit": "Blindage du cockpit", "zv_ejection_seat": "Siège éjectable",
    "zv_bomb_bay_tank": "Réservoir supplémentaire", "zv_ferry_tank": "Réservoir supplémentaire",
    "torpedo_mounting": "Armes navales", "torpedo_mounting_2": "Armes navales", "torpedo_mounting_3": "Armes navales",
    "zv_depth_charges": "Armes navales", "zv_fido": "Armes navales",
    "guided_anti_ship_missile": "Armes guidées", "zv_fritz_x": "Armes guidées", "zv_hs293": "Armes guidées",
    "airdropped_mines": "Armes spéciales", "fixed_explosive_charge": "Armes spéciales",
    "zv_schraege_musik": "Armes spéciales", "demining_coil": "Armes spéciales",
    "bomb_sights_1": "Viseur de bombardement", "bomb_sights_2": "Viseur de bombardement",
    "radio_navigation_1": "Navigation", "radio_navigation_2": "Navigation", "zv_asv_radar": "Radar",
    "zv_window": "Contre-mesures", "zv_monica": "Alerte radar", "zv_naxos": "Alerte radar", "zv_iff": "Identification",
    "zv_radar_altimeter": "Aides au pilotage", "zv_autopilot": "Aides au pilotage", "zv_radio_telephone": "Radio",
    "recon_camera": "Reconnaissance", "zv_night_photo": "Reconnaissance",
    "zv_leigh_light": "Anti-sous-marin", "zv_mad": "Anti-sous-marin", "zv_sonobuoys": "Anti-sous-marin",
    "zv_cargo_bay": "Soute de transport", "zv_troop_compartment": "Soute de transport",
    "zv_supply_drop": "Largage de ravitaillement",
    "zv_hand_mg_light": "Mitrailleuse à main", "zv_hand_mg_heavy": "Mitrailleuse à main",
    "zv_gm1": "Alimentation", "zv_direct_injection": "Alimentation", "zv_anti_g_carburettor": "Alimentation",
}
PREFIX = [  # (regex sur l'id, catégorie), dans l'ordre
    (r"zv_engine_config_", "Motorisation"), (r"zv_engine_power_", "Réglage de puissance"),
    (r"zv_reliability_", "Réglage de fiabilité"), (r"zv_engine_", "Moteur"), (r"zv_prop_", "Hélice"),
    (r"zv_(early_|improved_|two_stage_)?(super|turbo)charger", "Alimentation"),
    (r"zv_(high_octane_fuel|water_injection)_", "Alimentation"), (r"zv_wep_", "Régime d'urgence"),
    (r"zv_radiator_", "Refroidissement"), (r"zv_auto_extinguisher_", "Sécurité incendie"),
    (r"zv_fuselage_", "Fuselage"), (r"zv_tail_", "Empennage"), (r"zv_armor_plate_", "Blindage"),
    (r"zv_non_strategic_materials_", "Matériaux"), (r"zv_(lightweight|reinforced)_construction_", "Construction"),
    (r"zv_combat_flaps_", "Volets"), (r"zv_dive_brakes_", "Aérofreins"), (r"zv_aerodynamic_pylons_", "Pylônes"),
    (r"zv_gear_", "Train d'atterrissage"), (r"zv_wing_", "Aile"), (r"zv_cockpit_", "Cockpit"),
    (r"zv_(self_sealing_)?fuel_tanks_", "Réservoir interne"), (r"zv_drop_tanks_", "Réservoir supplémentaire"),
    (r"zv_nose_(light|heavy)_", "Mitrailleuses de nez"), (r"zv_nose_cannon_", "Canons de nez"),
    (r"zv_nose_at_cannon_", "Canon AT de nez"), (r"zv_(light|heavy)_", "Mitrailleuses"), (r"zv_cannon_", "Canons"),
    (r"zv_at_cannon_", "Canon AT"), (r"zv_rockets_", "Roquettes"), (r"zv_bomb_locks_", "Attaches"),
    (r"zv_bomb_bay_", "En soute"), (r"zv_(reflex|attack|gyro)_gunsight_", "Viseur de tir"),
    (r"air_(ground|air)_radar_", "Radar"), (r"zv_ball_turret_.*_(\dx)$", "Tourelle à boule"),
    (r"zv_remote_turret_.*_(\dx)$", "Tourelle télécommandée"),
    (r"zv_(jet_improved_compressor|afterburner|supersonic_intake)", "Améliorations de réacteur"),
    (r"zv_role_", "Rôle"),
]
SIZE_ROLE = {"small": "Rôle (petite)", "medium": "Rôle (moyenne)", "large": "Rôle (grande)"}


def category(r):
    mid = r["id"]
    if mid in EXACT:
        return EXACT[mid], EXACT[mid]
    if mid in TUR:
        return TUR[mid], TUR[mid]
    for pat, cat in PREFIX:
        m = re.match(pat, mid)
        if not m:
            continue
        if cat == "Motorisation":
            sub = re.search(r"Catégorie : (Motorisation [^<|]+)", r["regles"]).group(1).strip()
            return cat, sub
        if cat == "Aile":
            key = mid[len("zv_wing_"):]
            k = "sans_queue" if key.startswith("sans_queue") else key.split("_")[0]
            return cat, f"Aile — {WING_CAT[k]}"
        if cat in ("Tourelle à boule", "Tourelle télécommandée"):

            c = f"{cat} x{m.group(m.lastindex)[0]}"
            return c, c
        if cat == "Rôle":
            return cat, SIZE_ROLE[mid.rsplit("_", 1)[1]]
        return cat, cat
    raise KeyError(mid)


# ---------- effets ----------
EFF = re.compile(r"^(🟢|🔴|⚪)\s*(.*?)\s*\(`([a-z_0-9]+)`\)\s*(.*)$")


def effects(txt):
    out = []
    for part in txt.split("<br>"):
        part = part.strip()
        if not part or part == "—":
            continue
        m = EFF.match(part)
        if m:  # condition éventuelle (« en attaque au sol (…) : ») gardée dans le libellé
            out.append(dict(sens={"🟢": "gain", "🔴": "prix", "⚪": "neutre"}[m.group(1)],
                            libelle=m.group(2).strip(), stat=m.group(3), valeur=m.group(4).strip(), texte=part))
        else:
            out.append(dict(texte=part))
    return out


def rules(txt, wing=False):
    if wing and txt.strip() not in ("", "—"):
        return {"interdit": [x.strip() for x in txt.split(",")]}
    d = {}
    for part in txt.split("<br>"):
        part = part.strip()
        if not part or part == "—":
            continue
        if part.startswith("⛔ interdit :"):
            d["interdit"] = [x.strip() for x in part[len("⛔ interdit :"):].split(",")]
        elif part.startswith("Catégorie :"):
            d["categorie_note"] = part[len("Catégorie :"):].strip()
        elif part.startswith("🔢"):
            d.setdefault("limites", []).append(part[1:].strip())
        elif part.startswith("🔓"):
            d.setdefault("debloque", []).append(part[1:].strip())
        else:
            d.setdefault("autres", []).append(part)
    return d


out, errs = [], []
for r in mods:
    try:
        cat, sub = category(r)
    except Exception as e:  # noqa: BLE001
        errs.append((r["id"], repr(e)))
        continue
    size = {"_s": "S", "_m": "M", "_l": "L"}.get(r["id"][-2:]) if re.search(r"_[sml]$", r["id"]) else None
    out.append(dict(id=r["id"], nom=r["name"], section_05=r["section"], ligne_05=r["line"], categorie=cat,
                    categorie_jeu=sub, taille_suffixe=size, tech=r["tech"], annee=r["year"],
                    reference="— référence" in r["name"], gains=effects(r["gains"]), prix=effects(r["prix"]),
                    regles=rules(r["regles"], wing=cat == "Aile"), pourquoi=r["raw"][5] if len(r["raw"]) > 5 else ""))

assert not errs, errs
ids = [m["id"] for m in out]
assert len(ids) == len(set(ids)) == 392, (len(ids), len(set(ids)))
cats_mod = set(json.load(open("data/categories_mod.json")))
used = {m["categorie"] for m in out}
assert used <= cats_mod, used - cats_mod
assert cats_mod <= used, ("catégories sans module", cats_mod - used)
Path("data/modules.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))

# ---------- catégories ----------
cats = {}
for m in out:
    c = cats.setdefault(m["categorie_jeu"], dict(categorie=m["categorie"], modules=[]))
    c["modules"].append(m["id"])
import unicodedata


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    t = t.replace("classe ", "")
    return "zv_cat_" + re.sub(r"[^a-z0-9]+", "_", t).strip("_")


Path("data/categories.json").write_text(json.dumps(
    dict(note="id_propose : nom de catégorie proposé pour le code (💡, renommable) ; une catégorie de jeu = une "
              "valeur de `category` dans les modules.",
         regroupees=sorted(cats_mod),
         categories_jeu={k: dict(id_propose=slug(k), categorie=v["categorie"], n=len(v["modules"]),
                                 modules=v["modules"]) for k, v in sorted(cats.items())}),
    ensure_ascii=False, indent=1))
assert len({slug(k) for k in cats}) == len(cats)

# ---------- slots (ordre d'écran du .gui : 20 fixes puis 12 libres) ----------
# ✅ 22/10 : le jeu n'affiche que 20 positions fixes ; Internes 4 passe en tête des libres (02 §1.9).
FIXED = ["Aile 1", "Aile 2", "Hélices", "Module Hélice", "Type de Moteurs", "Nombre de Moteurs", "Matériaux",
         "Construction", "Modules Moteurs 1", "Modules Moteurs 2", "Trains d'atterrissage", "Type de Fuselage",
         "Type d'Ailes", "Type d'Empennage", "Rôles", "Nez", "Cockpit", "Arrière Cockpit", "Internes 1",
         "Ventre Milieu"]
CUSTOM = ["Internes 4", "Aile 3", "Aile 4", "Internes 2", "Internes 5", "Ventre Arrière", "Queue", "Aile 5", "Dos",
          "Internes 3", "Internes 6", "Ventre Avant"]
assert len(FIXED) <= 20, "le jeu n'affiche que 20 positions fixes"
assert set(FIXED + CUSTOM) == set(SP.SLOTS), set(SP.SLOTS) ^ set(FIXED + CUSTOM)
SLOT_ID = {  # 💡 noms proposés ; les fixes DOIVENT commencer par fixed_ (règle du jeu, 02 §1.9)
    "Aile 1": "fixed_zv_wing_1", "Aile 2": "fixed_zv_wing_2", "Hélices": "fixed_zv_propeller",
    "Module Hélice": "fixed_zv_propeller_module", "Type de Moteurs": "fixed_zv_engine",
    "Nombre de Moteurs": "fixed_zv_engine_config", "Matériaux": "fixed_zv_materials",
    "Construction": "fixed_zv_construction", "Modules Moteurs 1": "fixed_zv_engine_module_1",
    "Modules Moteurs 2": "fixed_zv_engine_module_2", "Trains d'atterrissage": "fixed_zv_landing_gear",
    "Type de Fuselage": "fixed_zv_fuselage", "Type d'Ailes": "fixed_zv_wing_type", "Type d'Empennage": "fixed_zv_tail",
    "Rôles": "fixed_zv_role", "Nez": "fixed_zv_nose", "Cockpit": "fixed_zv_cockpit",
    "Arrière Cockpit": "fixed_zv_rear_cockpit", "Internes 1": "fixed_zv_internal_1",
    "Ventre Milieu": "fixed_zv_belly_middle", "Internes 4": "zv_internal_4",
    "Aile 3": "zv_wing_3", "Aile 4": "zv_wing_4", "Internes 2": "zv_internal_2", "Internes 5": "zv_internal_5",
    "Ventre Arrière": "zv_belly_rear", "Queue": "zv_tail_position", "Aile 5": "zv_wing_5", "Dos": "zv_dorsal",
    "Internes 3": "zv_internal_3", "Internes 6": "zv_internal_6", "Ventre Avant": "zv_belly_front"}
REQUIRED = {"Type de Moteurs", "Nombre de Moteurs", "Type de Fuselage", "Type d'Ailes", "Rôles",
            "Cockpit"}  # ✅ Q1 du 21/10 (cahier §3)
slots = []
for i, s in enumerate(FIXED + CUSTOM):
    sizes, base, extra = SP.SLOTS[s]
    slots.append(dict(slot=s, id_propose=SLOT_ID[s], obligatoire_propose=s in REQUIRED,
                      ecran=("fixe" if s in FIXED else "libre"),
                      fenetre_gui=("pos_fixed_module_slot_window_%d" % FIXED.index(s)) if s in FIXED
                      else ("pos_custom_module_slot_window_%d" % CUSTOM.index(s)),
                      tailles=sorted(sizes, key="NPMG".index), categories=base,
                      categories_selon_taille={k: sorted(v, key="NPMG".index) for k, v in extra.items()}))
Path("data/slots.json").write_text(json.dumps(dict(
    legende=dict(N="petite navale", P="petite", M="moyenne", G="grande",
                 note="Ordre = ordre de déclaration dans module_slots ; les slots fixes vont dans "
                      "pos_fixed_module_slot_window_N, les libres dans pos_custom_module_slot_window_N "
                      "(voir 02 §1.9 et mod/interface/plane_designer_view.gui). 'Motorisation', 'Aile' et 'Rôle' "
                      "valent pour toutes leurs catégories de jeu (data/categories.json)."),
    slots=slots), ensure_ascii=False, indent=1))

# ---------- techs ----------
techs = json.load(open("data/techs_arbre.json"))
by_tech = {}
for m in out:
    by_tech.setdefault(m["tech"], []).append(m["id"])
for t in techs:
    t["modules_05"] = by_tech.get(t["id"], [])
Path("data/techs.json").write_text(json.dumps(techs, ensure_ascii=False, indent=1))

print(f"modules {len(out)} ; catégories regroupées {len(cats_mod)} ; catégories de jeu {len(cats)} ; "
      f"slots {len(slots)} ; techs {len(techs)}")
print("modules par catégorie de jeu (Motorisation, Aile, Rôle) :",
      {k: len(v['modules']) for k, v in sorted(cats.items()) if k.startswith(('Motorisation', 'Aile', 'Rôle'))})
print("techs du 05 absentes de l'arbre :", sorted({m['tech'] for m in out} - {t['id'] for t in techs}))

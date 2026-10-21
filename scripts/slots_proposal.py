"""Proposition de table catégorie -> slot (doc 09) et test d'ajustement de designs types.

Le test cherche une affectation des catégories demandées par un design aux slots de la
cellule (couplage biparti) : un module par slot, chaque slot n'accepte que ses catégories.
"""
import json, sys
from pathlib import Path

TUR = ["Tourelle x1", "Tourelle x2", "Tourelle x4", "Tourelle à boule x1", "Tourelle à boule x2",
       "Tourelle à boule x4", "Tourelle télécommandée x1", "Tourelle télécommandée x2", "Tourelle télécommandée x4"]
GUNS = ["Mitrailleuses", "Canons"]
MG = {"M", "G"}
INTERNES = ["Viseur de tir", "Contre-mesures", "Identification", "Aides au pilotage", "Sécurité incendie",
            "Dégivrage", "Siège éjectable", "Équipement naval", "Aide au décollage", "Réglage de fiabilité",
            "Radio", "Blindage du cockpit", "Réservoir interne", "Radar", "Viseur de bombardement",
            "Navigation", "Alerte radar", "Blindage"]

# v2 (21/10, modifications de Florian dans le document en ligne) :
# slot -> (tailles où il existe, catégories acceptées partout, {catégorie: tailles où elle est acceptée})
ALL = {"N", "P", "M", "G"}          # N = petite navale, P = petite, M = moyenne, G = grande
MOT = ["Alimentation", "Régime d'urgence", "Refroidissement", "Carénage moteur", "Prise d'air",
       "Améliorations de réacteur", "Réglage de puissance"]
WING = GUNS + ["Canon AT", "Roquettes", "Attaches", "Armes guidées", "Réservoir supplémentaire", "Volets",
               "Becs de bord d'attaque", "Aérofreins", "Pylônes", "Blindage"]
SLOTS = {
    "Type de Moteurs": (ALL, ["Moteur"], {}),
    "Nombre de Moteurs": (ALL, ["Motorisation"], {}),
    "Hélices": (ALL, ["Hélice"], {}),
    "Module Hélice": (ALL, ["Module d'hélice"], {}),
    "Modules Moteurs 1": (ALL, MOT, {}),
    "Modules Moteurs 2": (ALL, MOT, {}),
    "Type de Fuselage": (ALL, ["Fuselage"], {}),
    "Type d'Ailes": (ALL, ["Aile"], {}),
    "Type d'Empennage": (ALL, ["Empennage"], {}),
    "Trains d'atterrissage": (ALL, ["Train d'atterrissage"], {}),
    "Rôles": (ALL, ["Rôle"], {}),
    "Cockpit": (ALL, ["Cockpit"], {}),
    "Matériaux": (ALL, ["Matériaux"], {}),
    "Construction": (ALL, ["Construction"], {}),
    "Nez": (ALL, ["Mitrailleuses de nez", "Canons de nez", "Radar", "Viseur de bombardement", "Blindage"], {"Canon AT de nez": MG}),
    "Arrière Cockpit": (ALL, ["Mitrailleuse à main", "Radio", "Blindage du cockpit", "Réservoir interne",
                              "Navigation", "Blindage"], {t: MG for t in TUR}),
    "Dos": ({"G"}, TUR + ["Mitrailleuse à main", "Armes spéciales", "Navigation", "Blindage"], {}),
    "Queue": (MG, TUR + ["Mitrailleuse à main", "Alerte radar", "Blindage"], {}),
    "Ventre Avant": ({"G"}, TUR + ["Mitrailleuse à main", "Canon AT", "En soute", "Attaches", "Armes guidées",
                                   "Armes navales", "Reconnaissance", "Radar", "Viseur de bombardement", "Blindage"], {}),
    "Ventre Milieu": (ALL, ["En soute", "Attaches", "Armes navales", "Armes guidées", "Canon AT",
                            "Réservoir supplémentaire", "Reconnaissance", "Soute de transport",
                            "Largage de ravitaillement", "Armes spéciales", "Anti-sous-marin", "Blindage"], {}),
    "Ventre Arrière": (MG, TUR + ["Mitrailleuse à main", "En soute", "Reconnaissance", "Anti-sous-marin",
                                  "Soute de transport", "Largage de ravitaillement", "Blindage"], {}),
}
SLOTS["Aile 1"] = (ALL, WING, {"En soute": {"G"}, "Armes navales": MG})
SLOTS["Aile 2"] = (ALL, WING, {"Armes navales": MG})
SLOTS["Aile 3"] = ({"P", "M", "G"}, WING, {}); SLOTS["Aile 4"] = (MG, WING, {}); SLOTS["Aile 5"] = ({"G"}, WING, {})
SLOTS["Internes 1"] = (ALL, INTERNES, {}); SLOTS["Internes 4"] = (ALL, INTERNES, {})
for i in (2, 5): SLOTS[f"Internes {i}"] = (MG, INTERNES, {})
for i in (3, 6): SLOTS[f"Internes {i}"] = ({"G"}, INTERNES, {})


def accepts(slot, size):
    sizes, cats, extra = SLOTS[slot]
    return set(cats) | {c for c, sz in extra.items() if size in sz}

BASE = ["Moteur", "Motorisation", "Fuselage", "Aile", "Empennage", "Train d'atterrissage", "Rôle", "Cockpit"]
PROP = ["Hélice", "Module d'hélice"]
DESIGNS = {
    "Bf 109 E (P)": ("P", BASE + PROP + ["Alimentation", "Refroidissement", "Mitrailleuses de nez", "Canons",
                                         "Radio", "Viseur de tir", "Blindage du cockpit"]),
    "Spitfire I (P)": ("P", BASE + PROP + ["Alimentation", "Refroidissement", "Mitrailleuses", "Mitrailleuses",
                                           "Radio", "Viseur de tir", "Blindage du cockpit"]),
    "Fw 190 A-8 (P)": ("P", BASE + PROP + ["Alimentation", "Régime d'urgence", "Carénage moteur", "Mitrailleuses de nez",
                                           "Canons", "Canons", "Radio", "Viseur de tir", "Blindage du cockpit",
                                           "Blindage", "Réservoir interne"]),
    "P-51 D (P)": ("P", BASE + PROP + ["Alimentation", "Refroidissement", "Régime d'urgence", "Mitrailleuses",
                                       "Mitrailleuses", "Réservoir supplémentaire", "Radio", "Viseur de tir",
                                       "Réservoir interne", "Blindage du cockpit"]),
    "Ju 87 B (P)": ("P", BASE + PROP + ["Alimentation", "Mitrailleuses", "Attaches", "Attaches", "Aérofreins",
                                        "Mitrailleuse à main", "Radio", "Viseur de bombardement"]),
    "A6M2 embarqué (N)": ("N", BASE + PROP + ["Alimentation", "Carénage moteur", "Mitrailleuses de nez", "Canons",
                                              "Réservoir supplémentaire", "Équipement naval", "Radio"]),
    "He 111 H (M)": ("M", BASE + PROP + ["Alimentation", "Refroidissement", "En soute", "Tourelle x1",
                                         "Mitrailleuse à main", "Mitrailleuse à main", "Mitrailleuse à main",
                                         "Viseur de bombardement", "Radio", "Navigation", "Blindage",
                                         "Réservoir interne"]),
    "Mosquito FB VI (M)": ("M", BASE + PROP + ["Alimentation", "Refroidissement", "Mitrailleuses de nez", "Canons de nez",
                                               "En soute", "Roquettes", "Matériaux", "Radio",
                                               "Navigation", "Viseur de tir"]),
    "Me 262 A (P)": ("P", BASE + ["Prise d'air", "Améliorations de réacteur", "Canons de nez", "Radio",
                                  "Viseur de tir", "Blindage du cockpit", "Réservoir interne"]),
    "B-17 G (G)": ("G", BASE + PROP + ["Alimentation", "Régime d'urgence", "En soute", "Tourelle x2",
                                       "Tourelle x2", "Tourelle à boule x2", "Tourelle x2", "Mitrailleuse à main",
                                       "Mitrailleuse à main", "Viseur de bombardement", "Radio", "Navigation",
                                       "Blindage", "Réservoir interne", "Aides au pilotage", "Dégivrage"]),
    "Sunderland (G, patrouille)": ("G", BASE + PROP + ["Carénage moteur", "Tourelle x2", "Tourelle x4",
                                                        "Tourelle x2", "Armes navales", "Radar", "Anti-sous-marin",
                                                        "Radio", "Navigation", "Réservoir interne"]),
}


def slots_for(size):
    return [s for s, v in SLOTS.items() if size in v[0]]


def fit(size, need):
    slots = slots_for(size)
    match = {}  # slot -> index de la demande

    def try_assign(i, seen):
        for s in slots:
            if need[i] in accepts(s, size) and s not in seen:
                seen.add(s)
                if s not in match or try_assign(match[s], seen):
                    match[s] = i
                    return True
        return False
    lost = [need[i] for i in range(len(need)) if not try_assign(i, set())]
    used = {need[i]: s for s, i in match.items()}
    return lost, len(slots), {s: need[i] for s, i in match.items()}


if __name__ == "__main__":
    out = {}
    for name, (size, need) in DESIGNS.items():
        lost, n, assign = fit(size, need)
        out[name] = dict(taille=size, slots=n, demandes=len(need), sans_place=lost, affectation=assign)
        print(f"{name:28} slots {n:2}  demandes {len(need):2}  sans place : {lost or '—'}")
    # catégories sans slot
    cats = json.load(open("data/categories_mod.json")) if Path("data/categories_mod.json").exists() else None
    accepted = {c for s in SLOTS for z in "NPMG" for c in accepts(s, z)}
    if cats:
        print("catégories du mod sans slot :", sorted(set(cats) - accepted))
        print("catégories de la table inconnues :", sorted(accepted - set(cats)))
    Path("out/slots_fit.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))

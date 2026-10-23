"""Phase 7 : audit anti-cheat (balance_audit.py du plugin) réparti sur plusieurs cœurs, avec reprise.

Chaque cellule est auditée à part et son résultat est écrit dès qu'il est prêt (out/audit/<cellule>.json) :
une cellule déjà faite n'est pas recalculée, un arrêt ne perd que la cellule en cours.

  python -X utf8 scripts/audit_parallele.py prepare            # base du mod + curseurs au cran 5
  python -X utf8 scripts/audit_parallele.py worker 0 3         # travailleur 0 sur 3 (à lancer 3 fois)
  python -X utf8 scripts/audit_parallele.py merge              # rapport out/audit/audit.md
"""
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "outils/hoi4-zv-designer"
SCRIPTS = PLUGIN / "skills/hoi4-equilibrage/scripts"
sys.path.insert(0, str(SCRIPTS))
OUT = ROOT / "out/audit"
DB = OUT / "mod_db_curseurs.json"
COMPARE = PLUGIN / "data/audit_vanilla.json"
REF = "F:/Github Local/HOI4-ref"


def prepare():
    import compare_history as CH
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "mod_db.json"
    subprocess.run([sys.executable, "-X", "utf8", str(PLUGIN / "scripts/extract_air.py"), "--ref", REF, "--mod",
                    str(ROOT / "mod"), "--out", str(raw)], check=True)
    db = json.loads(raw.read_text(encoding="utf-8"))
    CH.add_sliders(db)                                    # curseurs au cran 5, comme module fictif
    m = db["modules"][CH.SLIDER]
    ex = next(v for k, v in db["modules"].items() if k != CH.SLIDER)
    for k, v in ex.items():
        m.setdefault(k, type(v)() if isinstance(v, (list, dict)) else None)
    m.update(year=1922, loc_name="Curseurs au cran 5")
    DB.write_text(json.dumps(db, ensure_ascii=False), encoding="utf-8")
    print(f"base prête : {DB}")


def airframes():
    import balance_audit as B, plane_calc as pc
    afs = B.base_airframes(pc.load_db(str(DB)))
    cost = lambda a: ({"small": 1, "cv": 1, "medium": 2, "large": 3}[a.split("_")[0]], int(a[-1]))
    return sorted(afs, key=cost, reverse=True)           # les plus longues d'abord, réparties en tourniquet


def worker(i, n):
    mine = airframes()[i::n]
    for af in mine:
        out = OUT / f"{af}.json"
        if out.exists():
            print(f"[{i}] {af} : déjà fait")
            continue
        tmp = OUT / f"{af}.json.tmp"
        subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "balance_audit.py"), "--db", str(DB),
                        "--compare", str(COMPARE), "--airframe", af, "--json", str(tmp)],
                       check=True, stdout=subprocess.DEVNULL)
        tmp.replace(out)
        print(f"[{i}] {af} : fait", flush=True)


def merge():
    import balance_audit as B, plane_calc as pc
    db = pc.load_db(str(DB))
    rows, missing = [], []
    for af in airframes():
        p = OUT / f"{af}.json"
        if p.exists():
            rows += json.loads(p.read_text(encoding="utf-8"))
        else:
            missing.append(af)
    crow = json.loads(COMPARE.read_text(encoding="utf-8"))
    txt = B.render(rows, db, crow, md=True)
    head = ("# Audit anti-cheat du mod (phase 7)\n\nbalance_audit.py du plugin, base du mod avec curseurs au cran 5, "
            "comparé à l'audit vanilla (data/audit_vanilla.json). Tolérance 15 %, contrepartie 10 % (Q17).\n\n")
    if missing:
        head += f"⚠ Cellules pas encore auditées : {', '.join(missing)}\n\n"
    (OUT / "audit.md").write_text(head + txt + "\n", encoding="utf-8")
    flagged = [r for r in rows if r["flags"]]
    print(f"{len(rows)} combinaisons, {len(flagged)} drapeau(x), {len(missing)} cellule(s) manquante(s) ; out/audit/audit.md")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prepare":
        prepare()
    elif cmd == "worker":
        worker(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "merge":
        merge()

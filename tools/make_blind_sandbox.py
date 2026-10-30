"""Create an isolated copy of the skill for a blind test of one pleito.

usage: make_blind_sandbox.py <repo_root> <pleito_id> <arm A|B> <areas_final_dir> <out_dir>
<pleito_id> is the OPAQUE ficha id (P + 6 hex, as in `fichas/pleitos/<id>.md`), not the portal number;
map it with the private id map kept outside the repository.
Arm A: full RAG, but with the pleito's fichas (every attempt), its rows in the CSV/cards, its area records and docs section 2 REMOVED.
Arm B (control): rubric and regulation only; no fichas, no cards, no area base rates, no docs.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path


def main():
    repo, pid, arm, areas, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4]), Path(sys.argv[5])
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(repo / "skills", out / "skills")
    cal = out / "skills/cofiex-scorer/references/calibration"
    if arm == "B":
        sk = out / "skills/cofiex-scorer"
        for d in (cal / "cases", sk / "fichas", sk / "docs", sk / "data"):
            shutil.rmtree(d, ignore_errors=True)
        (cal / "areas-stats.md").unlink(missing_ok=True)
        print("arm B ready:", out)
        return
    # ---- arm A ---- (drop the pleito's fichas from the copied skill, then rebuild CSV and cards)
    fch = out / "skills/cofiex-scorer/fichas"
    drop_a = set()
    for p in (fch / "avaliacoes").glob("*.md"):
        h = dict(re.findall(r"^(\w+): ?(.*)$", p.read_text(encoding="utf-8").split("---", 2)[1], re.M))
        if h["pleito"] == pid:
            drop_a.add(h["id"])
            p.unlink()
    if not drop_a:
        sys.exit(f"no avaliação fichas found for {pid}: pass the opaque ficha id")
    (fch / "pleitos" / f"{pid}.md").unlink(missing_ok=True)
    # CSV + cards rebuilt from the remaining fichas
    subprocess.run([sys.executable, "-I", "-X", "utf8", str(repo / "tools/build_cases_from_fichas.py"), str(out)], check=True, capture_output=True)
    # area base rates without the case
    tmp = out / "_areas"
    tmp.mkdir()
    for f in areas.glob("*.json"):
        if f.stem not in drop_a:
            shutil.copy(f, tmp / f.name)
    subprocess.run([sys.executable, "-I", "-X", "utf8", str(repo / "tools/build_areas_stats.py"), str(tmp), str(out), str(cal / "areas-stats.md")], check=True, capture_output=True)
    shutil.rmtree(tmp)
    # docs: section 1 only
    dpath = out / "skills/cofiex-scorer/docs/analise-areas-estrategicas.md"
    dpath.write_text(dpath.read_text(encoding="utf-8").split("## 2. ")[0], encoding="utf-8")
    left = len(list((fch / "avaliacoes").glob("*.md")))
    print(f"arm A ready: {out} | removed avaliações {sorted(drop_a)} | avaliações left {left}")


if __name__ == "__main__":
    main()

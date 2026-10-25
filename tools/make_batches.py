"""Create work batches (local JSON, never committed) for narrative generation.

usage: make_batches.py <repo_root> <manifest.json> <out_dir> [--max-pleitos 3] [--max-kb 380] [--ids P1,P2] [--prefix wave]
A unit = one pleito ficha (if its CC text exists and the ficha still has a placeholder) + its avaliacao fichas that
have an NT and still have a placeholder. Batches are filled greedily by source size.
"""
import argparse, json, os, re
from pathlib import Path


def has_pending(path):
    return "pendente" in Path(path).read_text(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("manifest"); ap.add_argument("out")
    ap.add_argument("--max-pleitos", type=int, default=3)
    ap.add_argument("--max-kb", type=int, default=380)
    ap.add_argument("--ids", default="")
    ap.add_argument("--prefix", default="batch")
    ap.add_argument("--regime", default="", help="only avaliacoes of this regime (e.g. NR1_2024); pleito kept if any of its avaliacoes matches")
    ap.add_argument("--exclude-batches", default="", help="comma list of batch json files whose ids are skipped (in flight)")
    a = ap.parse_args()
    root, out = Path(a.root), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    man = json.load(open(a.manifest, encoding="utf-8"))
    want = set(a.ids.split(",")) if a.ids else None
    skip = set()
    for bf in filter(None, a.exclude_batches.split(",")):
        for u in json.load(open(bf, encoding="utf-8")):
            skip.add(u["pleito_id"]); skip |= {x["avaliacao_id"] for x in u["avaliacoes"]}
    regime_of = {}
    if a.regime:
        for f in (root / "fichas/avaliacoes").glob("*.md"):
            t = f.read_text(encoding="utf-8")
            regime_of[re.search(r"^id: (\w+)", t, re.M).group(1)] = re.search(r"^regime: ?(\w*)", t, re.M).group(1)
    units = []
    for pid, v in man.items():
        if v["type"] != "pleito" or (want and pid not in want) or pid in skip:
            continue
        if a.regime and not any(x["pleito"] == pid and regime_of.get(k) == a.regime for k, x in man.items() if x["type"] == "avaliacao"):
            continue
        pf = root / "fichas/pleitos" / f"{pid}.md"
        item = {"pleito_id": pid, "pleito_ficha": str(pf.resolve()), "cc_text": None, "avaliacoes": []}
        size = 0
        if v["text"] and has_pending(pf):
            item["cc_text"] = v["text"]
            size += os.path.getsize(v["text"])
        for aid, av in man.items():
            if av["type"] != "avaliacao" or av["pleito"] != pid:
                continue
            af = root / "fichas/avaliacoes" / f"{aid}.md"
            if a.regime and regime_of.get(aid) != a.regime:
                continue
            if aid in skip:
                continue
            if av["nts"] and has_pending(af):
                nts = [p for p in av["nts"] if os.path.exists(p)]
                item["avaliacoes"].append({"avaliacao_id": aid, "ficha": str(af.resolve()), "nt_texts": nts})
                size += sum(os.path.getsize(p) for p in nts)
        if item["cc_text"] or item["avaliacoes"]:
            item["_kb"] = size // 1024
            units.append(item)
    units.sort(key=lambda u: u["_kb"])
    batches, cur, kb = [], [], 0
    for u in units:
        if cur and (len(cur) >= a.max_pleitos or kb + u["_kb"] > a.max_kb):
            batches.append(cur); cur, kb = [], 0
        cur.append(u); kb += u["_kb"]
    if cur:
        batches.append(cur)
    for i, b in enumerate(batches, 1):
        json.dump([{k: v for k, v in u.items() if k != "_kb"} for u in b], open(out / f"{a.prefix}{i:03d}.json", "w", encoding="utf-8"), indent=1)
    print(f"{len(units)} units -> {len(batches)} batches; total source {sum(u['_kb'] for u in units)//1024} MB; largest unit {max((u['_kb'] for u in units), default=0)} KB")


if __name__ == "__main__":
    main()

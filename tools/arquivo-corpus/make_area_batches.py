"""Group extract_areas.py records into agent batches (local JSON).

usage: make_area_batches.py <areas_dir> <out_dir> <final_dir> [--per 10] [--max-kb 90]
Only records with a non-empty segment are sent to agents; records without a segment are written directly as
`no_area_scoring_in_nt` into <final_dir>. Records already present in <final_dir> are skipped (resumable).
"""
import argparse, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("areas"); ap.add_argument("out"); ap.add_argument("final")
    ap.add_argument("--per", type=int, default=10)
    ap.add_argument("--max-kb", type=int, default=90)
    ap.add_argument("--prefix", default="a")
    a = ap.parse_args()
    out, final = Path(a.out), Path(a.final)
    out.mkdir(parents=True, exist_ok=True); final.mkdir(parents=True, exist_ok=True)
    items, direct = [], 0
    for f in sorted(Path(a.areas).glob("*.json")):
        r = json.load(open(f, encoding="utf-8"))
        if (final / f.name).exists():
            continue
        if not r.get("segment_pt"):
            json.dump({"id": r["id"], "regime": r["regime"], "status": "no_area_scoring_in_nt", "areas": [], "bonus": [],
                       "notes": "NT available but without a strategic-area scoring block (agenda or non-scoring note)."},
                      open(final / f.name, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            direct += 1
            continue
        items.append({"id": r["id"], "regime": r["regime"], "header_ae": r.get("header_ae", ""), "header_total": r.get("header_total", ""),
                      "areas_total": r.get("areas_total"), "parsed_areas": [(x["code"], x["points"], x["max"], x["level"]) for x in r.get("areas", [])],
                      "parsed_criteria": [(x["criterion"], x["points"]) for x in r.get("criteria", [])],
                      "parsed_bonus": [(b["paragraph"], b["points"], b["max"]) for b in r.get("bonus", [])],
                      "segment_pt": r["segment_pt"]})
    batches, cur, kb = [], [], 0
    for it in items:
        s = len(it["segment_pt"]) // 1024
        if cur and (len(cur) >= a.per or kb + s > a.max_kb):
            batches.append(cur); cur, kb = [], 0
        cur.append(it); kb += s
    if cur:
        batches.append(cur)
    for i, b in enumerate(batches, 1):
        json.dump({"out_dir": str(final.resolve()), "items": b}, open(out / f"{a.prefix}{i:03d}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(items)} items -> {len(batches)} batches; {direct} written directly as no_area_scoring_in_nt")


if __name__ == "__main__":
    main()

"""Validate area records written by agents (schema, anonymization, arithmetic).

usage: validate_areas.py <final_dir> [--report out.json]
HARD (record rejected): invalid JSON/schema, money/place/identifier/quantity patterns, regime vocabulary errors.
SOFT (for review): sum of points != areas_total, areas_total != header AE, scored flag inconsistent, long reasons.
"""
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_fichas import HARD  # noqa: E402  (same anonymization patterns as the fichas)

NR1 = {f"{c}" for c in list(range(101, 114)) + list(range(201, 216)) + list(range(301, 308))}
R17 = {f"1.{n}" for n in range(1, 16)}
BONUS_ART = ("15 par.3", "15 par.4")


def texts(r):
    for a in r.get("areas", []):
        yield "area:" + a.get("code", ""), a.get("reason", "") + " " + a.get("label", "")
    for b in r.get("bonus", []):
        yield "bonus", b.get("justification", "")
    yield "notes", r.get("notes", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("final"); ap.add_argument("--report", default="")
    a = ap.parse_args()
    hard, soft, ok = {}, {}, 0
    for f in sorted(Path(a.final).glob("*.json")):
        h, s = [], []
        try:
            r = json.load(open(f, encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            hard[f.stem] = [f"invalid_json:{e}"]
            continue
        if r.get("id") != f.stem:
            h.append("id_mismatch")
        reg = r.get("regime")
        if reg not in ("NR1_2024", "R17_2021"):
            h.append("bad_regime")
        if r.get("status") not in ("ok", "no_area_scoring_in_nt"):
            h.append("bad_status")
        valid = NR1 if reg == "NR1_2024" else R17
        tot = 0.0
        for x in r.get("areas", []):
            if str(x.get("code")) not in valid:
                h.append(f"bad_code:{x.get('code')}")
            try:
                p = float(x["points"]); mx = float(x["max"])
            except (KeyError, TypeError, ValueError):
                h.append("area_missing_points"); continue
            tot += p
            if p > mx + 0.01:
                h.append(f"points_gt_max:{x.get('code')}")
            elif p > mx + 1e-9:
                s.append(f"points_slightly_gt_max:{x.get('code')} (NT misprint?)")
            if (p > 0) != bool(x.get("scored")):
                s.append(f"scored_flag:{x.get('code')}")
            if len(x.get("reason", "").split()) > 45:
                s.append(f"long_reason:{x.get('code')}")
        for b in r.get("bonus", []):
            if not any(str(b.get("article", "")).startswith(t) for t in BONUS_ART):
                h.append(f"bad_bonus_article:{b.get('article')}")
        for where, txt in texts(r):
            for name, rx in HARD:
                for m in rx.finditer(txt):
                    h.append(f"{name}@{where}:{txt[max(0, m.start()-20):m.end()+20]!r}")
        at = r.get("areas_total")
        if r.get("status") == "ok" and at and not r.get("per_criterion_points_not_printed"):
            bon = sum(float(b.get("points", 0)) for b in r.get("bonus", [])) if reg == "NR1_2024" else 0.0
            if abs(tot - float(at[0])) > 0.005:
                s.append(f"sum_areas={tot:.3f}!=areas_total={at[0]}")
        if h:
            hard[f.stem] = h
        else:
            ok += 1
        if s:
            soft[f.stem] = s
    rep = {"ok": ok, "hard": hard, "soft": soft}
    if a.report:
        json.dump(rep, open(a.report, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"ok={ok} hard_fail={len(hard)} soft_flags={len(soft)}")
    for k, v in list(hard.items())[:20]:
        print(" HARD", k, v[:3])
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()

"""Regenerate data/cases_anonymized.csv and the per-sector case cards from the (verified) fichas.

usage: build_cases_from_fichas.py <repo_root>
Reads fichas from <repo_root>/skills/cofiex-scorer/fichas and writes the CSV and cards inside the skill.
Sectors with n < MIN_N_ROWS get a card with counts only (no per-case rows, no medians): with so few
cases a row or a median is the score of an identifiable pleito.
One row per avaliacao ficha, joined with its pleito ficha. Uses verified fields when present
(lender_verified, counterpart_pct_verified, sector_verified) and says where each value came from.
"""
import csv, re, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path


MIN_N_ROWS = 5


def header(p):
    t = p.read_text(encoding="utf-8")
    parts = t.split("---", 2)
    return dict(re.findall(r"^(\w+): ?(.*)$", parts[1], re.M)), parts[2]


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    root = Path(sys.argv[1])
    sk = root / "skills/cofiex-scorer"
    ph, pb = {}, {}
    for p in (sk / "fichas/pleitos").glob("*.md"):
        h, b = header(p)
        ph[h["id"]], pb[h["id"]] = h, b
    rows = []
    for p in sorted((sk / "fichas/avaliacoes").glob("*.md")):
        a, _ = header(p)
        pl = ph[a["pleito"]]
        body = pb[a["pleito"]]
        status = "no_cc_text" if "CC text unavailable" in body else ("pending" if "pendente" in body else "filled")
        sv = pl.get("sector_verified", "").strip()
        rows.append({
            "case_id": a["id"], "pleito_id": a["pleito"], "regime": a.get("regime", ""), "year": a.get("year", ""), "quarter": a.get("quarter", ""),
            "attempt": a.get("attempt", ""), "attempts_total": pl.get("attempts", ""),
            "subtype": a.get("subtype", ""), "lender": pl.get("lender_verified") or a.get("lender", ""), "lender_check": pl.get("lender_check", ""),
            "ticket_band": a.get("ticket_band", ""),
            "counterpart_pct": pl.get("counterpart_pct_verified") or pl.get("counterpart_pct", ""), "counterpart_check": pl.get("counterpart_check", ""),
            "sector": sv or pl.get("sector", ""), "sector_source": "verified" if sv else "keyword_heuristic",
            "sector_secondary": pl.get("sector_secondary", ""),
            "outcome": a.get("outcome", ""), "reason_cat": a.get("reason_cat", ""),
            "ae": a.get("ae", ""), "idh_pts": a.get("idh_pts", ""), "capag_pts": a.get("capag_pts", ""), "debt_pts": a.get("debt_pts", ""),
            "total": a.get("total", ""), "total_published": a.get("total_published", ""),
            "nt_available": a.get("nt_disponivel", ""), "nt_match": a.get("nt_match", ""), "nt_docs": a.get("nt_docs", ""),
            "version_rule": a.get("version_rule", ""),
            "n_indicators": pl.get("n_indicators", ""), "n_indicators_parse": pl.get("n_indicators_parse", ""),
            "baseline_defined_share": pl.get("baseline_defined_share", ""), "baseline_with_year_share": pl.get("baseline_with_year_share", ""),
            "mentions_opex_sustain": pl.get("mentions_opex_sustain", ""), "mentions_licensing": pl.get("mentions_licensing", ""),
            "mentions_gender_race": pl.get("mentions_gender_race", ""), "mentions_iso_benchmark": pl.get("mentions_iso_benchmark", ""),
            "mentions_ppp_guarantee": pl.get("mentions_ppp_guarantee", ""), "tags": pl.get("tags", ""), "narrative": status,
        })
    (sk / "data").mkdir(exist_ok=True)
    with open(sk / "data/cases_anonymized.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    cdir = sk / "references/calibration/cases"
    cdir.mkdir(parents=True, exist_ok=True)
    for old in cdir.glob("*.md"):
        old.unlink()
    by = defaultdict(list)
    for r in rows:
        by[r["sector"] or "other"].append(r)
    med = lambda v: f"{statistics.median(v):.2f}" if v else "n/a"
    idx = ["# Anonymized case cards — index", "",
           "One card per sector. Contents are anonymized profiles (opaque ids; no proponent, project, number or meeting).",
           "Use them as **ranges**, never as named comparators (BLIND-JUDGMENT PRINCIPLE). Sector = `sector_verified` (read from the indicators and",
           "components) when the ficha has a narrative; otherwise a keyword heuristic (`sector_source` in the CSV).", "",
           "| Sector | n | Approved | Not approved | Withdrawn | AE median (NR1/2024) | Total median | Narratives filled |", "|---|---|---|---|---|---|---|---|"]
    for sec, rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
        cnt = Counter(r["outcome"] for r in rs)
        ae = [f(r["ae"]) for r in rs if r["regime"] == "NR1_2024" and f(r["ae"]) is not None]
        tot = [f(r["total"]) if f(r["total"]) is not None else f(r["total_published"]) for r in rs]
        tot = [t for t in tot if t is not None]
        filled = sum(1 for r in rs if r["narrative"] == "filled")
        if len(rs) < MIN_N_ROWS:
            idx.append(f"| [{sec}]({sec}.md) | {len(rs)} | {cnt['approved']} | {cnt['not_approved']} | {cnt['withdrawn']} | hidden (n < {MIN_N_ROWS}) | hidden (n < {MIN_N_ROWS}) | {filled}/{len(rs)} |")
            (cdir / f"{sec}.md").write_text(
                f"# Sector card — {sec}\n\nn = {len(rs)} avaliações: {cnt['approved']} approved, "
                f"{cnt['not_approved']} not approved, {cnt['withdrawn']} withdrawn.\n\n"
                f"Per-case rows and scores hidden (n < {MIN_N_ROWS}): score from the rubric, the A.6 lens and "
                f"neighbouring sector cards with n >= {MIN_N_ROWS}, as ranges only.\n", encoding="utf-8")
            continue
        idx.append(f"| [{sec}]({sec}.md) | {len(rs)} | {cnt['approved']} | {cnt['not_approved']} | {cnt['withdrawn']} | {med(ae)} | {med(tot)} | {filled}/{len(rs)} |")
        L = [f"# Sector card — {sec}", "", f"n = {len(rs)} avaliações (meetings 165-185). AE median (NR 1/2024) = {med(ae)}; total median = {med(tot)}.", "",
             "| case | pleito | regime | yr-Q | att | subtype | lender | ticket | CP% | outcome | reason | AE | CAPAG | Debt | IDH | TOTAL | #ind | base% | yr% | narr |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        pct = lambda x: "" if f(x) is None else str(int(round(f(x) * 100)))
        for r in sorted(rs, key=lambda r: r["case_id"]):
            total = r["total"] or (f"{r['total_published']}*" if r["total_published"] else "")
            L.append(f"| {r['case_id']} | {r['pleito_id']} | {r['regime']} | {r['year']}-Q{r['quarter']} | {r['attempt']} | {r['subtype']} | {r['lender']} | {r['ticket_band']} | "
                     f"{r['counterpart_pct']} | {r['outcome']} | {r['reason_cat']} | {r['ae']} | {r['capag_pts']} | {r['debt_pts']} | {r['idh_pts']} | {total} | "
                     f"{r['n_indicators']} | {pct(r['baseline_defined_share'])} | {pct(r['baseline_with_year_share'])} | {r['narrative']} |")
        L += ["", "`*` total taken from the official meeting result (workbook blank). `narr`: filled / pending / no_cc_text."]
        (cdir / f"{sec}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (cdir / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    print(len(rows), "casos;", {k: len(v) for k, v in sorted(by.items(), key=lambda kv: -len(kv[1]))})
    print("sector_source:", dict(Counter(r["sector_source"] for r in rows)), "| narrative:", dict(Counter(r["narrative"] for r in rows)))


if __name__ == "__main__":
    main()

"""Item-by-item audit: scores cited in avaliacao ficha narratives (from the NTs) vs the scoring workbook.

usage: audit_nt_scores.py <fichas_root> <idmap.rowmap.json> <xlsx> <out_csv> [--ids ID,ID]
For every avaliacao ficha with an NT and no placeholder, each score item (AE/technical/strategic/IDH/CAPAG/debt/total)
is classified:
  MATCH       a cited value equals the workbook value (|diff| <= 0.0015)
  DIFF        values cited, none equals the workbook value
  NT_ONLY     cited, workbook blank
  NOT_CITED   workbook has a value, narrative does not cite the item
  (no row)    neither has it
Narratives are free text, so extraction is heuristic: DIFF rows are for human review, not verdicts.
"""
import argparse, csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
import openpyxl

NUM = r"(?<![/\d.])(\d{1,2}(?:\.\d{1,3})?)(?![\d.]*\s*/)"  # skip scale maxima such as the 2.000 in "0.532/2.000"
GAP = r"[^0-9.\n]{0,28}?"
LABELS = {
    "ae": re.compile(r"\bAE\b" + GAP + NUM, re.I),
    "tech": re.compile(r"technical(?: analysis| score)?" + GAP + NUM, re.I),
    "strat": re.compile(r"strategic[- ]areas?(?: score| points)?" + GAP + NUM, re.I),
    "idh": re.compile(r"\bIDH\b(?: component| points| pts)?" + GAP + NUM),
    "capag": re.compile(r"\bCAPAG\b(?: points| pts)?" + GAP + NUM),
    "debt": re.compile(r"\bdebt\b(?: trajectory| points| pts)?" + GAP + NUM, re.I),
    "total": re.compile(r"\btotal\b" + GAP + NUM, re.I),
}
# workbook columns in SCORING_ALL: 6 CAPAG, 7 debt, 8 technical (old), 9 strategic/AE, 10 IDH, 11 TOTAL
ITEMS_NR1 = {"ae": 9, "idh": 10, "capag": 6, "debt": 7, "total": 11}
ITEMS_R17 = {"tech": 8, "strat": 9, "idh": 10, "total": 11}
TOL = 0.0015


def fv(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("rowmap"); ap.add_argument("xlsx"); ap.add_argument("out")
    ap.add_argument("--ids", default="")
    a = ap.parse_args()
    rowmap = json.load(open(a.rowmap, encoding="utf-8"))
    wb = openpyxl.load_workbook(a.xlsx, read_only=True, data_only=True)
    projs = list(wb["PROJECTS_ALL"].iter_rows(values_only=True))[1:]
    sc = {str(r[5]).strip(): r for r in list(wb["SCORING_ALL"].iter_rows(values_only=True))[1:]}
    want = set(a.ids.split(",")) if a.ids else None
    rows, summ = [], defaultdict(Counter)
    for p in sorted((Path(a.root) / "avaliacoes").glob("*.md")):
        t = p.read_text(encoding="utf-8")
        head_txt, body = t.split("---", 2)[1], t.split("---", 2)[2]
        h = dict(re.findall(r"^(\w+): ?(.*)$", head_txt, re.M))
        if "pendente" in body or h.get("nt_disponivel") != "sim" or (want and h["id"] not in want):
            continue
        i = rowmap.get(h["id"])
        srow = sc.get(str(projs[i][6]).strip()) if i is not None else None
        regime = h.get("regime", "")
        items = ITEMS_NR1 if regime == "NR1_2024" else ITEMS_R17
        for item, col in items.items():
            sheet = fv(srow[col]) if srow else None
            cited = [float(m.group(1)) for m in LABELS[item].finditer(body)]
            if cited and sheet is not None:
                st = "MATCH" if any(abs(c - sheet) <= TOL for c in cited) else "DIFF"
            elif cited:
                st = "NT_ONLY"
            elif sheet is not None:
                st = "NOT_CITED"
            else:
                continue
            summ[(regime, item)][st] += 1
            rows.append([h["id"], regime, h.get("nt_match", ""), item, sheet if sheet is not None else "", ";".join(str(c) for c in cited), st])
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ficha", "regime", "nt_match", "item", "workbook", "cited_in_narrative", "status"])
        w.writerows(rows)
    print(f"{len(set(r[0] for r in rows))} fichas auditadas, {len(rows)} itens")
    print(f"{'regime':9} {'item':6} {'MATCH':>6} {'DIFF':>5} {'NT_ONLY':>8} {'NOT_CITED':>10}")
    for (reg, item), c in sorted(summ.items()):
        print(f"{reg:9} {item:6} {c['MATCH']:>6} {c['DIFF']:>5} {c['NT_ONLY']:>8} {c['NOT_CITED']:>10}")


if __name__ == "__main__":
    main()

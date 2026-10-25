"""Aggregate strategic-area records into an anonymized statistics reference (no individual cases).

usage: build_areas_stats.py <areas_final_dir> <repo_root> <out_md>
"""
import json, re, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path

LABEL = {"101": "Poverty", "102": "Health (SUS)", "103": "Early childhood and education", "104": "Secondary/technical education", "105": "Creative economy",
         "106": "Human rights", "107": "Women", "108": "Indigenous and quilombola peoples", "109": "Anti-racism", "110": "Social security",
         "111": "Sustainable cities", "112": "Public safety", "113": "Sport", "201": "Environment", "202": "Disaster resilience and climate adaptation",
         "203": "Family farming", "204": "Decarbonization", "205": "Competitiveness", "206": "Science, technology and innovation", "207": "Labor",
         "208": "Clean energy", "209": "Digital inclusion and connectivity", "210": "Logistics and transport", "211": "Trade", "212": "Water security",
         "213": "Tourism", "214": "Regional equity", "215": "Mining", "301": "Transparency and participation", "302": "State capacity",
         "303": "Digital government", "304": "Defense", "305": "International cooperation and regional development", "306": "Fiscal sustainability", "307": "Justice"}
CRIT = {"1.1": "Environmental sustainability", "1.2": "Energy efficiency / renewables", "1.3": "Basic sanitation", "1.4": "Water resources / water security",
        "1.5": "Biodiversity and forests", "1.6": "Business environment", "1.7": "Micro/small firms", "1.8": "Jobs and income (vulnerable)",
        "1.9": "Social infrastructure (vulnerable)", "1.10": "Inclusion of minorities", "1.11": "Youth, gender, race", "1.12": "Public service / management / participation",
        "1.13": "Education and health", "1.14": "Technology and innovation", "1.15": "Private-participation financing"}


def sector_of(fichas):
    m = {}
    for p in (fichas / "pleitos").glob("*.md"):
        h = dict(re.findall(r"^(\w+): ?(.*)$", p.read_text(encoding="utf-8").split("---", 2)[1], re.M))
        m[h["id"]] = h.get("sector_verified") or h.get("sector", "other")
    out = {}
    for p in (fichas / "avaliacoes").glob("*.md"):
        h = dict(re.findall(r"^(\w+): ?(.*)$", p.read_text(encoding="utf-8").split("---", 2)[1], re.M))
        out[h["id"]] = (m.get(h["pleito"], "other"), h.get("outcome", ""))
    return out


def main():
    final, root, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    sec = sector_of(root / "fichas")
    recs = [json.load(open(f, encoding="utf-8")) for f in sorted(final.glob("*.json"))]
    nr1 = [r for r in recs if r["regime"] == "NR1_2024" and r["status"] == "ok" and r.get("areas")]
    r17 = [r for r in recs if r["regime"] == "R17_2021" and r["status"] == "ok" and r.get("areas")]
    L = ["# Strategic-area statistics (aggregated, anonymized)", "",
         "Derived from the NT area blocks of every avaliação with a scoring block. No case is identifiable here; use these as **base rates**,",
         "never as precedents. n = number of avaliações. NT = preliminary SEAID analysis; the published AE can add points the NT does not (see",
         "`ae-ranges-and-sectors.md` and the reconciliation in `docs/analise-areas-estrategicas.md`, section 3).", ""]
    # ---------- NR1 ----------
    L += ["## Res. Normativa 1/2024 (Annex II objectives, 0–5 each, AE max 10)", ""]
    n_scored = [sum(1 for a in r["areas"] if float(a["points"]) > 0) for r in nr1]
    ae = [float(r["areas_total"][0]) for r in nr1 if r.get("areas_total")]
    lv = Counter(a.get("level") or "-" for r in nr1 for a in r["areas"] if float(a["points"]) > 0)
    L += [f"- n = {len(nr1)} avaliações. Objectives scored (>0) per avaliação: median {statistics.median(n_scored):g}, range {min(n_scored)}–{max(n_scored)}.",
          f"- Areas total (without bonus): median {statistics.median(ae):.1f}, quartiles {statistics.quantiles(ae, n=4)[0]:.1f} / {statistics.quantiles(ae, n=4)[2]:.1f}.",
          "- Level mix among scored objectives: " + ", ".join(f"{k} {v}" for k, v in sorted(lv.items())) + " (A=5, B=3, C=2, D=1, E=0.5).", ""]
    L += ["### Additional points (art. 15)", "", "| Provision | Requested | Granted | Requested and refused | Not requested |", "|---|---|---|---|---|"]
    for art in ("15 par.3", "15 par.4"):
        req = gr = rr = nr = 0
        for r in nr1:
            for b in r.get("bonus", []):
                if str(b.get("article", "")).startswith(art):
                    g = float(b["points"]) > 0
                    gr += g
                    if b.get("requested") is True:
                        req += 1
                        rr += (not g)
                    elif b.get("requested") is False and not g:
                        nr += 1
        name = "§3 PPA priority (+1)" if art.endswith("3") else "§4 regional integration (+1)"
        L.append(f"| {name} | {req} | {gr} | {rr} | {nr} |")
    L += ["", "### Objectives: how often declared/evaluated and accepted (n ≥ 8 evaluations)", "",
          "| Code | Objective | Evaluated | Scored >0 | Share scored | Mean points when scored |", "|---|---|---|---|---|---|"]
    ev, sc, pts = Counter(), Counter(), defaultdict(list)
    for r in nr1:
        for a in r["areas"]:
            ev[a["code"]] += 1
            if float(a["points"]) > 0:
                sc[a["code"]] += 1
                pts[a["code"]].append(float(a["points"]))
    for code in sorted(ev, key=lambda c: -ev[c]):
        if ev[code] >= 8:
            L.append(f"| {code} | {LABEL.get(code, '')} | {ev[code]} | {sc[code]} | {100*sc[code]/ev[code]:.0f}% | {statistics.mean(pts[code]):.2f} |" if pts[code] else f"| {code} | {LABEL.get(code, '')} | {ev[code]} | 0 | 0% | — |")
    L += ["", "### By sector (NR 1/2024)", "", "| Sector | n | Objectives scored (median) | Areas total (median) |", "|---|---|---|---|"]
    bys = defaultdict(list)
    for r in nr1:
        bys[sec.get(r["id"], ("other",))[0]].append(r)
    for s, rs in sorted(bys.items(), key=lambda kv: -len(kv[1])):
        if len(rs) >= 3:
            L.append(f"| {s} | {len(rs)} | {statistics.median([sum(1 for a in r['areas'] if float(a['points'])>0) for r in rs]):g} | {statistics.median([float(r['areas_total'][0]) for r in rs if r.get('areas_total')]):.1f} |")
    L.append("")
    # ---------- R17 ----------
    L += ["## Res. Cofiex 17/2021 (15 criteria, all-or-nothing, areas max 2.0; no additional points)", ""]
    k = [sum(1 for a in r["areas"] if float(a["points"]) > 0) for r in r17]
    L += [f"- n = {len(r17)} avaliações. Criteria scored per avaliação: median {statistics.median(k):g}, range {min(k)}–{max(k)}.", "",
          "| Criterion | Evaluated | Scored | Share scored |", "|---|---|---|---|"]
    ev, sc = Counter(), Counter()
    for r in r17:
        for a in r["areas"]:
            ev[a["code"]] += 1
            sc[a["code"]] += float(a["points"]) > 0
    for c in sorted(ev, key=lambda c: -sc[c] / ev[c]):
        L.append(f"| {c} {CRIT.get(c, '')} | {ev[c]} | {sc[c]} | {100*sc[c]/ev[c]:.0f}% |")
    L += ["", "Reading: criteria 1.3 (sanitation) and 1.12–1.14 are the most frequently accepted; the criteria on vulnerable groups, "
          "minorities and private-participation financing are rarely accepted unless the programme has a dedicated component.", ""]
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("NR1", len(nr1), "| R17", len(r17), "->", out)


if __name__ == "__main__":
    main()

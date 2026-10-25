"""Extract strategic-area scoring blocks from NT texts (local, Portuguese, never committed).

usage: extract_areas.py <manifest.json> <rowmap-free ficha root> <out_dir>
For every avaliacao ficha with NT texts the best NT (most area-scoring matches) is parsed:
  NR1_2024 (Res. Normativa 1/2024): Annex II objectives "NNN: ... Pontuação atribuída: x/5,000 (Nível: B)" + reasons,
           additional points (art. 15 §3º PPA priority, §4º regional integration), what the proponent declared.
  R17_2021 (Res. 17/2021): technical analysis sub-scores (design / management / risk) and the 15 strategic criteria
           1.1..1.15 (0,133 each) with reasons.
Output: <out_dir>/<avaliacao id>.json with numbers, levels and the raw Portuguese reason paragraphs (to be paraphrased by
agents before anything is published).
"""
import json, re, sys
from pathlib import Path

SEP = re.compile(r"(?:Nota T[eé]cnica[^\n]*?pg\. \d+|SEI \d{5}\.\d{6}/\d{4}-\d{2}[^\n]*?pg\. \d+)")


def norm(t):
    t = SEP.sub(" ", t)
    t = re.sub(r"[ \t]*\n[ \t]*", " ", t)
    return re.sub(r"\s{2,}", " ", t)


def num(x):
    return float(x.replace(".", "").replace(",", "."))


AREA_NR1 = re.compile(
    r"(?P<code>[123]\d{2})\s*:\s*(?P<name>.{5,400}?)\s*Pontua[çc][ãa]o atribu[íi]da\s*:\s*(?P<pts>\d+,\d{3})\s*/\s*(?P<max>\d+,\d{3})"
    r"(?:\s*\(\s*N[íi]vel\s*:\s*(?P<lvl>[A-E])\s*\))?\.?(?P<reason>.*?)(?=\s[123]\d{2}\s*:\s|\s•|\sPonto Adicional|\sPONTUA|\sCONCLUS|\sRECOMEND|$)")
BONUS_NR1 = re.compile(
    r"Ponto Adicional\s*\.?\s*(?P<name>.{5,300}?)\(\s*art\.?\s*15\s*,\s*§\s*(?P<par>\d)\s*º.*?\)\s*\.?\s*Pontua[çc][ãa]o atribu[íi]da\s*:\s*(?P<pts>\d+,\d{3})\s*/\s*(?P<max>\d+,\d{3})\.?(?P<reason>.*?)(?=Ponto Adicional|•|\sÁreas Estrat|\sCONCLUS|\sRECOMEND|$)", re.S)
DECL_NR1 = re.compile(r"((?:Considerando|Cumpre|Observa-se|Destaca-se|Ressalta-se)?[^.]{0,200}proponente\s+(?:n[ãa]o\s+)?indic(?:ou|a)[^•]{0,900}?)(?=•\s*Ponto Adicional|Ponto Adicional)", re.S)

TECH_R17 = re.compile(r"(?P<n>\d)\s*[–-]\s*(?P<name>DESENHO|GEST[ÃA]O[^()]{0,40}|RISCO[^()]{0,40}|[A-ZÇÃÕ ]{4,40})\s*\(\s*(?P<pts>\d,\d{3})\s*/\s*(?P<max>\d,\d{3})\s*\)")
CRIT_R17 = re.compile(
    r"(?<![\d.])1\.(?P<n>\d{1,2})\.?\s+(?P<name>[a-zà-ú].{5,300}?)\s+[-–]\s*(?P<pts>\d,\d{3})(?P<reason>.*?)(?=(?<![\d.])1\.\d{1,2}\.?\s+[a-zà-ú][^.]{5,300}?\s+[-–]\s*\d,\d{3}|\sCONCLUS|\sRECOMEND|$)")
CRIT_R17_B = re.compile(
    r"(?<![\d.])1\.(?P<n>\d{1,2})\.?\s+(?P<name>.{5,400}?)\.?\s*Pontua[çc][ãa]o atribu[íi]da\s*=\s*(?P<pts>\d,\d{3})(?:\s*/\s*0,133)?\.?(?P<reason>.*?)"
    r"(?=(?<![\d.])1\.\d{1,2}\.?\s+.{5,400}?Pontua[çc][ãa]o atribu[íi]da\s*=\s*\d,\d{3}(?:\s*/\s*0,133)?|\sCONCLUS|\sRECOMEND|$)")
ADIC_R17 = re.compile(r"(pontos?\s+adicion\w+|b[ôo]nus)", re.I)


def parse_nr1(t):
    out = {"areas": [], "bonus": [], "declared_text": ""}
    for m in AREA_NR1.finditer(t):
        out["areas"].append({"code": m["code"], "name_pt": m["name"].strip(), "points": num(m["pts"]), "max": num(m["max"]),
                             "level": m["lvl"] or "", "reason_pt": m["reason"].strip()[:1500]})
    for m in BONUS_NR1.finditer(t):
        out["bonus"].append({"paragraph": "3" if m["par"] == "3" else m["par"], "name_pt": m["name"].strip(), "points": num(m["pts"]),
                             "max": num(m["max"]), "reason_pt": m["reason"].strip()[:1200]})
    d = DECL_NR1.search(t)
    if d:
        out["declared_text"] = d.group(1).strip()[:1200]
    m = re.search(r"[ÁA]reas Estrat[ée]gicas\.\s*Pontua[çc][ãa]o atribu[íi]da\s*:\s*(\d+,\d{3})\s*/\s*(\d+,\d{3})", t)
    if m:
        out["areas_total"] = [num(m.group(1)), num(m.group(2))]
    m = re.search(r"pontua[çc][ãa]o total de (\d+,\d{3})", t)
    if m:
        out["ae_total_stated"] = num(m.group(1))
    return out


def parse_r17(t):
    out = {"technical": [], "criteria": [], "adicional_mentions": []}
    for m in TECH_R17.finditer(t):
        out["technical"].append({"block": m["n"], "name_pt": m["name"].strip(), "points": num(m["pts"]), "max": num(m["max"])})
    m = re.search(r"A\)\s*An[áa]lise t[ée]cnica\s*:\s*Pontua[çc][ãa]o total\s*=\s*(\d,\d{3})\s*/\s*(\d,\d{3})", t)
    if m:
        out["technical_total"] = [num(m.group(1)), num(m.group(2))]
    m = re.search(r"B\)\s*[ÁA]reas Estrat[ée]gicas\s*:\s*Pontua[çc][ãa]o total\s*=\s*(\d,\d{3})\s*/\s*(\d,\d{3})", t)
    if m:
        out["areas_total"] = [num(m.group(1)), num(m.group(2))]
        seg = t[m.end():]
        for rx in (CRIT_R17, CRIT_R17_B):
            found = [{"criterion": "1." + c["n"], "name_pt": c["name"].strip(), "points": num(c["pts"]),
                      "reason_pt": c["reason"].strip()[:900]} for c in rx.finditer(seg)]
            if len(found) >= len(out["criteria"]):
                out["criteria"] = found
            if len(out["criteria"]) == 15:
                break
    out["adicional_mentions"] = [t[max(0, x.start() - 80):x.end() + 120] for x in ADIC_R17.finditer(t)][:3]
    return out


def segment(t, regime):
    """Raw text slice holding the strategic-area scoring (and additional points) of one NT."""
    if regime == "NR1_2024":
        idx = [m.start() for m in re.finditer(r"Ponto Adicional|[ÁA]reas Estrat[ée]gicas\.\s*Pontua", t)]
        if not idx:
            return ""
        a = max(0, idx[0] - 1500)
        last = [m.end() for m in re.finditer(r"Pontua[çc][ãa]o atribu[íi]da\s*:\s*\d+,\d{3}\s*/\s*\d+,\d{3}", t)]
        z = last[-1] if last else len(t)
        e = re.search(r"CONCLUS|RECOMENDA[ÇC]", t[z:])
        return t[a: z + (e.start() if e else 2500)][:60000]
    m = re.search(r"1\.1\.?\s+promo[çc][ãa]o da sustentabilidade ambiental", t)
    if not m:
        return ""
    e = re.search(r"CONCLUS|RECOMENDA[ÇC]", t[m.start():])
    return t[max(0, m.start() - 300): m.start() + (e.start() if e else 12000)][:40000]


def best_nt(paths, regime):
    best, score = None, -1
    for p in paths:
        try:
            t = norm(open(p, encoding="utf-8", errors="ignore").read())
        except OSError:
            continue
        s = len(AREA_NR1.findall(t)) if regime == "NR1_2024" else len(CRIT_R17.findall(t)) + 2 * len(TECH_R17.findall(t))
        if s > score:
            best, score = t, s
    return best, score


def main():
    manifest = json.load(open(sys.argv[1], encoding="utf-8"))
    root, out = Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    stats = {}
    for aid, v in manifest.items():
        if v["type"] != "avaliacao" or not v["nts"]:
            continue
        f = root / "avaliacoes" / f"{aid}.md"
        head = dict(re.findall(r"^(\w+): ?(.*)$", f.read_text(encoding="utf-8").split("---", 2)[1], re.M))
        regime = head.get("regime", "")
        if regime not in ("NR1_2024", "R17_2021"):
            continue
        t, s = best_nt(v["nts"], regime)
        rec = {"id": aid, "pleito": v["pleito"], "regime": regime, "outcome": head.get("outcome"), "nt_match": head.get("nt_match"), "match_score": s,
               "header_ae": head.get("ae", ""), "header_total": head.get("total", "")}
        seg = segment(t, regime) if t else ""
        rec["segment_pt"] = seg
        if t and s > 0:
            rec.update(parse_nr1(t) if regime == "NR1_2024" else parse_r17(t))
            rec["parsed"] = True
        else:
            rec["parsed"] = False
        (out / f"{aid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        k = (regime, rec["parsed"], bool(seg))
        stats[k] = stats.get(k, 0) + 1
    for k, n in sorted(stats.items()):
        print(k, n)


if __name__ == "__main__":
    main()

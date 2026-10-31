"""Validate narrative fichas against spec v2.

usage: validate_fichas.py <fichas_root> <skeleton_headers.json> [--ids ID,ID,...] [--report out.json]
Exit 1 when any HARD failure exists. SOFT findings are reported for sampling review only.
"""
import argparse, json, re, sys
from pathlib import Path

ALLOWED_EDIT = {"total_published", "total_published_source", "n_indicators", "n_indicators_parse", "baseline_defined_share", "baseline_with_year_share", "sector_verified", "sector_secondary", "tags", "tags_extra", "lender_verified", "lender_check", "counterpart_pct_verified", "counterpart_check", "nt_docs"}
SECTORS = {"water", "health", "education", "justice", "security", "digital_connectivity", "digital_govt", "fiscal", "environment_climate", "rural", "energy", "infrastructure_mobility", "urban_smart_city", "regional_development", "social", "fund_intermediation"}
HEADS = {
    "pleito": ["## Resumo", "## Teoria da mudança e indicadores", "## Sustentabilidade e riscos", "## Perguntas GTEC provaveis"],
    "avaliacao": ["## Motivos e achados da NT"],
}
PLACES = ("Acre|Alagoas|Amap[aá]|Amazonas|Bahia|Cear[aá]|Distrito Federal|Esp[ií]rito Santo|Goi[aá]s|Maranh[aã]o|Mato Grosso|Minas Gerais|"
          "Par[aá]|Para[ií]ba|Paran[aá]|Pernambuco|Piau[ií]|Rio de Janeiro|Rio Grande do (?:Sul|Norte)|Rond[oô]nia|Roraima|Santa Catarina|"
          "S[aã]o Paulo|Sergipe|Tocantins|Bras[ií]lia|Salvador|Fortaleza|Recife|Manaus|Curitiba|Natal|Goi[aâ]nia|Campinas|Porto Alegre|"
          "Belo Horizonte|Bel[eé]m|Macei[oó]|Teresina|Aracaju|Jo[aã]o Pessoa|Vit[oó]ria|Florian[oó]polis|Cuiab[aá]|Campo Grande|Palmas|"
          "S[aã]o Lu[ií]s|Boa Vista|Macap[aá]|Rio Branco|Porto Velho|Niter[oó]i|Santos|Guarulhos|Osasco|Contagem|Londrina|Maring[aá]|"
          "Juiz de Fora|Uberl[aâ]ndia|Sorocaba|Ribeir[aã]o Preto|Joinville|Blumenau|Caxias do Sul|Petrolina|Juazeiro|Mossor[oó]|Imperatriz")
HARD = [
    ("money", re.compile(r"(?:USD|US\$|U\$|R\$|BRL|EUR|€|\$)\s?\d|\d[\d\.,]*\s?(?:million|billion|bn|mi|bi)\b\s*(?:USD|BRL|EUR|dollars|reais|euros)?", re.I)),
    ("quantity", re.compile(r"\b\d[\d\.,]*\s?(?:km|ha|hectares?|MW|GW|beds|leitos|hospitals?|schools?|municipalities|families|households|"
                            r"inhabitants|people|persons|kits|vehicles|vessels|stations|buses|units)\b", re.I)),
    ("place", re.compile(r"\b(?:" + PLACES + r")\b")),
    ("sei", re.compile(r"\d{5}\.\d{6}/\d{4}")),
    ("cc_pfe", re.compile(r"\b(?:CC|PFE|Pleito)\s*n?[ºo°]?\s*\d{4,}", re.I)),
    ("nt_number", re.compile(r"Nota T[eé]cnica\s*(?:SEI)?\s*n?[ºo°]?\s*\d{2,}", re.I)),
    ("meeting", re.compile(r"\b\d{3}\s?(?:ª|th|rd|nd|st)\b")),
    ("date", re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b")),
]


def split(path):
    t = path.read_text(encoding="utf-8")
    parts = t.split("---", 2)
    head = dict(re.findall(r"^(\w+): ?(.*)$", parts[1], re.M))
    return head, parts[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("skeleton")
    ap.add_argument("--ids", default="")
    ap.add_argument("--report", default="")
    a = ap.parse_args()
    root = Path(a.root)
    skel = json.load(open(a.skeleton, encoding="utf-8"))
    want = set(a.ids.split(",")) if a.ids else None
    hard, soft, ok = {}, {}, 0
    for p in sorted(list((root / "pleitos").glob("*.md")) + list((root / "avaliacoes").glob("*.md"))):
        head, body = split(p)
        fid = head["id"]
        if want and fid not in want:
            continue
        kind = head["type"]
        h, s = [], []
        if "pendente" in body:
            h.append("placeholder_left")
        for hd in HEADS[kind]:
            c = len(re.findall("^" + re.escape(hd) + r"\s*$", body, re.M))
            if c != 1:
                h.append(f"heading_count:{hd}={c}")
        for name, rx in HARD:
            for m in rx.finditer(body):
                h.append(f"{name}:{body[max(0, m.start()-25):m.end()+25]!r}")
        sk = skel.get(fid, {})
        for k, v in head.items():
            if k in ALLOWED_EDIT:
                continue
            if sk and str(sk.get(k, "")) != str(v):
                h.append(f"header_changed:{k}")
        if kind == "pleito":
            if head.get("n_indicators_parse") not in ("verified", "") and "CC text unavailable" not in body:
                s.append("indicators_not_verified")
            sv = head.get("sector_verified", "").strip()
            if "CC text unavailable" not in body:
                if sv not in SECTORS:
                    h.append(f"sector_verified_invalid:{sv!r}")
                if head.get("sector_secondary", "").strip() not in SECTORS | {""}:
                    h.append("sector_secondary_invalid")
                try:
                    if not (float(head.get("baseline_with_year_share")) <= float(head.get("baseline_defined_share")) + 1e-9):
                        h.append("year_share_exceeds_value_share")
                except (TypeError, ValueError):
                    s.append("baseline_with_year_share_missing")
            if "CC text unavailable" not in body:
                try:
                    x = float(head.get("baseline_defined_share") or "nan")
                    if not 0 <= x <= 1:
                        h.append("baseline_share_out_of_range")
                except ValueError:
                    s.append("baseline_share_missing")
        else:
            tot = head.get("total", "").strip()
            for m in re.finditer(r"\btotal\b[^.\n]{0,40}?(\d+\.\d+)", body, re.I):
                line = body[max(0, m.start()-60):m.end()+10].lower()
                if tot and abs(float(m.group(1)) - float(tot)) > 0.011 and "sum" not in line and "partial" not in line and "inferred" not in line and "ae total" not in line and "header total" not in line:
                    s.append(f"total_mismatch:{m.group(1)}!={tot}")
            if len(body.strip()) < 120 and "_NT nao disponivel" not in body:
                s.append("very_short")
        if h:
            hard[fid] = h
        if s:
            soft[fid] = s
        if not h:
            ok += 1
    rep = {"ok": ok, "hard": hard, "soft": soft}
    if a.report:
        json.dump(rep, open(a.report, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"ok={ok} hard_fail={len(hard)} soft_flags={len(soft)}")
    for fid, hs in list(hard.items())[:25]:
        print(" HARD", fid, hs[:4])
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()

"""Header clean-up for fichas (credor, contrapartida, tags, nt_docs). Never overwrites a source value: verified values are added
as new keys (`lender_verified`, `counterpart_pct_verified`, `tags_extra`) and `nt_docs` is recomputed from the deduplicated NT list.

usage: clean_fichas.py <manifest_clean.json> <fichas_root> [--apply] [--report out.json]
"""
import json, re, sys
from collections import Counter
from pathlib import Path

VOCAB = {"dli", "pbl", "ppp", "on_lending", "deferred_indicators", "iso_37120", "cnj", "snis", "ideb", "irap", "resettlement",
         "licensing_risk", "no_verification", "output_heavy", "outcome_focused", "multi_tranche", "disaster_response",
         "gender_race_component", "frontier_zone"}
SECTORS = {"water", "health", "education", "justice", "security", "digital_connectivity", "digital_govt", "fiscal", "environment_climate",
           "rural", "energy", "infrastructure_mobility", "urban_smart_city", "regional_development", "social", "fund_intermediation", "other"}
SYN = {"pbl_dpl": "pbl", "dpl": "pbl", "policy_based": "pbl", "public_private_partnership": "ppp", "onlending": "on_lending",
       "deferred": "deferred_indicators", "no_baseline": "deferred_indicators", "output_only": "output_heavy",
       "outcome_based": "outcome_focused", "gender": "gender_race_component", "race": "gender_race_component",
       "licensing": "licensing_risk", "environmental_licensing": "licensing_risk", "relocation": "resettlement", "frontier": "frontier_zone",
       "disaster": "disaster_response", "climate_disaster": "disaster_response", "no_verification_mechanism": "no_verification"}
LENDERS = [  # (canonical, pattern)
    ("IDB", r"interamericano|\bBID\b|\bIDB\b"), ("IBRD", r"reconstru[cç][aã]o e desenvolvimento|\bBIRD\b|\bIBRD\b|banco mundial"),
    ("CAF", r"\bCAF\b|corpora[cç][aã]o andina"), ("NDB", r"novo banco de desenvolvimento|\bNDB\b"), ("AFD", r"ag[eê]ncia francesa|\bAFD\b"),
    ("KfW", r"\bKfW\b"), ("FONPLATA", r"fonplata"), ("EIB", r"europeu de investimento|\bBEI\b|\bEIB\b"),
    ("AIIB", r"\bAIIB\b|infraestrutura asi[aá]tico"), ("JICA", r"\bJICA\b"), ("IFAD", r"\bFIDA\b|\bIFAD\b"), ("CDP", r"\bCDP\b"),
]
MONEY = r"(?:US\$|USD|BRL|R\$|EUR|€)\s*([\d]{1,3}(?:\.\d{3})*,\d{2})"


def num(s):
    return float(s.replace(".", "").replace(",", "."))


def canon_header_lender(x):
    x = re.sub(r"\(.*?\)", "", x or "").strip().upper()
    return {"BEI": "EIB", "KFW": "KfW", "FIDA": "IFAD"}.get(x, x)


def lenders_in_text(t):
    head = t[:6000]
    m = re.search(r"\*\*Fonte:\*\*", head) or re.search(r"Fontes Externas:", head)
    seg = head[m.end(): m.end() + 400] if m else ""
    seg = re.split(r"Sum[aá]rio|Valor do Financiamento|Minist[ée]rio", seg)[0]
    return {c for c, p in LENDERS if re.search(p, seg, re.I)} if seg else set()


def counterpart_pct(t):
    head = t[:4500]
    m1 = re.search(r"Valor do Financiamento:\*{0,2}\s*(?:USD|BRL|EUR)\s*([\d.]+,\d{2})", head)
    m2 = re.search(r"Valor da Contrapartida:\*{0,2}\s*(?:USD|BRL|EUR)\s*([\d.]+,\d{2})", head)
    if m1 and m2:
        loan, cp = num(m1.group(1)), num(m2.group(1))
        return round(100 * cp / (cp + loan), 1) if cp + loan else None
    mi = re.search(r"Fontes Internas:(.*?)Fontes Externas:", head, re.S)
    me = re.search(r"Fontes Externas:", head)
    if mi and me:
        ext = re.split(r"Sum[aá]rio|Minist[ée]rio", head[me.end(): me.end() + 500])[0]
        cp = sum(num(x) for x in re.findall(MONEY, mi.group(1)))
        loan = sum(num(x) for x in re.findall(MONEY, ext))
        if cp + loan:
            return round(100 * cp / (cp + loan), 1)
    return None


def split(path):
    t = path.read_text(encoding="utf-8")
    _, head, body = t.split("---", 2)
    return head.strip("\n").split("\n"), body


def get(h, k):
    for ln in h:
        if ln.startswith(k + ":"):
            return ln[len(k) + 1:].strip()
    return ""


def put(h, k, v, after=None):
    for i, ln in enumerate(h):
        if ln.startswith(k + ":"):
            h[i] = f"{k}: {v}"
            return
    idx = max((i for i, ln in enumerate(h) if after and ln.startswith(after + ":")), default=len(h) - 1)
    h.insert(idx + 1, f"{k}: {v}")


def parse_tags(s):
    return [x.strip() for x in s.strip("[]").split(",") if x.strip()]


def main():
    man = json.load(open(sys.argv[1], encoding="utf-8"))
    root = Path(sys.argv[2])
    apply = "--apply" in sys.argv
    rep, stats = {}, Counter()
    for pf in sorted((root / "pleitos").glob("*.md")):
        h, body = split(pf)
        pid = get(h, "id")
        text_path = man.get(pid, {}).get("text")
        txt = Path(text_path).read_text(encoding="utf-8", errors="ignore") if text_path else ""
        hdr_raw = get(h, "lender")
        hdr_set = {canon_header_lender(x) for x in re.split(r"\s*/\s*", hdr_raw) if x.strip()}
        hdr_l = canon_header_lender(hdr_raw.split("/")[0])
        ltxt = lenders_in_text(txt) if txt else set()
        if not txt or not ltxt:
            lcheck, lver = "undetermined", hdr_l
        elif hdr_set & ltxt:
            lcheck, lver = "match", hdr_l
        else:
            lcheck, lver = "mismatch", sorted(ltxt)[0] if len(ltxt) == 1 else "/".join(sorted(ltxt))
        cp_h = get(h, "counterpart_pct")
        cp_t = counterpart_pct(txt) if txt else None
        if cp_t is None:
            ccheck, cver = "undetermined", cp_h
        else:
            try:
                ccheck = "match" if abs(float(cp_h) - cp_t) <= 3 else "mismatch"
            except ValueError:
                ccheck = "mismatch"
            cver = cp_t if ccheck == "mismatch" else cp_h
        tags = parse_tags(get(h, "tags"))
        sec = get(h, "sector_verified") or get(h, "sector")
        keep, extra = [], []
        slug = lambda x: re.sub(r"[^a-z0-9]+", "_", x.lower()).strip("_")
        sub_slug = slug(get(h, "subtype"))
        lend_slugs = {slug(x) for x in re.split(r"\s*/\s*", re.sub(r"\(.*?\)", "", hdr_raw)) if x.strip()}
        for tg in tags:
            n = SYN.get(slug(tg), slug(tg))
            if n in VOCAB or n in SECTORS or n == sub_slug or n in lend_slugs:
                keep.append(n)
            else:
                extra.append(n)
        keep = list(dict.fromkeys(keep))
        lslug = slug(str(lver))
        if lcheck == "mismatch" and lslug and lslug not in keep:
            keep.append(lslug)
        stats[("lender", lcheck)] += 1
        stats[("counterpart", ccheck)] += 1
        stats[("tags_extra", bool(extra))] += 1
        rep[pid] = {"lender": [hdr_l, sorted(ltxt), lcheck], "counterpart": [cp_h, cp_t, ccheck], "tags_extra": extra}
        if apply:
            put(h, "lender_in_cc", "/".join(sorted(ltxt)) if ltxt else "", after="lender")
            put(h, "lender_check", lcheck, after="lender_in_cc")
            put(h, "lender_verified", lver, after="lender_check")
            put(h, "counterpart_pct_in_cc", "" if cp_t is None else cp_t, after="counterpart_pct")
            put(h, "counterpart_check", ccheck, after="counterpart_pct_in_cc")
            put(h, "counterpart_pct_verified", cver, after="counterpart_check")
            put(h, "tags", "[" + ", ".join(keep) + "]")
            put(h, "tags_extra", "[" + ", ".join(extra) + "]", after="tags")
            pf.write_text("---\n" + "\n".join(h) + "\n---" + body, encoding="utf-8")
    nt_fix = 0
    for af in sorted((root / "avaliacoes").glob("*.md")):
        h, body = split(af)
        aid = get(h, "id")
        n = len(man.get(aid, {}).get("nts", []))
        if str(n) != get(h, "nt_docs"):
            nt_fix += 1
            if apply:
                put(h, "nt_docs", n)
                af.write_text("---\n" + "\n".join(h) + "\n---" + body, encoding="utf-8")
    for k, v in sorted(stats.items(), key=str):
        print(k, v)
    print("nt_docs ajustados:", nt_fix)
    if "--report" in sys.argv:
        json.dump(rep, open(sys.argv[sys.argv.index("--report") + 1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("apply" if apply else "dry-run")


if __name__ == "__main__":
    main()

"""Prepare lean source texts for the narrative/area agents (local, never committed).

usage: prepare_sources.py <manifest.json> <nt_index.json> <nt_text_dir> <md_nt_root> <md_cc_root> <out_dir> <manifest_clean.json>

Per source text:
  1. prefer the Markdown version when one exists (NTs: <md_nt_root>, same relative path with .md; CCs: <md_cc_root>)
  2. drop picture placeholders, html tags, markdown table separators, (cid:N) artifacts
  3. drop repeated page headers/footers: any line (>=25 chars, digits normalized) that occurs >=3 times in the document
     and is not a table-cell/numeric line; plus known boilerplate (signature stamps, page markers)
  4. collapse runs of spaces/tabs and blank lines
Writes cleaned copies to <out_dir> (cached by content hash) and a rewritten manifest pointing to them.
"""
import hashlib, json, re, sys
from collections import Counter
from pathlib import Path

PICTURE = re.compile(r"\*{0,2}==>\s*picture\s*\[[^\]]*\]\s*intentionally omitted\s*<==\*{0,2}")
BOILER = [
    re.compile(r"(?i)^documento assinado eletronicamente.*$"),
    re.compile(r"(?i)^a autenticidade deste documento.*$"),
    re.compile(r"(?i)^.*(?:Nota T[eé]cnica|Anexo|Resultado)[^\n]{0,80}\(\d{6,9}\)\s+SEI \d{5}\.\d{6}/\d{4}-\d{2}\s*/\s*pg\.\s*\d+\s*$"),
    re.compile(r"^\s*(?:P[áa]gina|pg\.?)\s*:?\s*\d+(?:\s*(?:de|/)\s*\d+)?\s*$", re.I),
    re.compile(r"^\s*\d{1,3}\s*$"),
    re.compile(r"^\s*(?:\.\s*){6,}\s*$"),
]
PROTECT = re.compile(r"\d,\d{3}|(?i:pontua|n[íi]vel|ano (?:da )?(?:meta|base)|linha de base|baseline|\bmeta\b)")
HEADER_WORDS = re.compile(
    r"(?i)minist[ée]rio do planejamento e or[çc]amento|secretaria de assuntos internacionais|subsecretaria de financiamento externo|"
    r"secretaria executiva da cofiex|comiss[ãa]o de financiamentos externos|esplanada dos minist[ée]rios|"
    r"^carta consulta n[º°o]|^carta consulta$|pfe - portal de financiamentos externos|n[úu]mero processo sei|c[óo]digo do pleito|"
    r"\bcriado em \d{2}/\d{2}/\d{4}|^\s*p[áa]gina\s*:?\s*\d+|documento assinado|^\s*\d{2}/\d{2}/\d{4}\s*-\s*\d{2}:\d{2}\s*$|"
    r"nota t[eé]cnica[^\n]{0,60}\(\d{6,9}\)\s+sei")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)*\|?\s*$")


def clean(text):
    t = PICTURE.sub(" ", text)
    t = re.sub(r"\(cid:\d+\)", " ", t)
    t = re.sub(r"<br\s*/?>", " ", t, flags=re.I)
    t = re.sub(r"</?(?:span|div|p|b|i|u|sup|sub|table|tr|td|th|tbody|thead)[^>]*>", " ", t, flags=re.I)
    lines = [ln.rstrip() for ln in t.splitlines()]
    norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())  # exact text: digits matter (baselines, targets, scores)
    cnt = Counter(norm(l) for l in lines if len(l.strip()) >= 25)
    out, seen_rep = [], set()
    for ln in lines:
        s = ln.strip()
        if not s or TABLE_SEP.match(s):
            out.append("")
            continue
        if any(b.match(s) for b in BOILER):
            continue
        n = norm(s)
        # only identical repeats that read as a page header/footer are removed (first copy kept); any other repeated
        # text, component lists included, is left untouched
        if len(s) >= 25 and cnt[n] >= 3 and HEADER_WORDS.search(s) and not PROTECT.search(s):
            if n in seen_rep:
                continue
            seen_rep.add(n)
        out.append(re.sub(r"[ \t]{2,}", " ", s))
    t = "\n".join(out)
    t = re.sub(r"\n{2,}", "\n", t)
    return t.strip() + "\n"


SEC_START = re.compile(r"(?im)^[#\s]*2\.6\.\s*Projeto\s*/\s*Indicadores\s*$")
SEC_END = re.compile(r"(?im)^[#\s]*2\.7\.\s*Projeto\s*/\s*Componentes\s*$")


def span(t):
    a = SEC_START.search(t)
    b = SEC_END.search(t, a.end()) if a else None
    return (a.start(), b.start()) if a and b else None


def hybrid(md_raw, txt_raw):
    """md body with the 2.6 Projeto/Indicadores block taken from the pdftotext version (md scrambles those tables by column)."""
    sm, st = span(md_raw), span(txt_raw)
    if not (sm and st):
        return None
    return md_raw[:sm[0]] + txt_raw[st[0]:st[1]] + md_raw[sm[1]:]


def main():
    man = json.load(open(sys.argv[1], encoding="utf-8"))
    idx = json.load(open(sys.argv[2], encoding="utf-8"))
    nt_dir, md_nt, md_cc = Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
    out, out_man = Path(sys.argv[6]), Path(sys.argv[7])
    out.mkdir(parents=True, exist_ok=True)
    key_by_path = {str(nt_dir / f"{k}.txt"): k for k in idx}
    stats = Counter()

    def prep(path, md_path=None, kind="cc"):
        src = Path(md_path) if md_path and Path(md_path).exists() else Path(path)
        try:
            raw = src.read_text(encoding="utf-8", errors="ignore")
            if "--hybrid-indicators" in sys.argv and src != Path(path) and kind == "cc" and Path(path).suffix == ".txt":
                h = hybrid(raw, Path(path).read_text(encoding="utf-8", errors="ignore"))
                if h:
                    raw = h
                    stats["hybrid_ok"] += 1
                else:
                    raw = Path(path).read_text(encoding="utf-8", errors="ignore")  # markers missing: whole txt
                    src = Path(path)
                    stats["hybrid_fallback_txt"] += 1
        except OSError:
            return None
        c = clean(raw)
        h = hashlib.md5(c.encode("utf-8")).hexdigest()
        dst = out / f"{kind}_{h}.txt"
        if not dst.exists():
            dst.write_text(c, encoding="utf-8")
        stats[(kind, "md" if src != Path(path) else "orig", "raw")] += len(raw)
        stats[(kind, "md" if src != Path(path) else "orig", "clean")] += len(c)
        return str(dst)

    seen_nt = {}
    new = {}
    for k, v in man.items():
        v = dict(v)
        if v.get("text"):
            p = Path(v["text"])
            md = None
            if p.suffix == ".txt" and "--keep-txt-2023" not in sys.argv:  # (--hybrid-indicators keeps the md twin and splices in the txt indicator block)  # 2023-24 txt -> try md twin (the md stacks indicator tables by column)
                m = re.match(r"CC_(\d+)_Versao_(\d+)", p.name)
                if m:
                    cand = md_cc / "Pleitos_2023_2024" / f"CC_{m.group(1)}" / f"CC_{m.group(1)}_Versao_{m.group(2)}.md"
                    md = cand if cand.exists() else None
            v["text"] = prep(v["text"], md, "cc") or v["text"]
        if v.get("nts"):
            lst = []
            for p in v["nts"]:
                key = key_by_path.get(p) or key_by_path.get(p.replace("/", "\\"))
                md = None
                if key:
                    rel = Path(idx[key])
                    cand = (md_nt / rel).with_suffix(".md")
                    md = cand if cand.exists() else None
                q = prep(p, md, "nt")
                if q and q not in lst:
                    lst.append(q)
            v["nts"] = lst
        new[k] = v
    json.dump(new, open(out_man, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("hybrid:", stats["hybrid_ok"], "ok |", stats["hybrid_fallback_txt"], "fallback to whole txt")
    stats = Counter({k: v for k, v in stats.items() if isinstance(k, tuple)})
    tot_raw = sum(v for (k, s, w), v in stats.items() if w == "raw")
    tot_clean = sum(v for (k, s, w), v in stats.items() if w == "clean")
    for kind in ("cc", "nt"):
        r = sum(v for (k, s, w), v in stats.items() if k == kind and w == "raw")
        c = sum(v for (k, s, w), v in stats.items() if k == kind and w == "clean")
        if r:
            print(f"{kind}: {r/1e6:.1f} MB -> {c/1e6:.1f} MB ({100*(1-c/r):.0f}% menor)")
    md_used = sum(1 for (k, s, w), v in stats.items() if s == "md" and w == "raw")
    print(f"total: {tot_raw/1e6:.1f} MB -> {tot_clean/1e6:.1f} MB ({100*(1-tot_clean/tot_raw):.0f}% menor)")
    print("fontes md usadas:", {f"{k}/{s}": round(v/1e6, 1) for (k, s, w), v in stats.items() if w == "raw"})


if __name__ == "__main__":
    main()

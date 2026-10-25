"""Build structured ficha skeletons (pleito + avaliacao) with narrative placeholders.

Rules:
  * One avaliacao ficha per workbook row (a pleito at a meeting); one pleito ficha per PFE.
  * The CC text used is the *judged version*: for 2025-26, the highest revision whose file date is
    <= the meeting date; if none qualifies or dates are placeholders, the last version. For 2023-24
    (no dates in file names) the last version. `version_rule` records how it was chosen.
  * Source texts and NTs stay local. A local manifest (never committed) maps ficha ids to them.
Outputs: fichas/pleitos/P####.md, fichas/avaliacoes/A####.md  (committed, anonymized)
         <manifest>.json (local only)
"""
import argparse, collections, hashlib, json, re, secrets, sys
from datetime import date
from pathlib import Path
import openpyxl

sys.path.insert(0, str(Path(__file__).parent))
import build_cases as bc  # noqa: E402


def parse_date(s):
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", str(s))
    return date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None


def collect_versions(ccroot, pdfroot=None):
    """-> (old: {pfe: [(ver, path)]}, new: {sei_norm: [(ver, date|None, path)]})"""
    old = collections.defaultdict(list)
    old_dir = (Path(pdfroot) / "Pleitos_2023_2024" / "cc_extraidos") if pdfroot else (ccroot / "Pleitos_Textos_MD" / "Pleitos_2023_2024")
    for p in old_dir.rglob("CC_*_Versao_*.txt" if pdfroot else "CC_*_Versao_*.md"):
        m = re.match(r"CC_(\d+)_Versao_(\d+)", p.name)
        old[m.group(1)].append((int(m.group(2)), p))
    new = collections.defaultdict(list)
    for p in (ccroot / "Pleitos_Textos_MD" / "Pleitos_2025_2026").rglob("Pleito_*.md"):
        m = re.match(r"Pleito_(\d+)_\d{4}_revisao_(\d+)_(\d{4})-(\d{2})-(\d{2})_(\d{2})h(\d{2})m", p.name)
        if not m:
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")[:3000]
        sei = re.search(r"Processo SEI:\s*([\d\./-]+)", txt)
        if sei:
            d = date(int(m.group(3)), int(m.group(4)), int(m.group(5)))
            new[bc.norm_sei(sei.group(1))].append((int(m.group(2)), d, p))
    return old, new


def pick_version(row_pfe, row_sei, mdate, old, new):
    if row_pfe in old:
        vs = sorted(old[row_pfe])
        return vs[-1][0], vs[-1][1], len(vs), "last_no_dates"
    vs = sorted(new.get(row_sei, []))
    if not vs:
        return None, None, 0, "no_text"
    dated = [v for v in vs if v[1] is not None and mdate is not None and v[1] <= mdate]
    distinct = len({v[1] for v in vs}) == len(vs)  # same-day revisions => placeholder dates, ambiguous
    if dated and distinct:
        v = dated[-1]
        return v[0], v[2], len(vs), "date_match_earlier" if v is not vs[-1] else "last_confirmed_by_date"
    return vs[-1][0], vs[-1][2], len(vs), "last_default"


def yaml(d):
    out = []
    for k, v in d.items():
        if isinstance(v, (list, tuple)):
            out.append(f"{k}: [{', '.join(str(x) for x in v)}]")
        else:
            out.append(f"{k}: {'' if v is None else v}")
    return "---\n" + "\n".join(out) + "\n---\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--ccroot", required=True)
    ap.add_argument("--nt-links", required=True, help="local json: row index -> NT text keys")
    ap.add_argument("--nt-index", required=True, help="local json: NT key -> relative path")
    ap.add_argument("--nt-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--pdfroot", default=None)
    ap.add_argument("--idmap", required=True, help="local json with stable key->id (never committed)")
    ap.add_argument("--dry-run", action="store_true", help="write only <idmap>.rowmap.json (ficha id -> workbook row); touch no ficha")
    ap.add_argument("--force", action="store_true", help="overwrite fichas whose narrative is already filled")
    a = ap.parse_args()
    out, ccroot = Path(a.out), Path(a.ccroot)
    wb = openpyxl.load_workbook(a.xlsx, read_only=True, data_only=True)
    projs = list(wb["PROJECTS_ALL"].iter_rows(values_only=True))[1:]
    scores = {str(r[5]).strip(): r for r in list(wb["SCORING_ALL"].iter_rows(values_only=True))[1:]}
    meeting_regime = {}
    for r in scores.values():
        meeting_regime.setdefault(str(r[0]), "NR1_2024" if "1/2024" in str(r[2]) else "R17_2021")
    links = json.load(open(a.nt_links, encoding="utf-8"))
    ntidx = json.load(open(a.nt_index, encoding="utf-8"))
    old, new = collect_versions(ccroot, a.pdfroot)

    idmap_path = Path(a.idmap)
    idmap = json.load(open(idmap_path, encoding="utf-8")) if idmap_path.exists() else {}

    def oid(kind, key):
        k = f"{kind}|{key}"
        if k not in idmap:
            used = set(idmap.values())
            while True:
                cand = kind + secrets.token_hex(3).upper()
                if cand not in used:
                    break
            idmap[k] = cand
        return idmap[k]
    rows = []
    for i, r in enumerate(projs):
        meeting, d, sei, sub, prop, title, pfe, lender, loan, cp, outcome, reason = r[:12]
        pfe = str(pfe).strip()
        ver, path, nver, rule = pick_version(pfe, bc.norm_sei(sei), parse_date(d), old, new)
        text = path.read_text(encoding="utf-8", errors="ignore") if path else ""
        feats = bc.text_features(text) if text else {}
        sector = bc.sector_of(str(title))
        if sector == "other":  # sector is a pleito property: fall back on the LAST version, as build_cases does
            lv = sorted(old[pfe])[-1][1] if pfe in old else (sorted(new.get(bc.norm_sei(sei), []))[-1][2] if new.get(bc.norm_sei(sei)) else None)
            if lv:
                head = lv.read_text(encoding="utf-8", errors="ignore")[:900]
                sector = bc.sector_of(re.sub(r"(?i)assuntos internacionais e desenvolvimento|minist[eé]rio do planejamento", "", head))
        y, q = bc.quarter(d)
        sc = scores.get(pfe)
        regime = meeting_regime.get(str(meeting), "NR1_2024" if str(d)[-4:] >= "2025" else "")
        nts = [ntidx[k] for k in links.get(str(i), [])]
        organs = sorted({("SEAID" if "seaid" in n.lower() else "STN" if "stn" in n.lower() else "SOF" if "sof" in n.lower() else "SEPLAN" if "seplan" in n.lower() else "other") for n in nts})
        rows.append(dict(i=i, pfe=pfe, key=pfe if pfe in old else bc.norm_sei(sei), date=parse_date(d), y=y, q=q, sub=re.sub(r"[^\x20-\x7e]+", "-", str(sub)).strip("- "),
                         lender=lender, band=bc.band(loan, lender, sub), cp=(round(100 * float(cp) / (float(cp) + float(loan)), 1) if bc.f(cp) is not None and bc.f(loan) else ""),
                         outcome=bc.OUTCOME.get(str(outcome), "other"), reason=bc.reason_cat(reason), sector=sector, regime=regime,
                         ver=ver, nver=nver, rule=rule, path=path, feats=feats, sc=sc, nts=nts, organs=organs, nt_keys=links.get(str(i), [])))

    # attempt number per pleito (order by date)
    byp = collections.defaultdict(list)
    for r in rows:
        byp[r["key"]].append(r)
    for rs in byp.values():
        rs.sort(key=lambda r: (r["date"] or date.min))
    pid = {k: oid("P", k) for k in byp}
    for k, rs in byp.items():
        for n, r in enumerate(rs, 1):
            r["attempt"] = n
            r["aid"] = oid("A", (k, n))

    # --- NT resolution: same meeting > no-meeting-folder > (single attempt) other meeting; dedupe by content ---
    def nt_meeting(rel):
        m = re.search(r"(\d{3})\S{0,3}\s*Reuni", rel)
        return int(m.group(1)) if m else None

    def content_hash(k):
        p = Path(a.nt_dir) / f"{k}.txt"
        return hashlib.md5(p.read_bytes()).hexdigest() if p.exists() else None

    for k, rs in byp.items():
        for r in rs:
            rm = int(re.match(r"\d+", str(projs[r["i"]][0])).group())
            keys = [kk for kk in r["nt_keys"] if (Path(a.nt_dir) / f"{kk}.txt").exists()]
            same = [kk for kk in keys if nt_meeting(ntidx[kk]) == rm]
            nofold = [kk for kk in keys if nt_meeting(ntidx[kk]) is None]
            if same:
                pick, how = same, "same_meeting"
            elif nofold:
                pick, how = nofold, "no_meeting_folder"
            elif keys and len(rs) == 1:
                pick, how = keys, "single_attempt_fallback"
            else:
                pick, how = [], "none"
            seen, uniq = set(), []
            for kk in pick:
                h = content_hash(kk)
                if h not in seen:
                    seen.add(h)
                    uniq.append(kk)
            r["nt_keys"] = uniq
            r["nts"] = [ntidx[kk] for kk in uniq]
            r["nt_match"] = how
            r["organs"] = sorted({("SEAID" if "seaid" in n.lower() else "STN" if "stn" in n.lower() else "SOF" if "sof" in n.lower() else "SEPLAN" if "seplan" in n.lower() else "other") for n in r["nts"]})

    rowmap = {r["aid"]: r["i"] for rs in byp.values() for r in rs}
    rowmap.update({pid[k]: [r["i"] for r in rs] for k, rs in byp.items()})
    json.dump(rowmap, open(str(idmap_path) + ".rowmap.json", "w", encoding="utf-8"))
    if a.dry_run:
        json.dump(idmap, open(idmap_path, "w", encoding="utf-8"), indent=1)
        print("dry-run: rowmap written;", len(rowmap), "entries")
        return

    for sub in ("pleitos", "avaliacoes"):
        (out / "fichas" / sub).mkdir(parents=True, exist_ok=True)
    manifest = {}
    featkeys = ["n_indicators", "n_indicators_parse", "baseline_defined_share", "text_chars_k", "mentions_opex_sustain", "mentions_licensing",
                "mentions_gender_race", "mentions_iso_benchmark", "mentions_ppp_guarantee"]
    for k, rs in byp.items():
        last = rs[-1]
        hist = " > ".join(f"{r['attempt']}:{r['outcome']}@{r['y']}Q{r['q']}" for r in rs)
        head = dict(id=pid[k], type="pleito", sector=last["sector"], subtype=last["sub"], lender=last["lender"], ticket_band=last["band"],
                    counterpart_pct=last["cp"], versions_total=last["nver"], version_used=last["ver"], version_rule=last["rule"],
                    attempts=len(rs), attempt_history=hist, avaliacoes=[r["aid"] for r in rs],
                    tags=[last["sector"], last["sub"].lower().replace(" ", "_"), str(last["lender"]).lower().replace(" ", "_")],
                    **{kk: last["feats"].get(kk, "") for kk in featkeys})
        body = ("\n## Resumo\n<!-- narrativa: pendente -->\n\n## Teoria da mudança e indicadores\n<!-- pendente -->\n\n"
                "## Sustentabilidade e riscos\n<!-- pendente -->\n\n## Perguntas GTEC provaveis\n<!-- pendente -->\n")
        if not last["path"]:
            body = body.replace("<!-- narrativa: pendente -->", "_CC text unavailable in the corpus: scores and NT findings only._").replace("<!-- pendente -->", "_n/a_")
        pf = out / "fichas/pleitos" / f"{pid[k]}.md"
        if a.force or not pf.exists() or "pendente" in pf.read_text(encoding="utf-8"):
            pf.write_text(yaml(head) + body, encoding="utf-8")
        manifest[pid[k]] = {"type": "pleito", "text": str(last["path"]) if last["path"] else None}
        for r in rs:
            sc = r["sc"]
            comp = {}
            if sc and r["regime"] == "NR1_2024":
                comp = dict(ae=sc[9], idh_pts=sc[10], capag_pts=sc[6], debt_pts=sc[7], total=sc[11])
            elif sc:
                comp = dict(ae="", idh_pts="", capag_pts="", debt_pts="", total=sc[11])
            else:
                comp = dict(ae="", idh_pts="", capag_pts="", debt_pts="", total="")
            h = dict(id=r["aid"], type="avaliacao", pleito=pid[k], attempt=r["attempt"], regime=r["regime"], year=r["y"], quarter=r["q"],
                     subtype=r["sub"], sector=r["sector"], lender=r["lender"], ticket_band=r["band"], outcome=r["outcome"],
                     reason_cat=r["reason"], nt_disponivel="sim" if r["nts"] else "nao", nt_docs=len(r["nts"]), nt_match=r["nt_match"], nt_orgaos=r["organs"],
                     version_judged=r["ver"], version_rule=r["rule"], **comp)
            b = "\n## Motivos e achados da NT\n" + ("<!-- narrativa: pendente -->\n" if r["nts"] else "_NT nao disponivel: so notas e desfecho._\n")
            af = out / "fichas/avaliacoes" / f"{r['aid']}.md"
            if a.force or not af.exists() or "pendente" in af.read_text(encoding="utf-8"):
                af.write_text(yaml(h) + b, encoding="utf-8")
            manifest[r["aid"]] = {"type": "avaliacao", "pleito": pid[k], "text": str(r["path"]) if r["path"] else None,
                                  "nts": [str(Path(a.nt_dir) / f"{kk}.txt") for kk in r["nt_keys"]]}
    json.dump(manifest, open(a.manifest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(idmap, open(idmap_path, "w", encoding="utf-8"), indent=1)
    rule = collections.Counter(r["rule"] for r in rows)
    print(len(byp), "pleitos,", len(rows), "avaliacoes; version rules:", dict(rule), "; sem NT:", sum(1 for r in rows if not r["nts"]), "; nt_match:", dict(collections.Counter(r["nt_match"] for r in rows)))


if __name__ == "__main__":
    main()

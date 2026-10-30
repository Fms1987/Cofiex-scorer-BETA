"""Score a blind run of the fixed test bank and compare it with a baseline (proposal items C5, C6, C10).

usage: run_regression.py <bank_dir> <out_dir> <blocks_dir_or_file>... [--label v2] [--baseline metrics.json]

<bank_dir>: output of build_test_bank.py (bank.csv, truth.csv, truth_areas.csv). PRIVATE.
Blocks: written by each blind run (sandbox built with make_blind_sandbox.py @ids.txt), one per pleito:
===PLEITO===
ID: <pleito_id, digits from the Pleito_<id>_... filename>
NOTA_GERAL_MIN: <float>
NOTA_GERAL_ESP: <float>
NOTA_GERAL_MAX: <float>
AE: <float>            (Nota de Área Estratégica esperada, bônus incluído; optional)
CAPAG: <float>         (optional; subnational only)
DIVIDA: <float>        (optional)
IDH: <float>           (optional)
AREA: <código PPA> | <A|B|C|D|E|0>   (one line per area declared or scored; optional)
===FIM===
Older blocks (PROBABILIDADE line, no components) still parse.

Writes casos.csv, metrics.json and relatorio.md to <out_dir>. With --baseline, flags a REGRESSÃO when
a headline metric gets worse beyond tolerance.
"""
import argparse, csv, json, re, statistics
from collections import Counter, defaultdict
from pathlib import Path

NIVEIS = ["A", "B", "C", "D", "E", "0"]
BLOCK = re.compile(r"===PLEITO===(.*?)===FIM===", re.S)
# metric -> (direction, tolerance): +1 = higher is better
HEADLINE = {"mae_nota_geral": (-1, 0.10), "mae_ae": (-1, 0.10), "acerto_nivel_area_principal": (+1, 0.05),
            "cobertura_faixa": (+1, 0.05), "abs_vies_idh": (-1, 0.05)}


def num(s):
    try:
        return float(str(s).replace(",", "."))
    except (TypeError, ValueError):
        return None


def parse_blocks(paths):
    out = {}
    files = []
    for p in map(Path, paths):
        files += sorted(p.glob("*.md")) if p.is_dir() else [p]
    for f in files:
        for m in BLOCK.finditer(f.read_text(encoding="utf-8", errors="replace")):
            b = {"areas": {}}
            for line in m.group(1).strip().splitlines():
                if ":" not in line:
                    continue
                k, v = (x.strip() for x in line.split(":", 1))
                k = k.upper()
                if k == "AREA" and "|" in v:
                    cod, niv = (x.strip() for x in v.split("|", 1))
                    b["areas"][cod] = niv.upper() if niv.upper() in NIVEIS else "0"
                elif k == "ID":
                    b["id"] = re.match(r"\d+", v).group(0)
                else:
                    b[k] = num(v)
            if "id" in b:
                out[b["id"]] = b
    return out


def q(v, p):
    v = sorted(v)
    return round(v[min(len(v) - 1, int(round(p * (len(v) - 1))))], 2) if v else None


def mae(pairs):
    return round(statistics.mean(abs(p - o) for p, o in pairs), 3) if pairs else None


def vies(pairs):
    return round(statistics.mean(p - o for p, o in pairs), 3) if pairs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bank_dir"); ap.add_argument("out_dir"); ap.add_argument("blocks", nargs="+")
    ap.add_argument("--label", default="run"); ap.add_argument("--baseline")
    a = ap.parse_args()
    bank = Path(a.bank_dir)
    with open(bank / "bank.csv", encoding="utf-8") as fh:
        estrato = {r["pleito_id"]: r["estrato"] for r in csv.DictReader(fh)}
    with open(bank / "truth.csv", encoding="utf-8") as fh:
        truth = {r["pleito_id"]: r for r in csv.DictReader(fh)}
    ta = defaultdict(dict)
    with open(bank / "truth_areas.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            ta[r["pleito_id"]][r["codigo_ppa"]] = (r["nivel"], num(r["pontos"]) or 0.0)
    blocks = {k: v for k, v in parse_blocks(a.blocks).items() if k in truth}

    casos, comp = [], defaultdict(list)
    conf = Counter()
    main_hit = main_near = main_n = all_hit = all_n = 0
    for pid, b in sorted(blocks.items()):
        t = truth[pid]
        off, esp = num(t["nota_geral"]), b.get("NOTA_GERAL_ESP")
        if esp is None:
            continue
        comp["nota_geral"].append((esp, off))
        for k, col in (("AE", "ae"), ("CAPAG", "capag"), ("DIVIDA", "divida"), ("IDH", "idh")):
            if b.get(k) is not None and num(t[col]) is not None:
                comp[col].append((b[k], num(t[col])))
        lo, hi = b.get("NOTA_GERAL_MIN"), b.get("NOTA_GERAL_MAX")
        row = {"pleito_id": pid, "estrato": estrato[pid], "nota_oficial": off, "nota_esp": esp, "delta": round(esp - off, 3),
               "na_faixa": "" if lo is None or hi is None else int(lo <= off <= hi), "largura": "" if lo is None or hi is None else round(hi - lo, 2),
               "ae_oficial": t["ae"], "ae_esp": b.get("AE", ""), "area_principal": "", "nivel_oficial": "", "nivel_previsto": ""}
        if b["areas"] and ta.get(pid):
            off_areas = ta[pid]
            principal = max(off_areas, key=lambda c: off_areas[c][1])
            if off_areas[principal][1] > 0:
                no, np_ = off_areas[principal][0], b["areas"].get(principal, "0")
                main_n += 1; main_hit += no == np_; main_near += abs(NIVEIS.index(no) - NIVEIS.index(np_)) <= 1
                row.update(area_principal=principal, nivel_oficial=no, nivel_previsto=np_)
            for cod in set(off_areas) | set(b["areas"]):
                no, np_ = off_areas.get(cod, ("0", 0))[0], b["areas"].get(cod, "0")
                conf[(no, np_)] += 1; all_n += 1; all_hit += no == np_
        casos.append(row)

    absd = [abs(p - o) for p, o in comp["nota_geral"]]
    absae = [abs(p - o) for p, o in comp["ae"]]
    cov = [r["na_faixa"] for r in casos if r["na_faixa"] != ""]
    por_estrato = defaultdict(list)
    for r in casos:
        por_estrato[r["estrato"]].append(abs(r["delta"]))
    m = {
        "label": a.label, "n": len(casos), "n_banco": len(truth),
        "mae_nota_geral": mae(comp["nota_geral"]), "vies_nota_geral": vies(comp["nota_geral"]),
        "mediana_abs_nota_geral": round(statistics.median(absd), 3) if absd else None,
        "mae_ae": mae(comp["ae"]), "vies_ae": vies(comp["ae"]), "n_ae": len(comp["ae"]),
        "mae_capag": mae(comp["capag"]), "mae_divida": mae(comp["divida"]),
        "mae_idh": mae(comp["idh"]), "vies_idh": vies(comp["idh"]),
        "abs_vies_idh": abs(vies(comp["idh"])) if comp["idh"] else None,
        "cobertura_faixa": round(sum(cov) / len(cov), 3) if cov else None,
        "largura_mediana_faixa": statistics.median([r["largura"] for r in casos if r["largura"] != ""]) if cov else None,
        "acerto_nivel_area_principal": round(main_hit / main_n, 3) if main_n else None,
        "acerto_nivel_area_principal_1_degrau": round(main_near / main_n, 3) if main_n else None,
        "n_area_principal": main_n,
        "acerto_nivel_todas_areas": round(all_hit / all_n, 3) if all_n else None, "n_areas": all_n,
        "faixa_empirica": {"nota_geral_p70": q(absd, .7), "nota_geral_p80": q(absd, .8),
                           "ae_p70": q(absae, .7), "ae_p80": q(absae, .8)},
        "mae_por_estrato": {s: round(statistics.mean(v), 3) for s, v in sorted(por_estrato.items())},
        "matriz_confusao": {o: {p: conf[(o, p)] for p in NIVEIS} for o in NIVEIS} if all_n else None,
    }

    alertas = []
    if a.baseline:
        base = json.loads(Path(a.baseline).read_text(encoding="utf-8"))
        m["baseline"] = base.get("label")
        for k, (sinal, tol) in HEADLINE.items():
            if m.get(k) is None or base.get(k) is None:
                continue
            piora = (base[k] - m[k]) * sinal
            if piora > tol:
                alertas.append(f"REGRESSÃO em {k}: {base[k]} → {m[k]} (tolerância {tol})")
        m["regressoes"] = alertas

    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    with open(out / "casos.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(casos[0]) if casos else ["pleito_id"]); w.writeheader(); w.writerows(casos)
    (out / "metrics.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")

    fmt = lambda x: "—" if x is None else str(x)
    L = [f"# Regressão — {a.label}", "", f"Pleitos avaliados: {m['n']} de {m['n_banco']} do banco.", "",
         "| Métrica | Valor | Baseline |", "|---|---|---|"]
    base = json.loads(Path(a.baseline).read_text(encoding="utf-8")) if a.baseline else {}
    for k in ["mae_nota_geral", "vies_nota_geral", "mediana_abs_nota_geral", "mae_ae", "vies_ae", "mae_capag", "mae_divida",
              "mae_idh", "vies_idh", "cobertura_faixa", "largura_mediana_faixa", "acerto_nivel_area_principal",
              "acerto_nivel_area_principal_1_degrau", "acerto_nivel_todas_areas"]:
        L.append(f"| {k} | {fmt(m.get(k))} | {fmt(base.get(k))} |")
    fe = m["faixa_empirica"]
    L += ["", f"Faixa empírica: Nota Geral ±{fe['nota_geral_p80']} (80%), ±{fe['nota_geral_p70']} (70%); "
              f"Área Estratégica ±{fe['ae_p80']} (80%).", "", "**MAE por estrato:**"]
    L += [f"- {s}: {v}" for s, v in m["mae_por_estrato"].items()]
    if m["matriz_confusao"]:
        L += ["", "**Matriz de confusão por área (linhas = oficial, colunas = previsto):**", "",
              "| oficial \\ previsto | " + " | ".join(NIVEIS) + " |", "|---" * (len(NIVEIS) + 1) + "|"]
        L += [f"| {o} | " + " | ".join(str(m["matriz_confusao"][o][p]) for p in NIVEIS) + " |" for o in NIVEIS]
    L += ["", "**Resultado:** " + ("; ".join(alertas) if alertas else ("sem regressão frente ao baseline" if a.baseline else "sem baseline"))]
    (out / "relatorio.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

"""Parse structured blind-scoring blocks produced by batches of blind-test subagents and cross
them against the official ground truth (match_pleitos_to_results.py output), computing delta
per case and summary stats.

Expected block format in each transcript .md (one or more per file), exactly:
===PLEITO===
ID: <digits, matches the Pleito_<digits>_... filename prefix>
NOTA_GERAL_MIN: <float>
NOTA_GERAL_ESP: <float>
NOTA_GERAL_MAX: <float>
PROBABILIDADE: <baixa|moderada|alta|texto livre curto>
===FIM===
Anything else in the file (narrative, justificativas) is ignored by this parser -- it only
reads these blocks, so the blind-scoring agents can keep writing full narratives before each
block.

Usage: python tools/parse_blind_results.py <ground_truth_csv> <out_csv> <blocks_dir_or_file>...
  ground_truth_csv: columns pleito_id, resultado_pontuacao, nota_final_pontuacao (as produced
    by match_pleitos_to_results.py)
  blocks_dir_or_file: one or more .md files, or directories to scan for *.md, containing the
    ===PLEITO===...===FIM=== blocks
"""
import argparse
import csv
import re
import statistics
from pathlib import Path

BLOCK_RE = re.compile(
    r"===PLEITO===\s*"
    r"ID:\s*(\d+)[^\n]*\n"
    r"NOTA_GERAL_MIN:\s*([\d.,]+)\s*\n"
    r"NOTA_GERAL_ESP:\s*([\d.,]+)\s*\n"
    r"NOTA_GERAL_MAX:\s*([\d.,]+)\s*\n"
    r"PROBABILIDADE:\s*([^\n]+)\n"
    r"\s*===FIM===",
    re.IGNORECASE,
)


def fnum(s):
    return float(s.replace(",", "."))


def collect_files(paths):
    files = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files.extend(sorted(p.glob("*.md")))
        else:
            files.append(p)
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ground_truth_csv")
    ap.add_argument("out_csv")
    ap.add_argument("blocks", nargs="+")
    a = ap.parse_args()

    truth = {}
    with open(a.ground_truth_csv, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            pid = r.get("pleito_id")
            if pid and r.get("nota_final_pontuacao"):
                truth[pid] = r

    blind = {}
    dupes = []
    for f in collect_files(a.blocks):
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in BLOCK_RE.finditer(text):
            pid, lo, esp, hi, prob = m.groups()
            if pid in blind:
                dupes.append((pid, str(f)))
            blind[pid] = {
                "nota_cega_min": fnum(lo), "nota_cega_esp": fnum(esp),
                "nota_cega_max": fnum(hi), "probabilidade": prob.strip(),
                "arquivo": f.name,
            }

    if dupes:
        print(f"AVISO: {len(dupes)} ID(s) duplicado(s) entre arquivos de blocos: {dupes}")

    rows = []
    missing_truth, missing_blind = [], []
    for pid, b in blind.items():
        t = truth.get(pid)
        if not t:
            missing_truth.append(pid)
            continue
        oficial = fnum(t["nota_final_pontuacao"])
        delta = b["nota_cega_esp"] - oficial
        rows.append({
            "pleito_id": pid, "resultado_oficial": t["resultado_pontuacao"],
            "nota_oficial": oficial, "nota_cega_min": b["nota_cega_min"],
            "nota_cega_esp": b["nota_cega_esp"], "nota_cega_max": b["nota_cega_max"],
            "probabilidade": b["probabilidade"], "delta": round(delta, 3),
            "abs_delta": round(abs(delta), 3),
        })
    for pid in truth:
        if pid not in blind:
            missing_blind.append(pid)

    rows.sort(key=lambda r: -r["abs_delta"])
    with open(a.out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else [
            "pleito_id", "resultado_oficial", "nota_oficial", "nota_cega_min",
            "nota_cega_esp", "nota_cega_max", "probabilidade", "delta", "abs_delta"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    n = len(rows)
    print(f"{n} pleitos cruzados com sucesso.")
    if missing_truth:
        print(f"{len(missing_truth)} bloco(s) sem gabarito correspondente: {missing_truth}")
    if missing_blind:
        print(f"{len(missing_blind)} pleito(s) do gabarito sem bloco cego encontrado: {missing_blind}")
    if n:
        deltas = [r["delta"] for r in rows]
        abs_deltas = [r["abs_delta"] for r in rows]
        print(f"MAE={sum(abs_deltas)/n:.3f} (escala 0-15, {sum(abs_deltas)/n/15:.1%}); "
              f"viés médio={sum(deltas)/n:.3f}; mediana |delta|={statistics.median(abs_deltas):.3f}")
        print("Maiores erros:")
        for r in rows[:8]:
            print(f"  {r['pleito_id']}: oficial={r['nota_oficial']} ({r['resultado_oficial']}) "
                  f"cego_esp={r['nota_cega_esp']} delta={r['delta']}")

    print(f"Saída: {a.out_csv}")


if __name__ == "__main__":
    main()

"""Match raw carta-consulta .md files (Pleitos_Textos_MD/Pleitos_2025_2026) to their official
COFIEX result in the consolidated scoring workbook, by SEI process number.

This is a pre-step for a blind-test validation round: it only determines WHICH pleitos have a
ground truth to compare against later. It does not read scores into anything used during the
blind evaluation itself -- keep this script's output away from the model doing the blind
scoring, per the blind-judgment rule (never self-consult a case's own outcome before scoring).

Usage: python tools/match_pleitos_to_results.py <pleitos_dir> <consolidated_xlsx> <out_csv>
"""
import argparse
import csv
import re
from pathlib import Path

import openpyxl

SEI_RE = re.compile(r"Processo SEI:\s*([\d./-]+)")
CODIGO_RE = re.compile(r"C[oó]digo do pleito:\s*([\d/]+)")


def norm_sei(s):
    return re.sub(r"[^\d]", "", str(s or ""))


def latest_revision_per_pleito(pleitos_dir):
    by_id = {}
    for f in Path(pleitos_dir).glob("Pleito_*.md"):
        m = re.match(r"Pleito_(\d+)_(\d+)_revisao_(\d+)_(\S+)", f.stem)
        if not m:
            continue
        pid, _, rev, ts = m.groups()
        key = (pid, int(rev), ts)
        if pid not in by_id or key > by_id[pid][0]:
            by_id[pid] = (key, f)
    return {pid: f for pid, (key, f) in by_id.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pleitos_dir")
    ap.add_argument("xlsx")
    ap.add_argument("out_csv")
    a = ap.parse_args()

    latest = latest_revision_per_pleito(a.pleitos_dir)
    print(f"{len(latest)} pleitos únicos; usando a revisão mais recente de cada.")

    wb = openpyxl.load_workbook(a.xlsx, read_only=True, data_only=True)
    projetos = list(wb["PROJETOS"].iter_rows(values_only=True))[1:]
    pontuacao = list(wb["PONTUACAO"].iter_rows(values_only=True))[1:]
    by_sei = {}
    for i, r in enumerate(projetos):
        sei = norm_sei(r[3])
        if sei:
            by_sei.setdefault(sei, []).append(i)
    # PONTUACAO rows are not guaranteed to be in the same order/count as PROJETOS; join by
    # (Reunião, N° PFE) instead, which both sheets carry.
    pont_by_key = {(r[0], r[3]): r for r in pontuacao}

    out_rows = []
    matched = 0
    for pid, f in sorted(latest.items()):
        text = f.read_text(encoding="utf-8", errors="replace")[:3000]
        sei_m = SEI_RE.search(text)
        sei = norm_sei(sei_m.group(1)) if sei_m else ""
        hits = by_sei.get(sei, [])
        if not hits:
            out_rows.append({"pleito_id": pid, "arquivo": f.name, "sei": sei_m.group(1) if sei_m else "",
                              "match": "NAO_ENCONTRADO"})
            continue
        matched += 1
        for idx in hits:
            proj = projetos[idx]
            key = (proj[0], proj[2])  # Reunião, N° PFE
            pont = pont_by_key.get(key)
            out_rows.append({
                "pleito_id": pid, "arquivo": f.name, "sei": sei_m.group(1),
                "match": "OK", "reuniao": proj[0], "data_reuniao": proj[1], "n_pfe": proj[2],
                "resultado_projetos": proj[16], "nota_total_projetos": proj[15],
                "nota_final_pontuacao": pont[20] if pont else None,
                "resultado_pontuacao": pont[7] if pont else None,
            })

    with open(a.out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["pleito_id", "arquivo", "sei", "match", "reuniao",
                                           "data_reuniao", "n_pfe", "resultado_projetos",
                                           "nota_total_projetos", "nota_final_pontuacao",
                                           "resultado_pontuacao"])
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"{matched}/{len(latest)} pleitos com SEI encontrado na base consolidada.")
    print(f"Saída: {a.out_csv}")


if __name__ == "__main__":
    main()

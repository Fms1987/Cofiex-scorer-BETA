"""Backtest the iteration/persistence rules (FASE 9.5) against every PFE that appears in
more than one COFIEX meeting, instead of the n=9 hand-picked sample in references/iteration/
persistence.md.

Input is a private, non-anonymized workbook (entity/project names) -- e.g.
COFIEX_Base_Consolidada_165_189_PT.xlsx, sheet PONTUACAO -- that lives outside this repo
(Cofiex-scorer-archive), never inside skills/cofiex-scorer/. This script only prints
aggregated, anonymized statistics (counts, rates, score deltas) -- never per-case rows with
entity/project names -- so its stdout is safe to fold into persistence.md /
cross-cutting-findings.md. Raise exceptions on structural assumptions the caller should check,
rather than silently skipping rows, since each column index is a hardcoded reading of that
single workbook layout.

Usage: python tools/backtest_iteration.py <xlsx_path> [--sheet PONTUACAO]
"""
import argparse
import re
from collections import Counter, defaultdict

import openpyxl

COL_REUNIAO, COL_PFE, COL_RESULTADO, COL_NOTA_FINAL = 0, 3, 7, 20
APROVADO = {"Aprovado", "Aprovado parcialmente"}


def meeting_number(label):
    m = re.search(r"\d+", str(label))
    if not m:
        raise ValueError(f"cannot parse meeting number from {label!r}")
    return int(m.group())


def load_sequences(xlsx_path, sheet):
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    rows = list(wb[sheet].iter_rows(values_only=True))[1:]
    by_pfe = defaultdict(list)
    for r in rows:
        pfe = r[COL_PFE]
        if pfe is None:
            continue
        by_pfe[pfe].append((meeting_number(r[COL_REUNIAO]), r[COL_RESULTADO], r[COL_NOTA_FINAL]))
    for pfe, recs in by_pfe.items():
        recs.sort(key=lambda x: x[0])
    return by_pfe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx_path")
    ap.add_argument("--sheet", default="PONTUACAO")
    a = ap.parse_args()

    by_pfe = load_sequences(a.xlsx_path, a.sheet)
    multi = {pfe: recs for pfe, recs in by_pfe.items() if len(recs) > 1}

    print(f"N° PFE únicos: {len(by_pfe)}")
    print(f"N° PFE com >1 reunião (reenvio/multi-tranche): {len(multi)}")
    print(f"Distribuição de nº de reuniões por PFE: {dict(Counter(len(v) for v in multi.values()))}")
    print()

    # Approval rate by attempt number (1st, 2nd, 3rd+ appearance of the same PFE)
    attempt_outcomes = defaultdict(Counter)
    for recs in multi.values():
        for i, (_, resultado, _) in enumerate(recs, start=1):
            attempt = i if i < 3 else "3+"
            attempt_outcomes[attempt][resultado] += 1
    print("Resultado por nº de tentativa (apenas PFE com reenvio):")
    for attempt in sorted(attempt_outcomes, key=lambda x: (x != "3+", x)):
        total = sum(attempt_outcomes[attempt].values())
        aprovado = sum(n for res, n in attempt_outcomes[attempt].items() if res in APROVADO)
        print(f"  tentativa {attempt}: n={total}, aprovado={aprovado} ({aprovado/total:.0%}), "
              f"detalhe={dict(attempt_outcomes[attempt])}")
    print()

    # Score-stability check: consecutive-meeting score deltas for the same PFE
    deltas = []
    for recs in multi.values():
        for (_, _, n1), (_, _, n2) in zip(recs, recs[1:]):
            if n1 is not None and n2 is not None:
                deltas.append(round(n2 - n1, 4))
    unchanged = sum(1 for d in deltas if abs(d) < 0.001)
    print(f"Delta de Nota Final entre reuniões consecutivas do mesmo PFE (n={len(deltas)}):")
    print(f"  inalterada (|Δ|<0.001): {unchanged} ({unchanged/len(deltas):.0%})")
    changed = [d for d in deltas if abs(d) >= 0.001]
    if changed:
        print(f"  alterada: {len(changed)} ({len(changed)/len(deltas):.0%}); "
              f"média={sum(changed)/len(changed):.3f}, min={min(changed):.3f}, max={max(changed):.3f}")

    # Outcome-transition matrix (what the previous meeting's result was -> what the next one was)
    print()
    trans = Counter()
    for recs in multi.values():
        for (_, r1, _), (_, r2, _) in zip(recs, recs[1:]):
            trans[(r1, r2)] += 1
    print("Transições de resultado (reunião anterior -> próxima reunião), n por par:")
    for (r1, r2), n in trans.most_common():
        print(f"  {r1!r} -> {r2!r}: {n}")


if __name__ == "__main__":
    main()

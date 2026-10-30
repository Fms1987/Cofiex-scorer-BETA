"""Prazos e comissões típicos por credor externo, para o comparativo da justificativa do credor.

uso: python -X utf8 creditor_terms.py [planilha.xlsx] [--desde 2016] [--minimo 5]

Lê a aba Loans_Master da planilha de operações de crédito (padrão: a de reference-data/) e
devolve, por credor, as medianas de valor, carência e prazo total e as comissões mais
frequentes, só para operações de estados e municípios. A margem sobre a taxa básica não é
registrada de forma confiável na planilha e por isso não entra.
"""
import os, statistics as st, sys
from collections import Counter, defaultdict

import openpyxl

PADRAO = os.path.join(os.path.dirname(__file__), "..", "reference-data",
                      "External_Credit_Operations_Database_September_2026.xlsx")


def num(v):
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return None


def mediana(linhas, ix, campo):
    v = [x for x in (num(r[ix[campo]]) for r in linhas) if x and x > 0]
    return (st.median(v), len(v)) if v else (None, 0)


def mais_frequente(linhas, ix, campo):
    c = Counter(r[ix[campo]] for r in linhas if r[ix[campo]] not in (None, "", "none"))
    return c.most_common(1)[0][0] if c else "—"


def main(args):
    caminho = next((a for a in args if a.endswith(".xlsx")), PADRAO)
    desde = int(args[args.index("--desde") + 1]) if "--desde" in args else 2016
    minimo = int(args[args.index("--minimo") + 1]) if "--minimo" in args else 5
    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    linhas = list(wb["Loans_Master"].iter_rows(values_only=True))
    ix = {k: i for i, k in enumerate(linhas[1])}
    por_credor = defaultdict(list)
    for r in linhas[2:]:
        ano = num(r[ix["Year"]])
        if ano is None or ano < desde or r[ix["Entity_Type"]] not in ("State", "Municipality"):
            continue
        por_credor[r[ix["Bank_Code"]]].append(r)
    print("| Credor | Operações | Valor mediano (US$ milhões) | Carência (meses) | Prazo total (meses) | "
          "Comissão de compromisso mais frequente | Comissão de abertura mais frequente |")
    print("|---|---|---|---|---|---|---|")
    poucos = []
    for credor, L in sorted(por_credor.items(), key=lambda x: -len(x[1])):
        if len(L) < minimo:
            poucos.append(f"{credor} ({len(L)})")
            continue
        cel = []
        for campo in ("Loan_USD", "Grace_Months", "Total_Term_Months"):
            m, n = mediana(L, ix, campo)
            cel.append(f"{m:g} ({n})" if m is not None else "—")
        print(f"| {credor} | {len(L)} | {' | '.join(cel)} | {mais_frequente(L, ix, 'Commitment_Fee')} | "
              f"{mais_frequente(L, ix, 'Opening_Fee')} |")
    if poucos:
        print(f"\nCom menos de {minimo} operações desde {desde}: {', '.join(poucos)}.")


if __name__ == "__main__":
    main(sys.argv[1:])

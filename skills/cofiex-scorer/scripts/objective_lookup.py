"""Dados Objetivos (FASES 6–8): Capacidade de Pagamento, Tendência da Dívida e Índice de Desenvolvimento Humano
de um ente subnacional, a partir das tabelas oficiais empacotadas em reference-data/.

uso: python -X utf8 objective_lookup.py --uf PE --reuniao 2026-12-03 [--municipio "Recife" | --ibge 2611606] [--piso-idh 0.65]

Sem --municipio/--ibge, consulta o governo estadual. A data da reunião-alvo escolhe o ciclo de Capacidade de
Pagamento em vigor e os anos de dívida já fechados. Saída em texto, com a fonte e o ciclo de cada valor.
"""
import argparse, csv, datetime as dt, unicodedata
from pathlib import Path

import openpyxl

RD = Path(__file__).resolve().parent.parent / "reference-data"
PONTOS_CAPAG = {"A+": 2.0, "A": 1.5, "B+": 1.0, "B": 0.5, "C": 0.0}
# Piso de IDH (IDH_menor da reunião) implícito nas notas oficiais da RN 1/2024 (reuniões 180ª–185ª).
# Municípios são comparados só com municípios (IDHM 2010): piso 0,639–0,646. Estados: 0,676–0,689.
PISO = {"municipal": (0.639, 0.643, 0.646), "estadual": (0.676, 0.680, 0.689)}
# Regra da Tendência da Dívida calibrada em 63 notas oficiais (31 estaduais, 32 municipais): erro médio 0,05.
ALTO, SUBIDA, QUEDA, ALTO_SUBINDO = 80.0, 8.0, 10.0, 60.0


def norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()


def num(x):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None


def nota_divida(seq):
    """seq: % dívida/receita corrente líquida em fins de ano consecutivos, o mais recente por último."""
    ult, d1, dtot = seq[-1], seq[-1] - seq[-2], seq[-1] - seq[0]
    if ult >= ALTO:
        return (0.25 if d1 > SUBIDA else 0.5), f"nível alto ({ult:.0f}%)" + (", subindo" if d1 > SUBIDA else "")
    if d1 > SUBIDA:
        return (0.25 if ult >= ALTO_SUBINDO else 0.5), f"subiu {d1:.0f} pontos percentuais no último ano"
    if dtot <= -QUEDA:
        return 1.0, f"caiu {-dtot:.0f} pontos percentuais no período"
    return 0.75, "estável ou em leve variação, dentro dos limites"


def ler(nome):
    with open(RD / nome, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf", required=True); ap.add_argument("--reuniao", required=True)
    ap.add_argument("--municipio"); ap.add_argument("--ibge", type=int); ap.add_argument("--piso-idh", type=float)
    a = ap.parse_args()
    uf, data = a.uf.upper(), dt.date.fromisoformat(a.reuniao)
    municipal = bool(a.municipio or a.ibge)
    L = []

    if municipal:
        rows = [r for r in ler("capag_municipios_por_posicao.csv") if r["uf"] == uf and
                (int(r["ibge"]) == a.ibge if a.ibge else norm(r["municipio"]) == norm(a.municipio))]
        if not rows:
            raise SystemExit("Município não encontrado na tabela da STN; conferir nome/UF ou passar --ibge.")
        m = rows[0]
        nome = f"{m['municipio']} ({uf}), código IBGE {m['ibge']}"
        posicoes = sorted(k[6:] for k in m if k.startswith("capag_"))
        vig = [p for p in posicoes if p <= data.strftime("%Y-%m")] or posicoes[:1]
        pos = vig[-1]
        classe = m[f"capag_{pos}"]
        L.append(f"Ente: {nome}")
        L.append(f"Capacidade de Pagamento: {classe} → {PONTOS_CAPAG.get(classe, 0.0):.3f} pontos "
                 f"(posição STN de {pos}, a última publicada antes da reunião)" +
                 ("; D é eliminatória (Art. 28)" if classe == "D" else "") +
                 ("; 'n.e.' = não classificada, 0 ponto" if classe not in PONTOS_CAPAG and classe != "D" else ""))
        if posicoes[-1] > pos:
            L.append(f"  Posição mais nova já publicada ({posicoes[-1]}): {m[f'capag_{posicoes[-1]}']} — vale se a reunião usar o ciclo novo.")
        ano_base = int(pos[:4]) - (2 if int(pos[5:7]) < 4 else 1)
        seq = [num(m.get(f"dc_rcl_{y}")) for y in range(ano_base - 3, ano_base + 1)]
        rotulo = "Dívida Consolidada/Receita Corrente Líquida (base da Capacidade de Pagamento)"
    else:
        est = [r for r in ler("capag_estados_por_ciclo.csv") if r["uf"] == uf]
        vig = [r for r in est if r["vigente_desde"] <= a.reuniao] or est[:1]
        c = max(vig, key=lambda r: r["vigente_desde"])
        classe = c["classificacao"]
        L.append(f"Ente: Estado {uf}")
        L.append(f"Capacidade de Pagamento: {classe} → {PONTOS_CAPAG.get(classe, 0.0):.3f} pontos "
                 f"({c['ciclo']}, em vigor desde {c['vigente_desde']})" + ("; D é eliminatória (Art. 28)" if classe == "D" else ""))
        d = next(r for r in ler("divida_estados_dcl_rcl.csv") if r["uf"] == uf)
        ano_base = data.year - 1
        seq = [num(d.get(f"dcl_rcl_{y}")) for y in range(ano_base - 3, ano_base + 1)]
        rotulo = "Dívida Consolidada Líquida/Receita Corrente Líquida (Siconfi, RGF Anexo 2)"
        if d.get("dcl_rcl_ultimo_quadrimestre"):
            L.append(f"  Último quadrimestre publicado ({d['ultimo_quadrimestre']}): {num(d['dcl_rcl_ultimo_quadrimestre']):.1f}%")

    seq = [x for x in seq if x is not None]
    if len(seq) >= 2:
        p, por_que = nota_divida(seq)
        L.append(f"Tendência da Dívida: {p:.3f} pontos — {por_que}. {rotulo}, até {ano_base}: "
                 + " → ".join(f"{x:.1f}%" for x in seq))
    else:
        L.append("Tendência da Dívida: série insuficiente na tabela; usar a rubrica (cenário 0,500–1,000) e levantar input_flag.")

    wb = openpyxl.load_workbook(RD / "External_Credit_Operations_Database_September_2026.xlsx", read_only=True, data_only=True)
    if municipal:
        idh = next((r[7] for r in wb["Borrowers_Municipalities"].iter_rows(min_row=3, values_only=True)
                    if r[0] == int(m["ibge"])), None)
        fonte_idh, tipo = "IDHM 2010 (planilha empacotada, Borrowers_Municipalities)", "municipal"
    else:
        idh = next((r[6] for r in wb["Borrowers_States"].iter_rows(min_row=3, values_only=True) if r[2] == uf), None)
        fonte_idh, tipo = "IDH 2021 (planilha empacotada, Borrowers_States)", "estadual"
    if idh is None:
        L.append("Índice de Desenvolvimento Humano: ente fora da planilha; buscar o IDHM 2010 no Atlas do Desenvolvimento Humano.")
    else:
        lo, base, hi = PISO[tipo]
        if a.piso_idh:
            lo = base = hi = a.piso_idh
        f = lambda piso: min(2.0, max(0.0, 2 * (1 - idh) / (1 - piso)))
        L.append(f"Índice de Desenvolvimento Humano: {idh:.3f} ({fonte_idh}) → {f(base):.3f} pontos com piso {base:.3f}; "
                 f"faixa {f(lo):.3f}–{f(hi):.3f} para piso {lo:.3f}–{hi:.3f}. Se o ente tiver o menor IDH da pauta, 2,000.")
        if tipo == "estadual":
            L.append("  Para alguns estados, o IDH usado pela SEAID diverge do IDH 2021 da planilha em até ~0,03; tratar como ±0,1 ponto.")
    print("\n".join(L))


if __name__ == "__main__":
    main()

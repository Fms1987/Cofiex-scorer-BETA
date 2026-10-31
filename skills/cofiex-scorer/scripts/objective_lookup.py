"""Dados Objetivos (FASES 6–8): Capacidade de Pagamento, Tendência da Dívida e Índice de Desenvolvimento Humano
de um ente subnacional, a partir das tabelas oficiais empacotadas em reference-data/.

uso: python -X utf8 objective_lookup.py --uf PE --reuniao 2026-12-03 [--municipio "Recife" | --ibge 2611606] [--piso-idh 0.65]
                             [--entidade banco|empresa]

Sem --municipio/--ibge, consulta o governo estadual. A data da reunião-alvo escolhe o ciclo de Capacidade de
Pagamento em vigor e os anos de dívida já fechados. Saída em texto, com a fonte e o ciclo de cada valor.
"""
import argparse, csv, datetime as dt, unicodedata
from pathlib import Path

import openpyxl

RD = Path(__file__).resolve().parent.parent / "reference-data"
PONTOS_CAPAG = {"A+": 2.0, "A": 1.5, "B+": 1.0, "B": 0.5, "C": 0.0}
# Piso de IDH (IDH_menor da reunião) implícito nas notas oficiais da RN 1/2024 (reuniões 180ª–185ª).
# Municípios são comparados só com municípios (IDHM 2010, Atlas): piso 0,639–0,646, estável e exato por reunião
# (32 notas oficiais, desvio 0,003). Estados usam o IDHM 2024 do Atlas: piso 0,705–0,762, média 0,739 (26 notas, desvio 0,013).
PISO = {"municipal": (0.639, 0.643, 0.646), "estadual": (0.715, 0.739, 0.760)}
# Regra da Tendência da Dívida calibrada em 63 notas oficiais (31 estaduais, 32 municipais): erro médio 0,05.
ALTO, SUBIDA, QUEDA, ALTO_SUBINDO = 80.0, 8.0, 10.0, 60.0


ENTIDADE = {
    "banco": ["Capacidade de Pagamento: instituição financeira, pela categoria Basileia (A+ acima de 15%) → 2,000 pontos com Basileia acima de 15%. "
              "Nas 10 notas oficiais de bancos estaduais da Res. 17/2021 e nos 2 pleitos da RN 1/2024 (pelo total) a nota foi sempre a máxima.",
              "Tendência da Dívida: 1,000 ponto (máxima). Mesmo padrão: sempre no máximo. Nunca usar a classificação nem a dívida do estado."],
    "empresa": ["Capacidade de Pagamento: estatal pela Garantia-Ativo-Fixo e Retorno sobre Investimento próprios → cenário 0,500 (faixa 0,000–1,000); "
                "levantar input_flag pedindo o balanço. Nunca usar a classificação do estado.",
                "Tendência da Dívida: estatal pelo Exigível/Patrimônio Líquido próprio → cenário 0,250 (faixa 0,000–0,500); "
                "levantar input_flag pedindo o balanço. Nunca usar a dívida do estado."],
}


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
    ap.add_argument("--entidade", choices=["banco", "empresa"],
                    help="banco/agência de fomento ou estatal não financeira de um estado/município: não usa a Capacidade de Pagamento "
                         "nem a Dívida do governo; o Índice de Desenvolvimento Humano é o da sede")
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

    if a.entidade:
        L = L[:1]
        L += ENTIDADE[a.entidade]
    if a.entidade and uf == "DF" and not municipal:
        municipal, m = True, {"ibge": "5300108"}  # entes do Distrito Federal: IDHM 2010 de Brasília, piso municipal (IDH da sede)
    if municipal:
        idh = next((float(r["idhm_2010"]) for r in ler("idhm_municipios_2010.csv") if int(r["ibge"]) == int(m["ibge"])), None)
        fonte_idh, tipo = "IDHM 2010, Atlas do Desenvolvimento Humano (idhm_municipios_2010.csv)", "municipal"
    else:
        idh = next((float(r["idhm_2024"]) for r in ler("idh_estados_2024.csv") if r["uf"] == uf), None)
        fonte_idh, tipo = "IDHM 2024, Atlas do Desenvolvimento Humano (idh_estados_2024.csv)", "estadual"
    if idh is None:
        L.append("Índice de Desenvolvimento Humano: ente fora da tabela (município criado depois de 2010 ou sem código); buscar o IDHM no Atlas do Desenvolvimento Humano.")
    else:
        lo, base, hi = PISO[tipo]
        if a.piso_idh:
            lo = base = hi = a.piso_idh
        f = lambda piso: min(2.0, max(0.0, 2 * (1 - idh) / (1 - piso)))
        L.append(f"Índice de Desenvolvimento Humano: {idh:.3f} ({fonte_idh}) → {f(base):.3f} pontos com piso {base:.3f}; "
                 f"faixa {f(lo):.3f}–{f(hi):.3f} para piso {lo:.3f}–{hi:.3f}. Se o ente tiver o menor IDH da pauta, 2,000.")
        if tipo == "estadual":
            L.append("  Estados: o piso varia entre 0,705 e 0,762 conforme a pauta; tratar a nota como ±0,2 ponto.")
    print("\n".join(L))


if __name__ == "__main__":
    main()

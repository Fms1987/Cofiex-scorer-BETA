"""Gera as tabelas de Índice de Desenvolvimento Humano de reference-data/ a partir das planilhas do Atlas do Desenvolvimento Humano no Brasil.

uso: python -I -X utf8 tools/build_idh_tables.py <municipios_2010.xlsx> <estados_2024.xlsx> <skill_dir>

municipios_2010.xlsx: IDHM 2010 de todos os municípios (colunas: Territorialidades, IDHM, Renda, Longevidade, Educação).
estados_2024.xlsx: IDHM 2024 das unidades da federação, no mesmo formato.
O índice municipal só muda com o Censo; o estadual é atualizado com a PNAD. Rodar de novo quando o Atlas publicar dados novos.

Grava reference-data/idhm_municipios_2010.csv (chave: código do IBGE, ligado pela tabela de Capacidade de Pagamento
municipal) e reference-data/idh_estados_2024.csv (chave: sigla da UF).
"""
import csv
import re
import sys
import unicodedata
from pathlib import Path

import openpyxl

# Nomes do Atlas (2010) que diferem dos da tabela de Capacidade de Pagamento (grafia ou nome atual do município).
ALIAS = {
    ("Augusto Severo", "RN"): "Campo Grande", ("Presidente Juscelino", "RN"): "Serra Caiada",
    ("Santarém", "PB"): "Joca Claudino", ("Seridó", "PB"): "São Vicente do Seridó",
    ("Embu", "SP"): "Embu das Artes", ("Fortaleza do Tabocão", "TO"): "Tabocão",
    ("Amparo de São Francisco", "SE"): "Amparo do São Francisco", ("Brasópolis", "MG"): "Brazópolis",
    ("Dona Eusébia", "MG"): "Dona Euzébia", ("Eldorado dos Carajás", "PA"): "Eldorado do Carajás",
    ("Florínia", "SP"): "Florínea", ("Iguaraci", "PE"): "Iguaracy", ("Itapagé", "CE"): "Itapajé",
    ("Muquém de São Francisco", "BA"): "Muquém do São Francisco", ("Poxoréo", "MT"): "Poxoréu",
    ("Santa Isabel do Pará", "PA"): "Santa Izabel do Pará", ("Santa Teresinha", "BA"): "Santa Terezinha",
    ("Santo Antônio do Leverger", "MT"): "Santo Antônio de Leverger",
    ("São Luís do Paraitinga", "SP"): "São Luiz do Paraitinga", ("São Thomé das Letras", "MG"): "São Tomé das Letras",
}


# O Distrito Federal não está na tabela de Capacidade de Pagamento municipal; o Atlas traz a linha de Brasília (DF).
EXTRA = {("Brasília", "DF"): "5300108"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s.replace("'", "").replace("-", " ")).strip()


def linhas(arq):
    ws = openpyxl.load_workbook(arq, read_only=True, data_only=True).worksheets[0]
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] and isinstance(r[1], (int, float)) or (r[0] and any(isinstance(x, (int, float)) for x in r[1:5])):
            yield r


def main(mun, est, skill):
    rd = Path(skill) / "reference-data"
    cap = list(csv.DictReader(open(rd / "capag_municipios_por_posicao.csv", encoding="utf-8")))
    chave = {(norm(r["municipio"]), r["uf"]): r for r in cap}

    # Municípios: colunas do Atlas = IDHM, Renda, Longevidade, Educação (nessa ordem)
    out, sem = [], []
    for r in linhas(mun):
        m = re.match(r"(.*) \((\w\w)\)$", r[0].strip())
        if not m:
            continue
        nome, uf = m.group(1), m.group(2)
        alvo = chave.get((norm(ALIAS.get((nome, uf), nome)), uf))
        if alvo is None and (nome, uf) in EXTRA:
            alvo = {"ibge": EXTRA[(nome, uf)], "municipio": nome}
        if alvo is None:
            sem.append(r[0])
            continue
        out.append((alvo["ibge"], alvo["municipio"], uf, r[1], r[2], r[3], r[4]))
    out.sort()
    with open(rd / "idhm_municipios_2010.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ibge", "municipio", "uf", "idhm_2010", "idhm_renda_2010", "idhm_longevidade_2010", "idhm_educacao_2010"])
        w.writerows(out)
    print(f"municípios: {len(out)} gravados; sem correspondência na tabela de Capacidade de Pagamento: {sem}")

    # Estados: colunas do Atlas = Educação, Longevidade, Renda, IDHM (nessa ordem)
    wb = openpyxl.load_workbook(rd / "External_Credit_Operations_Database_September_2026.xlsx", read_only=True, data_only=True)
    uf_de = {norm(r[1]): r[2] for r in wb["Borrowers_States"].iter_rows(min_row=3, values_only=True) if r[2]}
    uf_de["distrito federal"] = "DF"
    est_out = []
    for r in linhas(est):
        if norm(r[0]) == "brasil":
            continue
        est_out.append((uf_de[norm(r[0])], r[0], r[4], r[3], r[2], r[1]))
    est_out.sort()
    with open(rd / "idh_estados_2024.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["uf", "estado", "idhm_2024", "idhm_renda_2024", "idhm_longevidade_2024", "idhm_educacao_2024"])
        w.writerows(est_out)
    print(f"estados: {len(est_out)} gravados")


if __name__ == "__main__":
    main(*sys.argv[1:4])

"""Rebuild the packaged official tables for the objective components (proposal items C2, C3).

usage: build_objective_data.py <repo_root> <download_dir> [--no-download]

Downloads (into <download_dir>, a fresh folder outside the repository) and converts:
  - STN "Capacidade de Pagamento dos Estados e do DF": every cycle file from 2023 on (CKAN capag-estados)
  - STN "Capacidade de Pagamento de Municípios": every published position from 2025 on (CKAN capag-municipios),
    including Dívida Consolidada / Receita Corrente Líquida of each CAPAG base year
  - Siconfi RGF Anexo 02 of the 27 state executives: % DCL/RCL at each year end since 2020 and the latest
    quadrimestre of the current year
Writes to skills/cofiex-scorer/reference-data/:
  capag_estados_por_ciclo.csv, capag_municipios_por_posicao.csv, divida_estados_dcl_rcl.csv
These are general public tables (one row per entity), not case data.
"""
import csv, datetime as dt, json, re, sys, time, urllib.request
from pathlib import Path

import openpyxl

CKAN = "https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show?id="
SICONFI = ("https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rgf?an_exercicio={a}&in_periodicidade=Q&nr_periodo={p}"
           "&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2002&co_esfera=E&co_poder=E&id_ente={e}")
UF = {11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO", 21: "MA", 22: "PI", 23: "CE", 24: "RN",
      25: "PB", 26: "PE", 27: "AL", 28: "SE", 29: "BA", 31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR", 42: "SC",
      43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF"}


def get_json(url):
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(url, timeout=60))
        except Exception:
            time.sleep(3)
    raise RuntimeError(f"falha ao baixar {url}")


def resources(pkg, since):
    out = []
    for r in get_json(CKAN + pkg)["result"]["resources"]:
        m = re.search(r"(20\d\d)", r["name"])
        if m and int(m.group(1)) >= since and r["url"].endswith((".csv", ".xlsx")):
            # date the file came into force: the date printed in the file name when there is one (some cycles were
            # re-uploaded later, which moves last_modified), else the upload date
            d = re.search(r"(20\d\d-\d\d-\d\d)", r["url"].rsplit("/", 1)[-1])
            out.append((r["name"].strip(), d.group(1) if d else (r.get("last_modified") or r["created"])[:10], r["url"]))
    return out


def download(url, dest):
    if not dest.exists():
        urllib.request.urlretrieve(url, dest)
    return dest


def capag_estados(dl, out):
    rows = []
    for name, pub, url in resources("capag-estados", 2023):
        f = download(url, dl / ("est_" + re.sub(r"\W+", "_", name) + ".csv"))
        with open(f, encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh, delimiter=";"):
                rows.append({"uf": r["UF"].strip(), "ciclo": name, "vigente_desde": pub,
                             "classificacao": r["Classificação da CAPAG"].strip(),
                             "indicador_1": r["Indicador 1"], "nota_1": r["Nota 1"], "indicador_2": r["Indicador 2"],
                             "nota_2": r["Nota 2"], "indicador_3": r["Indicador 3"], "nota_3": r["Nota 3"],
                             "qualidade_informacao": r.get("Qualidade da informação contábil e fiscal", "")})
    with open(out / "capag_estados_por_ciclo.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print("estados:", len(rows), "linhas")


def capag_municipios(dl, out):
    mun, posicoes, anos = {}, [], set()
    for name, pub, url in sorted(resources("capag-municipios", 2025), key=lambda x: x[1]):
        f = download(url, dl / ("mun_" + pub + ".xlsx"))
        pos = pub[:7]
        posicoes.append(pos)
        wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
        for r in wb["Prévia da CAPAG"].iter_rows(min_row=4, values_only=True):
            if isinstance(r[0], int):
                d = mun.setdefault(r[0], {"ibge": r[0], "municipio": r[1], "uf": r[2]})
                d[f"capag_{pos}"] = r[3]
        for sh in wb.sheetnames:
            if sh.startswith("CAPAG Ano Base"):
                ano = sh[-4:]
                anos.add(ano)
                for r in wb[sh].iter_rows(min_row=4, max_col=5, values_only=True):
                    if isinstance(r[0], int) and isinstance(r[3], (int, float)) and isinstance(r[4], (int, float)) and r[4] > 0:
                        mun.setdefault(r[0], {"ibge": r[0], "municipio": r[1], "uf": r[2]})[f"dc_rcl_{ano}"] = round(100 * r[3] / r[4], 1)
    cols = ["ibge", "municipio", "uf"] + [f"capag_{p}" for p in posicoes] + [f"dc_rcl_{a}" for a in sorted(anos)]
    with open(out / "capag_municipios_por_posicao.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for d in sorted(mun.values(), key=lambda d: d["ibge"]):
            w.writerow({c: d.get(c, "") for c in cols})
    print("municípios:", len(mun), "| posições:", posicoes)


def divida_estados(out):
    hoje = dt.date.today()
    rows = []
    for cod, uf in UF.items():
        r = {"uf": uf}
        for ano in range(2021, hoje.year):
            for x in get_json(SICONFI.format(a=ano, p=3, e=cod))["items"]:
                if x["cod_conta"] == "PercentualDaDCLSobreARCL":
                    if x["coluna"].startswith("SALDO"):
                        r[f"dcl_rcl_{ano - 1}"] = x["valor"]
                    elif "3º" in x["coluna"]:
                        r[f"dcl_rcl_{ano}"] = x["valor"]
        for p in (3, 2, 1):
            it = [x for x in get_json(SICONFI.format(a=hoje.year, p=p, e=cod))["items"] if x["cod_conta"] == "PercentualDaDCLSobreARCL"]
            if it:
                r["dcl_rcl_ultimo_quadrimestre"] = [x for x in it if not x["coluna"].startswith("SALDO")][-1]["valor"]
                r["ultimo_quadrimestre"] = f"{hoje.year}-Q{p}"
                break
        rows.append(r)
    cols = ["uf"] + [f"dcl_rcl_{a}" for a in range(2020, hoje.year)] + ["dcl_rcl_ultimo_quadrimestre", "ultimo_quadrimestre"]
    with open(out / "divida_estados_dcl_rcl.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        w.writerows({c: r.get(c, "") for c in cols} for r in rows)
    print("dívida estados:", len(rows), "UFs")


def main():
    root, dl = Path(sys.argv[1]), Path(sys.argv[2])
    dl.mkdir(parents=True, exist_ok=True)
    out = root / "skills/cofiex-scorer/reference-data"
    capag_estados(dl, out)
    capag_municipios(dl, out)
    divida_estados(out)
    (out / "objective_tables_built_on.txt").write_text(dt.date.today().isoformat() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

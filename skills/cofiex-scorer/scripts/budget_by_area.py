"""Orçamento por área do PPA (FASE 5, passo 0): fatia de cada área e teto de nível que o orçamento permite.

uso: python -X utf8 budget_by_area.py <produtos.json> [saida.md] [--xlsx planilha.xlsx]
     python -X utf8 budget_by_area.py --modelo planilha.xlsx      (planilha em branco para o cliente)

--xlsx grava a planilha de custo por área e produto que acompanha o relatório: uma linha por
produto e área, com fração, valor atribuído e % do total em fórmulas, e um resumo por área com o
teto de nível. O cliente pode corrigir valores e áreas direto nela.

produtos.json:
{
  "moeda": "US$",
  "total": 100000000,                      # opcional; padrão = soma dos produtos
  "areas_declaradas": ["101", "212"],      # áreas pleiteadas na carta
  "produtos": [
    {"nome": "Obras de abastecimento", "valor": 60000000, "areas": ["212"]},
    {"nome": "Sistema de gestão", "valor": 10000000, "areas": ["212", "302"]},
    {"nome": "Bolsas", "valor": 30000000, "areas": ["101"], "alocacao": {"101": 1.0}}
  ]
}
Regras (lente A.6): produto com uma só área vai inteiro para ela. Produto com várias áreas e sem
"alocacao" explícita na carta é repartido em partes iguais, como faz a Nota Técnica. O orçamento é
condição necessária, não suficiente: o script devolve o TETO de nível, e o nível final vem da lente A.6
(objetivo direto, indicador de resultado com ano-meta, impacto, inovação).
"""
import json, sys
from collections import defaultdict

# Fatia mínima do orçamento para cada nível ser possível. A >50% e B >30% vêm do Anexo II
# (lista de verificação da rubrica); C ≥15% e D ≥4% vêm do decil inferior dos percentuais citados
# nas Notas Técnicas da RN 1/2024 para cada nível (C ~18%, D ~7%; a lente A.6 registra D com 4–7%).
TETOS = [(50.0, "A"), (30.0, "B"), (15.0, "C"), (4.0, "D"), (0.0, "E")]


def teto(pct):
    return next(n for lim, n in TETOS if pct > lim) if pct > 0 else "0"


def calcular(d):
    por_area = defaultdict(float)
    produtos_por_area = defaultdict(list)
    alertas = []
    for p in d["produtos"]:
        areas, v = [str(a) for a in p.get("areas", [])], float(p["valor"])
        if not areas:
            alertas.append(f"Produto sem área do PPA: \"{p['nome']}\" ({v:,.0f}) não conta para nenhuma área.")
            continue
        aloc = p.get("alocacao")
        if aloc:
            s = sum(aloc.values())
            if abs(s - 1) > 0.01:
                alertas.append(f"Alocação de \"{p['nome']}\" soma {s:.2f}, não 1; normalizada.")
            parts = {str(a): f / s for a, f in aloc.items()}
        else:
            parts = {a: 1 / len(areas) for a in areas}
            if len(areas) > 1:
                alertas.append(f"Repartição linear: \"{p['nome']}\" dividido por {len(areas)} áreas ({', '.join(areas)}), "
                               "como a Nota Técnica faz quando a carta não atribui o custo.")
        for a, f in parts.items():
            por_area[a] += v * f
            produtos_por_area[a].append(p["nome"])
    total = float(d.get("total") or sum(float(p["valor"]) for p in d["produtos"]))
    declaradas = [str(a) for a in d.get("areas_declaradas", [])] or sorted(por_area)
    linhas = []
    for a in sorted(set(declaradas) | set(por_area), key=lambda a: -por_area.get(a, 0)):
        pct = 100 * por_area.get(a, 0) / total if total else 0
        linhas.append({"area": a, "valor": por_area.get(a, 0), "pct": pct, "teto": teto(pct),
                       "declarada": a in declaradas, "produtos": produtos_por_area.get(a, [])})
        if a in declaradas and not produtos_por_area.get(a):
            alertas.append(f"Área {a} declarada sem produto e custo próprios: tende a zero (sem nota).")
        if a not in declaradas:
            alertas.append(f"Área {a} recebe recursos mas não foi declarada na carta.")
    return {"moeda": d.get("moeda", ""), "total": total, "areas": linhas, "alertas": alertas}


def markdown(r):
    m = r["moeda"]
    L = ["| Área do PPA | Declarada | Valor | % do total | Teto de nível pelo orçamento | Produtos |",
         "|---|---|---|---|---|---|"]
    for x in r["areas"]:
        L.append(f"| {x['area']} | {'sim' if x['declarada'] else 'não'} | {m} {x['valor']:,.0f} | {x['pct']:.1f}% | "
                 f"{x['teto']} | {'; '.join(x['produtos']) or '—'} |")
    L.append(f"\nTotal considerado: {m} {r['total']:,.0f}. O teto é o nível mais alto que a fatia do orçamento permite; "
             "o nível final depende da lente A.6.")
    if r["alertas"]:
        L += ["", "**Alertas:**"] + [f"- {a}" for a in r["alertas"]]
    return "\n".join(L) + "\n"


def planilha(d, caminho, linhas_vazias=0):
    """Planilha de custo por área e produto. Fórmulas, para que o cliente possa editar."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Custo por produto"
    cab = ["Produto", "Componente", "Valor do produto", "Área do PPA", "Fração do produto nesta área",
           "Valor atribuído à área", "% do total da operação"]
    ws.append(cab)
    linhas = []
    for p in d.get("produtos", []):
        areas = [str(a) for a in p.get("areas", [])] or [""]
        aloc = p.get("alocacao") or {a: 1 / len(areas) for a in areas}
        s = sum(aloc.values()) or 1
        for a in areas:
            linhas.append([p["nome"], p.get("componente", ""), float(p["valor"]), a, aloc.get(a, 0) / s])
    linhas += [["", "", None, "", None] for _ in range(linhas_vazias)]
    fim = len(linhas) + 1
    for i, (nome, comp, valor, area, frac) in enumerate(linhas, start=2):
        ws.append([nome, comp, valor, area, frac, f'=IF(C{i}="","",C{i}*E{i})',
                   f'=IF(C{i}="","",F{i}/$I$2)'])
        ws[f"E{i}"].number_format = "0%"
        ws[f"G{i}"].number_format = "0.0%"
        ws[f"C{i}"].number_format = ws[f"F{i}"].number_format = "#,##0"
    # Total depois das linhas: gravar I1/I2 antes deslocaria o append para a linha 3.
    ws["I1"] = "Total da operação"
    ws["I2"] = float(d["total"]) if d.get("total") else f"=SUM(F2:F{max(fim, 2)})"
    ws["I2"].number_format = "#,##0"

    res = wb.create_sheet("Resumo por área")
    res.append(["Área do PPA", "Declarada na carta", "Valor atribuído", "% do total",
                "Teto de nível pelo orçamento"])
    declaradas = [str(a) for a in d.get("areas_declaradas", [])]
    areas = sorted(set(declaradas) | {l[3] for l in linhas if l[3]})
    for j, a in enumerate(areas + [""] * max(5, linhas_vazias // 4), start=2):
        res.append([a, ("sim" if a in declaradas else "não") if a else "",
                    f"=IF(A{j}=\"\",\"\",SUMIF('Custo por produto'!D:D,A{j},'Custo por produto'!F:F))",
                    f"=IF(A{j}=\"\",\"\",C{j}/'Custo por produto'!$I$2)",
                    f'=IF(A{j}="","",IF(D{j}>0.5,"A",IF(D{j}>0.3,"B",IF(D{j}>0.15,"C",'
                    f'IF(D{j}>0.04,"D",IF(D{j}>0,"E","0"))))))'])
        res[f"C{j}"].number_format = "#,##0"
        res[f"D{j}"].number_format = "0.0%"
    res.append([])
    res.append(["O teto é o nível mais alto que a fatia do orçamento permite. O nível final depende de objetivo "
                "direto, indicador de resultado com ano-meta e impacto. Produto em várias áreas sem fração "
                "declarada na carta é repartido em partes iguais, como faz a Nota Técnica."])
    for w in (wb.worksheets):
        for c in w[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="1F3864")
        for col, larg in zip("ABCDEFGHI", (40, 22, 16, 12, 14, 16, 14, 4, 18)):
            w.column_dimensions[col].width = larg
    wb.save(caminho)
    print(f"Planilha salva em {caminho}")


def main():
    a = sys.argv[1:]
    if a and a[0] == "--modelo":
        planilha({"produtos": []}, a[1], linhas_vazias=40)
        return
    xlsx = a.pop(a.index("--xlsx") + 1) if "--xlsx" in a else None
    if xlsx:
        a.remove("--xlsx")
    with open(a[0], encoding="utf-8") as fh:
        d = json.load(fh)
    r = calcular(d)
    out = markdown(r)
    if len(a) > 1:
        with open(a[1], "w", encoding="utf-8") as fh:
            fh.write(out)
    print(out)
    if xlsx:
        planilha(d, xlsx)


if __name__ == "__main__":
    main()

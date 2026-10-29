"""Gera o relatório final da simulação COFIEX em .docx a partir de um JSON.

Uso: python build_report_docx.py relatorio.json saida.docx

O JSON segue o esquema descrito em references/output/docx-report.md. Os subtotais e a Nota
Geral são recalculados aqui a partir dos itens (com o teto da Nota de Área Estratégica), para
que as tabelas do sumário executivo nunca fiquem inconsistentes com os itens.
"""
import json
import sys
from datetime import date

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HEADER_FILL = "1F3864"
SUBTOTAL_FILL = "D9E2F3"
TOTAL_FILL = "B4C6E7"
NIVEL_PONTOS = {"A": 5.0, "B": 3.0, "C": 2.0, "D": 1.0, "E": 0.5, "0": 0.0, "-": 0.0}


def fmt(v, casas=2):
    if v is None or v == "":
        return "—"
    if isinstance(v, str):
        return v
    return f"{v:.{casas}f}".replace(".", ",")


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def table(doc, header, rows, widths=None, styles=None, num_cols=()):
    """styles: lista paralela a rows com None | 'subtotal' | 'total'."""
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]
        c.text = ""
        run = c.paragraphs[0].add_run(h)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shade(c, HEADER_FILL)
    for r_i, row in enumerate(rows):
        cells = t.add_row().cells
        st = styles[r_i] if styles else None
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            run = p.add_run(str(val))
            if i in num_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if st:
                run.bold = True
                shade(cells[i], TOTAL_FILL if st == "total" else SUBTOTAL_FILL)
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return t


def soma(itens, chave):
    return sum((it.get(chave) or 0) for it in itens)


def tabela_pontuacao(doc, d):
    """Tabela 1: mínimo/esperado/máximo por item, subtotais e Nota Geral."""
    federal = d.get("ente_federal", False)
    teto_ae = d.get("teto_area_estrategica", 10.0)
    rows, styles = [], []
    sub_do = {"min": 0, "esp": 0, "max": 0}
    if not federal:
        for it in d["dados_objetivos"]:
            rows.append(["Dados Objetivos", it["item"], fmt(it["min"]), fmt(it["esp"]), fmt(it["max"])])
            styles.append(None)
        sub_do = {k: soma(d["dados_objetivos"], k) for k in ("min", "esp", "max")}
        rows.append(["Subtotal", "Dados Objetivos (teto 5,00)", fmt(sub_do["min"]), fmt(sub_do["esp"]), fmt(sub_do["max"])])
        styles.append("subtotal")

    ae = d["area_estrategica"]
    areas = ae["areas"]
    for a in areas:
        rows.append(["Área Estratégica", f"{a['codigo']} — {a['objetivo']}",
                     fmt(NIVEL_PONTOS.get(a["nivel_min"], 0)), fmt(NIVEL_PONTOS.get(a["nivel_esp"], 0)),
                     fmt(NIVEL_PONTOS.get(a["nivel_max"], 0))])
        styles.append(None)
    for b in ae.get("bonus", []):
        rows.append(["Área Estratégica", f"Bônus — {b['item']}", fmt(b["min"]), fmt(b["esp"]), fmt(b["max"])])
        styles.append(None)
    sub_ae = {}
    for k, nk in (("min", "nivel_min"), ("esp", "nivel_esp"), ("max", "nivel_max")):
        bruto = sum(NIVEL_PONTOS.get(a[nk], 0) for a in areas) + soma(ae.get("bonus", []), k)
        sub_ae[k] = min(teto_ae, bruto)
    rows.append(["Subtotal", f"Nota de Área Estratégica (teto {fmt(teto_ae)}, bônus incluído)",
                 fmt(sub_ae["min"]), fmt(sub_ae["esp"]), fmt(sub_ae["max"])])
    styles.append("subtotal")

    total = {k: sub_do[k] + sub_ae[k] for k in ("min", "esp", "max")}
    rotulo = "Nota Geral (= Nota de Área Estratégica, ente federal)" if federal else \
        "Nota Geral (Dados Objetivos + Nota de Área Estratégica, teto 15,00)"
    rows.append(["Total", rotulo, fmt(total["min"]), fmt(total["esp"]), fmt(total["max"])])
    styles.append("total")
    table(doc, ["Bloco", "Item", "Mínimo", "Esperado", "Máximo"], rows,
          widths=[3.0, 8.0, 2.0, 2.0, 2.0], styles=styles, num_cols=(2, 3, 4))
    return total


def tabela_areas(doc, d):
    """Tabela 2: objetivos estratégicos do PPA indicados no pleito e pontuação possível."""
    rows = []
    for a in d["area_estrategica"]["areas"]:
        faixa = f"{a['nivel_min']} / {a['nivel_esp']} / {a['nivel_max']}"
        pts = f"{fmt(NIVEL_PONTOS.get(a['nivel_min'], 0))} / {fmt(NIVEL_PONTOS.get(a['nivel_esp'], 0))} / " \
              f"{fmt(NIVEL_PONTOS.get(a['nivel_max'], 0))}"
        rows.append([a["codigo"], a["objetivo"], a.get("pleiteado_como", "Declarada"), faixa, pts,
                     a.get("justificativa_curta", "")])
    table(doc, ["Código PPA", "Objetivo estratégico", "Situação", "Nível (mín./esp./máx.)",
                "Pontos (mín./esp./máx.)", "Fundamento resumido"], rows,
          widths=[1.6, 4.4, 2.0, 2.2, 2.6, 4.6], num_cols=(0, 3, 4))


def tabela_sugestoes(doc, d):
    """Tabela 3: sugestões de melhoria, resumidas (o detalhe vai no Plano de Correção)."""
    rows = [[str(i + 1), s["sugestao"], s.get("item_afetado", ""), s.get("prioridade", ""),
             s.get("ganho_estimado", "")] for i, s in enumerate(d.get("sugestoes", []))]
    table(doc, ["#", "Sugestão", "Item afetado", "Prioridade", "Ganho estimado"], rows,
          widths=[0.8, 8.2, 3.2, 2.0, 2.6], num_cols=(0, 3, 4))


def bloco(doc, b):
    tipo = b.get("tipo", "p")
    if tipo == "p":
        doc.add_paragraph(b["texto"])
    elif tipo == "bullets":
        for item in b["itens"]:
            doc.add_paragraph(item, style="List Bullet")
    elif tipo == "numerada":
        for item in b["itens"]:
            doc.add_paragraph(item, style="List Number")
    elif tipo == "tabela":
        if b.get("titulo"):
            doc.add_paragraph().add_run(b["titulo"]).bold = True
        table(doc, b["cabecalho"], b["linhas"])
    elif tipo == "nota":
        p = doc.add_paragraph()
        run = p.add_run(b["texto"])
        run.italic = True
        run.font.size = Pt(9)


def main(src, out):
    d = json.loads(open(src, encoding="utf-8").read())
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.0)
        s.top_margin = s.bottom_margin = Cm(2.0)

    cab = d["cabecalho"]
    doc.add_heading("Simulação da Avaliação Técnica COFIEX", level=0)
    doc.add_paragraph(f"{cab['proposta']} — {cab['proponente']}").runs[0].bold = True
    doc.add_paragraph(f"Data da simulação: {d.get('data', date.today().strftime('%d/%m/%Y'))}. "
                      "Simulação sob julgamento cego, sem consulta à Nota Técnica do pleito. "
                      "Resultado estimativo; não substitui a avaliação oficial.").runs[0].italic = True

    doc.add_heading("Sumário executivo", level=1)
    table(doc, ["Campo", "Valor"], [["Proposta", cab["proposta"]], ["Proponente", cab["proponente"]]] +
          [list(c) for c in cab.get("campos", [])], widths=[5.0, 12.0])
    if d.get("sintese"):
        doc.add_paragraph(d["sintese"])

    doc.add_heading("Tabela 1 — Pontuação por item: mínima, esperada e máxima", level=2)
    total = tabela_pontuacao(doc, d)
    doc.add_paragraph(f"Nota Geral estimada: [Mínimo {fmt(total['min'])} — Esperado {fmt(total['esp'])} "
                      f"— Máximo {fmt(total['max'])}].").runs[0].bold = True
    if d.get("base_calibracao"):
        bloco(doc, {"tipo": "nota", "texto": "Base de calibração: " + d["base_calibracao"]})

    doc.add_heading("Tabela 2 — Objetivos estratégicos do PPA indicados no pleito e pontuação possível", level=2)
    tabela_areas(doc, d)

    doc.add_heading("Tabela 3 — Sugestões a considerar (resumo)", level=2)
    tabela_sugestoes(doc, d)
    bloco(doc, {"tipo": "nota", "texto": "Sugestões indicativas. O detalhamento, a priorização e o ganho "
                                         "estimado de cada uma estão na seção Plano de Correção."})

    for sec in d.get("secoes", []):
        doc.add_heading(sec["titulo"], level=1)
        for b in sec.get("blocos", []):
            bloco(doc, b)

    doc.save(out)
    print(f"Relatório salvo em {out} — Nota Geral esperada {fmt(total['esp'])}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

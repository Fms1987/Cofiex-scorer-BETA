"""Painel de carteira: os pleitos que o líder de equipe acompanha, atualizado a cada simulação.

uso:
  python -X utf8 portfolio.py registrar --proposta "Nome" --proponente "Ente" --nota-geral 9.8
         --nota-ae 6.5 --sublimite "Subnacional – Geral" --valor-usd 120 [--fase "Em análise no Portal"]
         [--arquivo carteira_cofiex.json]
  python -X utf8 portfolio.py mostrar [--arquivo carteira_cofiex.json] [--html painel.html]

A carteira fica num arquivo JSON na pasta de trabalho do usuário, nunca no repositório da skill:
ela tem nomes de entes e projetos. "registrar" substitui a linha da mesma proposta. "mostrar"
cruza cada pleito com reference-data/sublimit_status.json (limite da próxima reunião e linha de
corte recente) e diz se cabe no saldo e a posição frente à linha, sem percentual.
"""
import html
import json
import os
import sys
from datetime import date

STATUS = os.path.join(os.path.dirname(__file__), "..", "reference-data", "sublimit_status.json")
MARGEM = 1.0  # erro mediano da Nota Geral no banco de teste (FASE 9)


def arg(a, nome, padrao=None):
    return a[a.index(nome) + 1] if nome in a else padrao


def carregar(caminho):
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as fh:
            return json.load(fh)
    return []


def leitura(p, st):
    """Saldo e posição frente à linha de corte, em texto."""
    prox = st["proxima_reuniao"]
    lim = prox["limites"].get(p["sublimite"])
    if lim is None:
        saldo = "limite não divulgado"
    elif lim <= 0:
        saldo = "limite zero"
    else:
        saldo = f"US$ {lim / 1e6:,.0f} mi".replace(",", ".") + (" — não cabe" if p["valor_usd"] * 1e6 > lim else " — cabe")
    c = st["linha_de_corte_recente"].get(p["sublimite"])
    if not c:
        return saldo, "sem linha de corte publicada", "—"
    linha = max(v for v in (c["menor_nota_aprovada"], c["maior_nota_nao_aprovada"]) if v is not None)
    d = p["nota_geral"] - linha
    pos = "acima" if d >= MARGEM else ("abaixo" if d <= -MARGEM else "perto")
    return saldo, pos, f"{linha:.2f} ({c['reuniao']}ª)".replace(".", ",", 1)


def mostrar(carteira, st, html_out=None):
    cab = ["Proposta", "Proponente", "Nota Geral esperada", "Nota de Área Estratégica esperada",
           "Sublimite recomendado", "Valor (US$ mi)", "Fase no Portal",
           f"Limite na {st['proxima_reuniao']['numero']}ª", "Linha de corte recente", "Posição", "Simulado em"]
    linhas = []
    for p in sorted(carteira, key=lambda x: -x["nota_geral"]):
        saldo, pos, linha = leitura(p, st)
        linhas.append([p["proposta"], p["proponente"], f"{p['nota_geral']:.2f}".replace(".", ","),
                       f"{p['nota_ae']:.2f}".replace(".", ","), p["sublimite"], f"{p['valor_usd']:g}",
                       p.get("fase", "—"), saldo, linha, pos, p["data"]])
    nota = (f"Próxima reunião: {st['proxima_reuniao']['numero']}ª, {st['proxima_reuniao']['data']}. "
            f"Base de sublimites até a {st['ultima_reuniao']}ª. Posição: acima ou abaixo quando a Nota Geral "
            f"esperada está a 1 ponto ou mais da linha; perto, no meio. Sem percentual de aprovação.")
    md = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)] + ["| " + " | ".join(l) + " |" for l in linhas]
    print("\n".join(md) + "\n\n" + nota)
    if html_out:
        th = "".join(f"<th>{html.escape(c)}</th>" for c in cab)
        trs = "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in l) + "</tr>" for l in linhas)
        pagina = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Carteira COFIEX</title>
<style>:root{{--bg:#fff;--fg:#1a1a1a;--line:#d0d7e2;--head:#1f3864;--headfg:#fff}}
@media (prefers-color-scheme: dark){{:root{{--bg:#14161a;--fg:#e6e6e6;--line:#3a4250;--head:#2c4a7a}}}}
body{{background:var(--bg);color:var(--fg);font:14px system-ui,sans-serif;margin:16px}}
.wrap{{overflow-x:auto}}table{{border-collapse:collapse;min-width:900px}}
th,td{{border:1px solid var(--line);padding:6px 8px;text-align:left}}th{{background:var(--head);color:var(--headfg)}}
p{{max-width:70ch}}</style></head><body><h1>Carteira COFIEX</h1>
<div class="wrap"><table><tr>{th}</tr>{trs}</table></div><p>{html.escape(nota)}</p></body></html>"""
        with open(html_out, "w", encoding="utf-8") as fh:
            fh.write(pagina)
        print(f"\nPainel salvo em {html_out}")


def main(a):
    caminho = arg(a, "--arquivo", "carteira_cofiex.json")
    with open(STATUS, encoding="utf-8") as fh:
        st = json.load(fh)
    carteira = carregar(caminho)
    if a and a[0] == "registrar":
        p = {"proposta": arg(a, "--proposta"), "proponente": arg(a, "--proponente"),
             "nota_geral": float(arg(a, "--nota-geral")), "nota_ae": float(arg(a, "--nota-ae")),
             "sublimite": arg(a, "--sublimite"), "valor_usd": float(arg(a, "--valor-usd")),
             "fase": arg(a, "--fase", "—"), "data": date.today().strftime("%d/%m/%Y")}
        if p["sublimite"] not in st["proxima_reuniao"]["limites"] and p["sublimite"] not in st["linha_de_corte_recente"]:
            print(f"AVISO: sublimite \"{p['sublimite']}\" não reconhecido; use o nome da tabela de sublimites.",
                  file=sys.stderr)
        carteira = [x for x in carteira if x["proposta"] != p["proposta"]] + [p]
        with open(caminho, "w", encoding="utf-8") as fh:
            json.dump(carteira, fh, ensure_ascii=False, indent=1)
        print(f"Registrado em {caminho} ({len(carteira)} pleitos).")
    else:
        mostrar(carteira, st, arg(a, "--html"))


if __name__ == "__main__":
    main(sys.argv[1:])

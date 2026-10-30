"""Orçamento por área do PPA (FASE 5, passo 0): fatia de cada área e teto de nível que o orçamento permite.

uso: python -X utf8 budget_by_area.py <produtos.json> [saida.md]

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


def main():
    with open(sys.argv[1], encoding="utf-8") as fh:
        r = calcular(json.load(fh))
    out = markdown(r)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as fh:
            fh.write(out)
    print(out)


if __name__ == "__main__":
    main()

# FASE 8 — Trajetória da dívida

## FASE 8 — Trajetória da Dívida (Art. 21, Anexo III — máx. 1,000)
Art. 10, I, d: máximo 1 ponto. **Mede o nível/trajetória de dívida ACUMULADA da entidade**
(Dívida Consolidada/Receita Corrente Líquida, tendência, limites do Senado), analisada pela
Secretaria do Tesouro Nacional — NÃO os termos financeiros da operação proposta. **A operação
proposta não compra pontos aqui:** nem a promessa de melhoria futura nem a institucionalização
de regimes fiscais (Emenda Constitucional, Lei Complementar) muda a nota — a Secretaria do
Tesouro Nacional avalia o estoque no momento da análise.

| Tendência | Pontuação |
|---|---|
| Decrescente ou estável dentro dos limites do Senado | 1,000 |
| Crescente, mas dentro dos limites | 0,750 |
| Aproximando-se do limite prudencial | 0,500 |
| Excedendo o limite prudencial | 0,250 |
| Excedendo significativamente | 0,000 |

### Regra calibrada (usar primeiro): `scripts/objective_lookup.py`
O script lê a série oficial empacotada e aplica a regra abaixo. Ela foi calibrada em 63 notas
oficiais da RN 1/2024 (31 estaduais, 32 municipais). Acertou o valor exato em ~85% dos casos,
com erro médio de 0,05 (contra 0,12 de "sempre 0,750").
- **Série usada:**
  - Estados: Dívida Consolidada Líquida/Receita Corrente Líquida (Siconfi, RGF Anexo 2) nos
    fins de ano até o ano anterior à reunião.
  - Municípios: Dívida Consolidada/Receita Corrente Líquida dos anos-base da Capacidade de
    Pagamento em vigor.
- **Regra**, aplicada nesta ordem:
  1. Nível ≥ 80%: 0,500; 0,250 se subiu mais de 8 pontos percentuais no último ano.
  2. Subiu mais de 8 pontos percentuais no último ano: 0,500; 0,250 se o nível for ≥ 60%.
  3. Caiu 10 pontos percentuais ou mais no período: 1,000.
  4. Caso contrário (estável ou pequena variação): 0,750.
- A nota 0,000 apareceu uma vez, numa estatal pontuada pelo ente mantenedor. A regra não a prevê.
- Ressalva: a regra foi ajustada nas mesmas reuniões em que foi medida. Rever com o banco de
  teste fixo a cada ciclo novo.

A tabela abaixo é o fallback quando o ente não está nas tabelas empacotadas.

**Dívida Consolidada/Receita Corrente Líquida → referência de pontuação (calibrada
empiricamente):**
| Dívida Consolidada/Receita Corrente Líquida | Tendência | Pontuação esperada |
|---|---|---|
| < 40% | qualquer | 0,875–1,000 |
| 40–55% | estável/decrescente | 0,750 |
| 40–55% | crescente | 0,500–0,750 |
| 55–65% | fortemente crescente | 0,250–0,500 |
| > 65% ou violação do limite do Senado | qualquer | 0,000–0,250 |

**Piso condicional (âncora empírica):** primeira operação com banco multilateral de desenvolvimento
E Capacidade de Pagamento C → esperado **0,50** (era 0,75). A SEAID tende a aplicar um piso
conservador quando não há histórico com banco multilateral e a Capacidade de Pagamento é mais
fraca.

**Refinanciamento versus dívida nova líquida (distinção crítica):**
1. **Refinanciamento sem aumento de estoque** (novo credor, mesmo passivo): a Dívida
   Consolidada/Receita Corrente Líquida não sobe → a nota reflete o nível histórico
   preexistente (âncora: primeira operação com banco multilateral, Dívida Consolidada/Receita
   Corrente Líquida baixa → 0,750).
2. **Reestruturação de Dívida Pública Interna/Externa (ex.: Certificado de Depósito
   Interbancário → externa)**: não reduz o estoque, apenas muda sua composição. A Secretaria
   do Tesouro Nacional pontua a trajetória histórica, ignorando o efeito prospectivo (âncora:
   Dívida Consolidada/Receita Corrente Líquida ~62,7%, crescente desde 2017 → 0,250).

Estatais, Exigível/Patrimônio Líquido: Δ1→0,5 = 1→0,7 | Instituições financeiras: A+/A→1,0,
B+/B→0,5.

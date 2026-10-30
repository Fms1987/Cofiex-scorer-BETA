# Justificativa do financiamento externo e do credor

Usar na revisão sênior, como checklist, e no Plano de Correção, como texto-modelo e
comparativo. O texto-modelo está em `review/model-texts.md` §3.

No regime anterior, este era o item 1.5 da análise técnica. 44% das Notas Técnicas deram nota
cheia e 76% deram FORTE (ver `calibration/technical-quality-r17.md`). Na RN 1/2024 o item não
pontua, mas a SEAID e o Grupo Técnico continuam perguntando. Uma justificativa fraca vira
pergunta do Grupo Técnico e atrasa a preparação.

## Checklist (os quatro subitens que a SEAID conferia)
| # | Subitem | Atendido quando a carta… | Falha típica |
|---|---|---|---|
| 1 | Por que externo e não interno | compara custo efetivo, prazo e carência com uma fonte nacional (banco público de desenvolvimento, operação interna com garantia) | "justifica a necessidade do financiamento, mas não o porquê de ser externo" |
| 2 | Por que este credor | cita experiência do credor no setor, assistência técnica, apoio na preparação, condições | vantagens "sem evidências concretas" |
| 3 | Condições financeiras | traz moeda, prazo total, carência, amortização, taxa (base + margem), comissão de compromisso e de abertura | condições incompletas; comissões no cronograma que não batem com as do credor |
| 4 | Comparativo com outros credores externos | tabela com 2 ou 3 credores externos e a fonte nacional | "não apresentou comparativo das condições financeiras com outros agentes" |

Classificar com a régua de `technical-quality-r17.md`:
- **FORTE:** os 4 subitens atendidos, com tabela;
- **ADEQUADO:** os 4 atendidos, mas só em texto;
- **FRACO:** falta 1 subitem;
- **AUSENTE:** faltam 2 ou mais.

## Comparativo de referência: prazos e comissões típicos por credor
Base: operações de estados com credores externos na planilha de operações de crédito
(`reference-data/External_Credit_Operations_Database_September_2026.xlsx`, aba
Loans_Master), anos 2016–2026. Medianas; entre parênteses, quantas operações informam o
campo.

| Credor | Operações | Valor mediano (US$ milhões) | Carência (meses) | Prazo total (meses) | Comissão de compromisso mais frequente | Comissão de abertura mais frequente |
|---|---|---|---|---|---|---|
| BIRD (Banco Mundial) | 63 | 120 | 66 (32) | 249 (54); dispersão grande, 81 a 342 | 0,25% ao ano sobre o saldo não desembolsado | 0,25% do valor |
| BID | 72 | 71 | 66 (55) | 294 (71); a maioria entre 282 e 300 | até 0,75% ao ano sobre o saldo não desembolsado | 1,00% do valor, quando informada (poucas operações) |
| CAF | 7 | 136 | 66 (7) | 216 (7) | 0,35% ao ano sobre o saldo não desembolsado | 0,85% do valor |
| NDB, AFD, FIDA, Fonplata, KfW | menos de 12 cada | — | dados incompletos | dados incompletos | — | — |

Notas de uso:
- **A margem sobre a taxa básica não está registrada de forma confiável** na planilha, e a
  taxa básica mudou de LIBOR para SOFR a partir de 2022. Não comparar custo efetivo com estes
  dados. Pedir ao proponente as condições indicativas atuais de cada credor, com data.
- Prazo e carência servem como sinal: uma carta que declara condições muito fora da faixa do
  credor deve ser conferida, por exemplo prazo de 25 anos num credor cuja mediana é 18.
- Valor mediano por credor ajuda a ler o porte: um pleito muito acima da mediana do credor
  pede justificativa de capacidade de execução (item A.4).
- Atualizar esta tabela quando a planilha mudar de versão, com
  `python -X utf8 scripts/creditor_terms.py` (aceita `--desde <ano>` e `--minimo <n>`).

## Saída
Na revisão sênior: uma linha com o nível (FORTE, ADEQUADO, FRACO ou AUSENTE) e o subitem que
falta.

No Plano de Correção: a ação, com remissão ao texto-modelo e à tabela comparativa já
preenchida com as linhas dos credores que a carta deveria comparar.

Não há ganho direto de pontos na Nota de Área Estratégica. O ganho é evitar pergunta do Grupo
Técnico, e o Plano de Correção deve dizer isso.

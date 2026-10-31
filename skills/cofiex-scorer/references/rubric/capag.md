# FASE 7 — Capacidade de Pagamento

## FASE 7 — Capacidade de Pagamento (Art. 20, Anexo III — máx. 2,000)
Art. 10, I, c: máximo 2 pontos. A Capacidade de Pagamento mede a solidez fiscal e a capacidade
de serviço da dívida da entidade (Portaria MF 501/2017: endividamento, poupança corrente,
liquidez) — NÃO os termos da operação proposta.

**Fonte e ciclo (usar primeiro):** `scripts/objective_lookup.py --uf <UF> --reuniao <data>
[--municipio "<nome>"]` devolve a classificação oficial da STN do ciclo em vigor na data da
reunião. Para estados, o ciclo é o último publicado antes da reunião (2023, 2024, revisão de
2024, 2025). Para municípios, é a última posição publicada antes da reunião (2025 e 2026). Nas
63 notas oficiais da RN 1/2024, esse critério acertou 61. Os 2 erros foram uma estatal
pontuada pelo ente mantenedor e uma revisão estadual não publicada em arquivo. Se a STN
publicar um ciclo depois da data de corte da pauta, mostrar os dois como cenário. Atualizar as
tabelas com `tools/build_objective_data.py`.

**Tabela fixa de classificação→pontos (sem sobreposição ad hoc; valores do usuário exigem
metadado conforme a FASE 1.6):**
| Classificação | Pontos | Situação |
|---|---|---|
| A+ | 2,000 | Aprovada — máxima |
| A | 1,500 | Aprovada |
| B+ | 1,000 | Aprovada |
| B | 0,500 | Aprovada (mínimo para passar) |
| C | 0,000 | Não competitiva — não eliminatória |
| D | ELIMINATÓRIA | Art. 28, I, c |
| Não classificada | 0,000 | Não eliminatória |

Estatais não dependentes: A+ (Garantia-Ativo-Fixo>1 + Retorno sobre Investimento>custo) |
A (Garantia-Ativo-Fixo≤1 + Retorno sobre Investimento>custo) | B+ (Garantia-Ativo-Fixo>1 +
Retorno sobre Investimento≤custo) | B (Garantia-Ativo-Fixo≤1 + Retorno sobre Investimento≤custo).
Instituições financeiras: A+ (>15% Basileia) | A (13–15%) | B+ (12–13%) | B (10,5–12%).

### Bancos e estatais de um estado ou município: a nota é da entidade, não do governo mantenedor
Evidência nas notas oficiais (Res. 17/2021 e RN 1/2024):
- **Bancos e agências de fomento estaduais** (4 entidades): Capacidade de Pagamento sempre no máximo. Res. 17/2021: nota 1 de
  máx. 1 nas 10 notas; RN 1/2024: nos 2 pleitos de bancos e agências com total conhecido, o total só fecha com 2,000
  (com a classificação do estado, que para um deles é D, daria 0 e eliminaria o pleito).
- **Estatais não financeiras** (água, energia, porto, parque tecnológico): notas próprias e baixas, 0 a 1 na escala da Res. 17/2021
  e 0,5 na RN 1/2024, diferentes das do estado.
- Sem balanço da estatal: cenário 0,500 (faixa 0,000–1,000) e `input_flag` pedindo Garantia-Ativo-Fixo e Retorno sobre Investimento.

**Portaria 857/2026:** Capacidade de Pagamento recalculada com Fator de Ajuste 0,78 — uma
entidade no limiar de B pode ter se deteriorado; verificar a classificação atual e a data de
consulta (FASE 1.6).

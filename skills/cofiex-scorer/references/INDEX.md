# references/ — índice de recuperação

Carregar apenas o que a fase atual precisa (ver PROTOCOLO DE RECUPERAÇÃO em `../SKILL.md`).

| Pasta | Conteúdo | Usado em |
|---|---|---|
| `regulation/` | Triagem do Anexo I, checagens eliminatórias do Art. 28 | Fases 3–4 |
| `rubric/` | Rubrica da Nota de Área Estratégica + bônus, Índice de Desenvolvimento Humano, Capacidade de Pagamento, Dívida, fórmula da nota final, fontes de dados oficiais para conferência cruzada de Capacidade de Pagamento/dívida/Índice de Desenvolvimento Humano | Fases 1.6, 5–9 |
| `calibration/` | Achados transversais, faixas de Nota de Área Estratégica por setor, **taxas-base por área** (`areas-stats.md`), **cartões de caso** (`cases/`), régua de qualidade técnica do regime anterior (`technical-quality-r17.md`), biblioteca de indicadores (`indicator-library.md`), ponte com o regime anterior (`old-regime-bridge.md`) | Fases 5, 9, 11–12 |
| `iteration/` | Análise de persistência / reenvio | Fase 9.5 |
| `gtec/` | Perguntas calibradas do Grupo Técnico | Fase 10 |
| `review/` | Revisão sênior de banco multilateral de desenvolvimento, plano de correção, textos-modelo (`model-texts.md`) | Fases 11–12 |
| `output/` | Entrega final do relatório em .docx (esquema do JSON, estrutura do sumário executivo) | Após a Fase 12 |

Fora de `references/`:
- `fichas/pleitos/`, `fichas/avaliacoes/` — cabeçalho estruturado (pesquisável por grep) +
  narrativa anonimizada por pleito / avaliação (padrões, nunca casos).
- `data/cases_anonymized.csv` — uma linha por avaliação (esquema em `data/README.md`).
- `docs/analise-areas-estrategicas.md` — referência para humanos: esquema da análise de área
  estratégica (seção 1), registro de área por avaliação (seção 2, não carregar), reconciliação
  com a planilha de resultados (seção 3).

Cartões de caso: `calibration/cases/INDEX.md` lista os setores com n, contagem de aprovações,
medianas de Nota de Área Estratégica/total e quantas narrativas estão preenchidas.
As linhas são anonimizadas (identificadores opacos). **Identificadores nunca devem ser citados
em uma avaliação** (SKILL.md, regras duras).

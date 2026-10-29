# FASE 9.5 — Iteração e persistência

## FASE 9.5 — Análise de Iteração e Persistência
**Executa DEPOIS da pontuação.** Avalia a estratégia de reenvio para operações limitadas pelo
teto.
1. **Isto é um reenvio?** Perguntar ao **usuário** (nunca à web, nunca ao corpus): reunião(ões)
   anterior(es)/desfecho/nota? O texto da carta-consulta mudou? O valor da operação mudou?
   Buscar o próprio histórico deste caso para responder a esta pergunta é uma autoconsulta
   (SKILL.md, regra dura 5) — se o usuário não souber ou não disser, registrar "status de
   reenvio desconhecido" e continuar sem essa informação.
2. **Regra de estabilidade da nota — revisar a afirmação, não a prática de registrar a data/fonte.**
   A reivindicação original ("texto idêntico → nota idêntica") veio de n=9 casos lidos
   manualmente nas narrativas das fichas, onde a identidade do texto podia ser confirmada. O
   backtest em escala (`tools/backtest_iteration.py` sobre a base consolidada de reuniões
   165ª–189ª, agrupando por N° PFE) encontrou 111 N° PFE com mais de uma reunião e **78% deles
   com Nota Final diferente entre reuniões consecutivas** (Δ médio +0,28; variação -1,0 a
   +2,5) — mas essa base não registra se o texto da carta-consulta foi revisado entre
   reenvios, então a maioria dessa variação é esperada (reenvio revisado, não o mesmo texto).
   **Não há, nesta base, como confirmar nem refutar a regra de estabilidade em si** — ela
   permanece válida apenas para o caso estrito de texto comprovadamente idêntico (ainda n=9;
   não inflar essa afirmação com o n maior). Só o saldo do sublimite, o cenário de concorrentes
   e as atualizações no nível da entidade (Capacidade de Pagamento/dívida) mudam entre
   reuniões quando o texto é, de fato, o mesmo.
3. **Probabilidade de persistência — recalibrada com n=111 N° PFE reenviados (reuniões
   165ª–189ª), substituindo a estimativa anterior baseada em n=9:**
| Tentativa | Taxa de aprovação | n | Recomendação |
|---|---|---|---|
| 1ª (entre as que reenviaram) | 0% — por construção (se tivesse aprovado na 1ª, não haveria reenvio) | 111 | Enviar ao sublimite menos congestionado |
| 2ª | **41%** (foi ~60% na estimativa n=9) | 111 | Chances moderadas; qualificar probabilidade sem inflar para "forte" |
| 3ª+ | **24%** (foi ~17% na estimativa n=9) | 29 | Reestruturação fundamental recomendada |
| 4ª+ | sem dados nesta base (máximo observado = 3 reuniões por N° PFE) | 0 | Não afirmar "~0%" sem evidência; tratar como desconhecido |
   Matriz de transição de resultado (reunião anterior → próxima, mesmo N° PFE, n=115 pares):
   Retirado de pauta → Retirado de pauta (70), Retirado de pauta → Aprovado (30), Não aprovado
   → Aprovado (21), Não aprovado → Não aprovado (17), Não aprovado → Aprovado parcialmente (2).
   *Modificador do 4º trimestre:* ~75% das trajetórias "Não aprovado → Aprovado" sob a NR
   1/2024 ocorreram na reunião do 4º trimestre (maior taxa de aprovação ~81% devido aos tetos
   de rolagem) — achado anterior (n=9), ainda não recalibrado com a base maior por falta de
   coluna de trimestre explícita; refazer quando a data de reunião for mapeada para trimestre.
4. **Compressão do valor da operação:** a compressão isolada é insuficiente — funciona quando
   a Nota de Área Estratégica já é competitiva (≥8,5) e o valor comprimido cabe dentro do saldo
   do teto. (Âncoras: compressões de ~82% e ~72% tiveram sucesso com Nota de Área Estratégica
   alta no 4º trimestre; compressão de 0% com Nota de Área Estratégica moderada falhou.) Uma
   revisão de escopo acompanhando a compressão *sim* muda a nota (já não é o mesmo texto de
   carta-consulta).
5. **Recomendação de estratégia:**
| Situação | Estratégia |
|---|---|
| 1ª, nota ≥ 10 | Enviar ao 4º trimestre para saldo máximo de teto |
| 1ª, nota < 8 no sublimite Geral | Considerar sublimite PPP/Ambiental-Climático/Fiscal se elegível |
| 2ª, mesmo texto de carta-consulta | Visar o 4º trimestre; nota inalterada, só importa o saldo do teto |
| 2ª, carta-consulta revisada | Quantificar a variação esperada da Nota de Área Estratégica; se < +1,0, a compressão tem mais impacto |

6. **Evolução da Área Estratégica em reenvios (39 pares com Nota Técnica nas duas versões, RN
   1/2024).** Em 79% dos pares a Área Estratégica ficou idêntica (31/39). A variação média foi
   de +0,31, e só 7 subiram. Os ganhos vieram de: (a) áreas secundárias novas em D/E, cada uma
   com objetivo específico, produto, indicador e custo próprios; (b) correção de
   inconsistências entre texto e anexos, que destravou várias áreas de E para D; (c) ano-meta nos
   indicadores, que fechou o SMART; (d) a área principal passando de 30% do orçamento (C→B);
   (e) poda de áreas que pontuavam zero, com realocação dos recursos. Uma revisão de foco também
   já rebaixou uma área (C→D). Usar `review/correction-plan.md` ("Rota para Área Estratégica
   máxima") para estimar o Δ de uma carta revisada, em vez de supor ganho só por reenviar.
| 3ª+ | Redesenho fundamental: redução de escopo, troca de credor, ou migração de sublimite |

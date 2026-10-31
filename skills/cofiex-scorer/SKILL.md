---
name: cofiex-scorer
description: Simula a avaliação técnica da COFIEX para uma carta-consulta sob a Res. Normativa 1/2024 (alterada pelas Res. 32/2025, 142/2026, 150/2026, 151/2026). Produz faixa de nota (rubrica do Anexo II), checagem eliminatória (Art. 28), viabilidade de sublimite, revisão sênior de banco multilateral, perguntas do Grupo Técnico, análise de iteração/persistência e plano de correção. Baseado em recuperação (RAG): carrega rubrica, calibração e fichas de casos anonimizados de references/ sob demanda.
metadata:
  version: 'V.1 BETA'
  language: pt-BR
  author: Fabricio Martins
  updated: '2026-10-27'
---

## PRINCÍPIO DE JULGAMENTO CEGO (OBRIGATÓRIO — LER ANTES DE QUALQUER ATUALIZAÇÃO)
Esta habilidade é uma **avaliadora cega**. Deve pontuar qualquer carta-consulta recebida pelos
seus méritos intrínsecos e pela calibração regulatória/empírica codificada aqui — **nunca**
reconhecendo ou casando com um projeto real específico, proponente, número de carta-consulta
ou desfecho de reunião.

**A calibração é preservada apenas como âncoras empíricas anonimizadas:** faixas numéricas,
limiares de nota, descontos por modalidade, critérios de bônus e referências por perfil
(ex.: "operação de investimento, 4 áreas estratégicas, perfil B → nota de área estratégica
~6,5"). Metadados identificadores (nome do proponente, município/estado, número da carta-
consulta/Portal de Financiamento Externo, número de reunião ligado a um caso nomeado) são
deliberadamente removidos para que a avaliadora não consiga reconstruir um veredito conhecido.

**REGRA DE MANUTENÇÃO (vale para toda versão futura):**
1. Novos achados empíricos devem ser incorporados como **âncoras anonimizadas** (perfil +
   números), nunca como casos nomeados ou precedentes do tipo "este projeto foi aprovado".
2. Ao adicionar um novo teste cego ou sessão de corpus, remova a identidade antes de
   armazenar o valor de calibração que ele traz. Mantenha *o que ensina*, descarte *quem era*.
3. Não reintroduzir tabelas de precedentes nomeados, listas de cartas-consulta por reunião,
   ou changelogs sessão-a-sessão. Consolide os achados nas seções de calibração abaixo.
4. A saída nunca deve citar um projeto real como comparador. Use perfis anonimizados.

Violar essas regras destrói o caráter cego da habilidade e tendencia a pontuação.

### Disciplina de atualização (5 sub-regras de atualização do julgamento cego)
Sempre que nova evidência/calibração for incorporada, aplique TODAS as seguintes:
1. **Âncora empírica obrigatória.** Toda mudança de parâmetro vem com uma âncora (número de
   testes cegos / data) e uma justificativa de uma linha. Nenhuma mudança sem âncora.
2. **Faixas em vez de exceções.** Nova informação é traduzida em faixas/probabilidades,
   nunca em exceções nomeadas ad hoc.
3. **Tabelas oficiais não são sobrepostas pelo usuário.** Valores informados pelo usuário para
   insumos regulados (CAPAG, tetos de sublimite) nunca sobrepõem tabelas oficiais sem metadado
   verificável.
4. **Changelog apenas anônimo.** Registrar somente: parâmetro alterado, novo valor/faixa,
   razão empírica (ex.: "n testes cegos = k"). Nunca citar uma carta-consulta identificável.
5. **Regressão no banco de teste fixo.** Toda mudança que possa mover uma nota é medida no
   banco de teste fixo, em ambiente cego, antes de entrar (procedimento em
   `tools/regression_spec.md` do repositório). Piora de métrica principal além da tolerância
   não entra sem justificativa escrita.

## Sobre esta habilidade
Simula a avaliação técnica da COFIEX para uma carta-consulta (proposta de financiamento
externo) sob a **Resolução Normativa nº 1/2024**, consolidada em 18/05/2026 (alterada pelas
Res. COFIEX 32/2025, 142/2026, 150/2026, 151/2026).

Ao receber uma carta-consulta, declarar brevemente o que a habilidade faz antes de analisar:
simula a análise técnica (Art. 9–23), o filtro eliminatório (Art. 28), o sublimite (Art. 25),
a pontuação objetiva (Art. 10, Anexos II–III), as perguntas calibradas do Grupo Técnico, e o
parecer técnico final com sugestões de melhoria seção a seção.

**Qualidade SMART (todo o corpus):** Fórmula 100%, Unidade 100% são universais; **Verificação
é o campo mais fraco** (~40–53%); a presença de linha de base varia por setor (digital/justiça
a postergam; fiscal/ambiente/água a incluem). Média ≈ 3,7/5.

**Confirmações de leitura da regulação (NR 1/2024 consolidada).**
- Pesos do Anexo II A=5 / B=3 / C=2 / D=1 / E=0,5; fórmula do IDH conforme Art. 18 (relativa à
  reunião).
- Dois bônus distintos de +1, **limitados juntos à Nota de Área Estratégica = 10**: bônus de
  prioridade do PPA (Art. 15 §3º) e bônus de Zona de Fronteira (Art. 15 §4º).
- O catálogo de Áreas Estratégicas usa a numeração **101–307** (PPA 2024–2027). A numeração
  antiga 1.1–1.15 (Res. 17/2021, SIGS, descontinuada pelo Art. 50) é referência estrutural
  apenas.
- Estrutura oficial do Anexo I (Portal de Financiamento Externo): I. Projeto (Identificação,
  Justificativa, Objetivos, Indicadores, Componentes, Beneficiários) · II. Áreas Estratégicas
  · III. Gestão · IV. Riscos · V. Financiamento · VI. Ações Preparatórias · VII. Contatos.

**Tetos dos componentes da nota (confirmados contra a regulação):** Nota de Área Estratégica
máx. 10 · Índice de Desenvolvimento Humano máx. 2 · Capacidade de Pagamento máx. 2 · Dívida
máx. 1 · **Total máx. 15** (subnacional). Entidade federal = apenas Nota de Área Estratégica
(máx. 10). Os bônus são absorvidos dentro do teto de 10 da Nota de Área Estratégica; não
elevam o total acima de 15 por padrão (ver FASE 9, teto extensível).

## Regras de Comportamento
- Linguagem clínica. Deficiências primeiro.
- Nota: Área Estratégica (máx. 10) + Índice de Desenvolvimento Humano (máx. 2) + Capacidade
  de Pagamento (máx. 2) + Dívida (máx. 1) = máx. 15.
- Capacidade de Pagamento D = eliminatório obrigatório (Art. 28, I, c). Capacidade de Pagamento
  C = 0 pts, não competitivo mas **não** eliminatório. Capacidade de Pagamento 0,000 para
  entidades não classificadas (maioria dos municípios) = 0 pts, não eliminatório.
- Entidades federais: Capacidade de Pagamento/Índice de Desenvolvimento Humano/Dívida NÃO se
  aplicam; apenas Nota de Área Estratégica (máx. 10); sem piso de Nota de Área Estratégica.
- Piso de Nota de Área Estratégica subnacional: 3,0 pts (Art. 28, I, b).
- Pontuar como uma FAIXA (mínimo/esperado/máximo), com incerteza de ±1 nível. Em primeiro
  plano fica só a **Nota Geral esperada**, com a Nota de Área Estratégica esperada abaixo. A
  **faixa empírica** (FASE 9, `rubric/final-score.md`) vem logo depois, como frase; a faixa
  pela rubrica (soma dos extremos de cada item) fica como cenário.
- **Posicionamento no sublimite ≥ maximização da nota em um mercado com oferta restrita.**
- **O valor da operação ser menor ou igual ao teto estimado da reunião é condição necessária
  para a aprovação, independente da nota.**
- **Notas são estáveis entre reenvios de texto idêntico da carta-consulta → nota idêntica.**
  Estratégia de iteração = momento + valor + sublimite, não revisão da carta-consulta.
- **Persistência tem retornos decrescentes:** 2ª tentativa ~60% de sucesso, 3ª ~17%, 4ª+ ~0%.
  Recomendar no máximo 2 ciclos antes de uma reestruturação fundamental.
- "Retirado" (Res. 17/2021, proponente se autorretirou antes da pontuação) ≠ "Não aprovado"
  (Res. 1/2024, pontuado mas bloqueado pelo teto ou eliminado) — sinais estratégicos diferentes.
- Todos os insumos são repetidos textualmente. Toda saída traz o selo de versão.
- **A integridade dos insumos precede a pontuação** (ver FASE 1.6): insumos regulados não são
  automaticamente confiados.

## PROTOCOLO DE RECUPERAÇÃO (RAG sobre `references/`)
Este arquivo contém apenas o fluxo de trabalho e as regras duras. Tabelas detalhadas,
rubricas, âncoras de calibração e fichas de casos anonimizados vivem em `references/` e são
carregadas **sob demanda** — ler um arquivo só quando a fase abaixo precisar dele, nunca tudo
de uma vez. Começar por `references/INDEX.md`.

| Fase | Carregar antes de executar |
|---|---|
| 3–4 Triagem, Art. 28 | `references/regulation/screening-and-eliminatory.md` |
| 5 Nota de Área Estratégica | `references/rubric/ae-rubric-and-bonuses.md` + `references/calibration/ae-ranges-and-sectors.md` + `references/calibration/cross-cutting-findings.md` + `references/calibration/ae-criteria-by-level-and-ppa-area.md` |
| 5 (esquema de áreas) | `docs/analise-areas-estrategicas.md` **apenas seção 1** (primeiras ~60 linhas: como a Res. 17/2021 e a Res. 1/2024 pontuam as áreas); nunca carregar a seção 2 (registro por caso) |
| 5 (taxas-base por área) | `references/calibration/areas-stats.md` (taxas de aceitação por objetivo, mix de níveis, taxas de pontos adicionais); para n < 30 ou pleito vindo do regime anterior, `references/calibration/old-regime-bridge.md` |
| 5 (consulta de calibração) | seguir a **RECEITA DE RECUPERAÇÃO** abaixo: `cases/INDEX.md` → um cartão de setor → no máximo 6 fichas de pleito + 6 fichas de avaliação |
| 6–8 Dados Objetivos (subnacional) | rodar primeiro `scripts/objective_lookup.py --uf <UF> --reuniao <data> [--municipio "<nome>"]`: devolve Capacidade de Pagamento do ciclo em vigor, Tendência da Dívida pela regra calibrada e Índice de Desenvolvimento Humano com o piso calibrado, com fonte e ciclo (vale como metadado da FASE 1.6) |
| 6 Índice de Desenvolvimento Humano | `references/rubric/idh.md` |
| 7 Capacidade de Pagamento | `references/rubric/capag.md` |
| 8 Dívida | `references/rubric/debt.md` |
| 9 Nota final | `references/rubric/final-score.md` |
| 9.5 Iteração | `references/iteration/persistence.md` (apenas se houver reenvio) |
| Seção 10 Janela e Momento | `references/strategy/sublimit-targeting.md` + `reference-data/sublimit_status.json` (limites da próxima reunião e linha de corte recente; tabela completa em `references/strategy/sublimit-table.md`) |
| Carteira | `scripts/portfolio.py registrar …` depois de cada simulação, se o usuário mantiver uma carteira; `portfolio.py mostrar --html painel.html` para o painel |
| 10 Perguntas do Grupo Técnico | `references/gtec/questions.md` |
| 11 Revisão de banco multilateral | `references/review/senior-mdb-review.md` + régua de subitens `references/calibration/technical-quality-r17.md` + **lente Banco Mundial, sempre** `references/review/world-bank-lens.md` + checklist do credor `references/review/creditor-justification.md` |
| 12 Plano de correção | `references/review/correction-plan.md` + `references/review/model-texts.md` (textos-modelo) + `references/calibration/indicator-library.md` (indicadores por setor); comparativo de credores por `scripts/creditor_terms.py` |
| Entrega | `references/output/docx-report.md` (regras de redação, resumo para o líder de equipe, carta ao cliente) |

### O que é recuperável (camadas, mais baratas primeiro)
| Camada | Onde | Contém | Usar para |
|---|---|---|---|
| Regras e tabelas | `references/rubric|regulation|gtec|review|iteration/` | Regulação, rubrica, tabelas oficiais, perguntas do Grupo Técnico | A própria nota |
| Cartões de perfil | `references/calibration/cases/<setor>.md`, `data/cases_anonymized.csv` | Uma linha por avaliação: regime, ano-trimestre, subtipo, credor, faixa de valor, desfecho, notas, contagem de indicadores, participação de linha de base | **Faixas** e taxas de aprovação |
| Taxas-base por área | `references/calibration/areas-stats.md` | Taxa de aceitação por objetivo do Anexo II / critério R17, mix de níveis, taxas de pontos adicionais | Plausibilidade das áreas declaradas na Fase 5 |
| Fichas | `fichas/pleitos/P*.md`, `fichas/avaliacoes/A*.md` | Cabeçalho estruturado (pesquisável por grep) + narrativa anonimizada (notas A.1–A.5, aderência ao Grupo Técnico, achados da Nota Técnica) | **Padrões** ("o que esse tipo de programa costuma deixar faltando"), nunca casos |

### RECEITA DE RECUPERAÇÃO (executar uma vez, no início da FASE 5; orçamento: 1 cartão de setor + consultas ilimitadas de cabeçalho via Grep/CSV + no máximo 6 fichas de pleito + 6 fichas de avaliação abertas como corpo)
1. **Perfil de consulta** a partir da triagem: `regime` (padrão `NR1_2024`; usar `R17_2021`
   apenas para reuniões anteriores à NR1), `sector` (área estratégica dominante julgada pelos
   indicadores e componentes da carta-consulta, não pelo seu título — pergunta 23 do Grupo
   Técnico), `subtype`, `lender`, `ticket_band` (`<50M`, `50-100M`, `100-200M`, `200-400M`,
   `>400M` USD; operações em reais são `BRL-nominal` e ficam excluídas do filtro de faixa),
   marcadores de modalidade (`dli`, `pbl`, `ppp`, `on_lending`, …), número da tentativa.
2. **Cartões.** Ler `cases/INDEX.md` (tamanhos e medianas por setor), depois ler
   `cases/<setor>.md` e manter as linhas que casam com o perfil. O CSV pode ser filtrado da
   mesma forma. **Setor com n < 5:** o cartão traz só contagens. Não ler as linhas desse setor
   no CSV para ancorar a nota; usar a rubrica, os critérios por objetivo do PPA e os cartões
   vizinhos com n ≥ 5, apenas como faixa.
3. **Cabeçalhos primeiro, fichas só se necessário.** Contar e filtrar apenas pelo cabeçalho
   antes de abrir qualquer corpo de ficha: Grep com `output_mode: files_with_matches` (ou
   `count`), caminho `fichas/pleitos`:
   - setor: padrão `^sector_verified: <setor>$`; modalidade: `^tags: .*\b<marcador>\b`; credor:
     `^lender_verified: <CREDOR>$`
   - as avaliações de um pleito: caminho `fichas/avaliacoes`, padrão `^pleito: <id-P>$`
   O CSV (`data/cases_anonymized.csv`) pode responder à mesma pergunta de filtro-e-contagem
   sem tocar em nenhuma ficha. **Abrir o corpo de uma ficha apenas quando um padrão
   qualitativo genuinamente precisa da narrativa** (ex.: "o que programas assim costumam
   deixar faltando") — não para confirmar um número que o cabeçalho/CSV já deu, e não só
   porque uma lista de candidatos apareceu. Um teste cego encontrou um agente abrindo várias
   fichas não relacionadas em vez de parar na contagem do cabeçalho; tratar isso como o modo
   de falha a evitar. Quando a leitura do corpo é justificada, ler no máximo as primeiras ~60
   linhas de cada ficha escolhida, preferindo `narrative: filled` (sem marcador `pendente`) e
   `regime: NR1_2024`.
4. **Regra de n mínimo.** Uma afirmação numérica de calibração precisa de **n ≥ 5** linhas
   comparáveis (mesmo regime + setor + subtipo + credor + faixa de valor). Se houver menos,
   relaxar nesta ordem e declarar isso: (a) soltar o credor → (b) soltar a faixa de valor →
   (c) soltar o subtipo (manter regime + setor) → (d) adicionar o setor secundário. Se n < 5
   mesmo assim, escrever "calibração insuficiente (n=k)" e usar apenas as faixas da rubrica.
   Nunca agrupar `R17_2021` com `NR1_2024` para a Nota de Área Estratégica (essa nota só
   existe na NR1; os totais da R17 estão em outra escala). Um padrão qualitativo ("uma lacuna
   recorrente") precisa de ≥ 3 fichas mostrando-o.
5. **Ancoragem quando n ≥ 5.** O corpus ajusta a estimativa; não a fixa com precisão — uma
   verificação com retenção de amostra sobre 94 notas de Área Estratégica publicadas da
   NR1_2024 achou que a mediana do subtipo era apenas cerca de 0,1 ponto mais precisa do que
   simplesmente sempre apostar na mediana global (erro absoluto médio ≈1,1–1,3 em uma escala
   de 0–10), e intervalos construídos só a partir do conjunto comparável costumam ser largos
   demais para serem úteis por si sós. Então: quando n ≥ 5 no nível mais fino alcançado no
   passo 4, empurrar a estimativa da própria rubrica um pequeno passo em direção à mediana do
   conjunto comparável (não até ela) e manter a faixa [Mínimo–Esperado–Máximo] pelo menos tão
   larga quanto a dispersão do próprio conjunto comparável; não relatar a mediana comparável
   como se fosse uma previsão. Quando n < 5, não ancorar nada — declarar "n=k, insuficiente
   para ancorar" e usar apenas a faixa da rubrica.
6. **Filtros de confiabilidade.** Tratar como fraco (e declarar isso): `sector_source:
   keyword_heuristic`; `narrative: pending|no_cc_text`; `nt_match:
   no_meeting_folder|single_attempt_fallback`; `n_indicators_parse: heuristic`. Usar
   `lender_verified` e `counterpart_pct_verified`, não os valores brutos do cabeçalho. `ae` é
   o valor publicado (planilha de resultados); a Nota de Área Estratégica da própria Nota
   Técnica é preliminar e pode ser menor pelos pontos adicionais concedidos depois. Um `ae`
   em branco é ignorado, nunca lido como 0.
7. **Linha de base de calibração (obrigatória na saída):** `Base de calibração: n=<k> perfis
   comparáveis (regime, setor, subtipo[, credor][, faixa]); relaxado: <filtros>; dados fracos:
   <marcadores>; ancoragem: <nenhuma|empurrada em direção à mediana>`.

### Precedência entre âncoras (quando duas fontes apontam valores diferentes)
Aplicar nesta ordem; uma fonte de nível inferior só ajusta dentro do espaço deixado pela
superior, nunca a contradiz:
1. **Tabelas oficiais** (Capacidade de Pagamento, Dívida, Índice de Desenvolvimento Humano,
   tetos de sublimite, filtros do Art. 28).
2. **Rubrica aplicada aos números da carta:** orçamento por área (FASE 5, passo 0) e lente A.6.
   O teto pelo orçamento nunca é ultrapassado por nenhuma âncora abaixo.
3. **Critérios por objetivo do PPA** (`calibration/ae-criteria-by-level-and-ppa-area.md`):
   decidem entre dois níveis permitidos pelo item 2. Nas áreas secundárias, a seção 4 desse
   arquivo define o ponto de partida pelo grupo do objetivo: 0 nos que quase sempre ficam em 0
   e no grupo intermediário, E nos que costumam pontuar.
4. **Cartão de setor** (apenas n ≥ 5, apenas como faixa): empurra a estimativa um pequeno
   passo (passo 5 da receita), sem tirá-la do intervalo dado pelos itens 2 e 3.
5. **Achados transversais e âncoras de exemplo** (`cross-cutting-findings.md`, exemplos da
   rubrica): só explicam ou sinalizam; não movem nota sozinhos.
Quando houver conflito, registrar numa linha qual âncora prevaleceu e por quê.

### Regras duras (preservam o julgamento cego)
1. **Nunca citar um caso.** Nenhum identificador de ficha, nenhum "um projeto semelhante foi
   aprovado/rejeitado", nenhuma descrição de um projeto específico. Apenas agregados: "n=k
   perfis comparáveis: Nota de Área Estratégica mediana X (quartis a–b); aprovados m/k".
2. **Nunca citar ou parafrasear a narrativa de uma ficha para o usuário.** Usá-la para decidir
   o que verificar, depois confirmar o ponto no próprio texto da carta-consulta do usuário e
   citar *isso*.
3. **O corpus calibra; não pontua.** Toda nota vem da rubrica aplicada ao texto do usuário. As
   faixas do corpus definem a banda ± e acionam a salvaguarda de regressão à mediana; elas
   nunca sobrepõem uma tabela oficial (pontos de Capacidade de Pagamento, tetos de sublimite,
   filtros do Art. 28).
4. **Taxas de desfecho não são veredito.** A aprovação depende do teto da reunião; sempre
   relatar a taxa junto com a leitura de viabilidade de sublimite e nunca enquadrar uma nota
   alta ou uma taxa de aprovação alta como "provavelmente aprovado".
5. **Sem autoconsulta.** Se a carta-consulta parecer um caso do corpus (mesmo setor, credor,
   faixa, ano, tentativa), não procurar nem abrir a ficha desse caso, e não mencionar a
   semelhança. Continuar apenas com agregados. É também por isso que o passo 3 da RECEITA DE
   RECUPERAÇÃO prioriza contagens de cabeçalho/CSV: o corpo de uma ficha só é aberto quando a
   necessidade qualitativa é real, nunca como reflexo assim que uma lista de candidatos
   aparece.
   **Esta regra vale para a ferramenta de busca na web exatamente como vale para o corpus.**
   Nunca executar uma busca na web que inclua os próprios identificadores deste pleito (nome
   do programa, proponente, UF/município, número de processo do Portal de Financiamento
   Externo/SEI, valor da operação, combinação setor + credor + ano) junto com termos como
   `aprovados`, `resultado`, `pauta`, `reunião`, `deferido`, `indeferido`, ou similares. Em
   particular: **nunca buscar o código do Portal de Financiamento Externo/processo deste
   pleito contra pautas ou páginas de resultado de reuniões da COFIEX, de nenhuma forma** —
   nem mesmo "só para checar o calendário regulatório". Essa consulta só pode ter um
   propósito: achar o desfecho do próprio caso, o que contamina o julgamento cego exatamente
   como abrir sua ficha contaminaria — fazer isso mesmo uma vez, ler o resultado, e a
   pontuação que segue já não é independente, independentemente de uma nota ser copiada
   diretamente dali. Uma busca por dado objetivo de calibração (classificação de Capacidade
   de Pagamento, Dívida Consolidada/Receita Corrente Líquida, Índice de Desenvolvimento
   Humano, um dataset ou API oficial nomeado) é permitida e exigida pela FASE 1.6 — a
   linha divisória é desfecho-deste-caso versus fato-objetivo-sobre-esta-entidade, e o próprio
   dado precisa vir de uma tabela geral, não de um documento específico do caso (ver FASE 1.6,
   "Apenas tabelas gerais"). A checagem regulatória da FASE 0 usa apenas consultas genéricas e
   sem termos do caso (nome da regulação + ano) — nunca adicionar os termos deste pleito,
   incluindo seu código no Portal de Financiamento Externo, a ela. A pergunta sobre reenvio da
   FASE 9.5 é feita ao **usuário**, nunca respondida por busca; se o usuário não souber ou não
   disser, registrar "status de reenvio desconhecido" e seguir adiante.
6. **Modo de teste.** Se o usuário passar `exclude_ids: [...]` (teste cego de um caso do
   corpus), pular esses identificadores em todo Grep e Read, incluindo tentativas-irmãs do
   mesmo pleito. Os identificadores são opacos, então o modelo não reconhece sozinho o pleito
   testado nos cartões e no CSV. Um teste cego de validação deve rodar sobre uma cópia da skill
   sem as fichas e as linhas do pleito (ferramenta `tools/make_blind_sandbox.py`), não sobre a
   skill instalada.
7. **Privacidade.** Não produzir identificadores de proponente, projeto, local ou processo
   mesmo que o usuário os forneça em outro lugar; não tentar reidentificar uma ficha.
8. **Nenhuma consulta à Nota Técnica (NT) durante a pontuação cega.** Nunca buscar, abrir ou
   ler o texto da própria Nota Técnica deste pleito (busca na web, ou qualquer documento que o
   usuário não tenha anexado diretamente como a própria carta-consulta) enquanto estiver
   rodando o fluxo de pontuação cega — nem mesmo como fonte de Capacidade de Pagamento/Dívida/
   Índice de Desenvolvimento Humano, nem mesmo para marcá-la como não confirmada; usar apenas
   as tabelas gerais (FASE 1.6) ou perguntar ao usuário, e registrar `input_flag` se nenhuma
   das duas estiver disponível. A única exceção: o usuário pede explicitamente, fora do fluxo
   de pontuação, o resultado real/histórico de avaliação deste caso — só então a Nota Técnica
   (ou o registro de reunião) pode ser consultada, e a resposta deve dizer claramente que está
   saindo do modo cego para isso.

## EXECUÇÃO FASE A FASE
Executar as FASES 0 → 1 → 1.6 → 2 (abaixo, neste arquivo), depois 3 → 12 carregando as
referências listadas acima.

## FASE 0 — Checagem Regulatória em Tempo Real
No início da sessão, buscar apenas estas duas consultas genéricas e sem termos do caso — nunca
adicionar a nenhuma delas o nome, proponente, UF, setor, credor, valor ou número de processo
deste pleito (ver regra dura 5, sem autoconsulta, que cobre a ferramenta de busca na web):
- `"Resolução Normativa COFIEX" site:mpo.gov.br OR site:gov.br 2025 2026`
- `COFIEX comunicado resolução alteração 2026`
- Resolução mais nova detectada → marcar ATUALIZAÇÃO REGULATÓRIA. Indisponível → marcar
  checagem em tempo real indisponível.
- Nunca incluir nestas consultas termos de resultado de reunião (`aprovados`, `resultado`,
  `pauta`, `ata`, `deferido`, `indeferido`): eles trazem páginas que podem conter o desfecho
  do próprio pleito, e esta checagem serve só para detectar mudança normativa.
- Se uma página de resultado, pauta ou ata aparecer mesmo assim na lista de resultados, não
  abri-la, não ler além do trecho exibido, e não usar nem relatar o que ela dizia — esta
  checagem é só para atualizações regulatórias, não uma licença para navegar por resultados de
  reunião deste caso.

Base regulatória ativa:
- Res. Normativa COFIEX nº 1 (22 nov 2024) — marco principal
- Res. 32/2025 — altera a Res. 1/2024
- Res. 142/2026 (24 mar 2026) — altera a Res. 2/2025 e a Res. 1/2024
- Res. 150/2026 (26 mar 2026) — modificações técnicas/financeiras
- Res. 151/2026 (26 mar 2026) — restrições à reestruturação em reais
- Portaria MF/STN 857/2026 (27 mar 2026) — Fator de Ajuste 0,78, consolidação de Capacidade de
  Pagamento
- CMN 5.282/2026 (26 fev 2026) — participação do sublimite subnacional → 29,7%

## FASE 1 — Triagem Obrigatória
**Primeiro perguntar:** "Você tem um arquivo pré-preenchido (minuta de carta-consulta,
formulário de triagem ou planilha de pontuação anterior) para anexar? Se sim, envie agora."
- Arquivo anexado → ler por completo, pré-preencher todo campo inferível, perguntar só sobre
  lacunas/ambiguidades.
- **Modo pré-carta:** se o insumo for nota conceitual ou rascunho (faltam 2 ou mais seções do
  Anexo I, ou não há valor por componente, ou não há objetivos), seguir
  `references/output/pre-carta-mode.md`. A saída mostra as lacunas que impedem pontuar e uma
  faixa provisória só do que já é pontuável, e encaminha a redação para a skill
  cofiex-pleito-builder.
- Sem arquivo → executar a sequência completa de perguntas e respostas (usar
  `references/protocolo-preenchimento.md` v2.0 como guia estruturado; Parte I = insumos de
  pontuação Blocos 0–8, Parte II = formulário do Portal de Financiamento Externo Blocos 9–15).

**O valor da operação é o insumo obrigatório de primeira linha.**

Bloco I — Identidade e Finanças (PRIORIDADE): I.1 Nome completo | I.2 Abreviado | I.3 Tipo
(investimento/reestruturação/repasse) | I.4 Proponente | I.5 Tipo de entidade (federal/
estadual/DF/municipal/estatal federal/estatal subnacional/instituição financeira) | **I.6
Credor** | **I.7 Moeda** | **I.8 Valor total em dólares equivalentes ←OBRIGATÓRIO** | **I.9
Valor do empréstimo em dólares equivalentes ←OBRIGATÓRIO** | I.10 Contrapartida %
(marcar se <20% sem dispensa) | I.11 Sublimite-alvo (Geral/PPP/Ambiental-Climático/Fiscal/
Reestruturação de Dívida/Operações em Reais/Federal).

Bloco II — Áreas Estratégicas: códigos do Anexo II + narrativa por área.

Bloco III — Perfil da Entidade: Capacidade de Pagamento (A+/A/B+/B/C/D/não classificada) +
**data e fonte da consulta de Capacidade de Pagamento (metadado obrigatório)** | Basileia
(instituições financeiras) | Garantia-Ativo-Fixo/Retorno sobre Investimento (estatais) |
Dívida Consolidada/Receita Corrente Líquida | Tendência da dívida (5 níveis) | Índice de
Desenvolvimento Humano/Municipal (3 decimais) | Região | Zona de fronteira S/N | Prioridade
do PPA integral S/N | Plano de Recuperação Fiscal S/N | Art. 28 d–h cada um S/N | **código
IBGE (para conferência cruzada)**.

## FASE 1.6 — Portão de Integridade dos Insumos (obrigatório antes de pontuar)
Insumos regulados não são automaticamente confiados. Executar ANTES da classificação:
- **Metadado de Capacidade de Pagamento.** Rejeitar um valor de Capacidade de Pagamento sem
  data/fonte de consulta. Verificar se a classificação pertence ao ciclo da Secretaria do
  Tesouro Nacional vigente na data da reunião-alvo (recálculos da Portaria 857/2026 podem ter
  deslocado uma entidade no limiar de B). Metadado ausente → `input_flag`, não atribuir pontos
  de Capacidade de Pagamento até validar.
- **Conferência cruzada código IBGE × UF.** Confirmar que o código IBGE da entidade casa com o
  nome/UF declarados. Discrepância → `input_flag`; não usar automaticamente o valor de
  Capacidade de Pagamento/Índice de Desenvolvimento Humano do dataset para essa entidade até
  resolver.
- **Consistência da capacidade fiscal.** Checar a sanidade dos valores/projeções declarados
  contra o tipo de entidade e o valor da operação. Valores fora da curva → `input_flag`.
- **Sem sobreposição silenciosa.** Um insumo marcado bloqueia o uso automático do valor
  correspondente do dataset; expor a marcação na saída e solicitar a correção.
- **Apenas tabelas gerais, nunca um documento específico do caso.** Os valores de Capacidade
  de Pagamento, Dívida e Índice de Desenvolvimento Humano/Municipal precisam vir de uma tabela
  ou dataset oficial geral (a planilha empacotada, o boletim de Capacidade de Pagamento da
  Secretaria do Tesouro Nacional, Relatório Resumido de Execução Orçamentária/Relatório de
  Gestão Fiscal, Tesouro Transparente, IBGE, IPEA) que liste muitas entidades — nunca de uma
  Nota Técnica, parecer, ofício ou qualquer outro documento produzido para avaliar este
  processo específico (uma Nota Técnica "SEI .../MF", uma nota técnica da COFIEX/MPO citando o
  número de processo deste próprio pleito, etc.). Não buscar nem abrir esse tipo de documento
  de forma alguma durante a pontuação cega, nem mesmo como alternativa ou para marcá-lo (ver
  regra dura 8) — se a tabela geral não tiver o valor, o resultado é `input_flag`, ponto final;
  pedir o número ao usuário em vez de recorrer à Nota Técnica do próprio processo.
- **Onde checar.** Usar apenas fontes gratuitas/oficiais para conferência cruzada de
  Capacidade de Pagamento, Dívida e Índice de Desenvolvimento Humano/Municipal (Tesouro
  Transparente, API do IBGE, `ipeadatar`/`ipeadatapy` do IPEA, SNIRH, Base dos Dados — nunca
  um fornecedor pago); ver `references/rubric/official-data-sources.md`.

## FASE 2 — Classificação da Entidade
| Entidade | Piso de Nota de Área Estratégica | Capacidade de Pagamento | Índice de Desenvolvimento Humano | Dívida | Filtro principal |
|---|---|---|---|---|---|
| Órgão federal | Nenhum | Não se aplica | Não se aplica | Não se aplica | Adequação da Secretaria de Orçamento Federal, Art. 23 |
| Estatal federal não dependente | Nenhum | Garantia-Ativo-Fixo/Retorno sobre Investimento ou Basileia | Não se aplica | Matriz própria | — |
| Estado/DF/Município subnacional | 3,0 | Secretaria do Tesouro Nacional, se classificado | Sim | 5 níveis | Art. 28, I, a–h |
| Estatal subnacional não dependente | Nenhum | Garantia-Ativo-Fixo/Retorno sobre Investimento próprios (nunca os do estado) | **Sim**, do estado ou município-sede | Exigível/Patrimônio Líquido próprio | — |
| Instituição/agência financeira subnacional | Nenhum | Basileia (nas notas oficiais, sempre a máxima) | **Sim**, do estado-sede | Máxima (nas notas oficiais) | — |

> **Sociedade de economia mista municipal:** tratada sob as regras de estatal subnacional
> (sem piso de Nota de Área Estratégica, Capacidade de Pagamento baseada em Garantia-Ativo-
> Fixo/Retorno sobre Investimento, dívida por Exigível/Patrimônio Líquido). Uma sociedade de
> economia mista com receita própria forte (ex.: tarifa de água) pode se qualificar para
> dispensa do mínimo de contrapartida do Art. 28 (anomalia — confirmar o regime).

> **Banco, agência de fomento e estatal de um estado ou município (regra tirada das notas oficiais, ver
> `references/rubric/capag.md`, `debt.md` e `idh.md`):** os dados objetivos são os da própria entidade, nunca os do
> governo que a mantém. Banco ou agência de fomento: Capacidade de Pagamento e Dívida no máximo (RN 1/2024: 2,000 e
> 1,000), em todas as notas oficiais conhecidas. Estatal não financeira: Garantia-Ativo-Fixo, Retorno sobre
> Investimento e Exigível/Patrimônio Líquido próprios, em geral baixos; sem o balanço, cenário e `input_flag`. O Índice
> de Desenvolvimento Humano **vale para todas**, calculado com o índice do estado-sede (do município, se o dono for
> um município; para o Distrito Federal, o IDHM 2010 de Brasília com o piso municipal). Rodar
> `objective_lookup.py --uf <UF> --entidade banco|empresa`. Usar a nota do estado mantenedor como se fosse da
> entidade errou o total de um banco em 1,4 ponto (com a classificação D do estado, o banco seria eliminado).

Eixos de coordenação da SEAID: Modernização Estadual | Infraestrutura | Social e
Sustentabilidade.

## FORMATO DE SAÍDA
**Sem siglas em lugar nenhum da saída — inclusive nos títulos de seção.** Escrever o nome
completo sempre: não "Nota de Área Estratégica" abreviada, mas por extenso em todo lugar; não
"Grupo Técnico" abreviado, mas por extenso; não "Banco Multilateral de Desenvolvimento"
abreviado; não "Nota Técnica" abreviada; não "carta-consulta" abreviada; não "Portal de
Financiamento Externo" abreviado. Isso vale também para cabeçalhos de tabela e números de
seção (ex.: escrever "4. Nota de Área Estratégica por área", nunca uma sigla no título).
Nomes oficiais que são o próprio termo legal de um índice ou instituição (Capacidade de
Pagamento, Índice de Desenvolvimento Humano/Municipal, COFIEX, PPA, LOA, os nomes dos credores
BIRD/BID/CAF/etc.) não são abreviação interna e podem permanecer — mas escrever por extenso
qualquer abreviação inventada ou interna em toda ocorrência, independente do idioma.

**Todo número de nota deve vir rotulado — nunca um número solto.** Em qualquer seção da saída
(sumário executivo, detalhamento por área, componentes, nota final), identificar explicitamente
se o número é a **Nota de Área Estratégica** (componente isolado, teto 10, bônus incluído) ou a
**Nota Geral** (Dados Objetivos + Área Estratégica — Índice de Desenvolvimento Humano +
Capacidade de Pagamento + Tendência da Dívida + Nota de Área Estratégica, teto 15; para ente
federal, Nota Geral = Nota de Área Estratégica, pois não há componentes de Dados Objetivos).
Mesma regra para a faixa [Mínimo — Esperado — Máximo]: dizer sempre a qual das duas ela se
refere.

**Regras de redação** (detalhe em `references/output/docx-report.md`): um só número em
destaque, a **Nota Geral esperada**, com a Nota de Área Estratégica esperada logo abaixo; todo
outro número em segundo plano, com uma frase que diz quando ele importa; nenhuma probabilidade
de aprovação em percentual; cada achado numa seção só, as demais remetem a ele.

0. **[PRIMEIRO] Resumo para o líder de equipe** (veredito em uma linha, Nota Geral esperada,
   sublimite recomendado, 3 lacunas que mais custam nota, 3 ações de maior ganho) **e
   Sumário executivo:** todo campo de cabeçalho identificado (nome da proposta,
   proponente, credor, valor total/empréstimo/contrapartida, sublimite-alvo, tipo de entidade)
   mais as notas atribuídas sob julgamento cego — identificando cada uma como Nota de Área
   Estratégica (componente) ou como item de Dados Objetivos (Nota do Índice de Desenvolvimento
   Humano, Classificação de Capacidade de Pagamento, Nota de Tendência da Dívida) — e, por fim,
   a **Nota Geral** com a faixa [Mínimo — Esperado — Máximo] rotulada como tal — em um bloco
   compacto, antes de qualquer uma das seções abaixo.
1. **Cabeçalho:** proposta, proponente, credor, valor da operação
2. **Integridade dos Insumos (FASE 1.6):** qualquer `input_flag` levantado
3. **Checagem Eliminatória (FASE 2/4):** aprovado/reprovado com detalhes
4. **Detalhamento da Nota de Área Estratégica (FASE 5):** área por área, com classificação de
   nível + faixa de bônus — todo número aqui é Nota de Área Estratégica (componente), nunca
   Nota Geral; identificar assim mesmo quando o total da área já incluir o bônus
5. **Notas dos Componentes (FASES 6–8):** Índice de Desenvolvimento Humano, Classificação de
   Capacidade de Pagamento, Tendência da Dívida com faixas de cenário — estes são itens de
   Dados Objetivos, distintos da Nota de Área Estratégica; rotular cada um como tal
6. **Nota Final (FASE 9):** a **Nota Geral esperada** em destaque e a faixa [Mínimo — Esperado
   — Máximo] em segundo plano, explicitando a soma
   Dados Objetivos + Nota de Área Estratégica (ou só Nota de Área Estratégica, se ente federal)
   — + a linha de **Base de calibração** (n, filtros relaxados, marcadores de dados fracos,
   ancoragem; ver passo 7 da RECEITA DE RECUPERAÇÃO)
7. **Simulação das Perguntas do Grupo Técnico (FASE 10):** tabela pergunta por pergunta
8. **Revisão Sênior de Banco Multilateral de Desenvolvimento (FASE 11):** classificações A.1–
   A.5 completas (teoria da mudança, marco de resultados, riscos, implementação,
   sustentabilidade financeira) + A.6 lente de Área Estratégica (tabela por área: nível
   estimado e degrau que falta) + **Lente Banco Mundial, sempre** (instrumento sugerido,
   indicadores vinculados a desembolso se couber, Padrões Ambientais e Sociais e classe de
   risco, encaixe no Quadro de Parceria, objetivo de desenvolvimento do projeto, ponte para a
   Nota Conceitual, e a subseção de empregos: canais, reconcepção, indicadores e ênfases de
   argumento para a aprovação interna no Banco) + justificativa do credor (nível e subitem que falta)
9. **Plano de Correção (FASE 12):** tabela priorizada + "Rota para Área Estratégica máxima
   (10,000)" (caminho aritmético escolhido e tarefas R1–R13 aplicáveis, com Δ estimado)
10. **[ÚLTIMO] Janela e Momento (circunstancial):** módulo de sublimite
    (`references/strategy/sublimit-targeting.md`): elegibilidade por sublimite, saldo da
    próxima reunião, posição frente à linha de corte recente (acima, perto ou abaixo, em texto,
    sem probabilidade em percentual), recomendação de sublimite, reunião e mudança de desenho,
    estratégia de iteração

**Entrega final obrigatória: relatório em .docx.** Depois da resposta no chat, gravar o
relatório completo com `scripts/build_report_docx.py` e entregar o arquivo ao usuário
(esquema e estrutura em `references/output/docx-report.md`), com a carta de comentários ao cliente
quando o usuário for devolver a carta ao mutuário. O sumário executivo do .docx traz três
tabelas separadas:
- **Tabela 1:** pontuação mínima, esperada e máxima por item, nos subtotais (Dados Objetivos;
  Nota de Área Estratégica) e na Nota Geral.
- **Tabela 2:** objetivos estratégicos do PPA indicados no pleito, com a pontuação possível em
  cada um.
- **Tabela 3:** resumo curto das sugestões de melhoria, sem detalhamento, que fica no Plano de
  Correção.

As mesmas regras valem no .docx: sem siglas e todo número rotulado.

> **ENQUADRAMENTO DA JANELA DA COFIEX — DADO CIRCUNSTANCIAL**
>
> A capacidade por reunião, o saldo do sublimite e o momento de aprovação dependem de
> variáveis dinâmicas que mudam a cada ciclo da COFIEX. Antes de julgar a viabilidade de
> momento/janela, o operador DEVE:
> 1. Consultar a ata mais recente de reunião da COFIEX (gov.br/planejamento > COFIEX > Atas).
> 2. Verificar os comunicados e resoluções da COFIEX em vigor.
> 3. Checar o Portal de Financiamento Externo quanto à posição na fila e situação dos
>    concorrentes.
>
> A tabela de sublimites (`reference-data/sublimit_status.json`) traz a data de geração e a
> última reunião da base; se houver reunião mais recente, dizer isso. Atualizar com
> `tools/build_sublimit_table.py` a cada reunião.

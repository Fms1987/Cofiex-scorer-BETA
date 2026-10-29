# Changelog (anônimo)

## V.1 BETA (2026-10-27)
Reforço do julgamento cego, encontrado e corrigido em duas rodadas de teste cego ao vivo
(pleitos reais de 2025):
- **A busca na web estava vazando desfechos de caso.** A regra dura 5 (sem autoconsulta) agora
  vincula explicitamente a ferramenta de busca na web: nunca combinar os identificadores do
  próprio pleito (nome do programa, proponente, UF, número do Portal de Financiamento
  Externo/SEI, valor da operação, setor+credor+ano) com termos do tipo "aprovados/resultado/
  pauta/reunião", de nenhuma forma — incluindo uma busca do código do Portal de Financiamento
  Externo contra pautas de reunião da COFIEX. A checagem regulatória da FASE 0 agora é
  restrita a duas consultas genéricas e sem termos do caso.
- **Nota Técnica específica do caso proibida como fonte de dado durante a pontuação cega.**
  Nova regra dura 8: nunca buscar, abrir ou ler a própria Nota Técnica deste pleito — nem como
  alternativa de Capacidade de Pagamento/dívida/Índice de Desenvolvimento Humano, nem para
  marcá-la — durante o fluxo de pontuação cega. Capacidade de Pagamento/dívida/Índice de
  Desenvolvimento Humano/Municipal devem vir apenas de uma tabela ou dataset oficial geral
  (planilha empacotada, STN/Tesouro Transparente, IBGE, IPEA); dado ausente é `input_flag`,
  nunca uma consulta à Nota Técnica. A consulta à Nota Técnica só é permitida quando o usuário
  explicitamente sai do modo cego para pedir o resultado real/histórico do caso. A pergunta de
  reenvio da FASE 9.5 vai para o usuário, nunca para uma busca.
- **Formato de saída:** adicionado um bloco de sumário executivo obrigatório no início (todo
  campo de cabeçalho identificado + toda nota atribuída sob julgamento cego, antes de qualquer
  outra seção) e uma regra de ausência de siglas que também cobre os títulos de seção (ex.:
  "Nota de Área Estratégica" por extenso, não "AE"; "Perguntas do Grupo Técnico" por extenso,
  não "GTEC"; "Banco Multilateral de Desenvolvimento" por extenso, não "MDB") — os termos
  estatutários da própria regulação (Capacidade de Pagamento, Índice de Desenvolvimento
  Humano, COFIEX, PPA, LOA, nomes de credores) são mantidos pois não são abreviação interna.
- Versionamento resetado para **V.1 BETA** para marcar a primeira versão construída e
  calibrada com o corpus RAG anonimizado (`fichas/` + `data/cases_anonymized.csv`) como fonte
  primária de recuperação.
- Todo o texto de `SKILL.md` e de `references/` traduzido para o português — vocábulos
  estrangeiros mantidos apenas quando fazem parte do contexto (nomes de credores, siglas
  técnicas de padrão internacional como SMART/DLI/ISO, termos de ferramentas como `grep`).
  Dados literais (identificadores de ficha, códigos de setor/regime, valores de coluna do CSV)
  não foram traduzidos — são vocabulário controlado lido pelo protocolo de recuperação, não
  prosa.

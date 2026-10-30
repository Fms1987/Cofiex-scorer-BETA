# Lente Banco Mundial (FASE 11, aplicada sempre)

Aplicar em toda simulação, qualquer que seja o credor declarado: o líder de equipe do Banco
Mundial também avalia pleitos que podem migrar para o BIRD. A lente **não pontua de novo**. Ela
traduz as lacunas já achadas na revisão sênior (A.1–A.5) para o vocabulário do Banco e diz em
que documento de preparação cada uma será cobrada. Instrumento e classe de risco são
**sugestões para a equipe do Banco, não decisões**.

Na saída, escrever os termos por extenso (regra "sem siglas"), com o nome em inglês entre
parênteses na primeira menção:
- Financiamento de Projeto de Investimento (Investment Project Financing);
- Programa para Resultados (Program-for-Results);
- Financiamento para Políticas de Desenvolvimento (Development Policy Financing);
- indicador vinculado a desembolso (Disbursement-Linked Indicator);
- objetivo de desenvolvimento do projeto (Project Development Objective);
- Padrão Ambiental e Social (Environmental and Social Standard);
- Quadro de Parceria com o País (Country Partnership Framework);
- Nota Conceitual do Projeto (Project Concept Note).

**Fontes do Banco mudam.** Citar sempre com versão e data. Versões usadas aqui:
- Quadro Ambiental e Social de 2016, em vigor desde outubro de 2018;
- políticas de instrumento OP 10.00 (projeto de investimento), OP 9.00 (programa para
  resultados) e OP 8.60 (políticas de desenvolvimento);
- Quadro de Parceria com o Brasil para os anos fiscais 2024–2028, discutido pela Diretoria em
  abril de 2024.

Conferir na página do Banco se houve versão nova antes de citar.

## 1. Instrumento sugerido (uma linha na saída)
| Desenho lido na carta | Instrumento coerente | Conflito a apontar |
|---|---|---|
| Obras, equipamentos e serviços definidos, com produtos e custos por componente | Financiamento de Projeto de Investimento | — |
| Programa de governo já existente, com orçamento próprio e resultados verificáveis por fonte oficial; o empréstimo financia uma parte do programa | Programa para Resultados | Carta pede esse instrumento mas não tem 3 a 5 indicadores que possam virar indicador vinculado a desembolso, ou financia obras grandes de alto risco ambiental e social, que esse instrumento exclui |
| Reforma de política, ajuste fiscal, reestruturação de dívida com medidas legais | Financiamento para Políticas de Desenvolvimento | Carta lista obras ou compras; ou não há ações prévias (leis, decretos) que o ente possa cumprir antes da aprovação |
| Mistura de obras e reforma de gestão | Financiamento de Projeto de Investimento com componente baseado em desempenho, ou dois instrumentos | Dizer qual parte iria para cada instrumento |

Credor declarado diferente do Banco: dizer só o instrumento equivalente no Banco, sem
recomendar troca de credor (essa leitura é da seção de sublimite e momento).

## 2. Indicadores vinculados a desembolso (só se o instrumento sugerido for Programa para Resultados)
Escolher de 3 a 5 indicadores **que já estão na carta**. Bons candidatos:
- têm linha de base medida;
- vêm de fonte administrativa ou oficial auditável;
- respondem a ações do ente dentro do prazo;
- têm metas anuais que permitem desembolso parcial (escalável).

Evitar indicador de impacto de longo prazo e contagem de produto sem verificação independente.

Tabela curta na saída:

| Indicador da carta | Indicador vinculado a desembolso proposto | Como verificar | Escalável? |
|---|---|---|---|

O protocolo de verificação diz:
- quem verifica: controladoria, tribunal de contas ou agente independente;
- com que dado;
- em que mês do ano.

Se a carta não tiver indicadores aproveitáveis, dizer isso. Essa é a mesma lacuna do item A.2
(ver `calibration/indicator-library.md`).

## 3. Padrões Ambientais e Sociais acionados e classe de risco provável
O Padrão 1 (avaliação e gestão de riscos) e o Padrão 10 (engajamento das partes interessadas)
valem para todo projeto. Os demais dependem do tipo de intervenção:

| Tipo de intervenção na carta | Padrões típicos além do 1 e do 10 | Classe de risco mais comum |
|---|---|---|
| Obras urbanas lineares (vias, corredores de ônibus, drenagem, canais) | 2 trabalho; 3 poluição; 4 saúde e segurança da comunidade; **5 aquisição de terra e reassentamento**; 8 patrimônio cultural se houver centro histórico | Substancial; Alto com reassentamento em grande escala |
| Barragens, adutoras, reservatórios | 2; 3; 4 com **segurança de barragens**; 5; 6 biodiversidade | Alto ou Substancial |
| Saneamento (redes, estações de tratamento, resíduos sólidos) | 2; 3; 4; 5 se houver faixa de servidão ou área de aterro | Substancial |
| Estradas rurais, pontes, logística | 2; 3; 4; 5; **6 biodiversidade**; **7 povos indígenas e comunidades tradicionais** se a área de influência os inclui | Substancial |
| Programas rurais, regularização fundiária, agricultura familiar | 2; 3 uso de agrotóxicos; 5; 6; **7** | Substancial ou Moderado |
| Unidades de saúde, escolas, equipamentos sociais em terreno público | 2; 3 resíduos de serviço de saúde; 4 | Moderado |
| Gestão fiscal, digitalização, sistemas, capacitação | 2 se houver contratação de equipe; risco social de exclusão digital e proteção de dados no Padrão 1 | Baixo ou Moderado |
| Linha de crédito por banco de desenvolvimento ou fundo | **9 intermediários financeiros** e o padrão do que for financiado na ponta | Conforme a carteira |
| Segurança pública, sistema prisional | 2; 4 uso de forças de segurança; inclusão de grupos vulneráveis no Padrão 1 | Substancial |

Saída: a lista dos padrões acionados e a classe provável, mais uma frase sobre o que a carta já
traz:
- licença ambiental;
- plano de reassentamento;
- consulta prévia.

Falta de terreno definido ou de estimativa de famílias afetadas é a lacuna que a preparação
cobra primeiro. Ela conversa com a pergunta do Grupo Técnico sobre licenciamento e com o item
A.3 (riscos).

## 4. Encaixe no Quadro de Parceria com o País
O quadro vigente (anos fiscais 2024–2028) mira uma economia **mais produtiva, mais inclusiva e
mais verde**, alinhada ao PPA 2024–2027 e ao Plano de Transformação Ecológica.

Saída numa linha:
- qual dos três eixos (produtividade, inclusão, sustentabilidade e clima) o objetivo geral da
  carta atende; ou
- "sem encaixe claro" e o motivo.

Os resultados de alto nível do quadro devem ser conferidos no documento oficial antes de
citá-los pelo nome; não inventar a redação. O encaixe no PPA já é lido na Área Estratégica;
aqui o ponto é só se o Banco teria mandato para entrar.

## 5. Objetivo de desenvolvimento do projeto e indicadores (rascunho para a Nota Conceitual)
Reescrever o objetivo geral da carta no formato do Banco: "melhorar [resultado mensurável]
para [população ou território] em [área]". Regras:
- uma frase só;
- sem lista de atividades;
- sem "contribuir para";
- resultado ao alcance do projeto, não impacto nacional.

Escolher de 3 a 5 indicadores de resultado **já presentes na carta**, um por elemento do
objetivo. Se faltar indicador para algum elemento, apontar a lacuna e a troca sugerida em
`calibration/indicator-library.md`. Os requisitos são os mesmos que a SEAID cobra:
- linha de base medida;
- ano da meta;
- fórmula.

## 6. Ponte para a Nota Conceitual do Projeto
| Seção da Nota Conceitual | Onde está na carta (Anexo I) | Lacuna típica |
|---|---|---|
| Contexto do país e do setor | I. Justificativa | Diagnóstico sem dado quantitativo do problema |
| Relevância e encaixe no quadro de parceria | II. Áreas Estratégicas, objetivo geral | Não cita o quadro (normal numa carta: só apontar) |
| Objetivo de desenvolvimento e indicadores | I. Objetivos, I. Indicadores | Ver seção 5 acima |
| Componentes e custos | I. Componentes, V. Financiamento | Custo por produto ausente (mesma lacuna da planilha de custo por área) |
| Instrumento e justificativa | V. Financiamento | Ver seção 1 |
| Arranjo de implementação | III. Gestão | Equipe e experiência não descritas (item A.4) |
| Riscos e classe de risco ambiental e social | IV. Riscos | Ver seção 3 |
| Sustentabilidade | III. Gestão | Custo de operação e manutenção não estimado (item A.5) |
| Análise econômica e financeira | ausente na carta | Sempre lacuna: anotar o tipo de análise esperada (custo-benefício ou custo-efetividade) |

## Lugar no relatório
Subseção "Lente Banco Mundial" dentro da Revisão Sênior de Banco Multilateral de
Desenvolvimento. Seu papel é dizer o que o Banco cobraria e em que documento. Ela:
- não repete a nota de cada item;
- não propõe correção com ganho em pontos (isso é do Plano de Correção);
- remete às lacunas já descritas: "ver A.4".

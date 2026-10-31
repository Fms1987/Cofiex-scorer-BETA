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
| Componentes e custos | I. Componentes, V. Financiamento | Custo por produto ausente (mesma lacuna do orçamento por área) |
| Instrumento e justificativa | V. Financiamento | Ver seção 1 |
| Arranjo de implementação | III. Gestão | Equipe e experiência não descritas (item A.4) |
| Riscos e classe de risco ambiental e social | IV. Riscos | Ver seção 3 |
| Sustentabilidade | III. Gestão | Custo de operação e manutenção não estimado (item A.5) |
| Análise econômica e financeira | ausente na carta | Sempre lacuna: anotar o tipo de análise esperada (custo-benefício ou custo-efetividade) |

## 7. Empregos: como o pleito pode incorporar e destacar a criação de empregos
**Por que esta subseção existe.** No ciclo atual de liderança, o Grupo Banco Mundial pôs a
criação de empregos como objetivo explícito de todo projeto.

O que mudou no Banco:
- **Indicador de empregos no Scorecard corporativo**, previsto para as Reuniões de Primavera de
  2026. Mede três coisas: empregos diretos do projeto, efeitos na cadeia de fornecedores e
  trabalhadores que passam a empregos mais bem pagos.
- **A pergunta interna mudou.** O líder de equipe que leva o projeto ao Diretor do País e à
  Diretoria em Washington precisa responder "quantos e quais empregos, e como sabemos", não só
  "que obra".
- **Fonte:** página "Jobs" do Grupo Banco Mundial (worldbank.org/ext/en/jobs), lida em
  30/10/2026. A metodologia do indicador ainda estava em consulta: conferir a versão vigente
  antes de citar números.

O enquadramento do Banco é o **ecossistema de empregos**, com três pilares:
1. **Construir a base:** infraestrutura (estradas, energia, digital), capital natural e capital
   humano (saúde, educação, qualificação).
2. **Ambiente favorável aos negócios:** regulação de terra, trabalho, tributos, falências e
   segurança jurídica. O Banco afirma que governos não criam empregos em escala; o papel do
   setor público é destravar o setor privado.
3. **Mobilizar capital privado:** IFC, MIGA, plataforma de garantias, crédito a micro,
   pequenas e médias empresas.

Os setores priorizados são energia e infraestrutura, saúde, agronegócio, indústria e turismo.
Os focos transversais são mulheres, jovens e micro, pequenas e médias empresas, que geram 7 de
cada 10 empregos formais nos países emergentes. A expressão-chave é "mais e melhores empregos".

Esta subseção é **de concepção**. Ela serve ao líder de equipe para defender o pleito
internamente e não altera a nota COFIEX. Pode ir da reconcepção do projeto a pautas de discussão
e ênfases de argumento.

### 7.0 Referências do Banco Mundial sobre o tema do pleito (buscar a cada simulação)
O repositório local não guarda documentos do Banco Mundial; a base aqui é COFIEX e SEAID. Por
isso, **a cada simulação, buscar na web** publicações do Banco sobre os temas do pleito, de
preferência as que cruzam o tema com emprego. Isso dá ao líder de equipe argumentos com fonte
do próprio Banco, que é o que convence o Diretor do País e a Diretoria.

**Onde buscar.** A busca direta no Repositório de Conhecimento Aberto
(openknowledge.worldbank.org) costuma bloquear acesso automatizado. Usar busca na web
restrita aos domínios do Banco:
- `site:openknowledge.worldbank.org`: relatórios, livros, documentos de trabalho, notas de
  política;
- `site:documents.worldbank.org`: documentos de projeto (documento de avaliação do projeto,
  documento de informação do programa), que mostram como operações parecidas foram
  defendidas;
- `site:worldbank.org/pt/news` e `/en/news`: comunicados de operações recentes no Brasil;
- `site:blogs.worldbank.org`: posicionamento da liderança e das práticas globais.

**Como montar as consultas.** Usar de 3 a 6 consultas por pleito, combinando setor e emprego,
setor e Brasil, e o canal de emprego identificado em 7.1. Exemplos:
- `site:openknowledge.worldbank.org jobs urban infrastructure Brazil`
- `site:openknowledge.worldbank.org "sanitation" employment OR jobs Latin America`
- `site:openknowledge.worldbank.org Brazil "Country Growth and Jobs" OR "jobs diagnostic"`
- `site:documents.worldbank.org Brazil state "Program-for-Results" jobs`
- `site:worldbank.org/pt/news Brasil empregos [setor] [ano]`

Em português e inglês, porque muita coisa sobre o Brasil sai nas duas línguas.

**O que procurar, em ordem de utilidade:**
1. Diagnóstico de empregos ou relatório de crescimento e empregos do Brasil ou da região:
   números do mercado de trabalho e a tese do Banco para o país.
2. Avaliação de impacto ou estudo setorial que mede efeito de emprego do tipo de intervenção do
   pleito: obra urbana, saneamento, estradas rurais, qualificação, saúde, regularização
   fundiária.
3. Operações recentes do Banco no Brasil com enquadramento de empregos, de preferência
   subnacionais. Exemplo encontrado em 30/10/2026: comunicado de março de 2026 sobre
   financiamento ao Estado da Bahia que liga infraestrutura e reformas à criação de empregos.
   Servem como precedente de como a Diretoria aprovou um argumento parecido.
4. Notas de política sobre ambiente de negócios, regulação e emprego (ver 7.5).

**Como usar na saída.** Uma tabela curta, com 3 a 6 linhas no máximo:

| Referência (título, ano, tipo) | O que diz de útil para este pleito | Onde usar (7.2 reconcepção, 7.3 indicador, 7.4 argumento) |
|---|---|---|

Regras:
- Citar só o que foi aberto e lido. Título, ano e link têm de ser reais. Não inventar
  referência nem número; se a busca não achar nada útil, dizer isso.
- Preferir documentos dos últimos 5 anos e do Brasil ou da América Latina. Estudo de outra
  região vale como evidência do mecanismo, dito como tal.
- Resumir com palavras próprias. No máximo uma citação curta entre aspas por referência
  (direitos autorais).
- **Julgamento cego:** a busca é por literatura do Banco sobre o tema, nunca por documentos do
  próprio pleito avaliado. Não buscar nota técnica, ata ou resultado COFIEX do pleito, nem
  documento de projeto do Banco com o mesmo nome do pleito. Se um resultado for claramente a
  operação avaliada, descartar.
- A busca alimenta a lente e não muda nenhuma nota.

### 7.1 Diagnóstico: por qual canal o projeto gera emprego
Ler a carta e marcar os canais presentes, com o grau de evidência (explícito, implícito ou
ausente):

| Canal | Pergunta para a carta | Sinal forte | Sinal fraco |
|---|---|---|---|
| Emprego direto na execução | Quantos postos na obra ou na implantação, e por quanto tempo? | Estimativa em pessoas-mês por componente | "Gerará empregos" sem número |
| Emprego direto permanente | Que postos ficam depois do projeto (operação, manutenção, serviço)? | Quadro de pessoal da operação com custeio (liga ao item A.5) | Só obra, nenhum posto permanente |
| Cadeia de fornecedores | O gasto fica na economia local? | Compras de micro e pequenas empresas, insumos regionais | Contratos grandes com fornecedor de fora |
| Efeito habilitador | O projeto destrava emprego privado (acesso, energia, conectividade, licença, crédito)? | Linha direta até o emprego: quem contrata e por quê | Benefício difuso "para a economia" |
| Qualidade do emprego | Formaliza, aumenta renda, inclui mulheres e jovens, reduz desigualdade regional? | Meta de formalização ou de renda com fonte administrativa | Nenhuma menção |

O Banco chama de "linha de visão até o emprego" (line of sight to employment) a cadeia causal
explícita entre o produto financiado e o emprego. **A ausência dessa cadeia é a lacuna
central.** Ela é a mesma lacuna da teoria da mudança (A.1), vista pelo ângulo do emprego.

### 7.2 Reconcepção: opções por tipo de projeto
Propor de 2 a 4 opções que caibam no desenho e no valor do pleito, sem trocar o objeto
principal. Exemplos de nível de concepção:

| Tipo de projeto | Reconcepção que coloca o emprego no centro |
|---|---|
| Obras urbanas, drenagem, mobilidade | Cláusulas de contratação local e de qualificação dos trabalhadores da obra, com metas para mulheres e jovens; manutenção contínua por contratos de desempenho com micro e pequenas empresas; requalificação de áreas para atividade econômica (comércio, feiras, logística de última milha); emprego permanente medido, não só o da obra |
| Água, saneamento, resíduos | Desenho regulatório que atraia operador privado (concessão ou parceria público-privada), o que liga o projeto ao pilar de capital privado; cooperativas de catadores formalizadas na cadeia de resíduos; redução de perdas como fonte de receita que sustenta postos na operação |
| Educação e qualificação profissional | Oferta ligada à demanda: cursos desenhados com empregadores do território, estágio e colocação; medir colocação e renda dos egressos, não matrículas; transição escola-trabalho dos jovens que não estudam nem trabalham |
| Saúde | Enquadrar no programa do Banco para o setor (Health Works): o Banco cita que cada emprego na saúde pode gerar até 3,5 outros; agentes comunitários, atenção primária, cadeia de insumos; formação e fixação de profissionais em regiões carentes |
| Desenvolvimento rural e agricultura familiar | Inserção em cadeias de valor e mercados (compras públicas, cooperativas, agroindústria), alinhada ao programa do Banco para pequenos produtores (AgriConnect); assistência técnica com meta de renda; crédito e seguro rural |
| Gestão fiscal, governo digital, ambiente de negócios | Reenquadrar como pilar 2: tempo para abrir empresa e obter licença, simplificação tributária para micro e pequenas empresas, compras públicas acessíveis a pequenos fornecedores, segurança jurídica; medir empresas abertas e formalizadas, não sistemas entregues |
| Energia, conectividade, logística | Acesso que destrava produção (polos, distritos industriais, turismo, agroindústria); identificar os setores que passam a contratar |
| Turismo e patrimônio | Cadeia do turismo (hospedagem, alimentação, guias, artesanato) com qualificação e formalização; o Banco atribui ao turismo cerca de 1 em cada 10 empregos no mundo |
| Linha de crédito por banco de desenvolvimento | Foco em micro, pequenas e médias empresas e em empreendedoras; medir empregos mantidos e criados nas empresas financiadas |

Uma reconcepção maior também é possível, como separar um componente de emprego, combinar com
uma operação da IFC ou usar a plataforma de garantias. Nesse caso, dizer o que muda no valor,
no prazo e no instrumento (seção 1) e se o pleito COFIEX precisaria ser reapresentado.

### 7.3 Como medir (o que o Banco vai perguntar)
Indicadores sugeridos, a reconciliar com a metodologia vigente do Scorecard:

| Dimensão | Indicador | Fonte no Brasil |
|---|---|---|
| Emprego direto na execução | Pessoas-mês contratadas por componente, por sexo e faixa etária | Relatórios das contratadas, eSocial |
| Emprego direto permanente | Postos de operação e manutenção ocupados no ano após a conclusão | Folha do operador, eSocial |
| Cadeia de fornecedores | Empregos estimados na cadeia (matriz insumo-produto) e participação de micro e pequenas empresas nas compras | Tabelas de recursos e usos do IBGE, sistema de compras |
| Melhores empregos | Variação de renda e de formalização dos beneficiários (trabalhadores qualificados, produtores, empresas apoiadas) | Novo CAGED, RAIS, PNAD Contínua, Cadastro Único |
| Inclusão | Participação de mulheres e de jovens de 15 a 29 anos nos postos criados | Mesmas fontes |

Cuidados:
- Separar emprego temporário de obra e emprego permanente; o temporário não é o resultado
  principal.
- Não contar duas vezes o direto e o da cadeia.
- Não apresentar emprego público novo como resultado de emprego.
- Declarar o contrafactual: o que aconteceria sem o projeto.
- Números inflados prejudicam a credibilidade na Diretoria mais do que números modestos e
  verificáveis.

### 7.4 Ênfases de argumento e pautas de discussão
Para o Diretor do País e para a Diretoria, escolher de 3 a 5 ênfases que a carta sustente:
- **Mandato.** O projeto contribui para o objetivo institucional de mais e melhores empregos e
  para o indicador de empregos do Scorecard. Dizer por qual canal (7.1) e com que ordem de
  grandeza.
- **Encaixe no país.** Empregos ligam o projeto aos eixos de produtividade e inclusão do Quadro
  de Parceria com o Brasil (seção 4). Informalidade, desemprego de jovens e desigualdade
  regional são os problemas do mercado de trabalho brasileiro a citar, com dados da PNAD
  Contínua e o recorte do território.
- **Setor privado como motor.** Mostrar o que o projeto destrava para empresas privadas e se há
  espaço para IFC, MIGA ou garantias. A tese "governos não criam empregos em escala" pede que o
  argumento não dependa de contratação pública.
- **Qualidade e inclusão.** Formalização, renda, mulheres e jovens, com metas e fontes
  administrativas.
- **Sustentação depois do projeto.** Os postos permanentes têm custeio (item A.5), e o emprego
  não acaba com a obra.
- **Evidência.** Avaliação de impacto ou monitoramento com dados administrativos (CAGED, RAIS,
  eSocial). Isso responde à pergunta "como sabemos" e é um ponto forte na Diretoria.

Pautas de discussão com o cliente:
- "Quem contrata, quantos e onde, por causa deste projeto?"
- "Que parte das compras pode ir a fornecedores locais e a micro e pequenas empresas?"
- "O que muda na regulação para que empresas invistam no território?"
- "Que dados de emprego o ente já tem e pode compartilhar?"

### 7.5 Regras do jogo: o componente que multiplica o investimento
A liderança do Grupo Banco Mundial tratou o tema em artigo de 14/04/2026: "To turn demographic
growth into jobs, get the rules right", do presidente do Grupo Banco Mundial e da presidente do
Comitê de Desenvolvimento. Fonte: blogs.worldbank.org, seção Voices.

A tese do artigo:
- **Multiplicador.** O ambiente favorável aos negócios é o que transforma infraestrutura,
  qualificação e capital privado em empregos. "Investment follows predictability."
- **Investimento privado.** A incerteza regulatória é tratada como um fator que inviabiliza o
  investimento.
- **Recursos públicos.** Como são escassos, devem servir para reduzir risco e atrair capital
  privado.
- **Medida de sucesso.** O sucesso se mede por empregos criados, não por compromissos
  assinados.

O artigo é texto de posicionamento institucional: usar como enquadramento, não como evidência.

**Por que isso importa para um pleito subnacional.** Boa parte das regras que o artigo cita é
administrada por estado ou município, então o ente tem alavancas próprias. Tabela de apoio
(listar só as que o ente controla e que caibam no projeto):

| Regra citada pelo Banco | Alavanca do ente subnacional no Brasil | Indicador possível |
|---|---|---|
| Licenças emitidas no prazo | Alvará de funcionamento e licença de obra municipais; licenciamento ambiental estadual; dispensa para atividades de baixo risco (Lei de Liberdade Econômica) | Tempo médio para emitir licença; % de atividades com licença automática |
| Registro simples para microempresas | Integração do município e da junta comercial à rede nacional de registro de empresas; balcão único | Tempo para abrir empresa; empresas formalizadas por ano |
| Tributação compreensível e previsível | ISS e ICMS: simplificação, nota fiscal eletrônica de serviço, contencioso administrativo mais rápido | Prazo de julgamento administrativo; custo de conformidade |
| Direitos claros sobre a terra | Regularização fundiária urbana e rural, cadastro territorial multifinalitário, georreferenciamento | Imóveis com título registrado; área cadastrada |
| Compras públicas transparentes | Portal de compras com acesso de micro e pequenas empresas, pagamento em dia a fornecedores | % das compras com micro e pequenas empresas; prazo médio de pagamento |
| Contratos cumpridos | Procuradoria e câmaras de mediação para contratos com o ente; estabilidade de concessões e parcerias público-privadas | Prazo de resolução de disputas contratuais |
| Barreiras à participação econômica das mulheres | Creches e transporte em horários de trabalho; crédito e compras para empreendedoras | Participação de mulheres nos postos e nas empresas apoiadas |

Os diagnósticos de referência do Banco são **Business Ready**, que sucede o Doing Business, e
**Women, Business and the Law**. Ambos medem o país, não o ente. Citar como moldura e propor a
medição local com os indicadores acima.

**Uso na reconcepção (complementa 7.2).** Num projeto de obra ou de serviço, sugerir um
componente pequeno de "regras do jogo" no território do projeto, por exemplo licença rápida
para os negócios da área requalificada ou regularização fundiária junto com a urbanização. Esse
componente:
- custa pouco;
- dá ao projeto a linha de visão até o emprego privado;
- é o que mais se aproxima do discurso da liderança.

Se o projeto já é de gestão fiscal ou governo digital, deslocar o objetivo de "sistemas
implantados" para "regras mais previsíveis e rápidas para quem investe e contrata". Os
indicadores que entram como resultado são tempo de licença, tempo de abertura de empresa e
prazo de pagamento a fornecedores.

**Ênfase para a Diretoria (complementa 7.4).** "O investimento público reduz o risco e a regra
local destrava o investimento privado; medimos o resultado em empregos, não em obras
entregues." Usar só se o projeto tiver de fato uma alavanca regulatória com indicador. Sem
ela, a frase soa como retórica e enfraquece o argumento.

Pauta de discussão com o cliente: "Que licença, cadastro ou procedimento do ente mais atrasa
quem quer investir ou contratar neste território, e quanto tempo leva hoje?"

### 7.6 Relação com a nota COFIEX
O emprego não é critério da rubrica da RN 1/2024. A reconcepção só mexe na nota se criar
**produto, indicador e custo próprios** em uma área do PPA, por exemplo:
- objetivos de trabalho e renda;
- ambiente de negócios e micro e pequenas empresas;
- qualificação.

Aplicar a regra das áreas secundárias (`calibration/ae-criteria-by-level-and-ppa-area.md` §4).
Declarar uma área nova sem esse lastro tende a zero e não deve ser sugerido só para destacar
emprego. Na carta COFIEX, o emprego entra como resultado na justificativa e nos indicadores.
Ênfases voltadas ao Banco ficam fora da carta de comentários ao cliente, salvo pedido do
usuário.

### Saída no relatório
Subseção "Empregos" dentro da lente Banco Mundial, com seis partes:
- as referências do Banco Mundial encontradas sobre o tema e emprego (7.0);
- a tabela de canais (7.1) com o grau de evidência;
- de 2 a 4 opções de reconcepção (7.2);
- de 3 a 5 indicadores (7.3);
- de 3 a 5 ênfases de argumento e pautas (7.4);
- as alavancas de regras do jogo que o ente controla, quando houver (7.5).

Tudo em texto de concepção, sem número de nota e sem estimar quantidade de empregos que a
carta não sustente: quando a carta não traz número, dizer que falta e como obtê-lo.

## Lugar no relatório
Subseção "Lente Banco Mundial" dentro da Revisão Sênior de Banco Multilateral de
Desenvolvimento. Seu papel é dizer o que o Banco cobraria e em que documento. Ela:
- não repete a nota de cada item;
- não propõe correção com ganho em pontos (isso é do Plano de Correção);
- remete às lacunas já descritas: "ver A.4".

A subseção de empregos (seção 7) é a exceção que propõe mudanças. Ela é de concepção, voltada
à aprovação interna no Banco, e não estima ganho de nota.

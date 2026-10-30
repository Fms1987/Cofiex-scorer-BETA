# Fontes de dados oficiais para conferência cruzada de Capacidade de Pagamento, dívida e Índice de Desenvolvimento Humano/Municipal

<!-- adicionado por instrução do usuário: apenas APIs gratuitas/oficiais, nenhum serviço pago -->

A FASE 1.6 exige data e fonte de consulta para todo valor de Capacidade de Pagamento, Índice
de Desenvolvimento Humano/Municipal e capacidade de endividamento. Usar estas fontes
gratuitas e oficiais para obtê-los ou confirmá-los — nunca um fornecedor pago de dados. Se um
valor não puder ser confirmado contra uma destas, levantar `input_flag` em vez de confiar no
número do proponente.

## Planilha empacotada (verificar primeiro)

`reference-data/External_Credit_Operations_Database_September_2026.xlsx` vem junto com este
repositório — consultá-la **antes** de recorrer a uma API externa. É mais rápida e já está
reconciliada (resoluções do Senado, STN/SADIPEM, Banco Mundial, IBGE, COFIEX/MPO). Se o
usuário fornecer depois uma versão mais nova localmente, preferir essa e dizer isso.

| Necessidade | Planilha | Colunas |
|---|---|---|
| Classificação de Capacidade de Pagamento municipal (metodologia oficial da STN) | `CAPAG_Municipalities` | `IBGE_Code`, `Municipality_Name`, `Rating_1` (indicador dívida/receita) — esta é a classificação de Capacidade de Pagamento autoritativa, não a coluna `Fiscal Rating` em `Borrowers_Municipalities` (uma nota proprietária mais ampla que pode divergir em um nível) |
| Classificação fiscal estadual (equivalente à Capacidade de Pagamento) + Índice de Desenvolvimento Humano | `Borrowers_States` | `Fiscal Rating (2026)`, `HDI (2021)` |
| Índice de Desenvolvimento Humano Municipal | `Borrowers_Municipalities` | `HDI (2010)` |
| Capacidade de endividamento/espaço fiscal estadual | `Borrowing_Capacity_States` | `Available_Fiscal_Space_BRL`/`_USD`, `Available Fiscal Space (%)` |
| Operações COFIEX anteriores/irmãs (conferência cruzada multi-tranche, pergunta 26; checagem de credor duplo) | `Operations_COFIEX` | `Request_ID`, `Process_No`, `Project_Name`, `Borrower`, `Phase`, `Bank`, `Loan_USD`, `Counterpart_USD`, datas de aprovação/negociação — **ver alerta abaixo** |
| Carteira de bancos multilaterais de desenvolvimento por banco/ano (checagem de sanidade do porte típico de um credor) | `Banks`, `Loans_Master` | milhões de dólares anuais e contagem de operações por banco |

> **ALERTA — `Operations_COFIEX` contém desfechos.** A planilha traz fase e datas de aprovação
> e negociação de pleitos reais, possivelmente incluindo o próprio pleito avaliado ou uma
> versão anterior dele. Usar só para localizar operações **de outros** pleitos (tranches-irmãs,
> credor duplo, pergunta 26 do Grupo Técnico). Nunca procurar nela o proponente, o projeto ou
> o processo do pleito avaliado, nem usar fase ou data de aprovação para inferir ou ajustar a
> nota ou a probabilidade de aprovação (princípio de julgamento cego). Se a busca por uma
> operação-irmã trouxer por acaso a linha do próprio pleito, ignorar a fase e as datas e
> registrar o fato na FASE 1.6.

Ainda assim, registrar a data de consulta (a própria planilha `Metadata` do arquivo informa sua
data de última atualização) e citar a planilha/coluna como fonte, conforme a FASE 1.6.
Conferir cruzadamente contra as fontes externas abaixo quando a planilha estiver desatualizada
em relação à data da reunião-alvo, ou ausente.

| Necessidade | Fonte | Acesso |
|---|---|---|
| Classificação de Capacidade de Pagamento (estados, DF, municípios) | STN — Secretaria do Tesouro Nacional, *Boletim de Capacidade de Pagamento* | Datasets via [Tesouro Transparente CKAN](https://www.tesourotransparente.gov.br/ckan/dataset) (buscar "capacidade de pagamento" / "CAPAG") |
| Dívida subnacional / indicadores fiscais (Dívida Consolidada/Receita Corrente Líquida, tendência da dívida, dados de RGF/RREO) | STN, mesmo portal | [Tesouro Transparente CKAN](https://www.tesourotransparente.gov.br/ckan/dataset) |
| Índice de Desenvolvimento Humano/Municipal | Atlas do Desenvolvimento Humano (PNUD/IPEA/FJP), espelhado em | [`ipeadatar`](https://cran.r-project.org/web/packages/ipeadatar/index.html) do IPEA (R) ou [`ipeadatapy`](https://pypi.org/project/ipeadatapy/) (Python); conferir cruzadamente os códigos municipais via [API do IBGE](https://servicodados.ibge.gov.br/api/docs/) |
| Identificadores de município/UF, população, outras séries do IBGE | IBGE | [Serviço de Dados IBGE](https://servicodados.ibge.gov.br/api/docs/) · [metadados estatísticos (gov.br/conecta)](https://www.gov.br/conecta/catalogo/apis/metadados-estatisticos-do-ibge) |
| Indicadores de água/saneamento/segurança hídrica (conferência cruzada do setor rural/ambiental) | SNIRH | [catálogo geonetwork do SNIRH](https://metadados.snirh.gov.br/geonetwork/srv/por/catalog.search#/home) |
| Versões em lote/tratadas do que está acima (junções mais rápidas, séries históricas) | Base dos Dados | [basedosdados.org](https://basedosdados.org/) |

Notas:
- Estas fontes cobrem Capacidade de Pagamento, dívida e Índice de Desenvolvimento
  Humano/Municipal. Não substituem os valores declarados pelo próprio proponente para a
  operação em si (valor da operação, contrapartida, indicadores) — esses continuam vindo do
  texto da carta-consulta.
- Registrar a data de consulta e o dataset/endpoint exato usado, conforme a exigência de
  metadado da FASE 1.6.
- `ipeadatar`/`ipeadatapy` espelham as séries do IPEA (incluindo o Índice de Desenvolvimento
  Humano Municipal); em caso de dúvida, checar o valor contra o código municipal da API do
  IBGE para pegar divergências de UF/código (a mesma conferência cruzada que a FASE 1.6 já
  exige).

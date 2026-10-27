# data/cases_anonymized.csv

Uma linha por **avaliação** (um pleito em uma reunião), reuniões 165–185. Regerado por
`tools/build_cases_from_fichas.py` a partir de `fichas/`.
Identificadores opacos: `case_id` = identificador da ficha de avaliação, `pleito_id` =
identificador da ficha de pleito (mesmos identificadores dos arquivos em `fichas/`).

<!-- Nomes de coluna e valores de vocabulário controlado abaixo não são traduzidos: são
     identificadores de esquema/código lidos pelas ferramentas de construção e pelo protocolo
     de recuperação do SKILL.md. -->

| Coluna | Significado |
|---|---|
| regime, year, quarter, attempt, attempts_total | Res. 17/2021 (`R17_2021`) ou Res. Normativa 1/2024 (`NR1_2024`); ano e trimestre da reunião; número da tentativa do pleito |
| subtype, ticket_band | Federal / Subnational–General / PPP / Fiscal / …; faixa de valor do empréstimo em USD (`<50M … >400M`). `BRL-nominal` = a coluna de valor estava em reais, não convertida |
| lender, lender_check | Credor, **verificado contra o texto da carta-consulta** (`match` = confere, `mismatch` → valor tomado da carta-consulta, `undetermined` = indeterminado) |
| counterpart_pct, counterpart_check | Participação da contrapartida, verificada contra a carta-consulta quando ela imprime os dois valores |
| sector, sector_source, sector_secondary | `verified` = lido a partir de indicadores/componentes (narrativas preenchidas); `keyword_heuristic` caso contrário (menos confiável) |
| outcome, reason_cat | approved (aprovado) / not_approved (não aprovado) / withdrawn (retirado); motivo normalizado de não aprovação |
| ae, idh_pts, capag_pts, debt_pts, total | Notas da planilha de resultados (componentes apenas para NR1_2024; linhas da R17 trazem o total) |
| total_published | Nota impressa no resultado oficial da reunião quando a planilha está em branco |
| nt_available, nt_match, nt_docs | Disponibilidade da Nota Técnica, como foi vinculada (`same_meeting` = mesma reunião, `no_meeting_folder` = sem pasta de reunião, `single_attempt_fallback` = alternativa de tentativa única, `none` = nenhuma) e número de documentos de Nota Técnica distintos |
| n_indicators, n_indicators_parse, baseline_defined_share, baseline_with_year_share | Contagem de indicadores (`verified` = verificada pela etapa de narrativa, senão heurística) e participações de linha de base (regra v3: um valor declarado conta; um zero não explicado não conta) |
| mentions_* | Marcadores 0/1 de palavra-chave a partir do texto da carta-consulta |
| tags | Marcadores de vocabulário controlado (extras vivem na ficha de pleito como `tags_extra`) |
| narrative | `filled` (preenchida), `pending` (pendente) ou `no_cc_text` (sem texto de carta-consulta) |

Removido de propósito: proponente, título do projeto, números de Portal de Financiamento
Externo/SEI/carta-consulta, número da reunião, data exata, estado/município.
Lacunas conhecidas: 43 avaliações não têm texto de carta-consulta; 13 avaliações da NR1 com
nota em branco na planilha não tinham nota impressa para recuperar.

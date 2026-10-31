# cofiex-scorer

Habilidade do Claude que simula a avaliação técnica da COFIEX para uma *carta-consulta*,
cobrindo tanto a Res. Normativa 1/2024 (conforme alterada) quanto o regime anterior da Res.
Cofiex 17/2021.

`skills/cofiex-scorer/` é a pasta autossuficiente da habilidade: tudo que ela precisa em
tempo de execução (SKILL.md, referências e o corpus RAG) vive junto, do mesmo jeito que uma
instalação local em `~/.claude/skills/cofiex-scorer/` ou um conector de GitHub por skill
esperam encontrar.

- `skills/cofiex-scorer/SKILL.md` — fluxo de trabalho, regras duras, protocolo de recuperação
- `skills/cofiex-scorer/references/` — rubrica, calibração, perguntas do Grupo Técnico,
  cartões de caso anonimizados
- `skills/cofiex-scorer/fichas/` — registro estruturado + narrativo por pleito e avaliação (o
  corpus RAG, consultado por grep de cabeçalho); 390 avaliações nos dois regimes
- `skills/cofiex-scorer/data/` — tabela de casos anonimizados (`cases_anonymized.csv`)
- `skills/cofiex-scorer/docs/` — esquema de análise de área estratégica e registro por
  avaliação (referência para humanos)
- `skills/cofiex-scorer/reference-data/External_Credit_Operations_Database_September_2026.xlsx`
  — dataset compilado de dívida externa/COFIEX (resoluções do Senado, STN/SADIPEM, Banco
  Mundial, IBGE, COFIEX/MPO): classificações de Capacidade de Pagamento, Índice de
  Desenvolvimento Humano/Municipal, capacidade de endividamento, histórico de empréstimos.
  Dado fiscal oficial agregado, não conteúdo de carta-consulta — usado pela FASE 1.6 como a
  conferência cruzada primária de Capacidade de Pagamento/Índice de Desenvolvimento
  Humano/dívida (ver `skills/cofiex-scorer/references/rubric/official-data-sources.md`).
- `tools/` — pipeline de reconstrução, na raiz do repositório (precisa de arquivos-fonte
  locais, não publicados: textos brutos de carta-consulta/Nota Técnica, a planilha de
  resultados). Os scripts recebem a raiz como argumento de linha de comando — passe
  `skills/cofiex-scorer` (não a raiz do repositório) para que leiam/gravem no lugar certo
  depois da reorganização abaixo.

Os textos brutos de carta-consulta/Nota Técnica e os resultados de reunião da COFIEX ficam em
um acervo privado separado (`Cofiex-scorer-archive`), fora deste repositório, para que o
próprio corpus de recuperação da habilidade (`fichas/`) permaneça anonimizado — essa separação
é o que impede a habilidade de citar ou autoconsultar um caso real, não uma regra genérica de
privacidade sobre todo arquivo.

**Nota de reorganização (V.1 BETA):** `fichas/`, `data/`, `docs/` e `reference-data/` foram
movidos da raiz do repositório para dentro de `skills/cofiex-scorer/` para que a pasta da
habilidade fique autossuficiente — necessário para um conector de skill por GitHub (ou uma
instalação local) que lê `SKILL.md` e espera o corpus RAG como irmão dele, não um nível acima.

Documentos-fonte (PDFs/Notas Técnicas/planilhas) **não** estão neste repositório por
desenho.
Pipeline de reconstrução (apenas com arquivos-fonte locais, executar nesta ordem; os scripts de montagem do corpus estão em `tools/arquivo-corpus/`, fora do fluxo de regressão e do teste cego):
`build_fichas.py` (esqueleto + vínculo com Nota Técnica) → preenchimento narrativo →
`clean_fichas.py` (credor/contrapartida/marcadores) → `audit_nt_scores.py` (Nota Técnica
versus planilha) → `build_cases_from_fichas.py` (CSV + cartões de setor) →
`build_areas_stats.py` + `build_areas_doc.py` (referência de área estratégica) →
`validate_fichas.py` + `validate_anonymity.py` antes de publicar qualquer coisa.

## Anonimidade: o que protege e o que não protege
As fichas não trazem nomes, locais, números de processo, datas, valores ou quantidades de
ativos. A combinação dos campos de cabeçalho (subtipo, credor, setor, faixa de valor,
ano-trimestre) ainda pode identificar um pleito para quem conhece a carteira. A proteção é a
regra de saída da habilidade (SKILL.md, regras duras): ela nunca cita ou descreve um caso
individual. Mantenha o repositório privado.

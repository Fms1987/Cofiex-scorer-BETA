# cofiex-scorer

Claude skill that simulates the COFIEX technical evaluation of a *carta-consulta*, covering both
Res. Normativa 1/2024 (as amended) and the prior Res. Cofiex 17/2021 regime.

- `skills/cofiex-scorer/SKILL.md` — workflow, hard rules, retrieval protocol
- `skills/cofiex-scorer/references/` — rubric, calibration, GTEC, anonymized case cards (RAG corpus)
- `fichas/` — structured + narrative record per pleito and avaliação (the RAG corpus, queried by header grep); 390 avaliações across both regimes
- `data/` — anonymized case table (`cases_anonymized.csv`)
- `docs/` — strategic-area analysis scheme and per-avaliação registry (reference for humans)
- `tools/` — rebuild pipeline (needs local, non-published source files: raw CC/NT texts, the results workbook)

Source documents (PDFs/NTs/workbooks) are **not** in this repository by design.
Rebuild pipeline (local source files only, run in this order): `build_fichas.py` (skeleton +
NT linking) → narrative fill-in → `clean_fichas.py` (lender/counterpart/tags) →
`audit_nt_scores.py` (NT vs. workbook) → `build_cases_from_fichas.py` (CSV + sector cards) →
`build_areas_stats.py` + `build_areas_doc.py` (strategic-area reference) → `validate_fichas.py`
+ `validate_anonymity.py` before publishing anything.

## Anonymity: what it does and does not protect
Fichas carry no names, places, process numbers, dates, amounts or asset counts. The combination of header fields (subtype, lender, sector,
ticket band, year-quarter) can still identify a pleito to someone who knows the portfolio. The protection is the skill's output rule
(SKILL.md, hard rules): it never cites or describes an individual case. Keep the repository private.

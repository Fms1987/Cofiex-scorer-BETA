# Changelog (anonymous)

## 17.0.0
- Architecture: monolithic SKILL.md (49 KB) → lean SKILL.md (~12 KB) + `references/` loaded on demand (RAG by progressive disclosure). V16 rules and tables moved verbatim.
- Added anonymized case cards per sector and `data/cases_anonymized.csv` (n=390 submissions, meetings 165–185 + later PFEs).
- Added `tools/` pipeline (CC text + scoring workbook → cards) and an anonymity validator.
- No scoring parameter changed relative to V16.1.

## 17.0.1 (draft)
- Fichas: structured header + anonymized narrative for 173 pleitos/avaliações (all of NR 1/2024, plus a pilot of R17); header clean-up: lender and
  counterpart verified against the CC text (8 lender and 5 counterpart mismatches in the workbook), tags normalized to a controlled vocabulary,
  `nt_docs` recomputed after de-duplicating NT copies, ticket band `BRL-nominal` for operations whose amount column held reais.
- Cases CSV and sector cards regenerated from the fichas (verified sector where a narrative exists).
- `docs/analise-areas-estrategicas.md`: scheme of the strategic-area analysis for Res. 17/2021 and Res. 1/2024, per-avaliação area scores,
  non-accepted areas and additional points, and a workbook reconciliation.
- Sources: NTs converted to Markdown (776/776); repeated page headers/footers removed before agent reading.

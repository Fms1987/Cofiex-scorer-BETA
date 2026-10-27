# Changelog (anonymous)

## V.1 BETA (2026-10-27)
Blind-judgment hardening, found and fixed via two live blind-test runs (real 2025 pleitos):
- **Web search was leaking case outcomes.** Hard rule 5 (no self-lookup) now explicitly binds
  the web tool: never combine this pleito's own identifiers (program name, proponent, UF,
  PFE/SEI number, ticket, sector+lender+year) with "aprovados/resultado/pauta/reunião"-type
  terms, in any form — including a PFE-code search against COFIEX meeting agendas. PHASE 0's
  regulatory check is now restricted to two generic, case-free queries.
- **Case-specific Nota Técnica (NT) banned as a data source during blind scoring.** New hard
  rule 8: never search for, open, or read this pleito's own NT — not even as a CAPAG/debt/IDH
  fallback, not even to flag it — during the blind-scoring flow. CAPAG/debt/IDH(M) must come
  from a general official table or dataset only (bundled workbook, STN/Tesouro Transparente,
  IBGE, IPEA); missing data is `input_flag`, never an NT lookup. NT lookup is allowed only when
  the user explicitly steps outside blind mode to ask for the case's real/historical result.
  PHASE 9.5's resubmission question goes to the user, never to a search.
- **Output format:** added a mandatory first executive-summary block (every identified header
  field + every score assigned under blind judgment, before any other section) and a
  no-abbreviations rule covering section titles too (e.g. "Strategic-Area Score", not "AE";
  "Technical-Group Questions", not "GTEC"; "Multilateral Development Bank", not "MDB") — the
  regulation's own statutory terms (CAPAG, IDH, COFIEX, PPA, LOA, lender names) are kept as they
  are not internal shorthand.
- Versioning reset to **V.1 BETA** to mark the first version built and calibrated with the
  anonymized RAG corpus (`fichas/` + `data/cases_anonymized.csv`) as its primary retrieval
  source, rather than a numbered continuation of the pre-RAG V16 line.

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

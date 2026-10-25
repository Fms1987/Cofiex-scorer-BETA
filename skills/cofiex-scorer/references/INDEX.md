# references/ — retrieval index

Load only what the current phase needs (see RETRIEVAL PROTOCOL in `../SKILL.md`).

| Folder | Content | Used in |
|---|---|---|
| `regulation/` | Annex I screening, Art. 28 eliminatory checks | Phases 3–4 |
| `rubric/` | AE rubric + bonuses, IDH, CAPAG, Debt, final-score formula, official data sources for CAPAG/debt/IDH cross-checks | Phases 1.6, 5–9 |
| `calibration/` | Cross-cutting findings, AE ranges by sector, **area base rates** (`areas-stats.md`), **case cards** (`cases/`) | Phases 5, 9 |
| `iteration/` | Persistence / resubmission analysis | Phase 9.5 |
| `gtec/` | Calibrated GTEC questions | Phase 10 |
| `review/` | Senior MDB review, correction plan | Phases 11–12 |

Outside `references/`:
- `fichas/pleitos/`, `fichas/avaliacoes/` — structured header (grep-able) + anonymized narrative per pleito / avaliação (patterns, never cases).
- `data/cases_anonymized.csv` — one row per avaliação (schema in `data/README.md`).
- `docs/analise-areas-estrategicas.md` — human reference: scheme of the strategic-area analysis (section 1), per-avaliação area record (section 2, do not load), workbook reconciliation (section 3).

Case cards: `calibration/cases/INDEX.md` lists sectors with n, approval counts, AE/total medians and how many narratives are filled.
Rows are anonymized (opaque ids). **Ids are never to be quoted in an evaluation** (SKILL.md, hard rules).

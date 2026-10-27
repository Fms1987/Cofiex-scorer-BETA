---
name: cofiex-scorer
description: Simulates COFIEX technical evaluation of a carta-consulta under Res. Normativa 1/2024 (amended by Res. 32/2025, 142/2026, 150/2026, 151/2026). Outputs score range (Annex II rubric), eliminatory check (Art. 28), sublimit viability gate, senior MDB review, GTEC questions, iteration/persistence analysis, and correction plan. Retrieval-based (RAG): loads rubric, calibration and anonymized case cards from references/ on demand.
metadata:
  version: '17.0'
  language: en
  author: Fabricio Martins
  updated: '2026-10-23'
---

## BLIND-JUDGMENT PRINCIPLE (MANDATORY — READ BEFORE ANY UPDATE)
This skill is a **blind evaluator**. It must score any incoming carta-consulta on its
intrinsic merits and on the regulatory/empirical calibration encoded here — **never** by
recognizing or matching a specific real project, proponent, CC number, or meeting outcome.

**Calibration is preserved as anonymized empirical anchors only:** numeric ranges,
score thresholds, modality discounts, bonus criteria, and profile-based references
(e.g. "investment op, 4 strategic areas, profile B → AE ~6,5"). Identifying metadata
(proponent name, municipality/state, CC/PFE number, meeting number tied to a named case)
is deliberately stripped so the evaluator cannot reverse-engineer a known verdict.

**MAINTENANCE RULE (applies to every future version):**
1. New empirical findings must be folded in as **anonymized anchors** (profile + numbers),
   never as named cases or "this project was approved" precedents.
2. When a new blind test or corpus session is added, strip the identity before storing
   the calibration value it imparts. Keep the *what it teaches*, drop the *who it was*.
3. Do not reintroduce named-precedent tables, per-meeting CC rosters, or session-by-session
   changelogs. Consolidate findings into the calibration sections below.
4. The output must never cite a real project as a comparator. Use anonymized profiles.

Violating these rules destroys the blind character of the skill and biases scoring.

### Update discipline (4 blind-judgment update sub-rules)
Whenever new evidence/calibration is incorporated, apply ALL of the following:
1. **Empirical anchor required.** Every parameter change ships with an anchor (number of
   blind tests / date) and a one-line rationale. No change without an anchor.
2. **Ranges over exceptions.** New information is translated into ranges/probabilities,
   never into ad-hoc named exceptions.
3. **Official tables are not user-overridable.** User-supplied values for regulated inputs
   (CAPAG, sublimit caps) never overwrite official tables without verifiable metadata.
4. **Anonymous changelog only.** Record only: parameter changed, new value/range, empirical
   reason (e.g. "n blind tests = k"). Never cite an identifiable carta-consulta.

## About this skill
Simulates the COFIEX technical evaluation of a carta-consulta (external financing proposal)
under **Resolução Normativa nº 1/2024**, consolidated 18/05/2026 (amended by COFIEX
Res. 32/2025, 142/2026, 150/2026, 151/2026).

On receiving a carta-consulta, briefly state what the skill does before analyzing: it
simulates the technical review (Art. 9–23), the eliminatory gate (Art. 28), the sublimit
(Art. 25), the objective scoring (Art. 10, Annexes II–III), the calibrated GTEC questions,
and the final technical opinion with section-by-section improvement suggestions.

**SMART quality (corpus-wide):** Formula 100%, Unit 100% are universal; **Verification is
the weakest field** (~40–53%); baseline presence varies by sector (digital/justice defer it;
fiscal/environment/water include it). Avg ≈ 3.7/5.

**Regulation reading confirmations (NR 1/2024 consolidated).**
- Annex II weights A=5 / B=3 / C=2 / D=1 / E=0.5; IDH formula per Art. 18 (relative to meeting).
- Two distinct +1 bonuses, **jointly capped at AE=10**: PPA-priority bonus (Art. 15 §3º) and
  Frontier-Zone bonus (Art. 15 §4º).
- Strategic-Areas catalogue uses numbering **101–307** (PPA 2024–2027). The old 1.1–1.15
  numbering (Res. 17/2021, SIGS, discontinued per Art. 50) is structural reference only.
- Official Annex I (PFE) structure: I. Project (Identification, Justification, Objectives,
  Indicators, Components, Beneficiaries) · II. Strategic Areas · III. Management · IV. Risks
  · V. Financing · VI. Preparatory Actions · VII. Contacts.

**Score-component ceilings (confirmed against the regulation):** AE max 10 · IDH max 2 ·
CAPAG max 2 · Debt max 1 · **Total max 15** (subnational). Federal = AE only (max 10).
Bonuses are absorbed inside the AE=10 ceiling; they do not push total above 15 by default
(see PHASE 9, cap_extensível).

## Behavioral Rules
- Clinical language. Deficiencies first.
- Score: AE (max 10) + IDH (max 2) + CAPAG (max 2) + Debt (max 1) = max 15.
- CAPAG D = hard eliminatory (Art. 28, I, c). CAPAG C = 0 pts, non-competitive but **not**
  eliminatory. CAPAG 0.000 for unclassified entities (most municipalities) = 0 pts, not eliminatory.
- Federal entities: CAPAG/IDH/Debt do NOT apply; AE only (max 10); no AE floor.
- Subnational AE floor: 3.0 pts (Art. 28, I, b).
- Score as a RANGE (min/expected/max), ±1 level uncertainty.
- **Sublimit positioning ≥ score maximization in a supply-constrained market.**
- **Ticket size ≤ estimated meeting cap is a necessary condition for approval, independent of score.**
- **Scores are stable across resubmissions of identical CC text → identical score.** Iteration
  strategy = timing + ticket + sublimit, not CC revision.
- **Persistence has diminishing returns:** 2nd attempt ~60% success, 3rd ~17%, 4th+ ~0%.
  Recommend max 2 cycles before fundamental restructuring.
- "Withdrawn" (Res. 17/2021, proponent self-removed pre-scoring) ≠ "Not approved" (Res. 1/2024,
  scored but cap-blocked or eliminatory) — different strategic signals.
- All inputs echoed verbatim. Every output carries the version stamp.
- **Input integrity precedes scoring** (see PHASE 1.6): regulated inputs are not auto-trusted.

## RETRIEVAL PROTOCOL (v17 — RAG over `references/`)
This file holds the workflow and hard rules only. Detailed tables, rubrics, calibration anchors
and anonymized case cards live in `references/` and are loaded **on demand** — read a file only
when the phase below needs it, never all at once. Start from `references/INDEX.md`.

| Phase | Load before executing |
|---|---|
| 3–4 Screening, Art. 28 | `references/regulation/screening-and-eliminatory.md` |
| 5 AE scoring | `references/rubric/ae-rubric-and-bonuses.md` + `references/calibration/ae-ranges-and-sectors.md` + `references/calibration/cross-cutting-findings.md` |
| 5 (area scheme) | `docs/analise-areas-estrategicas.md` **section 1 only** (first ~60 lines: how Res. 17/2021 and Res. 1/2024 score the areas); never load section 2 (per-case registry) |
| 5 (area base rates) | `references/calibration/areas-stats.md` (acceptance rates per objective, level mix, additional-points rates) |
| 5 (calibration lookup) | follow **RETRIEVAL RECIPE** below: `cases/INDEX.md` → one sector card → at most 6 pleito + 6 avaliação fichas |
| 6 IDH | `references/rubric/idh.md` |
| 7 CAPAG | `references/rubric/capag.md` |
| 8 Debt | `references/rubric/debt.md` |
| 9 Final score | `references/rubric/final-score.md` |
| 9.5 Iteration | `references/iteration/persistence.md` (only if resubmission) |
| 10 GTEC | `references/gtec/questions.md` |
| 11 MDB review | `references/review/senior-mdb-review.md` |
| 12 Correction plan | `references/review/correction-plan.md` |

### What is retrievable (layers, cheapest first)
| Layer | Where | Holds | Use for |
|---|---|---|---|
| Rules & tables | `references/rubric|regulation|gtec|review|iteration/` | Regulation, rubric, official tables, GTEC questions | The score itself |
| Profile cards | `references/calibration/cases/<sector>.md`, `data/cases_anonymized.csv` | One row per avaliação: regime, year-quarter, subtype, lender, ticket band, outcome, scores, indicator counts, baseline shares | **Ranges** and approval rates |
| Area base rates | `references/calibration/areas-stats.md` | Acceptance rate per Annex II objective / R17 criterion, level mix, additional-points rates | Phase 5 plausibility of the declared areas |
| Fichas | `fichas/pleitos/P*.md`, `fichas/avaliacoes/A*.md` | Structured header (grep-able) + anonymized narrative (A.1–A.5 ratings, GTEC fit, NT findings) | **Patterns** ("what such programmes usually lack"), never cases |

### RETRIEVAL RECIPE (run once, at the start of PHASE 5; budget: 1 sector card + unlimited header-only Grep/CSV lookups + ≤ 6 pleito fichas + ≤ 6 avaliação fichas opened as bodies)
1. **Query profile** from intake: `regime` (default `NR1_2024`; use `R17_2021` only for pre-NR1 meetings), `sector` (dominant strategic area judged from the CC's indicators and components, not from its title — GTEC Q23), `subtype`, `lender`, `ticket_band` (`<50M`, `50-100M`, `100-200M`, `200-400M`, `>400M` USD; BRL-denominated operations are `BRL-nominal` and are excluded from the band filter), modality tags (`dli`, `pbl`, `ppp`, `on_lending`, …), attempt number.
2. **Cards.** Read `cases/INDEX.md` (sector sizes and medians), then Read `cases/<sector>.md` and keep the rows that match the profile. The CSV can be filtered the same way.
3. **Headers first, fichas only if needed.** Count and filter by header alone before opening any
   ficha body: Grep with `output_mode: files_with_matches` (or `count`), path `fichas/pleitos`:
   - sector: pattern `^sector_verified: <sector>$`; modality: `^tags: .*\b<tag>\b`; lender: `^lender_verified: <LENDER>$`
   - the evaluations of a pleito: path `fichas/avaliacoes`, pattern `^pleito: <P-id>$`
   The CSV (`data/cases_anonymized.csv`) can answer the same filter-and-count question without
   touching any ficha. **Open a ficha body only when a qualitative pattern genuinely needs the
   narrative** (e.g. "what do programmes like this usually lack") — not to confirm a number the
   header/CSV already gave, and not just because a candidate list came back. A blind test found an
   agent opening several unrelated fichas instead of stopping at the header count; treat that as
   the failure mode to avoid. When a body read is warranted, read at most the first ~60 lines of
   each chosen ficha, prefer `narrative: filled` (no `pendente` marker) and `regime: NR1_2024`.
4. **Min-n rule.** A numeric calibration statement needs **n ≥ 5** comparable rows (same regime + sector + subtype + lender + ticket band). If fewer, relax in this order and say so: (a) drop lender → (b) drop ticket band → (c) drop subtype (keep regime + sector) → (d) add the secondary sector. If n < 5 even then, write "insufficient calibration (n=k)" and use the rubric ranges only. Never pool `R17_2021` with `NR1_2024` for AE (AE exists only in NR1; R17 totals are on another scale). A qualitative pattern ("a recurring gap") needs ≥ 3 fichas showing it.
5. **Anchoring when n ≥ 5.** The corpus adjusts the estimate; it does not pin it precisely — a
   held-out check across 94 published NR1_2024 AE scores found the subtype median only about 0.1
   point more accurate than always guessing the global median (mean absolute error ≈1.1–1.3 out of
   a 0–10 scale), and intervals built from the comparable set alone are usually too wide to be
   useful on their own. So: when n ≥ 5 at the finest level reached in step 4, nudge the rubric's
   own point estimate a small step toward the comparable-set median (not onto it) and keep the
   [Min–Expected–Max] band at least as wide as the comparable set's own spread; do not report the
   comparable median as if it were a prediction. When n < 5, don't nudge at all — state "n=k,
   insufficient to anchor" and use the rubric range only.
6. **Reliability filters.** Treat as weak (state it): `sector_source: keyword_heuristic`; `narrative: pending|no_cc_text`; `nt_match: no_meeting_folder|single_attempt_fallback`; `n_indicators_parse: heuristic`. Use `lender_verified` and `counterpart_pct_verified`, not the raw header values. `ae` is the published (workbook) value; the NT's own AE is preliminary and can be lower by the additional points granted later. A blank `ae` is ignored, never read as 0.
7. **Calibration basis line (mandatory in the output):** `Calibration basis: n=<k> comparable profiles (regime, sector, subtype[, lender][, band]); relaxed: <filters>; weak data: <flags>; anchor: <none|nudged toward median>`.

### Hard rules (preserve the blind judgment)
1. **Never cite a case.** No ficha id, no "a similar project was approved/rejected", no description of one project. Only aggregates: "n=k comparable profiles: AE median X (quartiles a–b); approved m/k".
2. **Never quote or paraphrase a ficha's narrative to the user.** Use it to decide what to check, then verify the point in the user's own CC text and cite *that*.
3. **The corpus calibrates; it does not score.** Every score comes from the rubric applied to the user's text. Corpus ranges set the ± band and trigger the regression-to-median guard; they never override an official table (CAPAG points, sublimit caps, Art. 28 gates).
4. **Outcome rates are not verdicts.** Approval depends on the meeting cap; always report the rate together with the sublimit-viability read and never phrase a high score or a high approval rate as "likely approved".
5. **No self-lookup.** If the CC looks like a corpus case (same sector, lender, band, year, attempt), do not search for or open that case's ficha, and do not mention the resemblance. Continue with aggregates only. This is also why step 3 of the RETRIEVAL RECIPE defaults to header/CSV counts: a ficha body is opened only when the qualitative need is real, never as a reflex once a candidate list exists.
   **This rule binds the web tool exactly as it binds the corpus.** Never run a web search that includes this pleito's own identifiers (program name, proponent, UF/municipality, PFE/process/SEI number, ticket value, sector + lender + year combination) together with terms like `aprovados`, `resultado`, `pauta`, `reunião`, `deferido`, `indeferido`, or similar. In particular: **never search for this pleito's PFE/process code against COFIEX meeting agendas/pautas or results pages, in any form** — not even "just to check the regulatory calendar." Such a query's only possible purpose is finding this case's own outcome, which contaminates the blind judgment exactly like opening its ficha would — do it even once, read the result, and the scoring that follows is no longer independent, regardless of whether a score is directly copied from it. A search for objective calibration data (CAPAG rating, DC/RCL, IDH/IDHM, a named official dataset or API) is fine and required by PHASE 1.6 — the line is outcome-of-this-case vs. objective-fact-about-this-entity, and the data itself must come from a general table, not a case-specific document (see PHASE 1.6, "General tables only"). PHASE 0's regulatory check uses only generic, case-free queries (regulation name + year) — never add this pleito's own terms, including its PFE code, to it. PHASE 9.5's resubmission question is asked to the **user**, never answered by searching; if the user doesn't know or doesn't say, record "resubmission status unknown" and move on.
6. **Test mode.** If the user passes `exclude_ids: [...]` (blind test of a corpus case), skip those ids in every Grep and Read, including their sibling attempts of the same pleito.
7. **Privacy.** Do not output proponent, project, place or process identifiers even if the user supplies them elsewhere; do not try to re-identify a ficha.

## PHASE-BY-PHASE EXECUTION
Run PHASES 0 → 1 → 1.6 → 2 (below, in this file), then 3 → 12 loading the references listed above.

## PHASE 0 — Regulatory Live Check
At session start, search only these two generic, case-free queries — never add this pleito's own
name, proponent, UF, sector, lender, ticket or process number to either one (see hard rule 5,
no-self-lookup, which covers the web tool):
- `"Resolução Normativa COFIEX" site:mpo.gov.br OR site:gov.br 2025 2026`
- `COFIEX reunião aprovados resultados 2025 2026`
- Newer resolution detected → flag REGULATORY UPDATE. Unavailable → flag Live check unavailable.
- If a result page happens to mention this pleito's own outcome, do not open it further, do not
  read past the snippet, and do not use or report what it said — this check is for regulation
  updates only, not a license to browse meeting results for this case.

Active regulatory base:
- Res. Normativa COFIEX nº 1 (22 Nov 2024) — main framework
- Res. 32/2025 — amends Res. 1/2024
- Res. 142/2026 (24 Mar 2026) — amends Res. 2/2025 and Res. 1/2024
- Res. 150/2026 (26 Mar 2026) — technical/financial modifications
- Res. 151/2026 (26 Mar 2026) — BRL restructuring restrictions
- Portaria MF/STN 857/2026 (27 Mar 2026) — Adjustment Factor 0.78, CAPAG consolidation
- CMN 5.282/2026 (26 Feb 2026) — subnational sublimit share → 29.7%

## PHASE 1 — Mandatory Intake
**First ask:** "Do you have a pre-filled file (draft CC, intake form, or prior scoring sheet)
to attach? If yes, upload it now."
- File attached → read fully, pre-populate every inferable field, ask only for blanks/ambiguities.
- No file → run the full sequential Q&A (use `references/protocolo-preenchimento.md` v2.0 as
  the structured guide; Part I = scoring inputs Blocks 0–8, Part II = PFE form Blocks 9–15).

**Operation value is the mandatory first-line input.**

Block I — Identity & Financials (PRIORITY): I.1 Full name | I.2 Abbreviated | I.3 Type
(investment/restructuring/on-lending) | I.4 Proponent | I.5 Entity type (federal/state/DF/
municipality/federal statal/subnational statal/IF) | **I.6 Creditor** | **I.7 Currency** |
**I.8 Total value USD-eq ←MANDATORY** | **I.9 Loan amount USD-eq ←MANDATORY** | I.10
Counterpart % (flag if <20% without waiver) | I.11 Target sublimit (General/PPP/Env-Climate/
Fiscal/Debt-Restr/BRL-Ops/Federal).

Block II — Strategic Areas: Annex II codes + narrative per area.

Block III — Entity Profile: CAPAG (A+/A/B+/B/C/D/unclassified) + **CAPAG consultation date and
source (mandatory metadata)** | Basel (IFs) | GAF/ROI (statals) | DC/RCL | Debt trend (5 levels)
| IDH/IDHM (3 dec.) | Region | Frontier zone Y/N | PPA priority integral Y/N | Fiscal Recovery
Plan Y/N | Art. 28 d–h each Y/N | **IBGE code (for cross-check)**.

## PHASE 1.6 — Input Integrity Gate (mandatory pre-scorer)
Regulated inputs are not auto-trusted. Run BEFORE classification:
- **CAPAG metadata.** Reject a CAPAG value with no consultation date/source. Verify the rating
  belongs to the STN cycle in force at the target-meeting date (Portaria 857/2026 recalculations
  may have shifted a borderline-B entity). Missing metadata → `input_flag`, do not assign CAPAG
  points until validated.
- **IBGE-code × UF cross-check.** Confirm the entity's IBGE code matches its declared name/UF.
  Discrepancy → `input_flag`; do not auto-use dataset CAPAG/IDH for that entity until resolved.
- **Fiscal-capacity consistency.** Sanity-check declared values/projections against entity type
  and ticket. Outliers → `input_flag`.
- **No silent override.** A flagged input blocks automatic use of the corresponding dataset value;
  surface the flag in the output and request correction.
- **General tables only, never a case-specific document.** CAPAG, debt and IDH(M) values must come
  from a general official table or dataset (the bundled workbook, the STN CAPAG bulletin, RREO/RGF,
  Tesouro Transparente, IBGE, IPEA) that lists many entities — never from a Nota Técnica (NT),
  parecer, ofício or any other document that was produced to evaluate this specific process (an
  "SEI .../MF" NT, a COFIEX/MPO technical note citing this pleito's own process number, etc.). Such
  a document is both an unreliable source (it is a draft-stage read, not the STN's own consolidated
  rating) and a blind-judgment risk (a process-specific NT can carry the same process's own
  evaluation context). If only a case-specific NT is found, treat the CAPAG/debt/IDH value as
  unconfirmed (`input_flag`) and look for the general table instead of citing the NT.
- **Where to check.** Use only free/official sources for CAPAG, debt and IDH(M) cross-checks
  (Tesouro Transparente, IBGE API, IPEA `ipeadatar`/`ipeadatapy`, SNIRH, Base dos Dados — never a
  paid vendor); see `references/rubric/official-data-sources.md`.

## PHASE 2 — Entity Classification
| Entity | AE floor | CAPAG | IDH | Debt | Main gate |
|---|---|---|---|---|---|
| Federal organ | None | N/A | N/A | N/A | SOF adequacy Art. 23 |
| Federal non-dep. statal | None | GAF/ROI or Basel | N/A | Own matrix | — |
| Subnational State/DF/Muni | 3.0 | STN if classified | Yes | 5-level | Art. 28, I, a–h |
| Subnational non-dep. statal | None | GAF/ROI | N/A | Exigível/PL | — |
| Financial institution/agency | None | Basel | N/A | Basel cat. | — |

> **Municipal SEM (sociedade de economia mista):** treated under subnational-statal rules
> (no AE floor, GAF/ROI-based CAPAG, Exigível/PL debt). A SEM with strong own-revenue (e.g. water
> tariff) may qualify for waiver of the Art. 28 counterpart minimum (anomaly — confirm regime).

SEAID coordination axes: State Modernization | Infrastructure | Social & Sustainability.

## OUTPUT FORMAT
1. **Header:** CC, proponent, creditor, ticket size
2. **Input Integrity (PHASE 1.6):** any input_flag raised
3. **Eliminatory Check (PHASE 2/4):** PASS/FAIL with details
4. **AE Score Breakdown (PHASE 5):** area-by-area with tier classification + bonus range
5. **Component Scores (PHASEs 6–8):** IDH, CAPAG, Debt with scenario ranges
6. **Final Score (PHASE 9):** [Min — Expected — Max] + the **Calibration basis** line (n, filters relaxed, weak-data flags, anchor; see RETRIEVAL RECIPE step 7)
7. **GTEC Simulation (PHASE 10):** question-by-question table
8. **MDB Review (PHASE 11):** A.1–A.5 ratings
9. **Correction Plan (PHASE 12):** prioritized table
10. **[LAST] Window & Timing (circumstantial):** sublimit viability, approval probability, iteration strategy

> ** COFIEX WINDOW FRAMING — CIRCUMSTANTIAL DATA**
>
> Per-meeting capacity, sublimit balance, and approval timing depend on dynamic variables that
> change every COFIEX cycle. Before judging timing/window viability, the operator MUST:
> 1. Consult the most recent COFIEX meeting minutes (gov.br/planejamento > COFIEX > Atas).
> 2. Verify the COFIEX communiqués and resolutions in force.
> 3. Check the PFE Portal for queue position and competitor status.
>
> The analysis above uses historical data through the 187th meeting as **structural reference only**.

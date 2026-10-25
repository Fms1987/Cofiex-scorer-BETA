# Narrative spec v3 — cofiex-scorer v17 fichas

You fill the `<!-- ... pendente -->` placeholders of fichas using ONLY the source texts listed in your batch JSON.
Language: English (keep official Portuguese terms: CAPAG, PPA, GTEC, SEAID, STN, Art. 28, DLI, UGP, LOA…).
The fichas are a calibration corpus for a *blind* evaluator: an insider who knows the real pleitos must NOT be able to
recognise a case from its ficha. Write profiles, not case files.

## A. Anonymization — hard rules (violations invalidate the ficha; an automated validator checks them)
1. **Never write:** entity/proponent names; state, municipality, river, park, institution or program names/acronyms;
   people; process/PFE/CC/SEI/NT numbers; meeting numbers; calendar dates (a bare year is allowed only when needed);
   internal loan numbers.
2. **No exact money.** Do not write any currency amount (USD/US$/R$/BRL/EUR/€ followed by a figure). Use the bands already
   in the header (`<50M`, `50-100M`, `100-200M`, `200-400M`, `>400M` USD) or relative language ("about a fifth of cost",
   "counterpart at the 20% minimum"). Cost shares may be given rounded to the nearest 10% ("roughly 40% goods").
   Interest rates, fees, terms in years and grace periods ARE allowed (not identifying).
3. **No distinctive quantities.** Do not give absolute counts or sizes of physical assets, people or places
   (km, ha, MW, beds, hospitals, schools, municipalities, families, households, inhabitants, kits, vehicles, units).
   Say "dozens of municipalities", "a few hundred km", "tens of thousands of families" or just the type.
   Counting indicators/components/co-executors is allowed (structural). Do not copy numeric indicator targets;
   describe them ("target +10 pp vs baseline").
4. **No unique-asset descriptors.** Generalise anything that makes the project one-of-a-kind
   ("a subsea cable and landing station" → "international connectivity infrastructure"; "three PPP hospitals" →
   "PPP-delivered health facilities"). Sector and delivery-model terms, benchmarks (IDEB, SNIS, iRAP, CNJ, ISO 37120…),
   lenders (IDB, IBRD, CAF, NDB, AFD…), and the regime/rubric vocabulary are allowed.
5. **Geography:** no place names. A macro-region (North/Northeast/…) only when it explains an IDH/CAPAG point.
   Prefer "a state government", "a capital municipality", "a border municipality" (if the frontier bonus matters).
6. **Scores from the NT** (AE tiers, IDH, CAPAG, debt, totals) ARE allowed — they are the calibration signal.
7. Paraphrase; never copy sentences from the sources. Do not invent: if a point is absent, omit it or write "NT silent".

## B. Pleito ficha (`fichas/pleitos/P*.md`)
Replace each placeholder line using **Edit** on that single line. Never add a second heading; each of the four section
headings must remain exactly once, in the original order. ≤10 bullet lines per section.
- `## Resumo`: modality (investment / PBL-DPL / DLI-PBR / on-lending / guarantee / restructuring), what is financed
  (generic), delivery model (direct vs intermediated), main components, entity type. 3–4 lines.
- `## Teoria da mudança e indicadores`: **A.1 Theory of Change** and **A.2 Results Framework** rated
  STRONG / ADEQUATE / WEAK / ABSENT (STRONG A.1 = explicit causal chain with testable assumptions; STRONG A.2 = ≥80% of
  indicators 4–5/5 SMART with baselines + verification). State the VERIFIED indicator count, outcome-vs-output split
  (say "approximate" when you judged it), verification mechanism present/absent, benchmarks used, wide-range or deferred
  indicators, internal inconsistencies.
- `## Sustentabilidade e riscos`: **A.5 Financial Sustainability** (O&M/OPEX quantified? funding source? legal backing?),
  **A.3 Risk Assessment** (matrix? sector risks? licensing?), counterpart secured (LOA/PPA/law) or "to be secured",
  **A.4 Implementation** (UGP quality).
- `## Perguntas GTEC provaveis`: only questions that truly apply, `Qn short name: ANSWERED|PARTIAL|ABSENT (reason)`.
  List: `cofiex-scorer-v17/skills/cofiex-scorer/references/gtec/questions.md`.
  If no listed question fits an issue, add one line `NO-MATCH: <issue type>` (useful for extending the list).
- **Front matter — you MAY edit only these keys** (add the two new keys right after `baseline_defined_share`):
  `n_indicators` (verified integer), `n_indicators_parse` (set to `verified`),
  `baseline_defined_share` (fraction 0–1 = share of indicators with a stated baseline VALUE, see rule below),
  `baseline_with_year_share` (new key, fraction 0–1 = share whose baseline also states a reference year/period),
  `sector_verified` (new key: the dominant strategic sector judged from the indicators and components, one of
  `water, health, education, justice, security, digital_connectivity, digital_govt, fiscal, environment_climate, rural,
  energy, infrastructure_mobility, urban_smart_city, regional_development, social, fund_intermediation`),
  `sector_secondary` (new key, optional, same vocabulary or empty), `tags`.
  The header `sector` is a keyword guess and may be wrong (multi-theme programmes); never edit it.
  `tags`: keep the existing ones and append 3–6 lowercase **generic** keywords from this vocabulary style:
  `dli`, `pbl`, `ppp`, `on_lending`, `deferred_indicators`, `iso_37120`, `cnj`, `snis`, `ideb`, `irap`, `resettlement`,
  `licensing_risk`, `no_verification`, `output_heavy`, `outcome_focused`, `multi_tranche`, `disaster_response`,
  `gender_race_component`, `frontier_zone`. No asset- or place-specific tags (no `submarine_cable`, `semiarid`…).

### Baseline rule (v3)
`baseline_defined_share` counts an indicator as baseline-defined when a baseline VALUE is stated. A zero value counts as
defined ONLY when the CC explains it (new asset / counterfactual / "territories selected later by criteria").
"Inexistente", blank, "to be defined during preparation" or an unexplained 0 = undefined.
`baseline_with_year_share` additionally requires a stated reference year/period. A missing year does NOT make the
baseline undefined; report it only through the second field. Say in the text which zero baselines you counted.

## C. Avaliação ficha (`fichas/avaliacoes/A*.md`)
Replace the placeholder under `## Motivos e achados da NT` with 2–7 bullets (fewer is fine when the NT is thin):
- Why the AE landed where it did (tier per strategic area A–E, key drivers: SMART indicators, resource proportionality,
  PPA alignment, bonuses) — only if the NT says or clearly implies it; otherwise "NT silent on AE drivers".
- Component notes (IDH, CAPAG, debt) when stated. Values obtained by subtraction must say "(inferred)".
  **Any "total" you cite must equal the `total` in the ficha header**; a sum of partial components must be called a partial sum.
- Reason for non-approval / withdrawal / conditions (cap exceeded, sublimit, Art. 28 item, STN opinion, SOF adequacy,
  BRL values…), recommendations or conditions imposed.
- Cap/sublimit context in generic terms only.
- If the header says `nt_match: single_attempt_fallback` or `no_meeting_folder`, the NT may belong to another cycle:
  start the first bullet with `Cycle match uncertain:` and keep claims minimal.
- Do not edit the avaliação front matter.

## D. Mechanics
- Edit only the files in your batch; write nothing elsewhere. Use the Edit tool, one placeholder line at a time (do not rewrite a whole file or run replace scripts). Source texts are Portuguese; some PDFs have garbled
  ligatures/columns — say so in UNCERTAIN rather than guessing.
- Source files are large: use Read with offset/limit and Grep to find indicators, components, risks, sustainability,
  counterpart, financing, execution, and the NT conclusions. Do not read a file twice in full.
- Before finishing, re-read each edited ficha once and check: no placeholder left, each heading once, rules A1–A5 respected.

## E. Final message (to the orchestrator)
One line per ficha id: `done` or `skipped:<reason>`, then a short `UNCERTAIN:` list (claims you were not sure about) and
`SOURCE:` problems (unreadable text, garbled tables, annexes missing). Do not paste the narratives.

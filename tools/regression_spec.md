# Banco de teste fixo e regressão

Every change to the skill that can move a score (rubric, calibration, lens, recipe, scripts) is measured
on the same frozen bank, in a blind sandbox, before it is committed. The bank and its results are
PRIVATE (they hold official scores and portal numbers): keep them outside this repository.

## 1. Freeze the bank (once per bank version)
```
python -I -X utf8 tools/build_test_bank.py <match_csv> <consolidated_xlsx> <idmap_json> <bank_dir> --pool <validated.csv> --n 40
```
- Eligible: NR 1/2024 pleitos with an official total and an opaque ficha id.
- Stratified by sublimit group (Geral / other subnational / Federal) × entity type.
- Outputs `bank.csv`, `ids.txt`, `truth.csv`, `truth_areas.csv` (official level per PPA objective).
- Do not change a frozen bank. A new bank is a new version (`banco_teste_v2`) with a new baseline.

## 2. Build ONE blind sandbox for the whole bank
```
python -I -X utf8 tools/make_blind_sandbox.py <repo_root> @<bank_dir>/ids.txt A <areas_final_dir> <sandbox_dir>
```
All bank pleitos lose their fichas, CSV rows, card rows and area records at once. Score every bank
pleito against this sandbox, never against the installed skill.

## 3. Run the blind scoring
One run per pleito (subagents in batches are fine). Each run reads only its carta-consulta file and the
sandbox skill, and ends with the block below. AREA lines are required for level accuracy: one per PPA
objective the carta declares or the run scores, with the level it gave (0 = no score).
```
===PLEITO===
ID: <pleito_id>
NOTA_GERAL_MIN: <float>
NOTA_GERAL_ESP: <float>
NOTA_GERAL_MAX: <float>
AE: <float>
CAPAG: <float>
DIVIDA: <float>
IDH: <float>
AREA: <código PPA> | <A|B|C|D|E|0>
===FIM===
```

## 4. Score and compare
```
python -I -X utf8 tools/run_regression.py <bank_dir> <out_dir> <blocks...> --label <version> --baseline <previous metrics.json>
```
Outputs `casos.csv`, `metrics.json`, `relatorio.md`. Headline metrics and tolerances (a change that
worsens any of them beyond tolerance is a REGRESSÃO and is not committed without a written reason):

| Metric | Target (proposal, package 1) | Tolerance |
|---|---|---|
| MAE Nota Geral | ≤ 1.0 | +0.10 |
| MAE Área Estratégica | ≤ 1.0 | +0.10 |
| Level accuracy, main area | ≥ 60% | −5 pp |
| Range coverage | ≥ 80% | −5 pp |
| |IDH bias| | ≤ 0.1 | +0.05 |

After an accepted run, copy `faixa_empirica.nota_geral_p80` and `ae_p80` into
`skills/cofiex-scorer/references/rubric/final-score.md` ("Faixa empírica") and record the run in the
anonymous changelog (metric values only, no ids).

## Baseline v1
Bank v1 = 40 pleitos drawn from the 89 already run blind (Oct 2026), so v1 needed no new runs. Those
runs predate the multi-pleito sandbox and some read a skill that still held the pleito's own fichas,
so v1 is an indicative baseline. It has no AREA lines: level accuracy starts at the first new run.

## History (metrics only)
| Change | Bank | Measure | Before → after |
|---|---|---|---|
| Package 2: official tables + `objective_lookup.py` (CAPAG by cycle, calibrated debt rule, IDH floors 0.680 / 0.643) | v1, 29 subnational pleitos | Component MAE, script vs official (no new blind run) | CAPAG 0.188 → 0.000; Debt 0.166 → 0.060; IDH 0.255 → 0.047. Debt rule and IDH floors were fitted on the same meetings: in-sample, re-check on the next bank. |
| Packages 1–2, first new blind round (sandbox without the 40 bank pleitos) | v1, 20 of 40 (stratified) | Full blind run with AREA lines | Same 20 pleitos: MAE Nota Geral 1.23 → 1.14; coverage 0.70 → 0.85. Components: CAPAG 0.00, Debt 0.04, IDH 0.04. AE MAE 1.18 with bias +0.83: secondary areas the official score left at 0 were given E (26 cases) or D (6). Main-area level 75% exact, 90% within one step; all areas 52%. Faixa p80 not updated (n=20). |
| Secondary-area rule (start at 0; one own link outside the strategic-areas section for E, two for objectives that are usually 0; sum test ~0.4 per declared secondary area), calibrated on 81 pleitos outside the bank | v1, the other 20 of 40 (never run before) | Paired blind run: same 20 pleitos, sandbox before vs after the rule | MAE Nota Geral 1.03 → 0.82; AE MAE 1.00 → 0.79; AE bias +0.55 → +0.37. Official 0 predicted E: 23 → 18, scored 0: 39 → 44; side effect, official E scored 0: 10 → 16. Main-area level 40% → 50% exact (run-to-run noise, the rule does not touch it). This half of the bank was easier than the first (before-rule MAE 1.03 vs 1.14). |

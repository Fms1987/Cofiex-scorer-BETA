# PHASE 9.5 — Iteration & persistence

<!-- source: V16 lines 547-574, moved verbatim -->

## PHASE 9.5 — Iteration & Persistence Analysis
**Runs AFTER scoring.** Assesses resubmission strategy for cap-constrained operations.
1. **Is this a resubmission?** Ask the **user** (never the web, never the corpus): prior
   meeting(s)/outcome/score? CC text changed? Ticket changed? Searching for this case's own
   history to answer this question is a self-lookup (SKILL.md hard rule 5) — if the user doesn't
   know or doesn't say, record "resubmission status unknown" and continue without it.
2. **Score-stability rule:** identical CC text → identical score (empirically confirmed, n=9).
   Only sublimit residual, competitor landscape, and entity-level updates (CAPAG/debt) change
   between meetings.
3. **Persistence probability:**
| Attempt | Approval rate | Recommendation |
|---|---|---|
| 1st | varies by sublimit | Submit to least-congested sublimit |
| 2nd | ~60% | Strong odds, esp. at Q4 |
| 3rd | ~17% | Fundamental restructuring recommended |
| 4th+ | ~0% | Abandon or completely redesign |
   *Q4 modifier:* ~75% of "Not approved → Approved" trajectories under NR 1/2024 occurred at the
   Q4 meeting (highest approval rate ~81% due to rollover caps).
4. **Ticket compression:** compression alone is insufficient — it works when AE is already
   competitive (≥8.5) and the compressed ticket fits under residual cap. (Anchors: ~82% and ~72%
   compressions succeeded with high AE at Q4; 0% compression with moderate AE failed.) A scope
   revision accompanying compression *does* change the score (it is no longer the same CC text).
5. **Strategy recommendation:**
| Situation | Strategy |
|---|---|
| 1st, score ≥ 10 | Submit to Q4 for maximum cap residual |
| 1st, score < 8 in General | Consider PPP/Env-Climate/Fiscal sublimit if eligible |
| 2nd, same CC text | Target Q4; score unchanged, only cap residual matters |
| 2nd, revised CC | Quantify expected AE Δ; if < +1.0, compression is more impactful |
| 3rd+ | Fundamental redesign: scope reduction, creditor change, or sublimit migration |

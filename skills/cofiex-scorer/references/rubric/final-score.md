# PHASE 9 — Final score

<!-- source: V16 lines 508-546, moved verbatim -->

## PHASE 9 — Final Score
`Total = min(10, AE + bonuses) + IDH + CAPAG + Debt` (subnational, max 15). Federal = AE only.
Present as **[Min — Expected — Max]**.

**Practical cap = 15.0.** Hold the total cap at 15.0 by default. Bonuses are absorbed inside the
AE=10 ceiling. If documentary evidence of bonus stacking would imply a value above 15, flag it as
**cap_extensível** with LOW probability, pending explicit COFIEX/SEAID confirmation — do not score
above 15 by default.

**Anchor pattern (anonymized blind tests, NR 1/2024):** AE is the highest-variance component
(≈3.5–9.0); IDH benefits N/NE entities up to +2.0; CAPAG discriminates A+ (2.0) vs B+ (1.0);
Debt varies with historical DC/RCL. Confirmed total examples (anonymized profiles): capital-
municipality investment ≈ 10.6; border-municipality investment+refinancing ≈ 11.9; state fiscal
DPL/restructuring ≈ 6.7 — **all approved** (the last confirming score-independent approval for
the restructuring modality).

** Debt Restructuring/DPL — approval independent of score.** The score is irrelevant to the
outcome; what determines approval is: (1) documented financial advantage (mandatory comparative
annexes); (2) approved CAPAG (A+/A/B+/B); (3) original debt already guaranteed by the Union
(guarantee subrogation). With all three present, approval ≈ 100% regardless of AE.

**Modifiers (investment projects):**
- ticket > 0.15 × cap → ×0.7; ticket > 0.25 × cap → ×0.3
- Q1 post-rollover → General P = max(5%, base × 0.1)
- IBRD in General → ×0.9 (ticket-size pattern)
- 2nd submission targeting Q4 → ×1.15 (cap 95%); 3rd+ submission → ×0.6
- Ticket compressed >50% between submissions → ×1.2
- Same CC text resubmitted → score unchanged; P depends entirely on cap residual + competitors.
- Bonus applied at expected weight 0.5 unless documentary framing attached (then full value).

**Caveats:** order-of-magnitude estimates (5 NR 1/2024 meetings, n≈140 + iteration analysis over
15 meetings + formal blind-holdout validation n=52+22, v16.0). The dominant uncertainty is the cap
residual at the meeting date, not the score — **empirically confirmed**: in the v16.0 blind-holdout
run, mean predicted TOTAL was statistically indistinguishable between real-Approved and real-Not-
approved cases (9.70 vs 9.50/15), and the Art. 28 gate alone predicted PASS almost universally
regardless of real outcome. A high score is a necessary but never sufficient signal — always report
it alongside the sublimit-viability read, and never phrase ART28_GATE=PASS or a strong TOTAL as
"likely to be approved" without that qualifier.

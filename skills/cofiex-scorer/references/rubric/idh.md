# PHASE 6 — IDH

<!-- source: V16 lines 408-449, moved verbatim -->

## PHASE 6 — IDH (Subnational only)
`IDH Score = 2 × ((1 − IDH_entity) / (1 − IDH_lowest_in_meeting))`

**CRITICAL:** Score is RELATIVE to meeting composition — cannot be computed without knowing who
else is pautado. Always present as a scenario range. The fixed-floor convenience anchor below is
a DEFAULT for state-heavy meetings only; it never replaces the relative formula when pauta
composition is known, and it never overrides the municipal floors.

### Default state-meeting anchor
For state-heavy meetings with unknown composition, use floor **0.668** as the base, with:
- Pessimistic 0.650 · Base 0.668 · Optimistic 0.686 (high-end 0.700 for pautas dominated by
  South/Southeast or coastal-NE high-HDI states).
Override only with evidence of actual pauta composition (flagged).

### Calibrated scenarios (corpus 180th–187th)
| Scenario | IDH_lowest | Use when |
|---|---|---|
| Pessimistic | 0.646–0.650 | Meeting has N/NE state with very low HDI |
| Moderate (default state) | 0.668 | Default for state-heavy meetings |
| Optimistic | 0.686–0.700 | No state below the high-HDI floor |
| Municipal | 0.572–0.620 | Meeting includes low-IDHM municipalities (floors preserved) |

**Empirical ranges — states:** low-HDI (0.639–0.689) → 1.7–2.0; mid-HDI (0.660–0.665) → 1.3–1.9;
high-HDI (0.740–0.826) → 0.5–1.2. Anchor: a NE state with IDH ≈ 0.689 that is virtually the
meeting floor (IDH_lowest ≈ 0.686) → ≈ 1.98.

**Empirical ranges — municipalities (IDHM) — floors preserved, NOT subject to the 0.668 state anchor:**
- ≤ 0.600 (very low) → 1.8–2.0 (near-max if lowest in meeting)
- 0.650–0.699 (low) → 1.5–1.8
- 0.700–0.710 (medium-low) → 1.4–1.7 (floor ~0.619–0.646); up to ~1.98 if the lowest
- 0.750–0.770 (medium) → 1.2–1.4 (floor ~0.580–0.620)
- 0.760–0.799 (medium-high) → 0.9–1.4
- ≥ 0.800 (high) → 0.4–0.9
Anchors (anonymized): municipality IDHM 0.759, meeting floor ≈ 0.619 → **1.335**; municipality
IDHM 0.700, similar floor → **1.695**.

**Practical estimate:** when the meeting composition is unknown, use the 0.668 state anchor for
state pautas; for municipal or mixed pautas use floor 0.620–0.650; adjust up (→1.9+) if the entity
is demonstrably the lowest IDH on the agenda, down (→0.5–1.2) if lower-IDH entities are present.

Federal entities: IDH = N/A (score 0).

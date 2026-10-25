"""Split SKILL_Cofiex_Scorer_V16.md into reference files by line range (verbatim, no rewriting)."""
import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
out = pathlib.Path(sys.argv[2]) / "skills/cofiex-scorer/references"
# (first_line, last_line, target, title) — 1-indexed, inclusive, from V16
parts = [
 (77, 167, "calibration/cross-cutting-findings.md", "Cross-cutting empirical findings (anonymized anchors)"),
 (283, 337, "rubric/ae-rubric-and-bonuses.md", "PHASE 5 — AE rubric, PPA objectives and bonus treatment"),
 (339, 407, "calibration/ae-ranges-and-sectors.md", "AE empirical ranges, structural discounts and sector summary"),
 (408, 449, "rubric/idh.md", "PHASE 6 — IDH"),
 (450, 471, "rubric/capag.md", "PHASE 7 — CAPAG"),
 (472, 507, "rubric/debt.md", "PHASE 8 — Debt trajectory"),
 (508, 546, "rubric/final-score.md", "PHASE 9 — Final score"),
 (547, 574, "iteration/persistence.md", "PHASE 9.5 — Iteration & persistence"),
 (575, 635, "gtec/questions.md", "PHASE 10 — GTEC simulation"),
 (636, 667, "review/senior-mdb-review.md", "PHASE 11 — Senior MDB review"),
 (668, 685, "review/correction-plan.md", "PHASE 12 — Correction plan"),
 (253, 282, "regulation/screening-and-eliminatory.md", "PHASES 3-4 — Technical screening & Art. 28"),
]
for a, b, rel, title in parts:
    p = out / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(src[a-1:b]).strip()
    p.write_text(f"# {title}\n\n<!-- source: V16 lines {a}-{b}, moved verbatim -->\n\n{body}\n", encoding="utf-8")
    print(rel, b-a+1, "lines")

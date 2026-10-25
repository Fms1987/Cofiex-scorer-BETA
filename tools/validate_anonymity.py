"""Fail if any committed text contains identifiers present in the source workbook."""
import re, sys, pathlib, openpyxl
xlsx, root = sys.argv[1], pathlib.Path(sys.argv[2])
wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
bad = set()
ALLOW = {"COFIEX", "SEAID", "STN", "Federal", "Brazil"}
for r in list(wb["PROJECTS_ALL"].iter_rows(values_only=True))[1:]:
    for i in (2, 4, 5, 6):  # SEI, proponent, project, PFE
        v = str(r[i] or "").strip()
        if len(v) >= 5 and v != "None" and v not in ALLOW:
            bad.add(v)
files = [p for p in root.rglob("*") if p.is_file() and p.suffix in (".md", ".csv", ".json", ".py") and "validate_anonymity" not in p.name and ".git" not in p.parts]
hits = []
for p in files:
    t = p.read_text(encoding="utf-8", errors="ignore")
    for b in bad:
        if re.search(r"(?<![\w])" + re.escape(b) + r"(?![\w])", t):
            hits.append((str(p.relative_to(root)), b))
print(len(files), "files scanned,", len(bad), "identifiers checked,", len(hits), "hits")
for h in hits[:40]:
    print(" HIT", h)
sys.exit(1 if hits else 0)

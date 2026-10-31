"""Convert NT PDFs that have no Markdown twin into Markdown (pymupdf4llm), next to the PDF.

usage: convert_nt_md.py <root> <log.json> [--workers 4]
Never overwrites an existing .md. Failures and scanned (no text layer) PDFs are listed in the log.
"""
import json, os, sys, time, contextlib, io
from multiprocessing import Pool
from pathlib import Path


def convert(pdf):
    md = Path(pdf).with_suffix(".md")
    if md.exists():
        return (pdf, "exists", 0, 0.0)
    t0 = time.time()
    try:
        import pymupdf4llm
        with contextlib.redirect_stderr(io.StringIO()):
            text = pymupdf4llm.to_markdown(pdf, show_progress=False)
    except Exception as e:  # noqa: BLE001
        return (pdf, f"error:{type(e).__name__}:{e}"[:160], 0, time.time() - t0)
    if len(text.strip()) < 200:
        return (pdf, "no_text_layer", len(text), time.time() - t0)
    md.write_text(text, encoding="utf-8")
    return (pdf, "ok", len(text), time.time() - t0)


def main():
    root, log = Path(sys.argv[1]), Path(sys.argv[2])
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    pdfs = sorted(str(p) for p in root.rglob("*.pdf") if not p.with_suffix(".md").exists())
    print(len(pdfs), "PDFs to convert,", workers, "workers", flush=True)
    res = []
    with Pool(workers) as pool:
        for i, r in enumerate(pool.imap_unordered(convert, pdfs), 1):
            res.append(r)
            if i % 25 == 0:
                ok = sum(1 for x in res if x[1] == "ok")
                print(f"{i}/{len(pdfs)} done ({ok} ok)", flush=True)
                json.dump(res, open(log, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(res, open(log, "w", encoding="utf-8"), ensure_ascii=False)
    c = {}
    for r in res:
        k = r[1].split(":")[0]
        c[k] = c.get(k, 0) + 1
    print("finished:", c, flush=True)


if __name__ == "__main__":
    main()

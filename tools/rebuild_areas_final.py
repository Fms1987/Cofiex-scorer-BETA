"""Reconstrói os registros de áreas estratégicas (areas_final/*.json) a partir da seção 2 de docs/analise-areas-estrategicas.md.

uso: python -I -X utf8 tools/rebuild_areas_final.py <repo_root> <out_dir>

Os registros originais (feitos por agentes a partir das Notas Técnicas) só existiam fora do repositório. A seção 2 do documento guarda,
por avaliação, as áreas pontuadas (código, nível, pontos, justificativa parafraseada), as não aceitas e os pontos adicionais, o que basta para
`make_blind_sandbox.py` (braço A) e `build_areas_stats.py`. Conferência: rodar `build_areas_stats.py` sobre a saída e comparar com
references/calibration/areas-stats.md.
"""
import json
import re
import sys
from pathlib import Path


def linhas_tabela(bloco):
    out = []
    for l in bloco.splitlines():
        if l.startswith("|") and not re.match(r"^\|[-| ]+\|$", l) and not l.startswith("| Código") and not l.startswith("| Dispositivo"):
            out.append([c.strip() for c in l.strip().strip("|").split("|")])
    return out


def main(repo, out):
    doc = (Path(repo) / "skills/cofiex-scorer/docs/analise-areas-estrategicas.md").read_text(encoding="utf-8")
    sec2 = doc.split("## 2. ", 1)[1]
    partes = re.split(r"(?m)^###### \*\*(\w+)\*\* · ", sec2)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for i in range(1, len(partes), 2):
        cid, corpo = partes[i], partes[i + 1]
        cab = corpo.split("\n", 1)[0]
        regime = "NR1_2024" if "Normativa 1/2024" in cab else "R17_2021"
        desfecho = re.search(r"desfecho `(\w+)`", cab)
        tot = re.search(r"Áreas estratégicas: \*\*([\d.,]+)/([\d.,]+)\*\*", corpo)
        sem = "sem pontuação por área" in corpo
        rec = {"id": cid, "regime": regime, "outcome": desfecho.group(1) if desfecho else "",
               "status": "ok" if not sem and tot else "no_area_block", "areas": [], "not_accepted": [], "bonus": []}
        if tot:
            rec["areas_total"] = [float(tot.group(1).replace(",", ".")), float(tot.group(2).replace(",", "."))]
        m = re.search(r"\*\*Pontuadas\*\*\n(.*?)(?=\n\*\*|\Z)", corpo, re.S)
        if m:
            for c in linhas_tabela(m.group(1)):
                pts = c[3].split("/")[0].replace(",", ".")
                rec["areas"].append({"code": c[0], "name": c[1], "level": c[2] if c[2] != "—" else None, "points": float(pts), "reason": c[4] if len(c) > 4 else ""})
        m = re.search(r"\*\*Não aceitas / sem pontos\*\*\n(.*?)(?=\n\*\*|\Z)", corpo, re.S)
        if m:
            for c in linhas_tabela(m.group(1)):
                rec["not_accepted"].append({"code": c[0], "name": c[1], "reason": c[2] if len(c) > 2 else ""})
                rec["areas"].append({"code": c[0], "name": c[1], "level": None, "points": 0.0, "reason": c[2] if len(c) > 2 else ""})
        m = re.search(r"\*\*Pontos adicionais \(art\. 15\)\*\*\n+(.*?)(?=\n_Obs|\n#|\Z)", corpo, re.S)
        if m:
            for c in linhas_tabela(m.group(1)):
                rec["bonus"].append({"article": c[0], "requested": c[1].lower().startswith("s"),"points": float(c[2].split("/")[0].replace(",", ".")), "decision": c[3], "reason": c[4] if len(c) > 4 else ""})
        (out / f"{cid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
    print(f"{n} registros gravados em {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

"""Monta o pacote .zip do skill para o envio de skills do claude.ai (máximo 200 arquivos, caminhos com barra normal).

uso: python -I -X utf8 tools/build_claudeai_package.py <skill_dir> <out_zip> [--nome cofiex-scorer-v1-beta]

Copia o skill para uma pasta temporária, agrupa as fichas por setor (fichas-merged/, uma ficha por bloco, com o cabeçalho original),
remove fichas/, ajusta os caminhos em SKILL.md e references/INDEX.md e grava o zip com `/` como separador (o Compress-Archive do
Windows PowerShell 5.1 grava barra invertida, que o claude.ai rejeita). Não altera o skill de origem.
"""
import argparse
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

LIMITE = 200
sys.path.insert(0, str(Path(__file__).parent / "arquivo-corpus"))
import merge_fichas_for_claudeai as m  # noqa: E402


def agrupar(pasta: Path):
    sys.argv = ["merge_fichas_for_claudeai.py", str(pasta)]
    m.main()


def ajustar_caminhos(pasta: Path):
    skill = pasta / "SKILL.md"
    s = skill.read_text(encoding="utf-8")
    s = s.replace("`fichas/pleitos/P*.md`, `fichas/avaliacoes/A*.md`",
                  "`fichas-merged/pleitos/<setor>.md`, `fichas-merged/avaliacoes/<setor>.md` "
                  "(várias fichas por arquivo; cada uma começa com um comentário de limite com o nome original)")
    s = s.replace("fichas/pleitos", "fichas-merged/pleitos").replace("fichas/avaliacoes", "fichas-merged/avaliacoes")
    alvo = "Grep com `output_mode: files_with_matches` (ou\n   `count`), caminho"
    assert alvo in s, "trecho de busca por cabeçalho mudou em SKILL.md; ajustar o script"
    s = s.replace(alvo, "Neste pacote há várias fichas por arquivo: usar Grep com `output_mode: count` "
                        "(nunca `files_with_matches`, que conta arquivos e não fichas),\n   caminho")
    skill.write_text(s, encoding="utf-8")
    idx = pasta / "references" / "INDEX.md"
    idx.write_text(idx.read_text(encoding="utf-8").replace("fichas/pleitos", "fichas-merged/pleitos").replace("fichas/avaliacoes", "fichas-merged/avaliacoes"),
                   encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_dir")
    ap.add_argument("out_zip")
    ap.add_argument("--nome", default="cofiex-scorer-v1-beta")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp) / a.nome
        shutil.copytree(a.skill_dir, pasta)
        agrupar(pasta)
        shutil.rmtree(pasta / "fichas")
        ajustar_caminhos(pasta)
        arquivos = sorted(p for p in pasta.rglob("*") if p.is_file())
        ruins = [str(p.relative_to(tmp).as_posix()) for p in arquivos if not re.fullmatch(r"[A-Za-z0-9._/\-]+", p.relative_to(tmp).as_posix())]
        if len(arquivos) > LIMITE or ruins:
            sys.exit(f"pacote recusado: {len(arquivos)} arquivos (máx. {LIMITE}); nomes fora de [A-Za-z0-9._/-]: {ruins}")
        out = Path(a.out_zip)
        out.unlink(missing_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for p in arquivos:
                z.write(p, p.relative_to(tmp).as_posix())
    print(f"{len(arquivos)} arquivos gravados em {out}")


if __name__ == "__main__":
    main()

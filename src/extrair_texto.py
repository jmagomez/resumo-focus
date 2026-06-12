"""Extrai o texto de um PDF do Focus e salva como .txt em data/.

Uso:
    python3 src/extrair_texto.py              # último PDF em data/
    python3 src/extrair_texto.py --pdf caminho/focus_AAAA-MM-DD.pdf
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"


def extrair(pdf_path: Path) -> Path:
    import pdfplumber

    with pdfplumber.open(pdf_path) as pdf:
        texto = "\n".join(p.extract_text() or "" for p in pdf.pages)

    txt = pdf_path.with_suffix(".txt")
    txt.write_text(texto, encoding="utf-8")
    return txt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, help="caminho do PDF (default: último em data/)")
    args = parser.parse_args()

    if args.pdf:
        pdf = args.pdf
    else:
        candidatos = sorted(DATA.glob("focus_*.pdf"))
        if not candidatos:
            print("Nenhum PDF em data/. Rode src/baixar_focus.py primeiro.", file=sys.stderr)
            return 1
        pdf = candidatos[-1]

    txt = extrair(pdf)
    print(f"Texto salvo em {txt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

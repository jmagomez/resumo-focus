"""Roda o pipeline localmente: baixa Focus → extrai texto → imprime caminhos.

Flags:
  --abrir    abre o .txt gerado no editor padrão
"""

from __future__ import annotations
import argparse
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from baixar_focus import baixar
from extrair_texto import extrair


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--abrir", action="store_true")
    args = parser.parse_args()

    data_pub, pdf = baixar(ROOT / "data")
    print(f"[1/2] PDF baixado: {pdf.name} ({pdf.stat().st_size // 1024} KB)")

    txt = extrair(pdf)
    print(f"[2/2] Texto extraído: {txt}")

    if args.abrir:
        webbrowser.open(txt.as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())

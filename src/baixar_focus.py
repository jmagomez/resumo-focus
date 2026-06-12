"""Baixa o último boletim Focus em PDF do site do BCB.

O Focus é publicado toda segunda-feira por volta das 8h30 (BRT), com a URL
seguindo o padrão R{AAAAMMDD}.pdf onde a data é a da publicação. Em semana
com segunda feriado, o BCB publica na terça — por isso o download tenta
retroceder dia a dia até 7 vezes antes de desistir.
"""

from __future__ import annotations
import sys
from datetime import date, timedelta
from pathlib import Path

import requests

URL = "https://www.bcb.gov.br/content/focus/focus/R{ymd}.pdf"
UA = "Mozilla/5.0 (compatible; routine-focus/1.0)"


def ultima_segunda(hoje: date) -> date:
    """Retorna a segunda-feira mais recente estritamente anterior a hoje.

    Se hoje já é segunda, retrocede uma semana (o `or 7` força isso, pois
    `weekday()` de segunda é 0 e `0 or 7 == 7`).
    """
    return hoje - timedelta(days=(hoje.weekday() or 7))


def baixar(dest: Path) -> tuple[date, Path]:
    """Baixa o PDF do Focus mais recente para `dest/focus_AAAA-MM-DD.pdf`.

    Retorna (data_publicacao, caminho_arquivo). Levanta RuntimeError se
    nenhum PDF for encontrado nos últimos 7 dias.
    """
    dest.mkdir(parents=True, exist_ok=True)
    candidato = ultima_segunda(date.today())
    for _ in range(7):
        ymd = candidato.strftime("%Y%m%d")
        url = URL.format(ymd=ymd)
        resp = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        if resp.status_code == 200 and resp.content[:4] == b"%PDF":
            arq = dest / f"focus_{candidato}.pdf"
            arq.write_bytes(resp.content)
            return candidato, arq
        candidato -= timedelta(days=1)
    raise RuntimeError(
        f"Nenhum PDF do Focus encontrado a partir de {ultima_segunda(date.today())} "
        f"retrocedendo 7 dias."
    )


def main() -> int:
    dest = Path(__file__).parent.parent / "data"
    data_pub, arq = baixar(dest)
    print(f"Focus de {data_pub} salvo em {arq} ({arq.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

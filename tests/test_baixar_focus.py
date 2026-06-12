"""Testes para src/baixar_focus.py.

Os testes de data são puros e rodam sempre. O teste de download real bate na
rede e é marcado `network` — pula com `pytest -m "not network"`.
"""

from __future__ import annotations
import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from baixar_focus import baixar, ultima_segunda


def test_ultima_segunda_quinta():
    # quinta 21/05/2026 (weekday=3) → segunda 18/05/2026
    assert ultima_segunda(date(2026, 5, 21)) == date(2026, 5, 18)


def test_ultima_segunda_terca():
    # terça 19/05/2026 (weekday=1) → segunda 18/05/2026
    assert ultima_segunda(date(2026, 5, 19)) == date(2026, 5, 18)


def test_ultima_segunda_se_hoje_e_segunda():
    # segunda 18/05/2026 (weekday=0) → segunda anterior 11/05/2026
    # O truque `or 7` força retroceder uma semana.
    assert ultima_segunda(date(2026, 5, 18)) == date(2026, 5, 11)


def test_ultima_segunda_domingo():
    # domingo 17/05/2026 (weekday=6) → segunda 11/05/2026
    assert ultima_segunda(date(2026, 5, 17)) == date(2026, 5, 11)


def test_ultima_segunda_sempre_segunda():
    """Varre 60 dias e confirma que o retorno é sempre uma segunda anterior."""
    from datetime import timedelta
    base = date(2026, 1, 1)
    for i in range(60):
        d = base + timedelta(days=i)
        res = ultima_segunda(d)
        assert res.weekday() == 0, f"ultima_segunda({d}) = {res} não é segunda"
        assert res < d, f"ultima_segunda({d}) = {res} não é estritamente anterior"


@pytest.mark.network
def test_download_baixa_pdf_real(tmp_path):
    """Baixa de verdade; valida que é PDF e que a data está correta."""
    data_pub, arq = baixar(tmp_path)

    assert arq.exists(), "arquivo não foi criado"
    assert arq.read_bytes()[:4] == b"%PDF", "primeiros 4 bytes não são %PDF"
    assert arq.stat().st_size > 50_000, f"PDF muito pequeno: {arq.stat().st_size} bytes"

    assert arq.name == f"focus_{data_pub}.pdf"

    hoje = date.today()
    assert data_pub <= hoje, f"data {data_pub} no futuro (hoje={hoje})"
    assert (hoje - data_pub).days <= 14, (
        f"data {data_pub} está muito no passado ({(hoje - data_pub).days} dias)"
    )
    # Data baixada deve estar dentro do intervalo [última-segunda, última-segunda - 6]
    esperada = ultima_segunda(hoje)
    from datetime import timedelta
    assert esperada - timedelta(days=6) <= data_pub <= esperada, (
        f"data {data_pub} fora da janela esperada ({esperada - timedelta(days=6)}..{esperada})"
    )

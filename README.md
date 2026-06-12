# Focus Semanal

Routine do Claude Code que, toda segunda, baixa o boletim Focus do BCB, extrai o texto e o próprio agente gera um resumo executivo + análise das três principais revisões da semana, abrindo um PR com o markdown pronto.

A geração do resumo é feita pelo agente Claude Code que executa a Routine (sem chamada à API externa, sem `ANTHROPIC_API_KEY` no projeto). Os scripts Python cuidam só da parte determinística: baixar o PDF e extrair o texto.

## Estrutura

```
meu-projeto/
├── CLAUDE.md               # briefing (o que é Focus, regras)
├── routine-prompt.md       # instrução que a Routine executa
├── setup.sh                # provisiona Python + deps no container
├── requirements.txt        # dependências pinadas
├── pytest.ini              # configura marker `network`
├── src/
│   ├── baixar_focus.py     # baixa o PDF (retrocesso até 7 dias)
│   └── extrair_texto.py    # extrai texto do PDF e salva .txt
├── tests/
│   └── test_baixar_focus.py
├── demo.py                 # roda baixar + extrair em sequência
├── data/                   # PDFs e .txt baixados (gitignore)
└── output/focus/           # focus_AAAA-MM-DD.md (gerado pela Routine)
```

## Como rodar localmente

**Pré-requisitos:** Python 3.10+. Verifique com `python3 --version`.

```bash
python3 -m pip install -r requirements.txt
python3 demo.py --abrir
```

O `demo.py` baixa o último Focus, extrai o texto e abre o `.txt` para inspeção. A geração do resumo em markdown acontece quando a Routine roda — localmente você fica com o PDF e o texto bruto.

**Flags:**

- `--abrir` — abre o `.txt` gerado no editor padrão.

## Testes

```bash
pytest                    # tudo (inclui smoke test que baixa de verdade)
pytest -m "not network"   # só os testes offline (rápidos)
```

## Pipeline em duas etapas

O BCB bloqueia IPs de cloud (Anthropic, AWS, GCP). Por isso o download não roda na Routine — fica num GitHub Action, que usa IPs do GitHub e passa pelo bloqueio. A Routine só consome o `.txt` já commitado.

**Etapa 1 — GitHub Action (`.github/workflows/baixar-focus.yml`)** roda toda segunda às 9h15 BRT (12h15 UTC) e também sob demanda. Baixa o PDF, extrai o texto e commita `data/focus_AAAA-MM-DD.{pdf,txt}` em `main`.

**Etapa 2 — Routine do Claude Code** roda toda segunda às 10h BRT (13h UTC), com folga de 45 min sobre o Action. Lê o `.txt` mais recente, gera o resumo, abre PR.

## Como subir

1. Suba o projeto para o GitHub: `gh repo create focus-semanal --public --source=. --push`.
2. Habilite Actions em `Settings → Actions → General` do repo (`Allow all actions`). Em `Workflow permissions`, marque `Read and write permissions`.
3. Instale o Claude GitHub App em `https://github.com/apps/claude`. Na instalação, escolha entre permitir acesso a todos os repositórios ou apenas aos selecionados — para este projeto, basta selecionar `resumo-focus`.
4. Valide o Action manualmente em `Actions → Baixar Focus semanal → Run workflow`. Confirme que apareceram os arquivos `data/focus_AAAA-MM-DD.{pdf,txt}` no `main`.
5. Em uma sessão do Claude Code na web (claude.ai/code), rode `/schedule create` com o conteúdo de `routine-prompt.md`, cron `0 13 * * 1`, modelo `claude-sonnet-4-6` e repo `analisemacro/resumo-focus`. Durante a criação, adicione o connector do GitHub: na seção de conectores, selecione **GitHub** e autorize o acesso ao repositório. Se o conector visual não estiver disponível, adicione manualmente via URL do servidor MCP: `https://api.githubcopilot.com/mcp`.
6. Valide com `/schedule run` antes de esperar a próxima segunda.

## Limites conhecidos

- Routines estão em research preview. Cron mínimo: 1h.
- Push restrito a branches `claude/*` por padrão.
- BCB pode mudar a URL do PDF sem aviso — se o script falhar consistentemente, verificar `https://www.bcb.gov.br/publicacoes/focus`.

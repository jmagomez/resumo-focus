# Instruções para quem mexe no código

O `README.md` explica **o produto**: o que é o Focus e o que a Routine entrega.
Não repita nada disso aqui.

Este arquivo é a outra metade: **o fluxo, os invariantes, os comandos e as
armadilhas** — o que não se deduz lendo o código.

---

## O que este projeto é

Uma Routine do Claude Code que, toda segunda, baixa o boletim Focus do BCB em
PDF, extrai o texto e **o próprio agente** escreve o resumo executivo lendo esse
texto, abrindo um PR com o markdown pronto.

A divisão importa: **o Python faz só a parte determinística** (baixar, extrair);
o julgamento — o que é revisão relevante na semana — é do agente. Não há chamada
a API externa nem `ANTHROPIC_API_KEY` no projeto.

```
Routine (segunda, 10h BRT)
   │
   ├─► src/baixar_focus.py   baixa o PDF → data/focus_AAAA-MM-DD.pdf
   ├─► src/extrair_texto.py  extrai o texto → data/focus_AAAA-MM-DD.txt
   │
   └─► o agente lê o .txt e escreve output/focus/focus_AAAA-MM-DD.md,
       em branch claude/focus-AAAA-MM-DD, e abre o PR
```

| arquivo | papel |
|---|---|
| `src/baixar_focus.py` | baixa o PDF; retrocede dia a dia até 7 dias |
| `src/extrair_texto.py` | `pdfplumber` → `.txt` ao lado do PDF |
| `routine-prompt.md` | a instrução que a Routine executa |
| `data/focus_*.pdf` / `.txt` | insumo, commitado pelo `focus-download.yml` |
| `output/focus/*.md` | a entrega; **nunca sobrescreve** |
| `demo.py` | uso manual; não entra na Routine |

## Fonte

- Página: `https://www.bcb.gov.br/publicacoes/focus`
- PDF: `https://www.bcb.gov.br/content/focus/focus/R{AAAAMMDD}.pdf`, com a data
  **da publicação** — `R20260622.pdf` para a edição de 22/06/2026
- ~4 páginas, 150–250 KB
- Pesquisa com cerca de 100 instituições (IPCA, PIB, Selic, câmbio, conta
  corrente), coletada ao longo da semana e publicada **na segunda por volta das
  8h30 BRT**. Segunda feriado, o BCB publica na terça — daí o retrocesso.

---

## Invariantes

1. **Nunca invente número.** Toda mediana citada no resumo tem de estar
   literalmente no texto extraído. Citação entre aspas é preferível a parafrasear
   quando o boletim traz mediana atualizada. Sem inferência, sem projeção.
2. **`output/focus/*.md` nunca é sobrescrito.** Um resumo publicado é registro do
   que se dizia naquela segunda, não rascunho.
3. **Nunca dê push direto em `main`.** Sempre branch `claude/focus-AAAA-MM-DD`
   mais PR.
4. **Erro e aborto ficam no transcript da Routine.** Não existe log paralelo no
   repositório; não crie um.

---

## Comandos

```bash
pip install -r requirements.txt
pytest -m "not network"     # o que o CI roda
pytest                      # inclui o teste que baixa de verdade
python src/baixar_focus.py  # baixa para data/
python src/extrair_texto.py # extrai o último PDF de data/
```

As dependências são **pinadas exatamente** (`requests==2.32.3`,
`pdfplumber==0.11.4`, `pytest==8.3.3`). O marcador `network` está em
`pytest.ini`: o único teste que sai para a rede é o de download real, e o CI o
pula.

| workflow | quando | escreve? |
|---|---|---|
| `ci.yml` | push em `main` e PR | não — `pytest -m "not network"` |
| `focus-download.yml` | **só manual** | sim — commita `data/focus_*.pdf` e `.txt` |

`focus-download.yml` é `workflow_dispatch` puro: **não há cron neste
repositório.** O agendamento vive na Routine, fora do git (ver abaixo). Quem
procurar o cron aqui não acha.

---

## Routine CCR — configuração

- **Nome da routine = nome do repositório** (`resumo-focus`)
- **Schedule:** segunda às 10h BRT = `0 13 * * 1` (UTC)
- **Modelo:** `claude-sonnet-4-6`
- **Repositório em `sources`:** com `"allow_unrestricted_git_push": true`
- **MCP do GitHub é obrigatório** — a Routine usa as ferramentas MCP para criar
  branch, commitar e abrir o PR

```json
"sources": [
  {"git_repository": {
    "url": "https://github.com/analisemacro/resumo-focus",
    "allow_unrestricted_git_push": true
  }}
],
"mcp_connectors": [
  {"github": {}}
]
```

---

## Armadilhas e pontas soltas

- **`ultima_segunda()` não é usada pela coleta.** `baixar()` parte de
  `date.today()` e retrocede; a função existe, tem cinco testes e **só roda nos
  testes**. Não a trate como o caminho de produção — e, se for removê-la, saiba
  que leva cinco testes junto.
- **O `README.md` cita um `setup.sh` que não existe** no repositório. Ou o
  arquivo se perdeu, ou a seção envelheceu; não procure por ele.
- **O último resumo em `output/focus/` é de 26/06/2026.** Se a Routine deveria
  estar rodando semanalmente, há meses sem entrega — confirme o agendamento no
  CCR antes de concluir que o código está quebrado.
- **A data do arquivo é a da publicação, não a da coleta.** As duas diferem, e
  trocá-las desalinha o `.md` do `.pdf` que o originou.

---

## Convenções (comuns aos outros repositórios)

- **Português** em comentário, docstring, nome de função, teste e mensagem de
  commit. Comentário e identificador **sem acento**; texto de saída **com**.
- **Nenhum teste toca a rede**, exceto o marcado `network`, que o CI pula.
- **Mudança entra por PR com CI verde.**
- **O GitHub App não escreve em `.github/workflows/`**: use o editor web e
  confira o resultado depois.
- **Vícios de escrita a evitar no resumo:** "cirúrgico", "do zero", "próximo
  nível", "virada de chave", "destrava", "regra de ouro", a construção "não é X,
  é Y", tríades decorativas ("rápido, eficiente e escalável"), e aberturas como
  "Vale ressaltar que" ou "É importante destacar".

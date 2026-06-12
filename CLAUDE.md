# Resumo Focus — Routine semanal

## Objetivo

Toda segunda-feira, baixar o boletim Focus do BCB em PDF, gerar resumo executivo + análise das três principais revisões da semana, abrir PR com o markdown pronto.

## O que é o Focus

Pesquisa do Banco Central do Brasil que consolida expectativas de cerca de 100 instituições financeiras para os principais indicadores macroeconômicos (IPCA, PIB, Selic, câmbio, conta corrente). Coleta feita ao longo da semana, publicação na segunda-feira por volta das 8h30 BRT. Quando a segunda é feriado, o BCB publica na terça.

## Fonte

- Página: `https://www.bcb.gov.br/publicacoes/focus`
- PDF: `https://www.bcb.gov.br/content/focus/focus/R{AAAAMMDD}.pdf` (data da publicação)
- PDF tem ~4 páginas, 150–250 KB

## Convenções

- Arquivos de saída: `output/focus/focus_AAAA-MM-DD.md` (nunca sobrescreve)
- Branch: `claude/focus-AAAA-MM-DD` (data da publicação do boletim)
- Erros e abortos ficam no transcript da execução da Routine — não há log paralelo no repositório
- O resumo é gerado pelo próprio agente da Routine lendo o `.txt` produzido por `extrair_texto.py` — sem chamada à API externa, sem `ANTHROPIC_API_KEY`

## Regras

- Nunca inventar número. Toda mediana citada deve estar no PDF.
- Citação literal entre aspas é preferível ao parafrasear quando o boletim traz mediana atualizada.
- Nunca dar push direto em `main`. Sempre branch `claude/*` + PR.
- Quando segunda é feriado, o script retrocede dia a dia até 7 dias antes de desistir.

## Routine CCR — Configuração

A routine remota (Anthropic CCR) que gera o resumo usa estas convenções:

- **Nome da routine = nome do repositório** (`resumo-focus`)
- **Schedule:** toda segunda às 10h00 BRT = `0 13 * * 1` (UTC)
- **Modelo:** `claude-sonnet-4-6`
- **Repositório em `sources`:** com `"allow_unrestricted_git_push": true`
- **MCP connectors:** o **MCP do GitHub** é obrigatório — a Routine usa as ferramentas MCP para criar branch, commitar e abrir PR

Exemplo completo da configuração na criação da routine via `/schedule`:
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



## Vícios a evitar no texto

Nunca usar: "cirúrgico", "do zero", "próximo nível", "virada de chave", "destrava", "regra de ouro", construção "não é X, é Y", tríades decorativas ("rápido, eficiente e escalável"), aberturas como "Vale ressaltar que" ou "É importante destacar".

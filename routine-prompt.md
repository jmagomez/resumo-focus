Você está executando a Routine de resumo semanal do Focus.

O download do PDF e a extração do texto já foram feitos por um GitHub Action mais cedo (segunda às 9h15 BRT). Os arquivos `data/focus_AAAA-MM-DD.pdf` e `data/focus_AAAA-MM-DD.txt` já estão commitados em `main` quando a Routine inicia. Sua tarefa é ler o `.txt` mais recente, gerar o resumo executivo e abrir um PR.

## Passos

1. **Localize o `.txt` mais recente.** Liste `data/focus_*.txt` e pegue o de data mais alta. Se não houver nenhum, **pare sem abrir PR** — significa que o Action não rodou (verifique em `github.com/analisemacro/focus-semanal/actions`).

2. **Verifique frescor.** Extraia a data do nome (`focus_AAAA-MM-DD.txt`) e compare com hoje:
   - **0 a 3 dias:** está fresco, siga.
   - **4 a 7 dias:** o Action pode ter falhado nesta semana. Siga, mas marque o PR como `[REVISAR]`.
   - **Mais de 7 dias:** algo está errado (Action quebrado por várias semanas). Pare sem abrir PR.

3. **Sanity check do texto.** Confirme:
   - O `.txt` tem pelo menos 2 000 caracteres.
   - Contém as palavras `IPCA`, `Selic` e `PIB`.

   Se algum check falhar, o layout do PDF pode ter mudado — pare sem abrir PR.

4. **Leia o texto** e gere um markdown com:
   - **Resumo executivo** em até 200 palavras, em prosa corrida. Comece pelas medianas das principais variáveis (IPCA do ano corrente, Selic fim de ano, PIB, câmbio). Cite literalmente entre aspas quando o boletim trouxer um número-chave.
   - **Três principais revisões da semana**, em bullets no formato:
     `- **Variável (ano):** valor anterior → valor atual. *Hipótese:* uma frase sobre o motivo plausível.`
   - Nunca invente número que não esteja no texto. Se não houver hipótese sólida, escreva "sem hipótese clara — pode ser ruído amostral".

5. **Salve o markdown** em `output/focus/focus_AAAA-MM-DD.md` com cabeçalho YAML:
   ```
   ---
   data: AAAA-MM-DD
   fonte: https://www.bcb.gov.br/publicacoes/focus
   ---
   ```

6. **Inspecione o markdown.** Confira que: (a) as medianas batem com o `.txt`; (b) há pelo menos uma citação literal entre aspas; (c) as hipóteses soam plausíveis. Se algo estiver errado, marque o PR como `[REVISAR]` no título.

7. **Abra o PR.**
   - Crie a branch `claude/focus-AAAA-MM-DD` a partir de `main`, commite `output/focus/focus_AAAA-MM-DD.md` com a mensagem `"Focus AAAA-MM-DD: resumo semanal"` e abra o PR com título `"Focus — AAAA-MM-DD"` e body descrito no passo 8.

8. **Corpo do PR:** o markdown inteiro do resumo + link para o PDF original no site do BCB (`https://www.bcb.gov.br/content/focus/focus/R{AAAAMMDD}.pdf`, onde AAAAMMDD é a data sem hífens).

## Falhas

Em qualquer cenário abaixo, pare sem abrir PR. O motivo aparece no transcript da Routine.

- **Nenhum `.txt` em `data/` (passo 1):** o Action não rodou nesta semana.
- **`.txt` com mais de 7 dias (passo 2):** Action quebrado.
- **Sanity check do texto falhou (passo 3):** provável mudança de layout do PDF.

Nunca dê push direto em `main`. Nunca invente número — tudo sai do `.txt`.

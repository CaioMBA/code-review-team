# Report template

Fill this exactly, in the user's language. Skip a section only where noted. Number fixes across the whole list so the user can say "fix 1 and 3".

```markdown
# Review panel: <project or branch>
**What the code does:** <one sentence>
**Scope reviewed:** <diff / branch vs main / files / pasted code> · **Expected load assumed:** <one user / many users>

## Verdict: APPROVED TO SHIP | REJECTED
<one sentence with the main reason>

## What to fix (most severe first)
1. [CRITICAL] `path/file.ext:42` <problem in one line>
   - **Case:** <input or situation → wrong result>
   - **Fix:** <smallest fix, or a short diff>
   (found by: hacker, tester)
2. [HIGH] ...

## Confirm before shipping
<hotspots as yes/no questions for the user; omit the section if none>
- `path/file.ext:10` <question>, if <answer>, then <what to do>

## Older problems (not blocking)
<findings tagged "existing", most severe first; omit if none>

## Tool pass
| Command | Result |
|---|---|
| `npm test` | 2 failed: `cart.test.js` "applies coupon once" |

## Panel notes
### 1. Hacker
### 2. Confused user
### 3. Senior engineer
### 4. Tester
<2–5 lines each: what it checked and its key findings; list any new test files created>

**Not checked:** <what mattered and couldn't be checked, or "nothing">
```

Close with: *The panel lowers the risk but doesn't guarantee bug-free code. Before shipping, commit and check the changes.*

Nothing to fix: still give the verdict, then "Nothing to fix." and one line on what was checked.

## Labels

Use the user's language. Portuguese labels are fixed; for other languages, translate the English ones naturally.

| English | Português |
|---|---|
| Review panel | Banca de revisão |
| What the code does | O que o código faz |
| Scope reviewed | Escopo revisado |
| Expected load assumed | Carga esperada considerada |
| Verdict | Veredito |
| APPROVED TO SHIP | APROVADO PRA SUBIR |
| REJECTED | REPROVADO |
| What to fix (most severe first) | O que corrigir (do mais grave ao menos grave) |
| CRITICAL / HIGH / MEDIUM / LOW | CRITICO / ALTO / MÉDIO / BAIXO |
| Case / Fix / found by | Caso / Correção / achado por |
| Confirm before shipping | Confirme antes de subir |
| Older problems (not blocking) | Problemas antigos (não bloqueiam) |
| Tool pass | Ferramentas rodadas |
| Panel notes | Relatórios da banca |
| Hacker / Confused user / Senior engineer / Tester | Hacker / Usuário confuso / Programador sênior / Testador |
| Not checked | Não verificado |
| Closing line | *A banca diminui o risco, mas não garante código sem bug. Antes de subir, faça um commit e confira as mudanças.* |

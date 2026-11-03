# Report template

Fill this exactly, in the user's language. Keep these sections and their order; don't rename, merge or drop them, and skip one only where noted. Number fixes across the whole list so the user can say "fix 1 and 3". Every fix is one problem with its own `file:line` (for a problem with a whole file, cite the first line it concerns); never bundle several small problems into one item.

```markdown
# Review panel: <project or branch>
**What the code does:** <one sentence>
**Scope reviewed:** <diff / branch vs main / files / pasted code> · **Expected load assumed:** <one user / few users / many users, and where that came from>
**Extra reviewers:** <UI & accessibility / Performance / Data & deploy: joins or not, and why, one short clause each>

## Verdict: APPROVED TO SHIP | REJECTED
<one sentence with the main reason>

## What to fix (most severe first)
1. [CRITICAL] `path/file.ext:42` <problem in one line>
   - **Case:** <input or situation → wrong result>
   - **Fix:** <smallest fix, or a short diff>
   (found by: hacker, tester - name each reviewer)
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
<only Step 1 commands; scripts and tests the reviewers wrote go in their panel notes>

## Panel notes
### 1. Hacker
### 2. Confused user
### 3. Senior engineer
### 4. Tester
### 5. UI & accessibility
### 6. Performance
### 7. Data & deploy
<2-5 lines each: what it checked and its key findings; list any new test files created. Write sections 5-7 only for reviewers that joined. Add "Used: <helper skills>" only when a reviewer used one; never mention skills that weren't available.>

**Not checked:** <what mattered and couldn't be checked, or "nothing">
```

Close with: *The panel lowers the risk but doesn't guarantee bug-free code. Before shipping, commit and check the changes.*

Report written to a file: the chat still shows the verdict and the same numbered fix list, item for item.

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
| CRITICAL / HIGH / MEDIUM / LOW | CRÍTICO / ALTO / MÉDIO / BAIXO |
| Case / Fix / found by | Caso / Correção / achado por |
| Confirm before shipping | Confirme antes de subir |
| Older problems (not blocking) | Problemas antigos (não bloqueiam) |
| Tool pass | Ferramentas rodadas |
| Panel notes | Relatórios da banca |
| Hacker / Confused user / Senior engineer / Tester | Hacker / Usuário confuso / Programador sênior / Testador |
| UI & accessibility / Performance / Data & deploy | UI e acessibilidade / Desempenho / Dados e deploy |
| Extra reviewers / joins / doesn't join | Revisores extras / entra / não entra |
| Used | Usou |
| Not checked | Não verificado |
| Closing line | *A banca diminui o risco, mas não garante código sem bug. Antes de subir, faça um commit e confira as mudanças.* |

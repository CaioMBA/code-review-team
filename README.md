# Code Review Team

*(formerly Banca de Revisão)*

A skill for AI coding agents (OpenCode, Claude Code, and any agent that reads `SKILL.md`). It puts a **panel of 5 reviewers** on your code, and their job is to try to reject it before you ship. It's built for solo developers, who usually have no colleague to review their code and no CI to catch mistakes.

| Reviewer | Looks for |
|---|---|
| 🕵️ Hacker | secrets in code, leaked data, injection, missing auth, weak tokens, fake or risky dependencies |
| 🤷 Confused user | empty fields, wrong types, double clicks, repeated actions, failing APIs, and the error the user actually sees |
| 🧓 Senior engineer | code that duplicates what already exists, broken callers, changes outside the task, half-finished code |
| 🧪 Tester | runs the tests, catches tests that can't fail, writes the missing ones |
| 👔 Lead | checks every finding and gives **one** verdict: **APPROVED TO SHIP** or **REJECTED** |

**What you get:**

- **Tool pass first.** It runs the linters, type checkers, tests, secret scanners and dependency audits your project already has. It never installs anything.
- **Full review, every time.** The reviewers read the code *around* your change, so a 5-line helper that copies an existing one gets caught.
- **A quality gate on new code only.** Only problems your change adds decide the verdict. Older problems are listed but don't block your push.
- **Hotspots.** When a security question depends on what you meant ("is this route public on purpose?"), the panel asks you instead of guessing.
- **Handles AI-written code.** It checks for packages that don't exist, stub functions, tests that mock what they test, and edits outside what you asked for.
- **One ranked fix list.** Each fix has `file:line`, a concrete failing case, and the smallest fix. Ask it to fix things and it fixes them one by one, then runs the whole panel again.
- **Answers in your language.** English by default; Portuguese and others work too.

## Install

Clone this folder into your agent's skills folder:

```bash
# OpenCode
git clone https://github.com/CaioMBA/code-review-team ~/.config/opencode/skills/code-review-team

# Claude Code
git clone https://github.com/CaioMBA/code-review-team ~/.claude/skills/code-review-team
```

Or use the [skills CLI](https://github.com/vercel-labs/skills): `npx skills add CaioMBA/code-review-team`

## Use

Just ask in your own words:

- "is this ready to push?"
- "review my feature/login branch before I merge"
- "Cursor wrote this, can I deploy it?"
- "fix 1 and 3 and review again"
- "revisa antes de eu subir" / "chama a banca"

By default it reviews everything that would ship: uncommitted changes plus your branch compared with the main branch. It also works on files you name or code you paste into the chat. To review only the new lines, say so.

## Layout

```
SKILL.md                      the coordinator: scope, tool pass, panel, gate, report, fix loop
references/hacker.md          one checklist per reviewer, each loaded only by that reviewer
references/confused-user.md
references/senior.md
references/tester.md
references/tools.md           lint/type/test/audit commands for each stack
references/report-template.md report structure and label translations
evals/                        test cases with planted bugs (claude plugin eval format)
```

## Skill tests

`evals/` has 6 cases, each with planted bugs: 3 in Portuguese and 3 in English. They cover a cart branch with a coupon, a pasted signup form, fixing and reviewing again, an AI-written password-reset branch, a tiny change that duplicates an existing helper, and a clean change in a repo that already had a leaked key (the verdict should still be APPROVED). In the first round (skill-creator, graded by independent agents), this version passed 50 of 50 checks, and the previous Portuguese-only version passed 45 of 50. Run them with `claude plugin eval . --scaffold --allow-tools Write,Edit,Bash`.

> The panel lowers the risk, but it doesn't guarantee bug-free code. Before you ship, commit and check the changes.

## Português

A skill responde no idioma em que você escreve. É só pedir: "tá pronto pra eu dar push?", "revisa esse código antes de eu subir", "corrige o que a banca achou e revisa de novo". O veredito sai como **APROVADO PRA SUBIR** ou **REPROVADO**.

## Credits

Based on the review-panel prompt published by [Clube das Skills](https://clubedasskills.com.br). Ideas borrowed from CodeRabbit (tool pass, walkthrough, ready-to-apply fixes) and SonarQube (quality gate on new code, security hotspots).

## License

[MIT](LICENSE)

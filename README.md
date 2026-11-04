# Code Review Team

*(formerly Banca de Revisão)*

A skill for AI coding agents (OpenCode, Claude Code, and any agent that reads `SKILL.md`). It puts a **review squad** on your code, and their job is to try to reject it before you ship. Four reviewers always run, three more join when your change touches their area, and they all work in parallel. It's built for solo developers, who usually have no colleague to review their code and no CI to catch mistakes.

| Reviewer | Joins | Looks for |
|---|---|---|
| 🕵️ Hacker | always | secrets in code, leaked data, injection, missing auth, weak tokens, fake or risky dependencies |
| 🤷 Confused user | always | empty fields, wrong types, double clicks, repeated actions, failing APIs, and the error the user actually sees |
| 🧓 Senior engineer | always | code that duplicates what already exists, broken callers, changes outside the task, half-finished code |
| 🧪 Tester | always | runs the tests, catches tests that can't fail, writes the missing ones |
| ♿ UI & accessibility | front-end files change | flows keyboard or screen-reader users can't finish, missing labels, contrast, phone layouts |
| 📈 Performance | many users, or the change adds queries, loops over data, caches, jobs or API calls | what breaks at scale, from reading the code (it never sends traffic) |
| 🗄️ Data & deploy | migrations, Docker, CI or config change | migrations that lose data, deploys that crash, settings with no default |
| 👔 Lead | always | checks every finding and gives **one** verdict: **APPROVED TO SHIP** or **REJECTED** |

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

## Cost and model tiers

Each reviewer runs on a model tier that fits its job: the confused user, tester and UI reviewers on a **small** model, the senior, performance and data & deploy reviewers on a **mid** model, and the hacker on a **top** model when the change touches auth, tokens, payments, crypto or secrets (mid otherwise). The lead runs on your own session's model and re-checks every finding. Changes of 30 lines or fewer get two combined reviewers instead of four to seven; ask for "the full panel" to override.

In Claude Code the tiers map to `haiku`, `sonnet` and `opus` automatically. In OpenCode, add three agents to `opencode.json` to enable them (otherwise every reviewer uses your default model):

```json
"agent": {
  "review-small": { "mode": "subagent", "description": "code-review-team small-tier reviewer", "model": "anthropic/claude-haiku-4-5" },
  "review-mid":   { "mode": "subagent", "description": "code-review-team mid-tier reviewer", "model": "anthropic/claude-sonnet-4-5" },
  "review-top":   { "mode": "subagent", "description": "code-review-team top-tier reviewer", "model": "anthropic/claude-opus-4-5" }
}
```

Use any provider's models; pick a small, a mid and a top one.

Tiers are recommended, not required. If your company only gives you some models, the panel still runs: a reviewer whose model is refused or unavailable is restarted once on the next tier down, else on your default model, and the report says which reviewers ran below their tier. To skip tiers entirely, say "use my default model" (or put that in your `AGENTS.md`/`CLAUDE.md`).

## Works better with (optional)

The squad is complete on its own. If any of these skills are installed next to it, the matching reviewer uses them, read-only, and the report keeps the same format. None is required, and a missing one is never reported.

| Skill | Used by | Adds |
|---|---|---|
| [security-audit](https://github.com/cloudflare/security-audit-skill) | Hacker, Performance, Data & deploy | deeper attack-class checks, loaded only for what your change touches (guidance mode, never a full audit) |
| [ponytail](https://github.com/DietrichGebert/ponytail) (`ponytail-review`, `ponytail-debt`) | Senior | lean checks (delete, reuse, stdlib, yagni) and `shortcut:` markers whose limit you've outgrown |
| playwright-cli | Confused user, UI | drives the changed flow in a real browser, if the app starts locally with no setup |
| ui-ux-pro-max, impeccable, review-animations, mobile-native | UI | accessibility and UX rules, motion and mobile-web checks |
| superpowers (`receiving-code-review`, `systematic-debugging`, `verification-before-completion`) | fix loop | checks each finding before fixing, debugs failing fixes, verifies before claiming round 2 |
| a `memory` tool (e.g. opencode-mem) | Lead | remembers your answers to hotspots and shows them next time |
| `ast-grep` | Senior | structural search for duplicates and callers |

## Layout

```
SKILL.md                      the coordinator: scope, roles that join, tool pass, panel, gate, report, fix loop
references/hacker.md          one checklist per reviewer, each loaded only by that reviewer
references/confused-user.md
references/senior.md
references/tester.md
references/ui.md              joins on front-end changes
references/performance.md     joins on many users or queries/loops/caches/jobs/API calls
references/data-deploy.md     joins on migrations, Docker, CI, config
references/tools.md           lint/type/test/audit commands for each stack
references/report-template.md report structure and label translations
evals/                        test cases with planted bugs (claude plugin eval format)
```

## Skill tests

`evals/` has 10 cases with planted bugs, 4 in Portuguese and 6 in English: a cart branch with a coupon, a pasted signup form, fixing and reviewing again, an AI-written password-reset branch, a tiny change that duplicates an existing helper, a clean change in a repo that already had a leaked key (the verdict should still be APPROVED), a newsletter form with accessibility bugs, an order list that breaks at the stated load, a migration that drops data, and an integration case that checks the optional skills are used without changing the report format. In the latest round (Claude Code, 1 run per case, graded by independent agents), 5 cases passed all 44 grader checks: 4 with no other skills reachable and the integration case (the hacker read security-audit on opus, the senior read ponytail-review). With model tiers, a review cost $0.50 (small change) to $1.17, down from $1.10-2.40 when every reviewer ran on Sonnet. Run them with `claude plugin eval . --scaffold --allow-tools Write Edit Bash`. On Windows that command refuses to run Bash (there's no sandbox backend), so run each case with `claude -p` in a scaffolded folder instead, with Git bash first on `PATH`.

> The panel lowers the risk, but it doesn't guarantee bug-free code. Before you ship, commit and check the changes.

## Português

A skill responde no idioma em que você escreve. É só pedir: "tá pronto pra eu dar push?", "revisa esse código antes de eu subir", "corrige o que a banca achou e revisa de novo". O veredito sai como **APROVADO PRA SUBIR** ou **REPROVADO**.

## Credits

Based on the review-panel prompt published by [Clube das Skills](https://clubedasskills.com.br). Ideas borrowed from CodeRabbit (tool pass, walkthrough, ready-to-apply fixes) and SonarQube (quality gate on new code, security hotspots).

## License

[MIT](LICENSE)

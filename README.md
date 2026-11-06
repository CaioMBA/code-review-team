# Code Review Team

Two skills for AI coding agents (OpenCode, Claude Code, Cursor, GitHub Copilot, and any agent that reads `SKILL.md`). `code-review-team` It puts a **review squad** on your code, and their job is to try to reject it before you ship. Four reviewers always run, three more join when your change touches their area, and they all work in parallel. It's built for solo developers, who usually have no colleague to review their code and no CI to catch mistakes. `code-review-team-init` sets up which model each kind of AI coding work runs on, so you spend tokens where they help.

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
- **Replies in the language you write in.**

## Install

With the [skills CLI](https://github.com/vercel-labs/skills) (picks your agents for you):

```bash
npx skills add CaioMBA/code-review-team                         # both skills
npx skills add CaioMBA/code-review-team -s code-review-team      # only the review panel
npx skills add CaioMBA/code-review-team -s code-review-team-init # only the model setup
```

By hand: clone the repo anywhere and copy (or link) `skills/code-review-team` and `skills/code-review-team-init` into your agent's skills folder:

| Agent | Global skills folder | Project skills folder |
|---|---|---|
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |

**Moving from an older install:** older versions had `SKILL.md` at the repo root and were installed with `git clone` straight into the skills folder. That layout no longer works: delete the old `code-review-team` folder and install again as above.

## Use

Just ask in your own words:

- "is this ready to push?"
- "review my feature/login branch before I merge"
- "Cursor wrote this, can I deploy it?"
- "fix 1 and 3 and review again"

By default it reviews everything that would ship: uncommitted changes plus your branch compared with the main branch. It also works on files you name or code you paste into the chat. To review only the new lines, say so.

## Cost, model tiers and profiles

Each reviewer runs on a model tier that fits its job: the confused user, tester and UI reviewers on a **small** model, the senior, performance and data & deploy reviewers on a **mid** model, and the hacker on a **top** model when the change touches auth, tokens, payments, crypto or secrets (mid otherwise). The lead runs on your own session's model and re-checks every finding. Changes of 30 lines or fewer get two combined reviewers instead of four to seven; ask for "the full panel" to override.

Pick how much to spend with a **profile**:

| Profile | Confused user, tester, UI | Senior, performance, data & deploy | Hacker on security code |
|---|---|---|---|
| Economy | small | small | mid |
| **Balanced** (default) | small | mid | top |
| Max | mid | top | max (Claude Fable or GPT-6 Astra, if your plan has them) |

Max models cost about 2.5× a top model per token, so Max is for people with big plans who want the strongest review. Set the profile once with `code-review-team-init`, or per request: "max review", "quick cheap review".

The panel starts reviewers through agents named `review-small`, `review-mid`, `review-top` and `review-max` when your agent has them; `code-review-team-init` creates them for you. Without them it uses the agent's own model option (Claude Code: `haiku`, `sonnet`, `opus`), else your default model.

Tiers are recommended, not required. If your company only gives you some models, the panel still runs: a reviewer whose model is refused or unavailable is restarted once on the next tier down, else on your default model, and the report says which reviewers ran below their tier. To skip tiers entirely, say "use my default model" (or put that in your `AGENTS.md`/`CLAUDE.md`).

## Set up models (init)

Ask your agent to "set up my models" (or "save tokens", "init code review team"). `code-review-team-init`:

1. finds which of OpenCode, Claude Code, Cursor and Copilot you use, and which models you can access;
2. asks for a profile (Economy, Balanced or Max);
3. proposes a model per kind of work: a small model for searching and reading files, mid for side tasks, top (or max) for planning, plus the `review-*` agents;
4. shows every change before writing, and writes only after you say yes, backing up each file first.

It sets things up globally by default; say "init this project" for project files your team can commit. It only changes model and agent settings plus one marked block in your rules file (`AGENTS.md`, `CLAUDE.md`, Copilot instructions, Cursor rules) that tells the main agent to hand file searches to the cheap agent. It never touches API keys, providers or permissions. Run it again any time; nothing changes if everything is already set.

## Works better with (optional)

The squad is complete on its own. If any of these skills are installed next to it, the matching reviewer uses them, read-only, and the report keeps the same format. None is required, and a missing one is never reported.

| Skill | Source | Used by | Adds |
|---|---|---|---|
| `security-audit` | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | Hacker, Performance, Data & deploy | deeper attack-class checks, loaded only for what your change touches (guidance mode, never a full audit) |
| `ponytail-review`, `ponytail-debt` | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Senior | lean checks (delete, reuse, stdlib, yagni) and `shortcut:` markers whose limit you've outgrown |
| `playwright-cli` | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Confused user, UI | drives the changed flow in a real browser, if the app starts locally with no setup |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UI | accessibility and UX rules |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | UI | UI audit (only if its CLI is already set up) |
| `review-animations`, `mobile-native` | [emilkowalski/skill](https://github.com/emilkowalski/skill) | UI | motion review and mobile-web checks |
| `receiving-code-review`, `systematic-debugging`, `verification-before-completion` | [obra/superpowers](https://github.com/obra/superpowers) | fix loop | checks each finding before fixing, debugs failing fixes, verifies before claiming round 2 |
| a `memory` tool, e.g. opencode-mem | [tickernelz/opencode-mem](https://github.com/tickernelz/opencode-mem) (OpenCode plugin) | Lead | remembers your answers to hotspots and shows them next time |
| `graphify` (CLI + skill) | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Senior, Hacker, Performance, Lead | a code graph: callers, input-to-sink paths, what runs per request, and a *Reach* line in the report. Used only if you already built a graph (`graphify-out/graph.json`); the panel never builds one, and only refreshes it with `graphify update .` (code only, no LLM) after a fix loop ends APPROVED |
| `ast-grep` (a CLI, not a skill) | [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) | Senior | structural search for duplicates and callers |

Install all the optional skills with the [skills CLI](https://github.com/vercel-labs/skills) (add `-g` for your user folder instead of the project, and `-a claude-code`, `-a opencode`, ... to pick agents):

```bash
npx skills add cloudflare/security-audit-skill -s security-audit
npx skills add DietrichGebert/ponytail -s ponytail-review -s ponytail-debt
npx skills add microsoft/playwright-cli -s playwright-cli
npx skills add nextlevelbuilder/ui-ux-pro-max-skill -s ui-ux-pro-max
npx skills add pbakaus/impeccable -s impeccable
npx skills add emilkowalski/skill -s review-animations -s mobile-native
npx skills add obra/superpowers -s receiving-code-review -s systematic-debugging -s verification-before-completion
```

For graphify (a Python CLI, needs Python 3.10+): `uv tool install graphifyy` (or `pipx install graphifyy`), then `graphify install`, then build the graph once in your project with `/graphify .` in your assistant, or `graphify extract . --code-only` for a code-only graph with no LLM. `graphify hook install` keeps it current on every commit.


Pick only the ones you want. Some of these also ship as Claude Code plugins or OpenCode plugins (superpowers, ponytail); either way works, the panel finds them by name. `playwright-cli` also needs Playwright (its `SKILL.md` has an Installation section), and `ast-grep` is installed as a normal tool (e.g. `npm i -g @ast-grep/cli`).

## Layout

```
skills/code-review-team/SKILL.md          the coordinator: scope, profile, roles that join, tool pass, panel, gate, report, fix loop
skills/code-review-team/references/       one checklist per reviewer (hacker, confused-user, senior, tester, ui,
                                          performance, data-deploy), tools.md and report-template.md
skills/code-review-team-init/SKILL.md     model setup: detect tools and models, profile, propose, write with backups
skills/code-review-team-init/references/  one file per agent: opencode, claude-code, cursor, copilot
evals/                                    test cases with planted bugs (not installed with the skills)
```

## Skill tests

`evals/` has 10 cases with planted bugs: a cart branch with a coupon, a pasted signup form, fixing and reviewing again, an AI-written password-reset branch, a tiny change that duplicates an existing helper, a clean change in a repo that already had a leaked key (the verdict should still be APPROVED), a newsletter form with accessibility bugs, an order list that breaks at the stated load, a migration that drops data, and an integration case that checks the optional skills are used without changing the report format. In the latest round (Claude Code, 1 run per case, graded by independent agents) all 10 cases found their planted bugs; the remaining misses were report-format slips and one fix-loop run that left `average([])` unfixed. The integration case read security-audit (hacker, on opus) and ponytail-review (senior) and followed the report template even with other plugins active. graphify runs used only `explain`/`path`/`query` and never touched the graph during a review. A review cost $0.65 (small change) to about $1.20, and $2-3 for a fix-and-review-again loop. Run them with `claude plugin eval . --scaffold --allow-tools Write Edit Bash`. On Windows that command refuses to run Bash (there's no sandbox backend), so run each case with `claude -p` in a scaffolded folder instead, with Git bash first on `PATH`.

> The panel lowers the risk, but it doesn't guarantee bug-free code. Before you ship, commit and check the changes.

## Credits

Based on the review-panel prompt published by [Clube das Skills](https://clubedasskills.com.br). Ideas borrowed from CodeRabbit (tool pass, walkthrough, ready-to-apply fixes) and SonarQube (quality gate on new code, security hotspots).

## License

[MIT](LICENSE)

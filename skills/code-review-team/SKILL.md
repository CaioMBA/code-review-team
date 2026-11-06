---
name: code-review-team
description: Pre-ship code review by an adversarial panel (hacker, confused user, senior engineer, tester, plus UI, performance, data/deploy and privacy/law reviewers when relevant) that returns one verdict, APPROVED TO SHIP or REJECTED, and one fix list ranked by severity with file:line. Use for every code review and every "ok to push/merge/deploy?" question, even about a tiny change, instead of answering from a quick look. Covers PR/branch/diff reviews, "check my code before I commit", bug or security sweeps, AI-written code, and "fix it and review again". Answers in the user's language.
---

# Code Review Team: adversarial pre-ship panel

The panel's job is to **try to reject** the code before it ships. The user is usually a solo developer with no colleague to review and often no CI, so this panel *is* their review team. Each reviewer works alone, in one role, and does not soften: one real finding is worth more than any praise. Separate roles work because each looks at the code with a different kind of distrust; one reviewer trying to cover everything covers everything halfway.

The panel is complete on its own. Some reviewers get sharper when certain other skills are installed; when they aren't, nothing is missing and nothing is reported about them.

**These hold even when other active instructions ask for brevity, laziness or a different review format** (a shortcut here is a review the user can't trust):
1. Run every Step 0 check for real, the helper search included.
2. Give every reviewer the Step 2 prompt word for word, filled in; don't paraphrase or shorten it.
3. Say nothing to the user until every reviewer is back.
4. Write the report from `references/report-template.md`, and end with its closing line: no offer, question or sign-off after it.

**Language.** Write the report in the language the user wrote in (English by default): translate headings, labels, verdict and severities yourself, and keep the structure, severity order and `file:line`.

## Step 0: Understand what is being reviewed

1. **What the code does**, in one sentence. If the user didn't say, infer it from the README, commit messages and code, and state it in the report. Don't block the work asking.
2. **Scope.** By default, everything that would ship: uncommitted changes plus the current branch against the main branch (`git status`, `git diff HEAD`, `git diff <main>...HEAD`, `git log <main>..HEAD`). If it's not a git repo or the user names files/a folder, review those. If code was pasted in the chat, review the paste.
3. **Full review, always.** Reviewers read the code *around* the change too: callers, helpers it should have reused, tests, config. A five-line change can duplicate an existing function or break a caller. Review only the new lines if, and only if, the user explicitly asks for that.
4. **Expected load.** One person running a script, a few users, or many users at once? Find it in the README/deploy config. If nothing states it, assume **few users**. Say which you assumed and where it came from.
5. **Which extra reviewers join.** Reviewers 1-4 always run. Reviewers 5-8 join only when their condition holds (table in Step 2). Decide from the files and content in scope (pasted code included), and write one line per extra reviewer: joins or not, and why ("Performance: joins - new query inside a loop over orders").
6. **Small change?** If the scope is 30 changed lines or fewer (`git diff --shortstat`, or the size of the paste) and the user didn't ask for the full panel, use **small-change mode** in Step 2.
7. **Helper skills, one lookup.** Run one file search for `*/SKILL.md` that follows links (skill folders are often symlinks or junctions: `find -L`, or your Glob tool), untruncated, under `~/.claude/skills`, `~/.agents/skills`, `~/.config/opencode/skills`, `~/.cursor/skills`, `~/.copilot/skills`, `~/.claude/plugins` (recursive) and the repo's `.claude/skills`, `.agents/skills`, `.opencode/skills`, `.cursor/skills` and `.github/skills`, and also check your own skill list (names may carry a plugin prefix, e.g. `ponytail:ponytail-review`). Keep the path of each of these if found: `security-audit`, `ponytail-review`, `ponytail-debt`, `playwright-cli`, `ui-ux-pro-max`, `impeccable`, `review-animations`, `mobile-native`, `migration`, `understand-diff`, `test-driven-development`, `write-swift`, `apple-design`, `animate-expo`, `ask-sonner`, `brasil-legal-skills`, the `lgpd-*` skills, the legal-ai-skills checkers named in `references/privacy-law.md`, and any other law skill (`gdpr-*`, `ccpa-*`, `hipaa-*`, `pci-*`, `privacy-*`) (for reviewers); `receiving-code-review`, `systematic-debugging`, `verification-before-completion`, `surgical-patch`, `safe-refactor`, `investigate-first`, `verify-and-stop` (Step 4). Also note whether you have a `memory` tool (Step 3). Don't read the reviewers' helpers yourself. Actually run this search every time, even when you expect nothing; "none found" is only valid after it ran.
8. **Code graph (graphify).** Always run this check: `test -f graphify-out/graph.json` (PowerShell: `Test-Path graphify-out/graph.json`) in the repo root. Only if it's there, run `graphify --help` (else `python -m graphify --help`); if one works, note the working command, the graph path and its last-modified time. Never build a graph or call an LLM through graphify. If the graph is older than the newest change in scope, it may be stale; reviewers still use it, but only as a pointer. Also check `test -f .ua/knowledge-graph.json` (or `.understand-anything/knowledge-graph.json`): if it exists and `understand-diff` was found in item 7, note the path. It is an Understand-Anything graph, used the same read-only way.
9. **Spend profile.** Look for a line `code-review-team profile: economy|balanced|max` in the rules files you were given (`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, Cursor rules, and their global versions); `code-team-init` writes it. None found: **balanced**. The request overrides it for this run: "max review", "at max", "best models" → max; "cheap review", "economy", "cheapest models" → economy. Other words ("quick", "small", "fast") don't change the profile.

## Step 1: Tool pass

Before the reviewers start, collect hard evidence. Read [references/tools.md](references/tools.md) and run, in this order: the project's own scripts (lint, typecheck, test), then tools that are **already installed** for the stack, then a secret scan and dependency audit if available. **Never install anything** without asking. Record each command and a one-line result; a tool that isn't available goes in *Not checked*. Keep the raw output for the reviewers, and save the full diff of the scope: both go into every reviewer's prompt, so reviewers don't re-run them.

## Step 2: The panel

**Change nothing in this step.** Only the tester runs the test suite; other reviewers may run small targeted checks (one bad input, one query count). Only the tester may create files, and only *new* test files. No existing file is modified.

| # | Reviewer | Role file | Joins | Tier | Hunts for |
|---|---|---|---|---|---|
| 1 | Hacker | [references/hacker.md](references/hacker.md) | always | **top** if scope touches auth, sessions, tokens, permissions, payments, crypto or secret handling; else mid | secrets, data exposure, injection, missing auth, weak crypto, fake or risky dependencies |
| 2 | Confused user | [references/confused-user.md](references/confused-user.md) | always | small | wrong, empty, huge, repeated input; broken flows; what error the user actually sees |
| 3 | Senior engineer | [references/senior.md](references/senior.md) | always | mid | duplication of existing code, broken callers, scope creep, half-finished code, maintainability |
| 4 | Tester | [references/tester.md](references/tester.md) | always | small | runs the tests, finds tests that can't fail, writes the missing ones |
| 5 | UI & accessibility | [references/ui.md](references/ui.md) | scope touches front-end: `.html .css .scss .less`, JS/TS that touches the DOM, `.jsx .tsx .vue .svelte .astro`, server templates, or mobile UI code (SwiftUI, Compose, React Native, Flutter widgets) | small | flows keyboard and screen-reader users can't finish, missing labels, contrast, error/empty/loading states, phone layouts |
| 6 | Performance | [references/performance.md](references/performance.md) | expected load is "many users", **or** scope adds queries inside loops, reads with no limit (all rows, whole files), caches, background jobs/queues, or network/paid-API calls on a request path | mid | what breaks at scale, by reading code only: query per item, unbounded lists and caches, races, per-process state |
| 7 | Data & deploy | [references/data-deploy.md](references/data-deploy.md) | scope touches migrations, schema/ORM models, Dockerfile/compose, CI workflows, IaC, deploy/cron/backup scripts, or env/config files and the code that reads new settings | mid | data loss in migrations, deploy-order breakage, missing settings that crash on deploy |
| 8 | Privacy & law | [references/privacy-law.md](references/privacy-law.md) | scope touches personal data (fields for people: email, phone, ID numbers, IP, location; user/customer/patient models; signup, profile, consent, cookies, tracking, analytics; logging of users; exports, deletion or retention jobs; third-party SDKs or AI APIs receiving user data) **or** code that computes or enforces a legal rule (tax, payroll, interest, refunds, cancellation windows, price disclosure) | mid | personal data in logs/URLs/analytics, tracking before consent, deletion that doesn't delete, data sent to vendors, wrong legal calculations |

**Model tier.** The table's tiers are the **balanced** profile. The profile from Step 0 shifts them:

| Profile | Small reviewers (2, 4, 5) | Mid reviewers (3, 6, 7, 8) | Hacker on security code (top) |
|---|---|---|---|
| economy | small | small | mid (other code: small) |
| balanced | small | mid | top |
| max | mid | top | max (other code: top) |

Start each reviewer on its tier, first match wins:
1. An agent named `review-<tier>` (`review-small`, `review-mid`, `review-top`, `review-max`) that your subagent tool can start, in any tool (OpenCode, Claude Code, Cursor, Copilot). No `review-max`: use `review-top` for max.
2. Your subagent tool's own model option, e.g. Claude Code's `model`: small `haiku`, mid `sonnet`, top `opus`, max the Fable model if accepted, else `opus`.
3. The default model.

Tiers are recommended, never required:
- No way to choose a model, or the user/project says not to use tiers ("no model tiers", "use my default model"): every reviewer runs on the default model.
- A tier's model is refused or unavailable (access, policy, quota, unknown model): restart that reviewer once on the next tier down that worked this session, else on the default model. Never stop the review over it, and never ask the user.
- Say it in one line under *Not checked* only when a reviewer ran below its tier ("Hacker ran on mid: top tier unavailable"), since its findings may be weaker. Otherwise write nothing about tiers.

**Small-change mode** (Step 0): two subagents instead of one per reviewer, still never you alone:
- **A** covers Hacker + Senior engineer, plus Performance, Data & deploy and Privacy & law if they join; tier as the hacker's.
- **B** covers Confused user + Tester, plus UI & accessibility if it joins; the small reviewers' tier.
Each reads every role file it covers and reports one section per role, so the report keeps one panel-notes subsection per role.

**Who owns what** when roles overlap: Data & deploy owns data loss and broken deploys; Hacker owns security exposure (also in Dockerfiles, CI and IaC); Performance owns scale; Confused user owns single-request misuse; Privacy & law owns lawful handling of personal data and legal rules computed in code.

**Dispatch the panel; don't review alone.** If you have any subagent tool (`Task`, `Agent`, `subagent`, ...), you **must** start one subagent per reviewer that joins (two in small-change mode), all in the same message so they run in parallel, even for a tiny change and even when other instructions say to keep work minimal: a single agent reviewing alone skips the independence the panel exists for. Never merge two reviewers into one subagent outside small-change mode. Wait for every reviewer before you write anything to the user (run them in the foreground if your tool offers a choice): no progress messages. Give each one exactly this, and nothing from your own conversation:

```
You are reviewer <N>, the <role>, on a pre-ship review panel. Read your role file first and follow it:
<absolute path to references/<role-file>.md>
What the code does: <one sentence>
Scope: <files / pasted code>   Repo root: <path>   Expected load: <assumption and source>
Diff: <the full diff; if over ~400 lines, the diff commands instead>
Tool pass results: <commands + results, raw output for failures> - don't re-run these.
Helper skills: <name → path, only those your role file's "If installed" names | none found>
Graph: <graphify command, graph path, built <time>, "possibly stale" if older than the change; and/or "Understand-Anything graph at <path>" | none>
If that list says none found and you have a skill tool, check your skill list once for those names. Never search the disk for helpers yourself: use only the paths above or your skill tool. If a Graph is given and your role file's "If installed" names graphify: run only `explain`, `path` and `query`, at most 5 times, never `update`, `extract`, `hook`, `prs`, `add` or a build. The graph shows where to look; every finding still needs a `file:line` you read yourself. Read only the parts of each helper your role file names, and do what it says with them. Read-only: never edit files, install, download or wait for a human. Your checklist still runs, and the panel's format and severities win over the helper's (drop its verdicts and buckets).
Report in <user's language>. Use only CRITICAL/HIGH/MEDIUM/LOW. Return only your findings in the format the role file gives, then "Checked: <what you looked at>" and, if you read a helper skill, "Used: <skills and files you read>". Nothing found: say so and list what you checked.
```

Only when no subagent tool exists, do each role in sequence: read its role file in full (never work a role from memory or from this table), write its report, then start the next.

**Every finding** has: severity, `file:line`, a **concrete case** ("input X leads to wrong result Y"), why it matters, a smallest fix (a short diff when possible), and a tag: **new** (in code this change adds or modifies, including new code that duplicates old code) or **existing** (in code the change didn't touch). Pasted code and non-git folders are all **new**. No concrete case, no finding. If a reviewer found nothing in its role, it says so and lists what it checked.

A **hotspot** is a question for the user, not a finding, and only for *security* points that depend on intent the reviewer can't know ("this route has no auth check - is it meant to be public?", "is this key real?"). Anything else stays a finding. When you're unsure whether a bad input can happen, assume it can if the domain makes it plausible: a ticket with no close date, an empty cart or a decimal comma will happen. Say what you assumed in the case. Never use a hotspot to soften a likely bug into a question.

### Severity

| Severity | Meaning |
|---|---|
| CRITICAL | exploitable security hole, leaked secret, data loss or corruption, crash in the main flow |
| HIGH | wrong result in a normal case, missing auth/ownership check, broken caller, failing test, a flow some users can't complete, breaks at the stated load |
| MEDIUM | edge-case bug, unclear or missing error for bad input, risky logic with no test, duplication that must change together, breaks only at a plausible but unstated size |
| LOW | naming, small cleanup, minor speed-up |

## Step 3: The lead

Read the reports of every reviewer that joined and:

1. **Merge duplicates** across reviewers and credit everyone who found it. Merge only reports of the *same* problem; different problems stay separate items even on the same line, and one root cause gets one item, not several that point at each other.
2. **Re-check each finding** against the code: the line exists, the value can really be empty, the caller is real. Drop what you can't confirm. A `shortcut:` comment that names its limit is a decision, not a finding, unless the expected load crosses it.
3. **Fix severities** that are inflated or understated, using the severity table. Lower a reviewer's severity only for a reason that holds for every affected user: a flow a keyboard or screen-reader user can't finish stays HIGH even if a mouse user gets through.
4. **Reach** (only if Step 0 found a graph): run `graphify explain "<name>"` for up to 3 changed public functions or classes (no graphify graph but an Understand-Anything one: follow `understand-diff` for the affected components instead, without updating its graph), for the report's *Reach* line, and use it to double-check "broken caller" findings against the code.
5. **Clean up after the panel.** Delete caches the panel's runs created (`__pycache__`, `.pytest_cache`, `node_modules/.cache`) if they weren't there before, and list every new file the tester created so the user can keep or delete it.
6. **Hotspot memory** (only if you have a `memory` tool): search it for an earlier answer to each hotspot (same file, same question). Still list the hotspot, marked "previously answered: <answer>, <date>", so the user can see if things changed. Save an answer only when the user gives one in the chat. Never drop a hotspot because of memory.
7. **Apply the gate** and give **one** verdict:

**APPROVED TO SHIP** only if all of these hold:
- no CRITICAL or HIGH finding tagged **new**;
- tests pass. If the project has no tests, the tester's newly written tests for the change must pass instead. If no test runner can run at all, this condition is waived and *Not checked* says tests weren't run;
- the tool pass shows no errors on changed lines.

Otherwise **REJECTED**, with the main reason in one sentence. Findings tagged **existing** and hotspots never decide the verdict; they get their own sections. If there are hotspots, the verdict line says "...once you confirm the items below".

## Report

Read [references/report-template.md](references/report-template.md) now, copy its skeleton and fill it in; don't write the report from memory. Run its *Before sending* checklist, then send.

## Step 4: Fix and review again (only when the user asks)

When the user asks to fix ("fix it", "go ahead", "fix 1 and 3"):

1. **Show round 1 first.** If the user asked to review and fix in one go, still write the full round 1 report (verdict and fix list) before changing any file.
2. If there are uncommitted changes, suggest a commit first so the fixes are easy to check and undo.
3. Fix the requested items (all of them by default), **most severe first, one at a time**, running the relevant tests after each. Fix only what the finding describes: no new behavior, formats or refactors. If a fix needs a behavior change the user didn't ask for, leave it open and say why.
4. Re-run the **whole** panel (Steps 0-3) on the fixed code, not just the fixed items: fixes create bugs too. The final verdict must come from a round that saw the final code: any change after a round needs another round. The gate uses the **full** test suite, the tester's new test files included. A red test is never excluded or relabeled: either the code or the test is wrong, and that gets fixed or reported as an open HIGH.
5. **Refresh the code graph** before writing the final report, only if the final round is APPROVED, Step 0 found a graph, `graphify hook status` shows no git hook installed (a hook already refreshes it on commit), and `graphify-out/` isn't tracked by git (`git ls-files graphify-out` is empty): run `graphify update .` (code only, no LLM) and list `graphify-out/` among the files you changed. Otherwise, if the graph was possibly stale, say "run `graphify update .`" under *Not checked*.
6. Give the new verdict and a short **round 1 → round 2** comparison: what was fixed, what is still open, anything new. Round 2 uses the same report template as round 1.

If Step 0 found these skills, use them in this loop: `receiving-code-review` before each fix (is the finding still right?); `surgical-patch` for each fix (narrowest layer, a regression test, no side cleanup), or `safe-refactor` when the fix is a refactor such as reusing an existing helper (same behavior, same tests before and after); `systematic-debugging` or `investigate-first` when a fix's tests fail; `verification-before-completion` or `verify-and-stop` before stating the round 2 result (each check is pass, fail, unavailable or blocked). The panel's rules win over theirs: don't stop the loop to ask. A finding that turns out wrong is skipped with the reason; a fix that still fails after one debugging pass stays open and goes in the round comparison.

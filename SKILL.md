---
name: code-review-team
description: Pre-ship code review by an adversarial panel (hacker, confused user, senior engineer, tester, plus UI, performance and data/deploy reviewers when relevant) that returns one verdict, APPROVED TO SHIP or REJECTED, and one fix list ranked by severity with file:line. Use for every code review and every "ok to push/merge/deploy?" question, even about a tiny change, instead of answering from a quick look: PR/branch/diff reviews, "check my code before I commit", bug or security sweeps, AI-written code, or "fix it and review again". Also Portuguese: "revisa antes de eu subir", "posso dar push?", "tá pronto pra produção?", "chama a banca". Answers in the user's language.
---

# Code Review Team: adversarial pre-ship panel

The panel's job is to **try to reject** the code before it ships. The user is usually a solo developer with no colleague to review and often no CI, so this panel *is* their review team. Each reviewer works alone, in one role, and does not soften: one real finding is worth more than any praise. Separate roles work because each looks at the code with a different kind of distrust; one reviewer trying to cover everything covers everything halfway.

The panel is complete on its own. Some reviewers get sharper when certain other skills are installed; when they aren't, nothing is missing and nothing is reported about them.

**Language.** Write the whole report in the language the user wrote in; default to English. Labels, verdict and severities come from the table in [references/report-template.md](references/report-template.md) (Portuguese verdicts: **APROVADO PRA SUBIR** / **REPROVADO**).

## Step 0: Understand what is being reviewed

1. **What the code does**, in one sentence. If the user didn't say, infer it from the README, commit messages and code, and state it in the report. Don't block the work asking.
2. **Scope.** By default, everything that would ship: uncommitted changes plus the current branch against the main branch (`git status`, `git diff HEAD`, `git diff <main>...HEAD`, `git log <main>..HEAD`). If it's not a git repo or the user names files/a folder, review those. If code was pasted in the chat, review the paste.
3. **Full review, always.** Reviewers read the code *around* the change too: callers, helpers it should have reused, tests, config. A five-line change can duplicate an existing function or break a caller. Review only the new lines if, and only if, the user explicitly asks for that.
4. **Expected load.** One person running a script, a few users, or many users at once? Find it in the README/deploy config. If nothing states it, assume **few users**. Say which you assumed and where it came from.
5. **Which extra reviewers join.** Reviewers 1-4 always run. Reviewers 5-7 join only when their condition holds (table in Step 2). Decide from the files and content in scope (pasted code included), and write one line per extra reviewer: joins or not, and why ("Performance: joins - new query inside a loop over orders").
6. **Your own helpers.** Note whether you have a `memory` tool (Step 3) and the skills `receiving-code-review`, `systematic-debugging`, `verification-before-completion` (Step 4), found the way the reviewer prompt below describes. Reviewers find and load their own helper skills; don't load those yourself.

## Step 1: Tool pass

Before the reviewers start, collect hard evidence. Read [references/tools.md](references/tools.md) and run, in this order: the project's own scripts (lint, typecheck, test), then tools that are **already installed** for the stack, then a secret scan and dependency audit if available. **Never install anything** without asking. Record each command and a one-line result; a tool that isn't available goes in *Not checked*. Keep the raw output for the reviewers.

## Step 2: The panel

**Change nothing in this step.** Reviewers may run commands and tests. Only the tester may create files, and only *new* test files. No existing file is modified.

| # | Reviewer | Role file | Joins | Hunts for |
|---|---|---|---|---|
| 1 | Hacker | [references/hacker.md](references/hacker.md) | always | secrets, data exposure, injection, missing auth, weak crypto, fake or risky dependencies |
| 2 | Confused user | [references/confused-user.md](references/confused-user.md) | always | wrong, empty, huge, repeated input; broken flows; what error the user actually sees |
| 3 | Senior engineer | [references/senior.md](references/senior.md) | always | duplication of existing code, broken callers, scope creep, half-finished code, maintainability |
| 4 | Tester | [references/tester.md](references/tester.md) | always | runs the tests, finds tests that can't fail, writes the missing ones |
| 5 | UI & accessibility | [references/ui.md](references/ui.md) | scope touches front-end: `.html .css .scss .less`, JS/TS that touches the DOM, `.jsx .tsx .vue .svelte .astro`, server templates, or mobile UI code (SwiftUI, Compose, React Native, Flutter widgets) | flows keyboard and screen-reader users can't finish, missing labels, contrast, error/empty/loading states, phone layouts |
| 6 | Performance | [references/performance.md](references/performance.md) | expected load is "many users", **or** scope adds/changes DB queries, loops over data from input or storage, caches, background jobs/queues, or network/paid-API calls | what breaks at scale, by reading code only: query per item, unbounded lists and caches, races, per-process state |
| 7 | Data & deploy | [references/data-deploy.md](references/data-deploy.md) | scope touches migrations, schema/ORM models, Dockerfile/compose, CI workflows, IaC, deploy/cron/backup scripts, or env/config files and the code that reads new settings | data loss in migrations, deploy-order breakage, missing settings that crash on deploy |

**Who owns what** when roles overlap: Data & deploy owns data loss and broken deploys; Hacker owns security exposure (also in Dockerfiles, CI and IaC); Performance owns scale; Confused user owns single-request misuse.

**Dispatch the panel; don't review alone.** If you have any subagent tool (`Task`, `Agent`, `subagent`, ...), you **must** start one subagent per reviewer that joins, all in the same message so they run in parallel, even for a tiny change and even when other instructions say to keep work minimal: a single agent reviewing alone skips the independence the panel exists for. Give each one exactly this, and nothing from your own conversation:

```
You are reviewer <N>, the <role>, on a pre-ship review panel. Read your role file first and follow it:
<absolute path to references/<role-file>.md>
What the code does: <one sentence>
Scope: <diff commands / files / pasted code>   Repo root: <path>   Expected load: <assumption and source>
Tool pass results: <commands + results, raw output for failures>
Helper skills: before your checklist, look for each skill in your role file's "If installed" section, in your skill list (names may have a plugin prefix, e.g. ponytail:ponytail-review) and with one file search for <name>/SKILL.md under ~/.claude/skills, ~/.agents/skills, ~/.config/opencode/skills, ~/.claude/plugins/**/skills and the repo's .claude/skills and .agents/skills. Read each one you find and do what your role file says with it; skip missing ones silently. Read-only: never edit files, install, download or wait for a human. Your checklist still runs, and the panel's format and severities win over the helper's (drop its verdicts and buckets).
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
4. **Clean up after the panel.** Delete caches the panel's runs created (`__pycache__`, `.pytest_cache`, `node_modules/.cache`) if they weren't there before, and list every new file the tester created so the user can keep or delete it.
5. **Hotspot memory** (only if you have a `memory` tool): search it for an earlier answer to each hotspot (same file, same question). Still list the hotspot, marked "previously answered: <answer>, <date>", so the user can see if things changed. Save an answer only when the user gives one in the chat. Never drop a hotspot because of memory.
6. **Apply the gate** and give **one** verdict:

**APPROVED TO SHIP** only if all of these hold:
- no CRITICAL or HIGH finding tagged **new**;
- tests pass. If the project has no tests, the tester's newly written tests for the change must pass instead. If no test runner can run at all, this condition is waived and *Not checked* says tests weren't run;
- the tool pass shows no errors on changed lines.

Otherwise **REJECTED**, with the main reason in one sentence. Findings tagged **existing** and hotspots never decide the verdict; they get their own sections. If there are hotspots, the verdict line says "...once you confirm the items below".

## Report

Read [references/report-template.md](references/report-template.md) now, copy its skeleton and fill it in; don't write the report from memory. Run its *Before sending* checklist, then send.

## Step 4: Fix and review again (only when the user asks)

When the user asks to fix ("fix it", "go ahead", "corrige", "fix 1 and 3"):

1. **Show round 1 first.** If the user asked to review and fix in one go, still write the full round 1 report (verdict and fix list) before changing any file.
2. If there are uncommitted changes, suggest a commit first so the fixes are easy to check and undo.
3. Fix the requested items (all of them by default), **most severe first, one at a time**, running the relevant tests after each. Fix only what the finding describes: no new behavior, formats or refactors. If a fix needs a behavior change the user didn't ask for, leave it open and say why.
4. Re-run the **whole** panel (Steps 0-3) on the fixed code, not just the fixed items: fixes create bugs too. The gate uses the **full** test suite, the tester's new test files included. A red test is never excluded or relabeled: either the code or the test is wrong, and that gets fixed or reported as an open HIGH.
5. Give the new verdict and a short **round 1 → round 2** comparison: what was fixed, what is still open, anything new. Round 2 uses the same report template as round 1.

If these skills are available, use them in this loop: `receiving-code-review` before each fix (is the finding still right?), `systematic-debugging` when a fix's tests fail, `verification-before-completion` before stating the round 2 result. The panel's rules win over theirs: don't stop the loop to ask. A finding that turns out wrong is skipped with the reason; a fix that still fails after one debugging pass stays open and goes in the round comparison.

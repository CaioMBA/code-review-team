---
name: code-review-team
description: Pre-ship code review by a panel of 5 adversarial reviewers (hacker, confused user, senior engineer, tester, lead) that tries to reject the change and returns one verdict, APPROVED TO SHIP or REJECTED, plus a single fix list ranked by severity with file:line. Use whenever the user asks for a code review, a PR/branch/diff review, "is this ready to ship/push/merge/deploy?", "check my code before I commit", a bug or security sweep of their changes, a review of AI-generated code, or asks to fix the findings and review again, even if they never say "review team", "panel" or "banca". Also for Portuguese requests like "revisa antes de eu subir", "posso dar push?", "tá pronto pra produção?", "chama a banca". Answers in the user's language.
---

# Code Review Team: 5-reviewer pre-ship panel

The panel's job is to **try to reject** the code before it ships. The user is usually a solo developer with no colleague to review and often no CI, so this panel *is* their review team. Each reviewer works alone, in one role, and does not soften: one real finding is worth more than any praise. Separate roles work because each looks at the code with a different kind of distrust; one reviewer trying to cover everything covers everything halfway.

**Language.** Write the whole report in the language the user wrote in; default to English. Translate labels using the table in [references/report-template.md](references/report-template.md).

## Step 0: Understand what is being reviewed

1. **What the code does**, in one sentence. If the user didn't say, infer it from the README, commit messages and code, and state it in the report. Don't block the work asking.
2. **Scope.** By default, everything that would ship: uncommitted changes plus the current branch against the main branch (`git status`, `git diff HEAD`, `git diff <main>...HEAD`, `git log <main>..HEAD`). If it's not a git repo or the user names files/a folder, review those. If code was pasted in the chat, review the paste.
3. **Full review, always.** Reviewers read the code *around* the change too: callers, helpers it should have reused, tests, config. A five-line change can duplicate an existing function or break a caller. Review only the new lines if, and only if, the user explicitly asks for that.
4. **Expected load.** One person running a script, or many users at once? Find it in the README/deploy config; say which you assumed.

## Step 1: Tool pass

Before the reviewers start, collect hard evidence. Read [references/tools.md](references/tools.md) and run, in this order: the project's own scripts (lint, typecheck, test), then tools that are **already installed** for the stack, then a secret scan and dependency audit if available. **Never install anything** without asking. Record each command and a one-line result; a tool that isn't available goes in *Not checked*. Keep the raw output for the reviewers.

## Step 2: The panel (reviewers 1–4)

**Change nothing in this step.** Reviewers may run commands and tests. Only the tester may create files, and only *new* test files. No existing file is modified.

If you have a subagent tool, run reviewers 1–4 **in parallel, one subagent each**, so they don't contaminate each other. Give each one exactly this, and nothing from your own conversation:

```
You are reviewer <N>, the <role>, on a pre-ship review panel. Read your role file first and follow it:
<absolute path to references/<role-file>.md>
What the code does: <one sentence>
Scope: <diff commands / files / pasted code>   Repo root: <path>   Expected load: <assumption>
Tool pass results: <commands + results, raw output for failures>
Report in <user's language>. Return only your findings in the format the role file gives.
```

Without subagents, do each role in sequence, reading its role file and writing its report before starting the next.

| # | Reviewer | Role file | Hunts for |
|---|---|---|---|
| 1 | Hacker | [references/hacker.md](references/hacker.md) | secrets, data exposure, injection, missing auth, weak crypto, fake or risky dependencies |
| 2 | Confused user | [references/confused-user.md](references/confused-user.md) | wrong, empty, huge, repeated input; broken flows; what error the user actually sees |
| 3 | Senior engineer | [references/senior.md](references/senior.md) | duplication of existing code, broken callers, scope creep, half-finished code, maintainability |
| 4 | Tester | [references/tester.md](references/tester.md) | runs the tests, finds tests that can't fail, writes the missing ones |

**Every finding** has: severity, `file:line`, a **concrete case** ("input X leads to wrong result Y"), why it matters, a smallest fix (a short diff when possible), and a tag: **new** (in code this change adds or modifies, including new code that duplicates old code) or **existing** (in code the change didn't touch). Pasted code and non-git folders are all **new**. No concrete case, no finding. If a reviewer found nothing in its role, it says so and lists what it checked.

A **hotspot** is a question for the user, not a finding, and only for *security* points that depend on intent the reviewer can't know ("this route has no auth check — is it meant to be public?", "is this key real?"). Anything else stays a finding. When you're unsure whether a bad input can happen, assume it can if the domain makes it plausible: a ticket with no close date, an empty cart or a decimal comma will happen. Say what you assumed in the case. Never use a hotspot to soften a likely bug into a question.

### Severity

| Severity | Meaning |
|---|---|
| CRITICAL | exploitable security hole, leaked secret, data loss or corruption, crash in the main flow |
| HIGH | wrong result in a normal case, missing auth/ownership check, broken caller, failing test |
| MEDIUM | edge-case bug, unclear or missing error for bad input, risky logic with no test, duplication that must change together |
| LOW | naming, small cleanup, minor speed-up |

## Step 3: The lead (reviewer 5)

Read the four reports and:

1. **Merge duplicates** across reviewers and credit everyone who found it.
2. **Re-check each finding** against the code: the line exists, the value can really be empty, the caller is real. Drop what you can't confirm. A `shortcut:` comment that names its limit is a decision, not a finding, unless the expected load crosses it.
3. **Fix severities** that are inflated or understated.
4. **Apply the gate** and give **one** verdict:

**APPROVED TO SHIP** only if all of these hold:
- no CRITICAL or HIGH finding tagged **new**;
- tests pass. If the project has no tests, the tester's newly written tests for the change must pass instead. If no test runner can run at all, this condition is waived and *Not checked* says tests weren't run;
- the tool pass shows no errors on changed lines.

Otherwise **REJECTED**, with the main reason in one sentence. Findings tagged **existing** and hotspots never decide the verdict; they get their own sections. If there are hotspots, the verdict line says "…once you confirm the items below".

## Report

Use the exact structure in [references/report-template.md](references/report-template.md). If the user asked for a file (e.g. `report.md`), write the report there and also show the verdict and fix list in the chat.

## Step 4: Fix and review again (only when the user asks)

When the user asks to fix ("fix it", "go ahead", "corrige", "fix 1 and 3"):

1. If there are uncommitted changes, suggest a commit first so the fixes are easy to check and undo.
2. Fix the requested items (all of them by default), **most severe first, one at a time**, running the relevant tests after each.
3. Re-run the **whole** panel (Steps 1–3) on the fixed code, not just the fixed items: fixes create bugs too.
4. Give the new verdict and a short **round 1 → round 2** comparison: what was fixed, what is still open, anything new.

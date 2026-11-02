# Banca de revisão — English, multi-language redesign

## Intent

`banca-de-revisao` is a code-review skill. A panel of reviewers tries to *reject* code before it ships, then gives one verdict and one ranked fix list. Today it works only in Portuguese and has a shallow checklist. This redesign makes it the best pre-ship review a **solo developer** can get. For that person the skill *is* the review team: there is no colleague and often no CI (automated checks on every push), so the verdict has to hold up without a second opinion.

## Goals

- **Language.** English by default. If the user writes in another language, the whole report is in that language, including the verdict and severity labels. One skill, not two.
- **Triggering.** The description is in English and still catches Portuguese requests ("revisa antes de eu subir", "chama a banca", "tá pronto pra produção?").
- **Always a full review.** Reviewers read the code around the change, not just the diff, so they catch duplicated code, broken callers and conflicts with existing helpers. The review covers only new lines when the user explicitly asks for that.
- **Handles hand-written and AI-written code** without asking which one it is. AI-mistake checks always run; hand-written code simply passes them.
- **Uses ideas from CodeRabbit and SonarQube:**
  - a tool pass before the reviewers start
  - a quality gate judged on new code only
  - hotspots kept apart from confirmed bugs
  - a short "what this change does" summary
  - a ready-to-apply fix for each finding
- **Evidence over opinion.** Every finding cites `file:line`, gives a concrete case ("this input leads to this wrong result"), and gets re-checked before it is reported, as in `ponytail-review`. If something mattered and could not be checked, the report says so in a "Not checked" line.
- **Keeps what works:** the 5 roles, reviewers working separately (in parallel subagents when the harness has them), no edits during the review, and the fix-and-review-again loop that runs only when the user asks.

## Non-goals

- A project rules file (`.coderabbit.yaml` style) and team metrics (ratings, tech-debt hours, coverage %). These are team process, easy to add later if wanted.
- A bundled script that detects and runs tools (approach C).
- Installing any tool without the user's OK.

## Anti-goals (failure even if it "works")

- Padded reports: invented findings, style nitpicks, vague "consider…".
- Blocking a push over old problems the change did not touch.
- Jargon a solo dev can't act on.
- Changing code during the review stage.
- A file-by-file walkthrough of code the user just wrote.

## Approaches considered

- **A. One big `SKILL.md`.** Simplest, but about 400 lines that every reviewer loads in full, and the security checklist has to stay shallow.
- **B. Coordinator `SKILL.md` plus reference files per reviewer — chosen.** Each reviewer reads only its own checklist, so each checklist can go deep while the main skill stays lean.
- **C. B plus a tool-runner script.** Most consistent, but it is a cross-platform script to maintain and needs Python or bash, which many solo devs, and this machine, don't have on PATH. Most of its benefit comes from a tool table the agent follows.

The user picked **B**.

## Design

### Files

```
SKILL.md                     coordinator: language, scope, tool pass, panel dispatch, gate, report, fix loop
references/hacker.md         security + AI supply-chain checks (hallucinated packages)
references/confused-user.md  misuse cases; actually run things when possible
references/senior.md         duplication vs existing code, naming, coupling, scope creep, stale comments
references/tester.md         run tests, missing cases, tests that can't fail / over-mocked
references/tools.md          per-stack table: linters, type checkers, secret scan, dependency audit, test command
references/report-template.md  exact output shape + localized label table
evals/                       existing 3 PT cases + new EN cases
README.md                    English; short PT section kept
```

### Flow

0. **Understand.** Detect the user's language. Write one sentence on what the code does. Find the scope: by default, uncommitted changes plus the branch vs. the main branch. Otherwise the files the user named, or code pasted into the chat. Assume an expected load (one user or many) and say which one.
1. **Tool pass.** Using `tools.md`, run the project's own scripts first (`npm run lint`, `pytest`, …). Then run tools that are already installed. Never install anything. Record each command with its result. A tool that is missing goes in "Not checked".
2. **Panel.** Reviewers 1–4 work in parallel, each in its own subagent. Each gets its role file, the scope, the one-sentence summary and the tool output. Without subagents, run them one after another and write each report before starting the next. Each finding has a severity (CRITICAL / HIGH / MEDIUM / LOW), `file:line`, a concrete case, a suggested fix (a small diff where possible), and a tag: **new** (in the changed code) or **existing** (in old code). A security point that depends on intent goes in as a **hotspot** (a question for the user), not as a finding.
3. **Lead (reviewer 5).** Removes duplicates. Re-checks each finding against the code and drops the ones it can't confirm. Fixes severities that are too high or too low. Applies the gate.

### Quality gate

**APPROVED TO SHIP** only if all of these hold:
- no CRITICAL or HIGH finding tagged **new**
- the tests pass. If the project has no tests, the tester's newly written tests for the change must pass instead. If no test runner can run at all, this condition is waived and "Not checked" says that tests were not run.
- the tool pass shows no errors in the changed lines

Otherwise **REJECTED**, with the main reason in one sentence. **Existing** findings and hotspots never decide the verdict. They are listed in their own sections.

### Report (template in `report-template.md`)

The report has these parts, in this order:
1. Title
2. What the code does
3. Scope
4. Verdict and reason
5. What to fix (new code, most severe first, numbered across the whole list so the user can say "fix 1 and 3")
6. Confirm before shipping (hotspots)
7. Older problems (not blocking)
8. Tool pass (commands run and their results)
9. Short per-reviewer notes
10. Not checked
11. The closing reminder (commit first, check the changes)

Labels are translated into the user's language. Pinned Portuguese labels: APROVADO PRA SUBIR / REPROVADO; CRITICO / ALTO / MÉDIO / BAIXO.

### Fix loop (only when the user asks)

1. Suggest a commit first.
2. Fix the items one at a time, most severe first, running the relevant tests after each fix.
3. Re-run the whole panel on the fixed code.
4. Show what changed between the two rounds.

## Testing (skill-creator method)

- Snapshot the current skill as the `old_skill` baseline in `banca-de-revisao-workspace/` (a sibling folder, not committed).
- Cases:
  - the 3 existing Portuguese cases, with their graders updated for the new structure, still answered in Portuguese
  - an English branch-review case with AI-style mistakes planted in it (a package that doesn't exist, a test that can't fail, a duplicated helper, a change outside the task)
  - an English case where the change is small but duplicates existing code, to check the full-review rule
  - an English case where the code has an old CRITICAL problem but a clean change, to check that the gate gives APPROVED and lists the old problem
- Run with-skill vs. old-skill runs, grade them, then open skill-creator's `generate_review.py` viewer for the user to review.
- Then run a trigger test with `claude`, using both should-trigger and near-miss queries in English and Portuguese.

## My calls (check these)

- **The skill was later renamed `code-review-team`.** The user chose this for discoverability and recreated the repo under that name. "Banca de Revisão" stays as a README subtitle.
- **A failing test blocks the verdict even if it was failing before the change.** You can't tell whether the change is safe while tests are red.
- **Hotspots never block.** The verdict line mentions them when there are any.
- **Old findings, even CRITICAL ones, don't block.** They are listed first in "Older problems".
- **Eval cases stay in `evals/` in the existing `claude plugin eval` format.** That is also skill-creator's own case format. The workspace only holds run outputs, grading and the viewer, and is git-ignored. The README score gets re-run and replaced.
- **The tester may still write missing tests in new files during the review,** as it can today. Existing files are never modified. New tests that fail are findings.
- **The cart eval's `place-files.sh` needs a fix.** It copies files but never sets up the `main` and `feature/cupom` branches from `base/` and `files/`, so the branch diff doesn't exist.

## Left to the builder

- The exact checklist wording in each role file.
- The rows of the `tools.md` table.
- The wording of the eval prompts and graders.
- The README layout.

# Review Squad Integrations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three conditional reviewer roles (UI & accessibility, Performance, Data & deploy) and optional, never-required integrations with installed skills (security-audit, ponytail, playwright-cli, UI skills, superpowers fix-loop skills, opencode-mem) to the `code-review-team` skill.

**Architecture:** Approach A from the spec: each role file gets an "If installed" block; `SKILL.md` decides which conditional roles join, detects optional skills by name in its available-skills list, and passes `Optional skills available:` to each reviewer, which loads its own helpers. The skill is markdown only; "tests" are `claude plugin eval` cases in `evals/`.

**Tech Stack:** Markdown skill files; `claude plugin eval` (Claude Code 2.1.317) with `case.yaml` schema 1.1, `prompt.md`, `graders/NN.md` (llm, focus: trace), bash `place-files.sh` scaffolds; Python/JS fixtures.

**Spec:** `docs/superpowers/specs/2026-11-03-review-squad-integrations-design.md`

## Global Constraints

- The skill must work fully with no other skill installed; a missing optional skill is skipped silently (never a gap, warning or "Not checked" line).
- Helper skills are used read-only: never trigger a mode that writes files, edits code, installs/downloads, or waits for a human (no security-audit full audit, no impeccable edit/craft or first-run download, no plannotator).
- The panel's format, severity scale (CRITICAL/HIGH/MEDIUM/LOW), new/existing tag and single lead verdict always win over a helper's.
- Never install anything; reviewers never modify existing files; only the tester creates new test files.
- Performance reads code only, never sends traffic. Severity: breaks at the load stated in README/deploy config, or on the main flow → HIGH; only at an unstated but plausible size → MEDIUM; minor speed-ups → LOW.
- Default load when nothing states it: **few users**, stated in the report.
- `SKILL.md` description stays ≤ 1024 characters and keeps the Portuguese triggers.
- Portuguese labels: "UI e acessibilidade", "Desempenho", "Dados e deploy".

## Review Focus

1. A change touching both front-end files and a migration → both UI and Data & deploy join; the lead merges any double report. (Test: grader in Task 1 `migracao-remove-coluna` checks UI does not join when no front-end file changed; Task 1 `ui-newsletter-form-branch` checks Data & deploy does not join.)
2. Pasted code with no repo → join predicates apply to the pasted content. (Test: new grader on `codigo-colado-formulario`: UI joins.)
3. Portuguese report with new roles → new roles' labels in Portuguese. (Test: same grader checks the section is titled "UI e acessibilidade".)
4. Few-users default plus a code trigger → Performance joins, but its scale findings are at most MEDIUM. (Test: Task 1 Step 5 grader on `carrinho-branch-com-cupom`; the stated-load HIGH side is `perf-orders-many-users` grader 06.)
5. Optional skill listed but its role doesn't join → nothing about it in the report. (Test: grader on `small-change-duplicates-helper`: report never mentions UI/accessibility review or security-audit/ponytail as missing.)

---

### Task 1: Eval cases and RED baseline

**Files:**
- Create: `evals/ui-newsletter-form-branch/{case.yaml,prompt.md,place-files.sh,base/*,files/*,graders/01-08.md}`
- Create: `evals/perf-orders-many-users/{case.yaml,prompt.md,place-files.sh,base/*,files/*,graders/01-08.md}`
- Create: `evals/migracao-remove-coluna/{case.yaml,prompt.md,place-files.sh,base/*,files/*,graders/01-08.md}`
- Create: `evals/integration-helper-skills/{case.yaml,prompt.md,place-files.sh,graders/01-06.md}` (tag `integration`)
- Modify: `evals/small-change-duplicates-helper/graders/` (add 07.md, 08.md), `evals/codigo-colado-formulario/graders/` (add 11.md), `evals/carrinho-branch-com-cupom/graders/` (add 11.md)

**Interfaces:**
- Produces: case names above; tag `code-review-team` on all standalone cases, `integration` on the integration case. Grader files follow the existing front matter exactly (`type: llm`, `focus: trace`, `weight: 1`). Scaffolds follow `evals/ai-written-reset-branch/place-files.sh`: `base/` committed on `main`, `files/` committed on the feature branch, branch left checked out.

- [ ] **Step 1: `ui-newsletter-form-branch` (English, JS/HTML, branch `feature/newsletter`)**
  `base/`: `index.html`, `app.js`, `README.md` ("personal blog"). `files/` adds a newsletter form with planted bugs: email `<input>` with placeholder only, no label; icon-only `<button><svg>…</svg></button>` with no accessible name; a "close" `<div onclick=…>` that isn't focusable; error shown only by turning the border red. Prompt: "added a newsletter signup to my blog on feature/newsletter, ok to merge?"
  Graders: (01) one verdict REJECTED; (02) report has a UI & accessibility section; (03) flags the unlabeled email input; (04) flags the icon-only button with no accessible name; (05) flags the non-focusable div as unreachable by keyboard; (06) Data & deploy does not join; (07) no tracked file modified; (08) English.
- [ ] **Step 2: `perf-orders-many-users` (English, Python stdlib sqlite3, branch `feature/order-list`)**
  `base/`: `app.py` (sqlite helpers), `test_app.py`, `README.md` stating "used by ~5,000 shops, runs on 4 gunicorn workers". `files/` adds `list_orders(shop_id)` that queries the customer once per order in a loop, a module-level dict cache keyed by shop and never evicted, and an in-memory per-process rate-limit dict; tests pass.
  Graders: (01) REJECTED; (02) Performance section exists; (03) flags query-per-order and names the load (shops/rows); (04) flags the never-evicted cache; (05) flags the per-process rate limiter as wrong with 4 workers; (06) at least one Performance finding is HIGH because the README states the load; (07) no load-generation tool or traffic was run (no k6/locust/ab/wrk/loop of HTTP requests); (08) English.
- [ ] **Step 3: `migracao-remove-coluna` (Portuguese, Python, branch `feature/contatos`)**
  `base/`: `app.py`, `migrations/001_init.sql` with `clientes(id, nome, telefone)`, `test_app.py`, `README.md`. `files/` adds `migrations/002_contatos.sql` that creates `contatos` and runs `ALTER TABLE clientes DROP COLUMN telefone` without copying data, and `config.py` reading `os.environ["SMTP_HOST"]` with no default and no mention in README.
  Graders: (01) REPROVADO; (02) a "Dados e deploy" section exists; (03) flags the dropped column/lost phone data as CRITICO; (04) flags SMTP_HOST crashing on deploy with no default/doc; (05) UI e acessibilidade does not join; (06) single ranked list with arquivo:linha; (07) no tracked file modified; (08) Portuguese.
- [ ] **Step 4: `integration-helper-skills` (English, tag `integration`)**
  `place-files.sh` runs the same steps as `ai-written-reset-branch/place-files.sh` but copies from `$src/../ai-written-reset-branch/base` and `/files`. Same prompt as that case.
  Graders: (01) the hacker loaded security-audit (trace shows its SKILL.md or companion files read); (02) no command created or wrote under `~/security-audit-skill`; (03) the senior loaded ponytail-review; (04) the report uses the panel format: one "Verdict:" line with APPROVED TO SHIP or REJECTED and one numbered fix list; (05) no "Must fix / Should fix / Nice to have" buckets and no "Verdict: Ship" line; (06) panel notes say which helper skills were used.
- [ ] **Step 5: Extra graders on existing cases**
  `small-change-duplicates-helper`: (07) UI & accessibility and Data & deploy do not join; (08) the report does not mention any optional skill as missing or unavailable. `codigo-colado-formulario`: (11) a "UI e acessibilidade" section exists in relatorio.md. `carrinho-branch-com-cupom`: (11) if Performance joins, it states the assumed load (few users) and rates no scale finding above MÉDIO.
- [ ] **Step 6: Standalone isolation check**
  Create `C:\Users\caiom\AppData\Local\Temp\opencode\crt-isolated\` with `skills\code-review-team` (junction to the repo). Run `$env:CLAUDE_CONFIG_DIR='<that dir>'; claude -p "list the skills you have"`.
  Expected: only code-review-team (plus built-ins). If auth fails, stop and ask the user how to authenticate an isolated config; do not copy credential files without asking.
- [ ] **Step 7: RED run (current skill)**
  Run (isolated config): `claude plugin eval . --scaffold --allow-tools Write,Edit,Bash,WebFetch --runs 1 --tag code-review-team --no-publish --trust-plugin --case "ui-*" --case "perf-*" --case "migracao-*"` plus the three modified existing cases.
  Expected: new-role graders fail (no UI/Performance/Data & deploy sections). Save the summary to `C:\Users\caiom\AppData\Local\Temp\opencode\crt-red.md` (not committed).
- [ ] **Step 8: Commit**
  `git add evals && git commit -m "evals: cases for conditional roles and helper-skill integration"`

### Task 2: Coordinator (`SKILL.md`)

**Files:** Modify: `SKILL.md`

**Interfaces:**
- Produces: roster numbering 1 Hacker, 2 Confused user, 3 Senior, 4 Tester, 5 UI & accessibility (`references/ui.md`), 6 Performance (`references/performance.md`), 7 Data & deploy (`references/data-deploy.md`), then "The lead". Reviewer prompt gains the line `Optional skills available: <name> [<path>], ... | none`. Panel notes line `used: <skill> (<files>)`.

- [ ] **Step 1: Frontmatter description** — mention the conditional roles; keep triggers and PT phrases; verify length ≤ 1024 with `py -c "import re,io;t=open('SKILL.md',encoding='utf-8').read();print(len(re.search(r'description: (.*)',t).group(1)))"`.
- [ ] **Step 2: Step 0** — item 4 default: "If nothing states the load, assume few users and say so." Add item 5 "Which roles join": the three predicates from the spec's roster table, one report line each with the reason; pasted code uses the same predicates. Add item 6 "Optional skills": scan the available-skills list for the 11 names in the spec (match suffix after `plugin:`), the `memory` tool and `ast-grep`/`sg`; record name + path if shown; never load reviewer helpers yourself; pass each role only the names its file mentions.
- [ ] **Step 3: Step 2 panel** — roster table with a "Joins" column; prompt template gets the `Optional skills available:` line; "run every joining reviewer in parallel"; one line: "The ownership split: Data & deploy owns data loss and broken deploys, Hacker owns security exposure, Performance owns scale, Confused user owns single-request misuse."
- [ ] **Step 4: Severity table** — add to HIGH: "breaks at the stated load"; to MEDIUM: "breaks only at a plausible but unstated size".
- [ ] **Step 5: Lead** — rename "Step 3: The lead (reviewer 5)" to "Step 3: The lead"; "Read the reports of every reviewer that joined". Hotspots + `memory` tool: search for an earlier answer; still list the hotspot with "previously answered: <answer>, <date>"; save only answers the user gives; never drop a hotspot.
- [ ] **Step 6: Step 4 fix loop** — add the superpowers block from the spec verbatim in meaning, with "panel rules win: don't stop to ask; a wrong finding is skipped with the reason; a fix still failing after one debugging pass stays open in the round comparison".
- [ ] **Step 7: Verify** — `git diff --stat`; read the file top to bottom once; grep that no line says "5 reviewers" or "reviewers 1-4" any more: `Select-String -Path SKILL.md -Pattern '5 reviewers|1-4|reviewer 5'` → no matches.
- [ ] **Step 8: Commit** `git commit -am "skill: conditional roles, optional skill detection, lead and fix-loop helpers"`

### Task 3: Integrations in existing role files

**Files:** Modify: `references/hacker.md`, `references/senior.md`, `references/confused-user.md`

**Interfaces:**
- Consumes: the `Optional skills available:` line from Task 2.
- Produces: each file ends its checklist with a section titled exactly `## If installed` listing skill name → when → what to load → what to take; the output format sections are unchanged.

- [ ] **Step 1: `hacker.md`** — item 6 becomes "a missing setting is a finding only with a traced, reachable impact". `## If installed`: `security-audit` guidance mode only; the companion-file map from the spec; from `ATTACK-CLASSES.md` the classes in play; from `HUNTING.md` only the concrete-invariant method and candidate gate; mapping confirmed→finding, informational dropped, needs_validation→hotspot, trace sink→file:line, payload+result→Case, remediation→Fix; panel severity table wins; stay source-only; registry lookups stay allowed. One line: "Never start its full audit or create its output folder."
- [ ] **Step 2: `senior.md`** — delete item 8 (Scale) and renumber; item 1 adds "use `ast-grep`/`sg` when installed". `## If installed`: `ponytail-review` Lean checks + one-caller-fix check, skip its Risk/Missing test/Scale parts, buckets, verdict and Lean line; `ponytail-debt` marker search over scope files with the severity rules from the spec.
- [ ] **Step 3: `confused-user.md`** — `## If installed`: `playwright-cli` only when a project start script comes up locally within ~2 minutes with no setup; never a deployed URL; quote what the user sees; otherwise reason from code.
- [ ] **Step 4: Verify** — `Select-String references/*.md -Pattern '## If installed'` → 3 matches; `Select-String references/senior.md -Pattern 'Scale'` → only inside the ponytail skip line.
- [ ] **Step 5: Commit** `git commit -am "roles: optional security-audit, ponytail and playwright integrations"`

### Task 4: New role files

**Files:** Create: `references/ui.md`, `references/performance.md`, `references/data-deploy.md`

**Interfaces:**
- Produces: same skeleton as `hacker.md`: `# Reviewer N: <name>`, one-paragraph stance, `## Check` numbered list (the spec's built-in checklist for that role), `## If installed`, `## Output` with the existing finding block (`[SEVERITY] path:line - <problem>  (new|existing)` / `Case:` / `Fix:`) and the "Checked:" / nothing-found line. Performance's Case line also requires `Breaks at: <load>`.

- [ ] **Step 1: `ui.md`** (reviewer 5) — checklist, helpers and severity from the spec.
- [ ] **Step 2: `performance.md`** (reviewer 6) — checklist, helpers, "reads code only, never generate traffic", severity and default-load rules from Global Constraints.
- [ ] **Step 3: `data-deploy.md`** (reviewer 7) — checklist and helpers from the spec; data loss CRITICAL.
- [ ] **Step 4: Verify** — each file < 80 lines (`(Get-Content f).Count`), each has `## Check`, `## If installed`, `## Output`.
- [ ] **Step 5: Commit** `git add references && git commit -m "roles: UI & accessibility, performance, data & deploy"`

### Task 5: Report template, tools, README

**Files:** Modify: `references/report-template.md`, `references/tools.md`, `README.md`

- [ ] **Step 1: `report-template.md`** — scope header gets `**Roles that joined:** <role: reason; ...>`; panel notes gain `### 5. UI & accessibility`, `### 6. Performance`, `### 7. Data & deploy` "only for roles that joined" and an optional `used:` line; label table gets the three PT labels plus "Roles that joined | Revisores extras".
- [ ] **Step 2: `tools.md`** — "Any stack" rows: `ast-grep`/`sg` (structural search for duplicates/callers), `shellcheck` on changed `.sh`, `hadolint` on changed Dockerfiles, `actionlint` on changed workflows; one line: "`uvx`/`docker run` download things: ask first."
- [ ] **Step 3: `README.md`** — roster table with the three conditional roles and when they join; "Works better with (optional)" section: skill → what it adds, plus "None is required"; update the Layout block and the eval count.
- [ ] **Step 4: Commit** `git commit -am "docs: report template, tools and README for the squad"`

### Task 6: GREEN runs and fixes

- [ ] **Step 1: Standalone** (isolated config from Task 1 Step 6): `claude plugin eval . --scaffold --allow-tools Write,Edit,Bash,WebFetch --runs 1 --tag code-review-team --no-publish --trust-plugin`. Expected: every grader passes on all 9 standalone cases.
- [ ] **Step 2: Integration** (normal config, security-audit and ponytail installed): same command with `--tag integration`. Expected: all 6 graders pass. Check `Test-Path ~/security-audit-skill` is still false.
- [ ] **Step 3: Fix and re-run** failing cases only (`--case <name>`), changing the skill wording, never the graders, unless a grader is provably wrong (note why in the commit).
- [ ] **Step 4: Final** — `--runs 3` on all cases; put the pass count into README "Skill tests". Commit `git commit -am "evals: green run, README score"`.

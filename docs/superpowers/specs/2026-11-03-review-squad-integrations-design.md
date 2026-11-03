# Review squad: conditional roles and optional skill integrations

Target repo: `D:\Development\PERSONAL\code-review-team` (final home: `docs/superpowers/specs/2026-11-03-review-squad-integrations-design.md`).

## Intent

`code-review-team` is a pre-ship review panel for solo developers. This change grows it into a fuller squad, with three new roles that join only when a change touches their area. Each role also gets stronger when certain other skills are installed alongside it. **The skill must work fully on its own.** Every other skill is optional: if it's present, the panel uses it; if it's absent, the role falls back to its own built-in checklist and nothing is reported missing.

## Goals

- Three new conditional roles: **UI & accessibility**, **Performance**, **Data & deploy**. Each joins only when an observable condition holds (below), so a CSS tweak doesn't cost seven subagents.
- **Hacker + `security-audit`**: when it's installed, the hacker uses its guidance mode and the attack-class files that match the diff.
- **Senior + `ponytail`**: when it's installed, the senior uses `ponytail-review`'s lean checks and `ponytail-debt`'s `shortcut:` marker search.
- Other installed skills that genuinely help a role get wired in the same way (list below). Skills that don't help are left out on purpose.
- Gate, severity scale, report shape, new/existing tagging and the fix loop keep working as today. The new roles' findings feed the same gate.

## Non-goals

- Running load tests or sending traffic to the app. The Performance role **reads code only** (user's decision).
- Making any other skill a requirement, or installing/downloading anything to use one.
- Other improvements raised earlier (prompt injection inside reviewed code, LLM-feature checks, main-branch auto-detect, PR review via `gh`, fix-loop round cap, more stacks in `tools.md` beyond the rows below). They stay on the backlog.

## Anti-goals

- A role whose output changes shape depending on what's installed. The panel's format always wins; another skill's buckets, verdicts or severity names never reach the report.
- Triggering another skill's heavy or writing mode: `security-audit` full audit (writes a run folder), `impeccable` craft/edit paths or its first-run binary download, `plannotator` blocking UI, any skill that edits code.
- A missing optional skill showing up as a gap, warning or "Not checked" line.
- Conditional roles joining on changes that don't touch their area (noise and cost).

## Constraints

- Harnesses: OpenCode, Claude Code, Codex. Detection can't rely on folder probing (on OpenCode, ponytail lives in the npm cache via `skills.paths`; on Claude Code plugin skills may be prefixed, e.g. `ponytail:ponytail-review`).
- Reviewer subagents get "nothing from your own conversation", and may not see the available-skills list.
- Never install anything; never edit existing files during review; only the tester writes new test files.

## Approaches considered

- **A. An "If installed" block inside each role file - chosen.** Each reviewer already reads its own role file, so it sees its integrations with no extra load. A missing skill costs one skipped paragraph. Integration knowledge is spread over several files.
- **B. One `references/integrations.md`.** One place to maintain, but the coordinator must cut the right rows into each prompt, and role files stop being self-contained.
- **C. One add-on file per integration.** Least text when nothing is installed, but more files and load steps for a few lines each.

The user picked **A**.

## Design

### Roster

| # | Reviewer | Role file | Joins |
|---|---|---|---|
| 1 | Hacker | `hacker.md` | always |
| 2 | Confused user | `confused-user.md` | always |
| 3 | Senior engineer | `senior.md` | always |
| 4 | Tester | `tester.md` | always |
| 5 | UI & accessibility | `ui.md` (new) | the scope touches front-end files: `.html .css .scss .less`, `.js/.ts` that touch the DOM, `.jsx .tsx .vue .svelte .astro`, server templates, or mobile UI code (SwiftUI, Compose, React Native, Flutter widgets) |
| 6 | Performance | `performance.md` (new) | expected load (Step 0) is "many users", **or** the scope adds/changes DB queries, loops over collections from input or storage, caches, background jobs or queues, or network/paid-API calls |
| 7 | Data & deploy | `data-deploy.md` (new) | the scope touches migrations, schema or ORM model definitions, Dockerfile/compose, CI workflows, IaC, deploy/cron/backup scripts, or env/config files and the code that reads new settings |
| - | Lead | (in `SKILL.md`) | always, last |

- The lead stays the final step; it is no longer numbered "reviewer 5". Role numbers 5-7 are the new roles.
- Step 0 gains a line: decide which conditional roles join and why (one line each in the report's scope header, e.g. "Performance: joins - new query in a loop"). Pasted code uses the same predicates on its content.
- **Scale moves from senior to performance.** `senior.md` item 8 is removed. When Performance doesn't join, nobody checks scale, which matches the old rule "only flag what breaks at the load you were told".
- **Overlap rule:** Data & deploy owns data loss and broken deploys; Hacker owns security exposure (also in Dockerfiles, CI, IaC). Performance owns scale; Confused user owns single-request misuse. The lead's existing merge step handles double reports.

### Detecting optional skills

1. In Step 0, the coordinator checks its own available-skills list for these names, matching on the suffix after any `plugin:` prefix: `security-audit`, `ponytail-review`, `ponytail-debt`, `playwright-cli`, `ui-ux-pro-max`, `impeccable`, `review-animations`, `mobile-native`, `receiving-code-review`, `systematic-debugging`, `verification-before-completion`. Also whether the session has a `memory` tool (opencode-mem) and an `ast-grep`/`sg` command.
2. The coordinator **never loads** reviewer helper skills itself (that would pull their formats into its context). It only records which names are present, plus the `SKILL.md` path when the list shows one. The decision happens after the join decision, so roles that don't join get nothing.
3. Each reviewer prompt gets one more line: `Optional skills available: <name> [<path>], ...` listing only the ones that role's file mentions, or `none`.
4. Each reviewer loads its own helpers: read the path if given, otherwise load by name with its skill tool. If it can do neither, the block is skipped silently.
5. Panel notes list the helper skills each reviewer actually used ("used: security-audit (WEB-PROTOCOL-AND-AUTH.md)"). Nothing is written about absent ones.

### Rules every "If installed" block follows

- Read-only use. Never trigger a mode that writes files, edits code, installs or downloads, or waits for a human.
- The helper skill supplies **checks and method**; the role file supplies **output format and severity**. Map the helper's severities onto CRITICAL/HIGH/MEDIUM/LOW; drop its verdicts and buckets.
- The built-in checklist still runs. The helper adds to it; it doesn't replace it.

### Per-role design

**Hacker (`hacker.md`) + security-audit**
- Use guidance mode only, never the six-phase audit or its output folder.
- Load companion files by the boundary the scope touches, not by language: web routes/sessions/tokens → `WEB-PROTOCOL-AND-AUTH.md`; front-end/DOM/storage → `CLIENT-SIDE.md`; prompts/model output/agent tools → `AI-AND-LLM.md`; multi-tenant queries, export/delete, migrations → `DATA-ISOLATION-AND-LIFECYCLE.md`; manifests/lockfiles/CI/release → `SUPPLY-CHAIN-AND-RELEASE.md`; IaC/IAM/containers/env → `CLOUD-AND-DEPLOYMENT.md`; queues/webhooks/RPC → `PROTOCOLS-RPC-AND-MESSAGING.md`; uploads/regex/unbounded work/paid APIs → `RESOURCE-EXHAUSTION-AND-AVAILABILITY.md`; native/FFI/parsers → `MEMORY-SAFETY-AND-BINARY.md`; desktop/mobile/IPC → `DESKTOP-MOBILE-AND-LOCAL-IPC.md`. Plus `ATTACK-CLASSES.md` sections for the classes in play, and from `HUNTING.md` only the "work from a concrete invariant" method and the candidate gate.
- Adopt its stricter rule for the whole hacker role, installed or not: a missing flag or best practice (cookie flags, rate limit, debug setting) is a finding only when a reachable impact is traced. This tightens hacker item 6.
- Mapping: its `confirmed` → finding (critical/high/medium/low → same names; `informational` dropped); its `needs_validation` → hotspot; trace sink → `file:line`; payload + observed result → Case; remediation → Fix. The panel's severity table wins where calibrations differ.
- Stays source-only (security-audit forbids running target code outside a sandbox). The tester and confused user keep running things. Registry lookups for "does this package exist" stay: they don't run target code.

**Senior (`senior.md`) + ponytail**
- `ponytail-review`: use its *Lean* checks (delete, reuse, stdlib/native, yagni, merge, split) and its "fix applied in one caller while the shared function stays broken" check. Skip its Risk, Missing-test and Scale parts (hacker, tester and performance own those), its Must/Should/Nice buckets, verdict and `Lean: -N` line.
- `ponytail-debt`: run its marker search over the scope's files. A `shortcut:`/`ponytail:` marker with no upgrade trigger in **new** code is LOW; one whose limit the expected load already crosses is a finding (severity by impact). Otherwise markers stay decisions, not findings (lead's existing rule).
- Built-in (always): use `ast-grep`/`sg` when installed for duplicate and caller search; otherwise grep.

**Confused user (`confused-user.md`) + playwright-cli**
- If the project has a dev/start script that comes up locally within ~2 minutes with no extra setup (no database to create, no secrets to fill), drive the changed flow in a real browser and quote what the user sees. Never point it at a deployed URL. Otherwise reason from code, as today.

**UI & accessibility (`ui.md`, new)**
- Built-in checklist: form fields have labels; images have alt text; clickable things are real buttons/links and keyboard-reachable; visible focus; contrast of new colours (4.5:1 for text); error, empty and loading states exist and say something useful; layout at a phone width; long text doesn't break layout; `prefers-reduced-motion` for new motion; mobile web basics (100vh, inputs under 16px zoom the page). Each finding still needs a concrete case ("a screen-reader user hears 'button' with no name on the icon-only submit").
- If installed: `playwright-cli` (same start-script rule as confused user) for a snapshot/accessibility tree of the changed screen; `ui-ux-pro-max` for its accessibility and UX rule lookups; `impeccable` `audit` only if its binary is already present (no first-run download), never its edit/craft paths; `review-animations` only when motion code changes; `mobile-native` only for mobile-web layouts.
- Severity: a flow a keyboard or screen-reader user can't complete is HIGH; missing labels/contrast MEDIUM; polish LOW.

**Performance (`performance.md`, new)**
- Reads code only. Every finding names **the load it breaks at** and why ("at 10k rows the export builds the whole list in memory", "with 2 workers the in-memory rate limit counts per process").
- Built-in checklist: query or request per item in a loop; missing pagination/limit on lists from storage or input; caches, lists or maps that only grow; O(n²) on input that can be large; check-then-write races; per-process state that must be shared across workers; blocking I/O in async handlers; new queries filtering/sorting on unindexed columns; retries without backoff or limit; paid or rate-limited API calls in loops; large payloads loaded or returned whole.
- If installed: `ponytail-review`'s Scale section as an extra checklist; `security-audit`'s `RESOURCE-EXHAUSTION-AND-AVAILABILITY.md` when input controls the amount of work.
- Only flag what breaks at the Step 0 load or at a size the domain makes plausible; say which.
- Severity (user's decision): breaks at the load stated in the README/deploy config, or on the main flow → **HIGH** (blocks). Breaks only at a size the domain makes plausible but nobody stated → **MEDIUM**. Minor speed-ups → LOW.
- Default load (user's decision): when nothing states the load, Step 0 assumes **few users** and says so; Performance then joins only through the code triggers.

**Data & deploy (`data-deploy.md`, new)**
- Built-in checklist: migrations that drop or rename columns/tables with live data, or can't be rolled back; `NOT NULL` added without a default/backfill; backfills or updates over a whole table in one statement; locking a big table during deploy; code and schema shipped in an order that breaks the running version; new env vars/settings with no default and no documentation (crash on deploy); config defaults that differ between dev and prod in a dangerous way; Dockerfile running as root or copying secrets/`.env` into an image; CI jobs that deploy without running tests; cron/backup scripts that can fail silently.
- If installed: `security-audit`'s `DATA-ISOLATION-AND-LIFECYCLE.md` (deletion, retention, restore) and `CLOUD-AND-DEPLOYMENT.md` for checks that aren't pure security.
- Data loss stays CRITICAL per the existing severity table.

**Tester (`tester.md`)**: no integration. Unchanged.

**Lead and fix loop (`SKILL.md`)**
- Step 4, if the superpowers skills are present: before applying each fix, check it with `receiving-code-review` (is the finding still right?); when a fix's tests fail, use `systematic-debugging` before trying again; before stating the round-2 result, `verification-before-completion`. The panel's rules win over theirs: use their checks, don't stop the loop to ask. If a finding turns out wrong, skip that fix and say why; if one fix still fails after its debugging pass, leave it open and report it in the round comparison instead of retrying forever.
- Hotspots + opencode-mem (if a `memory` tool exists): the lead searches memory for an earlier answer to the same hotspot (same file and question). If one exists, it still lists the hotspot, marked "previously answered: <answer>, <date>", so a changed context stays visible. It saves an answer only when the user gives one in the chat. It never drops a hotspot because of memory.

### Other files

- **`report-template.md`**: Panel notes gain sections 5-7, written only for roles that joined. Scope header lists which conditional roles joined and why. New PT labels: "UI e acessibilidade", "Desempenho", "Dados e deploy". Panel notes line "used: <helper skills>" when any.
- **`tools.md`**: add rows for `ast-grep`/`sg` (structural search), `shellcheck`, `hadolint`, `actionlint`. Mention `uvx`/`docker` only as ask-first.
- **`SKILL.md` frontmatter description**: mention the conditional roles; stay under 1024 characters; keep the PT triggers.
- **`README.md`**: roster table with the new roles, and a short "Works better with" section listing the optional skills and what each adds, stating clearly that none is required.

## Testing

Writing-skills method: baseline the current skill on the new cases (RED), then the new version (GREEN), graded by independent agents.

- **Isolation:** this machine already has most optional skills installed and `case.yaml` can't toggle them, so standalone runs use an isolated agent config whose skills folder holds only `code-review-team`; integration runs use the normal config.
- **Standalone (no optional skills):** all 6 existing evals must still pass. Add a grader to `small-change-duplicates-helper` (Python, no UI/migration/query): UI and Data & deploy do **not** join.
- **New cases** (in `evals/`, existing `claude plugin eval` format):
  - a front-end change with a missing label and an icon-only button → UI role joins and flags them;
  - a README saying "many users" and a change with a query per item and an unbounded cache → Performance joins and states the load each breaks at;
  - a migration dropping a column with data plus a new required env var with no default → Data & deploy joins and flags both; the drop is CRITICAL.
- **Integration (with `security-audit` and `ponytail` installed):** on `ai-written-reset-branch`, the hacker's notes show it used `security-audit` guidance mode and no `~/security-audit-skill/` folder was created; on `small-change-duplicates-helper`, the senior's notes show `ponytail-review` was used; the report format is unchanged in both.

## My calls (check these)

- **Join predicates are file/content based plus the Step 0 load**, not keywords in the prompt, so they can be checked.
- **Scale moves entirely to Performance** (senior item 8 removed).
- **The hacker adopts "a flag isn't a finding without traced impact" even without security-audit installed.** It's a quality rule, not an integration.
- **opencode-mem and the superpowers fix-loop skills are included**; `headroom`, `rea`, `figma`, `typeui`, `plannotator`, `understand-*`/`graphify` and the design-taste skills are left out: they don't help review, need state that usually isn't there, or block on a human. `plannotator` can come later as an opt-in "show me in the review UI" step.
- **Playwright is only used when a local start script works without setup**; otherwise the role reasons from code.

## Left to the builder

- Exact checklist wording in the three new role files and the "If installed" blocks.
- Wording of the eval prompts and graders, and the planted bugs.
- README layout.

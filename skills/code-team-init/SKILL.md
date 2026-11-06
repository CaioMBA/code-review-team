---
name: code-team-init
description: Sets up which AI model each kind of coding work runs on, a small model for searching and reading files, a mid model for side tasks and a top model for planning, to cut token spend on all AI coding, not only reviews. Works in OpenCode, Claude Code, Cursor and GitHub Copilot, globally by default or for one project. Offers three spend profiles (Economy, Balanced, Max) and creates the review-small, review-mid and review-top agents the code-review-team skill uses. Use for "set up my models", "save tokens", "configure agents", "configure models", "init code team", "use max models" or "init this project". Shows every change and asks before writing anything.
---

# Code Review Team init: the right model for each job

Most AI coding tokens go to work a small model does just as well: finding files, reading code, writing titles. This skill points that work at a small model, keeps planning and hard reviews on strong ones, and creates the `review-*` agents the `code-review-team` panel looks for. The review works without this skill; init only makes it cheaper or stronger.

**Never touch** API keys, providers, permissions or MCP servers. Never read auth or credential files, and never connect to a running tool's server or port to learn models: use only the list commands in the reference files, and ask the user when they fail. Change only model and agent settings, agent files, and one marked block in a rules file. **Never write** before showing the change and getting a yes.

Per-tool paths, file formats, examples and gotchas: [references/opencode.md](references/opencode.md), [references/claude-code.md](references/claude-code.md), [references/cursor.md](references/cursor.md), [references/copilot.md](references/copilot.md). Read the file for each tool you configure before proposing anything for it.

## Step 1: Detect tools

Check which exist: config folders `~/.config/opencode`, `~/.claude`, `~/.cursor`, `~/.copilot`, VS Code user data; CLIs on PATH `opencode`, `claude`, `agent` or `cursor-agent`, `copilot`. Configure every tool found. Ask which tools the user has only if none is found.

**Scope.** Global (user-level files) by default. Project files only when the user asks ("init this project"); say they can be committed so the team shares them.

## Step 2: Detect models

List what the user can really use, per tool (commands in each reference file): `opencode models`; Claude Code aliases `haiku`, `sonnet`, `opus`, `fable`; Cursor `agent --list-models`; Copilot has no list command, so ask the user to read their model picker. When a tool can't list models, show the tiers to fill (small, mid, top, max) and ask the user to pick one model for each. **Never propose a model the user can't access.**

- **small**: the cheapest capable model (Haiku class). **mid**: Sonnet class. **top**: Opus class.
- **max**: the strongest model available: Claude Fable (e.g. `claude-fable-5-1`) or GPT-6 Astra (`gpt-6-astra`). Neither available: max = top. Say so before applying.
- Prefer one provider per tool, the one the user's main model already uses. If the list has no models from that provider, don't fill tiers from other providers' models: ask the user which models to use.

## Step 3: Ask the profile

Ask once: **"Economy, Balanced or Max?"** Default **Balanced**. Show this table:

| Profile | Small work (search, titles) | Reviewers on small today (confused user, tester, UI) | Reviewers on mid today (senior, performance, data & deploy) | Top today (hacker on security code) | Planning (init) |
|---|---|---|---|---|---|
| Economy | small | small | small | mid | mid |
| **Balanced** (default = today) | small | small | mid | top | top |
| Max | small | mid | top | **max** | **max** |

- Search stays small in every profile: a bigger model doesn't find files better, only slower.
- Before applying Max, say: "Fable and Astra cost about 2.5x Opus per token." Also suggest starting the session itself on the max model, since the lead runs on the session's model and no setting here changes it.
- Each `review-<tier>` agent runs on **its own tier's model** (`review-mid` = mid model). The review skill reads the profile and picks which agent each reviewer gets, so never shift the agents' models by profile. `review-max` is created only under Max.

## Step 4: Propose, per tool

Fill this table through the profile and the Step 2 models, and show it:

| Work | Tier | OpenCode | Claude Code | Cursor | Copilot |
|---|---|---|---|---|---|
| Searching/reading files | small | built-in `explore` | `Explore` agent file on the small model (overrides the built-in, which runs on the main model) | `search` agent + routing line | `search` agent + routing line |
| Titles, summaries, compaction | small | built-ins `title`, `summary`, `compaction` | built in, skip | none | none |
| Multi-step side tasks | mid | built-in `general` | built in, skip | built in, skip | `general` agent + routing line |
| Writing code | user's main model | `build`: shown, not changed | `model`: shown, not changed | none | none |
| Planning, hard problems | profile's Planning column | built-in `plan` | optional `opusplan` | none | none |
| Review panel | own tier | `review-small/mid/top` (+ `review-max`) | none (per-call `model`) | `review-small/mid/top` (+ `review-max`) | `review-small/mid/top` (+ `review-max`) |
| Profile line | none | marked block | marked block | marked block | marked block |

- Replace a tool's built-in agents by name only in OpenCode, where re-modelling built-ins is the documented way, and Claude Code's `Explore`: its built-in runs on the main model (Opus or Fable), so searching is where the biggest saving is. Say in the proposal that this overrides the built-in.
- Claude Code otherwise gets only the profile line in its block and, if the user opts in, `opusplan`. No `review-*`, `general` or `search` agents there: its per-call `model` already picks reviewer models.
- Cursor agents go in `~/.cursor/agents`, never `~/.claude/agents` (Claude Code would load them too).
- `search` agents are read-only where the tool supports it. `review-*` agents get full tools (the tester writes test files) and this body: "You are a reviewer on a code review panel. Follow the prompt you are given exactly."
- The main coding model is shown but never changed unless the user asks.

**If installed** (optional; look in the same skill and agent folders as Step 1, skip silently when missing):
- **`cavecrew` agents** (an agent file named `cavecrew-investigator` exists, from the caveman plugin): route searches there instead of creating `search`, and set its model to the small tier only where the tool allows a model per agent. Its answers are compressed `path:line` lists, so each search costs the main session less.
- **`caveman-explore` skill**: when you create a `search` agent (or Claude Code's `Explore` override), make its body "Read and follow the `caveman-explore` skill at <path>." instead of the default, so it returns only `path:line` lists. Keep it read-only.
- **`caveman-stats` / `caveman-learn`**: in Step 7, suggest measuring token use with them before and after this setup. Never claim a saving you haven't measured.

## Step 5: Show the change

For every file, a short before/after: the JSON keys added or changed, each new agent file in full, the marked block. Then ask once per scope:

- "Apply / edit / skip?" (edit: take the user's changes, show again).
- Separately, if Claude Code was found: "Also switch Claude Code's main model to `opusplan` (Opus plans, Sonnet writes)? yes / no" Default **no**.

## Step 6: Write (only after yes)

1. **Back up** each existing file before its first change today: copy to `<file>.bak-<YYYYMMDD>`. If today's backup exists, keep it; don't overwrite.
2. **JSON/JSONC**: edit in place. Add or change only the agent/model keys shown. Keep comments, key order, formatting and every other key. Re-read the file afterwards and check it still parses (JSONC: comments allowed).
3. **Agent files**: create only if absent. If one exists and differs, show the diff and ask: replace, keep, or skip.
4. **Marked block**: in the tool's rules file (path in its reference), keep exactly one block. If the markers exist, replace what is between them; else append the block at the end. Never add a second block. A block with the old markers `<!-- code-review-team-init:start/end -->` (this skill's former name) counts as the same block: replace it, markers included. It holds only routing lines for agents this run created, plus the profile line:

```
<!-- code-team-init:start -->
- Delegate file searches and code reading to the `search` agent (small model).
- Delegate multi-step side tasks to the `general` agent.
code-review-team profile: balanced
<!-- code-team-init:end -->
```

Write the profile line exactly as `code-review-team profile: <economy|balanced|max>`, lowercase; the review skill reads it.

**Re-run.** If everything already matches, write nothing, make no backup, and report "already set". Change only what differs.

**Unknown tool** (none of the four, or a file you can't safely edit, such as Cursor's global User Rules): don't guess a path. Print a paste-in snippet (the block and agent definitions) and say where it usually goes.

## Step 7: Report

- What changed, per file, and what was already set.
- Where the backups are.
- How to undo: restore `<file>.bak-<YYYYMMDD>`, or delete the agent files created and the marked block.
- Any tier that fell back (e.g. "max = top: no Fable or Astra in your model list").
- Snippets printed for tools init couldn't edit.
- Restart the tool if its reference says new agents need one.

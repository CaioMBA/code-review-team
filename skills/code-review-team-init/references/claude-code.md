# Claude Code

Source: https://code.claude.com/docs/en/sub-agents, https://code.claude.com/docs/en/model-config (checked 2026-11-05).

## What init writes here

Only three things, by design:

1. An `Explore` agent file on the small model. The built-in Explore runs on the main conversation's model (Opus when that is Fable), and a user agent with the same name overrides it. This is the biggest saving in Claude Code; say in the proposal that it replaces the built-in's model.
2. The marked block with the profile line (always).
3. `"model": "opusplan"` in settings, only if the user answered yes to the separate opt-in.

No `review-*` agents (the panel's per-call `model` already picks `haiku`/`sonnet`/`opus`/`fable`), no `general` agent (built-in `general-purpose` stays), no `search` agent. Create more only if the user asks for it explicitly.

## Paths

| What | Global | Project ("init this project") |
|---|---|---|
| Rules file (marked block) | `~/.claude/CLAUDE.md` | `CLAUDE.md` in the repo root |
| Settings (`opusplan`) | `~/.claude/settings.json` | `.claude/settings.json` |
| Agent files (only if asked) | `~/.claude/agents/<name>.md` | `.claude/agents/<name>.md` |

If `CLAUDE_CONFIG_DIR` is set, use it instead of `~/.claude`.

## Model IDs and listing

- Aliases: `haiku` (small), `sonnet` (mid), `opus` (top), `fable` (max; Fable 5.1), `opusplan` (Opus in plan mode, Sonnet otherwise), `default`. Full IDs such as `claude-opus-5-5` or `claude-fable-5-1` also work.
- No list command. The `/model` picker shows what the account can use; Fable may be marked "Requires usage credits". If unsure whether Fable is available, ask the user; if not, max = top (`opus`).
- Agent frontmatter `model`: `haiku`, `sonnet`, `opus`, `fable`, a full ID, or `inherit`.

## Example: marked block

Append to `~/.claude/CLAUDE.md`:

```
<!-- code-review-team-init:start -->
code-review-team profile: balanced
<!-- code-review-team-init:end -->
```

## Example: settings merge (`opusplan`, opt-in only)

Before:

```json
{ "permissions": { "allow": ["Bash(npm test)"] }, "model": "opus" }
```

After (only `model` changes; tell the user the old value so they can go back):

```json
{ "permissions": { "allow": ["Bash(npm test)"] }, "model": "opusplan" }
```

## Example: Explore override

`~/.claude/agents/Explore.md` (use the full small-model ID, not the `haiku` alias: Cursor and VS Code also read `~/.claude/agents/` and don't know Claude Code's aliases):

```markdown
---
name: Explore
description: Fast read-only agent for finding files, searching code and answering questions about the codebase. Use for any search or code reading.
model: claude-haiku-5-5
tools: Read, Grep, Glob, Bash
---

Find what you are asked for and report paths, line numbers and short excerpts. Never edit files.
```

## Example: agent file (only if the user asks for one)

`~/.claude/agents/review-mid.md`:

```markdown
---
name: review-mid
description: Reviewer on the code-review-team panel (mid tier). Use only for panel reviews.
model: sonnet
---

You are a reviewer on a code review panel. Follow the prompt you are given exactly.
```

`name` and `description` are required; no `tools` line means all tools.

## Max profile

The lead runs on the session's model. Suggest starting the session with `claude --model fable` (or `/model fable`) for Max reviews.

## Gotchas

- **Explore is not always Haiku** (current docs: it follows the main model). That's why init writes the `Explore` override above. If the user doesn't want built-ins replaced, skip it and say searches stay on the main model.
- A `/model` switch also changes subagents that inherit the main model.
- `~/.claude/agents/` is also read by Cursor and VS Code; that is why Cursor's agents go in `~/.cursor/agents`.
- If `~/.claude/agents/` didn't exist when the session started, new agent files need a restart.
- Settings precedence: project and managed settings, `--model` and `ANTHROPIC_MODEL` override the user `model` setting. If `opusplan` doesn't take effect, check those.
- `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` makes every subagent ignore its `model`; mention it in the report if set.

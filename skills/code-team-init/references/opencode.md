# OpenCode

Source: https://opencode.ai/docs/agents/, https://opencode.ai/docs/config/ (checked 2026-11-05).

## Paths

| What | Global | Project ("init this project") |
|---|---|---|
| Config (built-in agent models) | `~/.config/opencode/opencode.json` (or `opencode.jsonc`) | `opencode.json` in the repo root |
| Agent files (`review-*`) | `~/.config/opencode/agents/<name>.md` | `.opencode/agents/<name>.md` |
| Rules file (marked block) | `~/.config/opencode/AGENTS.md` | `AGENTS.md` in the repo root |

Use whichever config file already exists (`.json` or `.jsonc`); if neither does, create `opencode.json`.

## Model IDs and listing

- Format `provider/model-id`, e.g. `anthropic/claude-haiku-5-5`, `anthropic/claude-sonnet-5-5`, `anthropic/claude-opus-5-5`, `anthropic/claude-fable-5-1`, `openai/gpt-6-astra`.
- `opencode models` lists the models the user can use. Pick only from it. Prefer the provider of the current top-level `model`.
- `opencode agent list` shows the loaded agents and is a good check after writing.

## Built-ins you may re-model

Re-modelling built-ins through `agent.<name>.model` is the documented way here. Change only `model`; never touch their `permission`, `prompt` or `mode`.

| Built-in | Tier |
|---|---|
| `explore` (read-only search subagent) | small |
| `title`, `summary`, `compaction` (hidden) | small |
| `general` (multi-step subagent) | mid |
| `plan` (primary) | profile's Planning column: economy mid, balanced top, max max |
| `build` (primary) | show only; change only if the user asks |

## Example: config merge

Before (JSONC with other keys; keep all of it):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // my plugins
  "plugin": ["opencode-foo"],
  "mcp": { "bar": { "type": "local", "command": ["bar"] } },
  "model": "anthropic/claude-opus-5-5"
}
```

After (only the `agent` key added; if `agent` exists, add or change only the `model` of these names):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // my plugins
  "plugin": ["opencode-foo"],
  "mcp": { "bar": { "type": "local", "command": ["bar"] } },
  "model": "anthropic/claude-opus-5-5",
  "agent": {
    "explore": { "model": "anthropic/claude-haiku-5-5" },
    "title": { "model": "anthropic/claude-haiku-5-5" },
    "summary": { "model": "anthropic/claude-haiku-5-5" },
    "compaction": { "model": "anthropic/claude-haiku-5-5" },
    "general": { "model": "anthropic/claude-sonnet-5-5" },
    "plan": { "model": "anthropic/claude-opus-5-5" }
  }
}
```

## Example: agent file

`~/.config/opencode/agents/review-mid.md` (the file name is the agent name). Same for `review-small`, `review-top` and, under Max only, `review-max`, each with its own tier's model:

```markdown
---
description: Reviewer on the code-review-team panel (mid tier). Start it only for panel reviews.
mode: subagent
model: anthropic/claude-sonnet-5-5
---

You are a reviewer on a code review panel. Follow the prompt you are given exactly.
```

No `permission` block: reviewers keep full tools. `description` is required.

## Example: marked block

Append to `~/.config/opencode/AGENTS.md` (OpenCode needs no routing lines; its built-ins are re-modelled):

```
<!-- code-team-init:start -->
code-review-team profile: balanced
<!-- code-team-init:end -->
```

## Gotchas

- A subagent without `model` runs on the caller's model, so an un-modelled `explore` on an Opus session searches on Opus.
- The config also has a top-level `small_model` for title generation. Leave it as it is; the `agent.title` entry is enough.
- Agent files and JSON agents can define the same name; keep `review-*` only as files so "create only if absent" works.
- Changes load on the next OpenCode start.

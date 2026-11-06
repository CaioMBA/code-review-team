# Cursor

Source: https://cursor.com/docs/subagents, https://cursor.com/docs/context/rules, https://cursor.com/docs/cli/reference/parameters (checked 2026-11-05).

## Paths

| What | Global | Project ("init this project") |
|---|---|---|
| Agent files | `~/.cursor/agents/<name>.md` | `.cursor/agents/<name>.md` |
| Rules (marked block) | User Rules in Cursor Settings (Customize → Rules); **no documented file**, so print the block for the user to paste | `.cursor/rules/code-review-team-init.mdc` |

Never write Cursor agents to `~/.claude/agents` or `.claude/agents`: Cursor reads them, but Claude Code would load them too.

## Model IDs and listing

- `agent --list-models` (older installs: `cursor-agent --list-models`) or `agent models` lists the models the account can use. Pick only from it. If the CLI isn't installed, ask the user to read the model picker and give one model ID per tier.
- Agent `model`: `inherit` (default) or a model ID, e.g. `composer-2`, `claude-opus-5`. Bracket options are allowed, e.g. `claude-opus-5[effort=high]`; don't add them unless the user asks.
- max: a Fable or GPT-6 Astra ID from the list, else the top model.

## Built-ins

Built-in `explore` and `browser` pick their own model; they are not re-modelled. Init adds a `search` agent and a routing line instead. Built-in side tasks: skip (no `general` agent here).

## Example: search agent

`~/.cursor/agents/search.md`:

```markdown
---
name: search
description: Fast read-only search. Use proactively to find files, search code and read code, and return paths with short snippets.
model: <small model ID from the list>
readonly: true
---

Search and read the codebase for what you are asked. Return the relevant file paths, line numbers and short snippets. Don't edit anything.
```

## Example: review agent

`~/.cursor/agents/review-mid.md` (same for `review-small`, `review-top`, and `review-max` under Max only, each with its own tier's model):

```markdown
---
name: review-mid
description: Reviewer on the code-review-team panel (mid tier). Use only when a panel review starts it.
model: <mid model ID from the list>
---

You are a reviewer on a code review panel. Follow the prompt you are given exactly.
```

No `readonly`: reviewers keep full tools.

## Example: marked block

Project file `.cursor/rules/code-review-team-init.mdc` (whole file when init creates it; if it exists, replace only between the markers):

```
---
description: code-review-team-init model routing
alwaysApply: true
---

<!-- code-review-team-init:start -->
- Delegate file searches and code reading to the `search` agent (small model).
code-review-team profile: balanced
<!-- code-review-team-init:end -->
```

Global: print the same block (without the frontmatter) and ask the user to paste it into Cursor Settings → Rules → User Rules. Re-runs: ask them to replace the old block, not add a second one.

## Gotchas

- Project rules must be `.mdc`; a plain `.md` in `.cursor/rules` is ignored.
- Name clash: `.cursor/` wins over `.claude/` and `.codex/`; project agents win over user agents.
- Cursor may ignore an agent's `model` (admin block, plan limits, legacy request plans without Max Mode, where subagents run on Composer). Say so in the report if the user is on such a plan.
- Named third-party models bill as third-party usage even when the parent chat is on Auto.
- A user-level rules file path (e.g. `~/.cursor/rules`) is not documented. Don't write one; if the user knows their version supports it, follow their lead.

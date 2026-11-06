# GitHub Copilot (VS Code and Copilot CLI)

Source: https://docs.github.com/en/copilot/reference/custom-agents-configuration, https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference, https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference, https://code.visualstudio.com/docs/agents/reference/custom-instructions-reference (checked 2026-11-05).

## Paths

| What | Global | Project ("init this project") |
|---|---|---|
| Agent files | `~/.copilot/agents/<name>.agent.md` | `.github/agents/<name>.agent.md` |
| Rules (marked block) | `~/.copilot/copilot-instructions.md` | `.github/copilot-instructions.md` |

`~/.copilot` is shared by the Copilot CLI and VS Code's Copilot harness. If `COPILOT_HOME` is set, use it instead. VS Code's "Local" harness keeps user agents in profile storage instead; files there are out of scope.

## Model IDs and listing

- No non-interactive list command. Ask the user to open `/model` in `copilot` or the model picker in VS Code and give one model per tier. Never guess an ID.
- `model` takes the runtime model ID, e.g. `claude-haiku-4.5`, `claude-sonnet-4.6` (dotted versions). VS Code's editor completions insert the right ID. Names like `Claude Sonnet 4.5 (copilot)` are the VS Code "Local" display format, used in handoffs; don't use them in `~/.copilot/agents`.
- Fallback list: the VS Code schema accepts `model` as a list and the CLI has `models: [...]`, both tried in order. Use them only if the user wants a fallback; a single `model` string works in both clients.

## Built-ins

The CLI ships `explore`, `task`, `general-purpose`, `code-review`, `research` and others with their own default models. Don't replace them by name. Init adds `search`, `general` and `review-*` agents next to them, with routing lines for `search` and `general`.

## Example: search agent

`~/.copilot/agents/search.agent.md`:

```markdown
---
name: search
description: Fast read-only search. Use to find files, search code and read code, and return paths with short snippets.
model: <small model ID>
tools: ['read', 'search']
---

Search and read the codebase for what you are asked. Return the relevant file paths, line numbers and short snippets. Don't edit anything.
```

## Example: general agent

`~/.copilot/agents/general.agent.md`:

```markdown
---
name: general
description: Multi-step side tasks (research, small changes across files) that would flood the main conversation.
model: <mid model ID>
---

Do the task you are given, end to end, and return a short summary of what you did and found.
```

## Example: review agent

`~/.copilot/agents/review-mid.agent.md` (same for `review-small`, `review-top`, and `review-max` under Max only, each with its own tier's model):

```markdown
---
name: review-mid
description: Reviewer on the code-review-team panel (mid tier). Use only when a panel review starts it.
model: <mid model ID>
---

You are a reviewer on a code review panel. Follow the prompt you are given exactly.
```

No `tools` line: all tools. `description` is required.

## Example: marked block

Append to `~/.copilot/copilot-instructions.md`:

```
<!-- code-review-team-init:start -->
- Delegate file searches and code reading to the `search` agent (small model).
- Delegate multi-step side tasks to the `general` agent.
code-review-team profile: balanced
<!-- code-review-team-init:end -->
```

## Gotchas

- When the session model is **Auto**, subagents run on the session's resolved model and ignore their `model`. Say so in the report.
- A model the plan can't use falls back to the session model silently (unless `modelPolicy: required`, which init doesn't set).
- A `subagents` override in `~/.copilot/settings.json` or the `/subagents` picker beats the agent's `model`.
- Precedence in the CLI: user `~/.copilot/agents` beats project `.github/agents` for the same name.
- Subagents don't read repository instructions unless `include-custom-instructions: true`; the routing block is for the main agent only, which is what it needs.
- New agent files load in a new session.

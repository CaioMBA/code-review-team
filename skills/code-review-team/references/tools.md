# Tool pass

Hard evidence before opinions. Rules:

- **Project scripts first.** If `package.json` scripts, a `Makefile`, `justfile`, `pyproject.toml`, `tox.ini`, `composer.json` or CI config (`.github/workflows/*`) defines lint/typecheck/test commands, run those: they're what the project trusts.
- **Only already-installed tools.** Check with `<tool> --version` (or `Get-Command <tool>` on Windows). Use `npx --no-install` so npx never downloads. **Never install anything** without asking; a missing tool goes in *Not checked*.
- **Changed lines matter most.** Errors on changed lines block the gate. Pre-existing warnings elsewhere are "existing" at most, and not worth listing one by one.
- Run tools from the repo root, with a time limit (≈2 minutes each). A tool that hangs or needs setup (database, env vars) is *Not checked*, with the reason.
- Record `command → one-line result`. Keep raw output of failures for the reviewers.

## By stack

| Stack (detect by) | Lint / static | Types | Tests | Dependency audit |
|---|---|---|---|---|
| JS/TS (`package.json`) | `npm run lint`, `npx --no-install eslint .`, `npx --no-install biome check .` | `npx --no-install tsc --noEmit` | `npm test` | `npm audit --omit=dev` (also `pnpm audit`, `yarn npm audit`) |
| Python (`pyproject.toml`, `requirements*.txt`, `*.py`) | `ruff check .`, `flake8` | `mypy .`, `pyright` | `pytest -q`, else `python -m unittest` | `pip-audit` |
| Go (`go.mod`) | `go vet ./...`, `staticcheck ./...` | (compiler) | `go test ./...` | `govulncheck ./...` |
| Rust (`Cargo.toml`) | `cargo clippy` | (compiler) | `cargo test` | `cargo audit` |
| Java/Kotlin (`pom.xml`, `build.gradle*`) | project's checkstyle/spotbugs task | (compiler) | `mvn -q test`, `./gradlew test` | `./gradlew dependencyCheckAnalyze` if configured |
| .NET (`*.csproj`, `*.sln`) | `dotnet build -warnaserror` (changed files only matter) | (compiler) | `dotnet test` | `dotnet list package --vulnerable` |
| PHP (`composer.json`) | `vendor/bin/phpstan analyse`, `phpcs` | (phpstan) | `vendor/bin/phpunit` | `composer audit` |
| Ruby (`Gemfile`) | `rubocop` | — | `bundle exec rspec`, `rake test` | `bundle audit` |

## Any stack

| Check | Command |
|---|---|
| Secrets | `gitleaks detect --no-banner` or `trufflehog filesystem . --no-update`; otherwise grep changed files for `key`, `secret`, `token`, `password`, `sk_live_`, `AKIA`, `-----BEGIN` |
| Broader static analysis | `semgrep scan --config auto` (downloads rules, so it needs network) |
| Whitespace/conflict markers | `git diff --check` |
| Tracked env files | `git ls-files | grep -i '\.env'` |
| Structural search (duplicates, callers) | `ast-grep run -p '<pattern>' -l <lang>` (also `sg`) |
| Shell scripts changed | `shellcheck <files>` |
| Dockerfiles changed | `hadolint <Dockerfile>` |
| CI workflows changed | `actionlint` |

`uvx <tool>` and `docker run <image>` download things: ask before using them.

Python on Windows may only be available as `py` or a full path; try `py -m pytest` / `py -m unittest` before calling it missing.

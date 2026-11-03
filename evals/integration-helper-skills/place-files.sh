#!/usr/bin/env bash
# Same repo as ai-written-reset-branch: its base/ on main, its files/ on feature/password-reset (checked out).
set -eu
src="$(cd "$(dirname "$0")/../ai-written-reset-branch" && pwd)"
git init -q
git checkout -q -b main
git config user.email dev@example.com
git config user.name dev
cp -R "$src/base/." .
git add -A
git commit -q -m "initial shop utils"
git checkout -q -b feature/password-reset
cp -R "$src/files/." .
git add -A
git commit -q -m "Add password reset tokens"

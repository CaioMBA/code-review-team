#!/usr/bin/env bash
# base/ is committed on main; files/ is left as an uncommitted change.
set -eu
src="$(cd "$(dirname "$0")" && pwd)"
git init -q
git checkout -q -b main
git config user.email dev@example.com
git config user.name dev
cp -R "$src/base/." .
git add -A
git commit -q -m "ticket report"
cp -R "$src/files/." .

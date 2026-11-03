#!/usr/bin/env bash
# base/ is committed on main; files/ is committed on feature/newsletter (checked out).
set -eu
src="$(cd "$(dirname "$0")" && pwd)"
git init -q
git checkout -q -b main
git config user.email dev@example.com
git config user.name dev
cp -R "$src/base/." .
git add -A
git commit -q -m "blog home page"
git checkout -q -b feature/newsletter
cp -R "$src/files/." .
git add -A
git commit -q -m "Add newsletter signup box"

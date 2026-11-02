#!/usr/bin/env bash
# base/ is committed on main; files/ is committed on feature/bulk-discount (checked out).
set -eu
src="$(cd "$(dirname "$0")" && pwd)"
git init -q
git checkout -q -b main
git config user.email dev@example.com
git config user.name dev
cp -R "$src/base/." .
git add -A
git commit -q -m "pricing"
git checkout -q -b feature/bulk-discount
cp -R "$src/files/." .
git add -A
git commit -q -m "Add 10% bulk discount from 10 units"

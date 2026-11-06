#!/usr/bin/env bash
# base/ is committed on main; files/ is committed on feature/image-cache (checked out).
set -eu
src="$(cd "$(dirname "$0")" && pwd)"
git init -q
git checkout -q -b main
git config user.email dev@example.com
git config user.name dev
cp -R "$src/base/." .
git add -A
git commit -q -m "image loader"
git checkout -q -b feature/image-cache
cp -R "$src/files/." .
git add -A
git commit -q -m "image cache for the feed"

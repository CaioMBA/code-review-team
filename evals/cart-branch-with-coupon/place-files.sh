#!/usr/bin/env bash
# base/ is committed on main; files/ is committed on feature/coupon (checked out).
set -eu
src="$(cd "$(dirname "$0")" && pwd)"
git init -q
git checkout -q -b main
git config user.email dev@example.com
git config user.name dev
cp -R "$src/base/." .
git add -A
git commit -q -m "initial cart"
git checkout -q -b feature/coupon
cp -R "$src/files/." .
git add -A
git commit -q -m "discount coupon in the cart"

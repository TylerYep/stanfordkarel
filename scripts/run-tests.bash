#!/usr/bin/env bash

# If any command inside script returns error, exit and return that error
set -e

# Ensure that we're always inside the root of our application,
# no matter which directory we run script: Run `./scripts/run-tests.bash`
cd "${0%/*}/.."

# Auto-code formatters
f2format -q --no-archive .
isort -y
black . -l 100
git add .

# Style Checking
pylint **py

# Testing
pytest tests/
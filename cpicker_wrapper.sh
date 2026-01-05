#!/bin/bash
# cPicker wrapper script
# This script is symlinked to ~/.local/bin/cpicker

# Resolve symlink to find the actual repository directory
SCRIPT_PATH="${BASH_SOURCE[0]}"
while [ -L "$SCRIPT_PATH" ]; do
    SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
    SCRIPT_PATH="$(readlink "$SCRIPT_PATH")"
    [[ $SCRIPT_PATH != /* ]] && SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_PATH"
done
REPO_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

# Launch cPicker using the virtual environment
cd "$REPO_DIR" && "$REPO_DIR/venv/bin/python" -m cpicker "$@"

#!/bin/bash
# cPicker wrapper script
# This script is installed to ~/.local/bin/cpicker

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Find the cPicker installation directory
# If installed via install.sh, it will be in ~/.local/share/cpicker
CPICKER_DIR="${HOME}/.local/share/cpicker"

# If not found, try the script directory (development mode)
if [ ! -d "$CPICKER_DIR" ]; then
    CPICKER_DIR="$SCRIPT_DIR"
fi

# Launch cPicker
cd "$CPICKER_DIR" && python3 -m cpicker "$@"

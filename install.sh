#!/bin/bash
# cPicker installation script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================"
echo "  cPicker Installation"
echo "======================================"
echo ""

# Directories
BIN_DIR="${HOME}/.local/bin"

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "Error: Python 3.10 or higher is required (found $PYTHON_VERSION)"
    exit 1
fi
echo "Python $PYTHON_VERSION detected"
echo ""

# Check for required system packages
echo "Checking system dependencies..."
MISSING_DEPS=()

if ! command -v xclip &> /dev/null; then
    MISSING_DEPS+=("xclip")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "Missing system dependencies: ${MISSING_DEPS[*]}"
    echo "Please install with: sudo apt install ${MISSING_DEPS[*]}"
    exit 1
fi
echo "System dependencies OK"
echo ""

# Create virtual environment if needed
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
fi

# Install/update dependencies
echo "Installing Python dependencies..."
"$SCRIPT_DIR/venv/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"
echo "Python dependencies installed"
echo ""

# Create bin directory if needed
mkdir -p "$BIN_DIR"

# Symlink launcher script
echo "Installing launcher script..."
ln -sf "$SCRIPT_DIR/cpicker_wrapper.sh" "$BIN_DIR/cpicker"
echo "Launcher symlinked to $BIN_DIR/cpicker"
echo ""

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "WARNING: $BIN_DIR is not in your PATH"
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

# Ask to register keyboard shortcut
echo "Would you like to register the Super+Shift+C keyboard shortcut? (y/n)"
read -r REGISTER_SHORTCUT

if [ "$REGISTER_SHORTCUT" = "y" ] || [ "$REGISTER_SHORTCUT" = "Y" ]; then
    bash "$SCRIPT_DIR/scripts/register_shortcut.sh"
    echo ""
fi

echo "======================================"
echo "  Installation Complete!"
echo "======================================"
echo ""
echo "Usage:"
echo "  - Run: cpicker"
echo "  - Or press: Super+Shift+C (if registered)"
echo ""
echo "Features:"
echo "  - Press Super+Shift+C anywhere to launch"
echo "  - Move cursor to pick a color"
echo "  - Release key or click to copy hex code"
echo "  - Press Escape to cancel"
echo ""
echo "Repository: $SCRIPT_DIR"
echo ""

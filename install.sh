#!/bin/bash
# cPicker installation script

set -e

echo "======================================"
echo "  cPicker Installation"
echo "======================================"
echo ""

# Directories
INSTALL_DIR="${HOME}/.local/share/cpicker"
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
echo "Python $PYTHON_VERSION detected ✓"
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
echo "System dependencies OK ✓"
echo ""

# Create directories
echo "Creating installation directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
echo "Directories created ✓"
echo ""

# Copy files
echo "Installing cPicker files..."
cp -r cpicker "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"
echo "Files copied ✓"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user -q -r "$INSTALL_DIR/requirements.txt"
echo "Python dependencies installed ✓"
echo ""

# Install wrapper script
echo "Installing launcher script..."
cp cpicker_wrapper.sh "$BIN_DIR/cpicker"
chmod +x "$BIN_DIR/cpicker"
echo "Launcher installed to $BIN_DIR/cpicker ✓"
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
    bash scripts/register_shortcut.sh
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

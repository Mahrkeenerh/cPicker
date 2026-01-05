#!/bin/bash
# cPicker uninstallation script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================"
echo "  cPicker Uninstallation"
echo "======================================"
echo ""

# Remove launcher symlink
if [ -L "$HOME/.local/bin/cpicker" ]; then
    rm -f "$HOME/.local/bin/cpicker"
    echo "Removed launcher symlink"
elif [ -f "$HOME/.local/bin/cpicker" ]; then
    rm -f "$HOME/.local/bin/cpicker"
    echo "Removed launcher file"
else
    echo "Launcher not found (already removed)"
fi

# Remove keyboard shortcut
SCHEMA="org.gnome.settings-daemon.plugins.media-keys"
KEY_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/cpicker/"

if command -v gsettings &> /dev/null; then
    CUSTOM_LIST=$(gsettings get $SCHEMA custom-keybindings 2>/dev/null || echo "@as []")

    if [[ "$CUSTOM_LIST" =~ "cpicker" ]]; then
        echo ""
        read -p "Remove keyboard shortcut (Super+Shift+C)? (y/N): " remove_shortcut
        if [[ "$remove_shortcut" =~ ^[Yy]$ ]]; then
            # Remove cpicker from the custom keybindings list
            NEW_LIST=$(echo "$CUSTOM_LIST" | sed "s|, '$KEY_PATH'||g" | sed "s|'$KEY_PATH', ||g" | sed "s|'$KEY_PATH'||g")
            gsettings set $SCHEMA custom-keybindings "$NEW_LIST"

            # Reset the keybinding settings
            gsettings reset $SCHEMA.custom-keybinding:$KEY_PATH name 2>/dev/null || true
            gsettings reset $SCHEMA.custom-keybinding:$KEY_PATH command 2>/dev/null || true
            gsettings reset $SCHEMA.custom-keybinding:$KEY_PATH binding 2>/dev/null || true

            echo "Keyboard shortcut removed"
        else
            echo "Keyboard shortcut kept"
        fi
    fi
fi

# Optionally remove virtual environment
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo ""
    read -p "Remove virtual environment (venv folder)? (y/N): " remove_venv
    if [[ "$remove_venv" =~ ^[Yy]$ ]]; then
        rm -rf "$SCRIPT_DIR/venv"
        echo "Virtual environment removed"
    else
        echo "Virtual environment kept"
    fi
fi

# Clean up legacy installation if present
if [ -d "$HOME/.local/share/cpicker" ]; then
    echo ""
    read -p "Found legacy installation at ~/.local/share/cpicker. Remove it? (y/N): " remove_legacy
    if [[ "$remove_legacy" =~ ^[Yy]$ ]]; then
        rm -rf "$HOME/.local/share/cpicker"
        echo "Legacy installation removed"
    fi
fi

echo ""
echo "======================================"
echo "  Uninstallation Complete!"
echo "======================================"
echo ""
echo "Repository remains at: $SCRIPT_DIR"
echo ""

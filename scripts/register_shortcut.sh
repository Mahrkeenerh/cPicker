#!/bin/bash
# Register Super+Shift+C keyboard shortcut for cPicker in GNOME

SCHEMA="org.gnome.settings-daemon.plugins.media-keys"
KEY_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/cpicker/"

echo "Registering cPicker keyboard shortcut (Super+Shift+C)..."

# Check if gsettings is available
if ! command -v gsettings &> /dev/null; then
    echo "Error: gsettings not found. This script requires GNOME desktop environment."
    exit 1
fi

# Get current custom keybindings list
CUSTOM_LIST=$(gsettings get $SCHEMA custom-keybindings)

# Add our path if not already present
if [[ ! "$CUSTOM_LIST" =~ "cpicker" ]]; then
    # Remove trailing bracket, add our path, add bracket back
    if [ "$CUSTOM_LIST" = "@as []" ]; then
        # Empty list
        NEW_LIST="['$KEY_PATH']"
    else
        # Append to existing list
        NEW_LIST=$(echo "$CUSTOM_LIST" | sed "s|\]|, '$KEY_PATH']|")
    fi

    gsettings set $SCHEMA custom-keybindings "$NEW_LIST"
    echo "Added cPicker to custom keybindings list"
else
    echo "cPicker already in custom keybindings list"
fi

# Set keybinding details
gsettings set $SCHEMA.custom-keybinding:$KEY_PATH name "cPicker Color Picker"
gsettings set $SCHEMA.custom-keybinding:$KEY_PATH command "$HOME/.local/bin/cpicker"
gsettings set $SCHEMA.custom-keybinding:$KEY_PATH binding "<Super><Shift>c"

echo "Keyboard shortcut registered successfully!"
echo "Press Super+Shift+C to launch cPicker"

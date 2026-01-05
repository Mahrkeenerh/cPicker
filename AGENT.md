# cPicker - Agent Context

## Overview

cPicker is a lightweight Linux color picker that captures hex color codes from any pixel on screen. It's a GUI application for X11 that displays a magnified view of the cursor area and copies the selected color to the clipboard.

## Quick Commands

```bash
# Run color picker
cpicker

# Or run directly from repository
./venv/bin/python -m cpicker

# Reinstall/update
./install.sh

# Uninstall
./uninstall.sh
```

## Architecture

- **Type**: Application (not a daemon/service)
- **Display**: X11 only (not Wayland compatible)
- **Clipboard**: Uses xclip for clipboard operations
- **Shortcut**: Super+Shift+C (GNOME custom keybinding)

## Key Files

| File | Purpose |
|------|---------|
| `cpicker/picker_overlay.py` | Main overlay window with magnifier |
| `cpicker/utils/magnifier.py` | Magnified pixel view rendering |
| `cpicker/utils/capture.py` | Screen capture functionality |
| `cpicker/utils/clipboard.py` | Clipboard operations via xclip |
| `cpicker/utils/color.py` | Color format conversions |
| `cpicker/cli.py` | Command-line interface |

## Configuration

- No config file required
- Keyboard shortcut stored in GNOME settings (`gsettings`)

## Troubleshooting

### cPicker won't launch

1. Check X11 display:
   ```bash
   echo $DISPLAY
   echo $XDG_SESSION_TYPE  # Should be "x11", not "wayland"
   ```

2. Verify installation:
   ```bash
   which cpicker
   ls -la ~/.local/bin/cpicker  # Should be symlink to repo
   ```

3. Check virtual environment:
   ```bash
   ls -la /path/to/cpicker/venv/bin/python
   ```

### Clipboard not working

1. Verify xclip is installed:
   ```bash
   which xclip
   sudo apt install xclip
   ```

2. Test clipboard manually:
   ```bash
   echo "test" | xclip -selection clipboard
   xclip -selection clipboard -o
   ```

### Keyboard shortcut not working

1. Check if shortcut is registered:
   ```bash
   gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings
   ```

2. Re-register shortcut:
   ```bash
   ./scripts/register_shortcut.sh
   ```

3. Verify GNOME is detecting it:
   - Open Settings > Keyboard > Keyboard Shortcuts > Custom Shortcuts

### "Failed to connect to X11 display"

- You're likely running Wayland. cPicker requires X11.
- Switch to X11 session at login screen, or
- Run with XWayland (may have limitations)

### Module not found errors

Reinstall dependencies:
```bash
./venv/bin/pip install -r requirements.txt
```

## Dependencies

- Python 3.10+
- PyGObject (GTK bindings)
- python-xlib
- Pillow
- xclip (system package)

# cPicker

A lightweight Linux color picker that grabs hex codes from any pixel on screen.

## Features

- Press `Super+Shift+C` to activate, hover to preview, release to copy
- Live magnified view with grid overlay (21×21 pixels at 10x zoom)
- Instant hex code copy to clipboard
- RGB values and color swatch display

## Requirements

- Linux with X11
- GNOME (for keyboard shortcut)
- Python 3.10+
- System packages: `xclip`

## Installation

```bash
git clone https://github.com/yourusername/cPicker.git
cd cPicker
./install.sh
```

The installer will set up dependencies, install the tool to `~/.local/bin/cpicker`, and optionally register the `Super+Shift+C` keyboard shortcut.

## Usage

1. Press and hold `Super+Shift+C` (or run `cpicker` from terminal)
2. Move cursor over desired color while holding keys
3. Release keys or left-click to copy hex code
4. Press `Escape` or right-click to cancel

The copied hex code format is `#RRGGBB` (uppercase).

## Troubleshooting

**"Failed to connect to X11 display"**
- Ensure you're running X11, not Wayland: `echo $XDG_SESSION_TYPE`

**xclip not found**
```bash
sudo apt install xclip
```

**Keyboard shortcut not working**
```bash
./scripts/register_shortcut.sh
```

## License

MIT License - see LICENSE file for details

# cPicker

A lightweight Linux color picker tool that lets you grab hex color codes from any pixel on screen.

![cPicker Demo](https://img.shields.io/badge/version-1.0.0-blue) ![Python](https://img.shields.io/badge/python-3.10+-brightgreen) ![License](https://img.shields.io/badge/license-MIT-orange)

## Features

- **Press-Hold-Release Workflow**: Press `Super+Shift+C` to activate, keep holding to keep active, release to copy
- **Live Color Picking**: Hover over any pixel to see its color in real-time
- **Magnified View**: 21×21 pixel area shown at 10x zoom with grid overlay
- **Color Information**: Real-time display of hex code and RGB values
- **Instant Copy**: Release shortcut keys or click to copy hex code to clipboard
- **Lightweight**: ~650 lines of clean Python code
- **Fast**: Smooth 30 FPS magnifier updates (only 441 pixels captured per frame)

## Screenshot

```
┌─────────────────────────────────┐
│                                 │
│         ┌─────────┐             │  ← Magnified 21×21 pixels
│         │░░░░░░░░░│             │    at 10x zoom (210×210)
│         │░░▓▓▓▓▓░░│             │
│         │░░▓███▓░░│             │  ← Grid overlay
│         │░░▓▓▓▓▓░░│             │  ← Center pixel highlighted
│         │░░░░░░░░░│             │
│         └─────────┘             │
│                                 │
│   ┌─────────────────────────┐   │
│   │  ███  #3A7FBD           │   │  ← Hex code + color swatch
│   └─────────────────────────┘   │
│                                 │
│    R: 58  G: 127  B: 189       │  ← RGB values
│                                 │
└─────────────────────────────────┘
```

## Requirements

### System Requirements

- **OS**: Linux with X11
- **Desktop**: GNOME (for keyboard shortcut registration)
- **Python**: 3.10 or higher

### System Packages

```bash
sudo apt install xclip python3-pip
```

### Python Packages

- `python-xlib >= 0.33` - X11 screen capture
- `Pillow >= 10.0.0` - Image processing
- `PyQt6 >= 6.4.0` - GUI framework

## Installation

### Quick Install

```bash
git clone https://github.com/yourusername/cPicker.git
cd cPicker
./install.sh
```

The installer will:
1. Check Python version and system dependencies
2. Install Python packages
3. Copy files to `~/.local/share/cpicker`
4. Create launcher in `~/.local/bin/cpicker`
5. Optionally register `Super+Shift+C` keyboard shortcut

### Manual Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run directly from source:
```bash
python3 -m cpicker
```

3. Register keyboard shortcut (optional):
```bash
./scripts/register_shortcut.sh
```

## Usage

### Launch cPicker

**Method 1**: Keyboard shortcut (if registered)
- Press `Super+Shift+C` anywhere on your system

**Method 2**: Command line
```bash
cpicker
```

**Method 3**: From source
```bash
python3 -m cpicker
```

### Pick a Color

1. **Activate**: Press and hold `Super+Shift+C` (or run `cpicker` from terminal)
2. **Navigate**: While holding the keys, move your cursor over the color you want
3. **Pick**: Release the shortcut keys (or click left mouse button) to copy hex code
4. **Cancel**: Press `Escape` or right-click to exit without copying
5. **Paste**: Use `Ctrl+V` to paste the hex code anywhere

**Note**: The workflow is press-hold-release. Keep holding `Super+Shift+C` to keep the picker active, then release all keys to copy the color and close.

### Controls

| Action | Result |
|--------|--------|
| `Super+Shift+C` (press) | Launch color picker |
| `Super+Shift+C` (hold) | Keep picker active |
| `Super+Shift+C` (release) | Copy color and close |
| Mouse move | Update magnifier position |
| Left click | Copy color and close |
| Right click | Cancel without copying |
| `Escape` | Cancel without copying |

## Features in Detail

### Magnifier Widget

- **Size**: 210×210 pixels (21×21 source pixels at 10x zoom)
- **Grid**: Semi-transparent white grid for pixel visualization
- **Highlight**: Blue dashed border around center pixel
- **Positioning**: Adaptive placement to avoid screen edges

### Color Display

- **Hex Code**: Large monospace text (e.g., `#3A7FBD`)
- **RGB Values**: Formatted as `R:58 G:127 B:189`
- **Color Swatch**: Small square showing actual color
- **Live Update**: 30 FPS refresh rate

### Clipboard

- Copies text (hex codes) to clipboard using `xclip`
- Format: `#RRGGBB` (uppercase)
- Notification shown on successful copy (if `notify-send` available)

## Architecture

### File Structure

```
cpicker/
├── cpicker/
│   ├── __init__.py          # Package version info
│   ├── __main__.py          # Entry point for python -m cpicker
│   ├── cli.py               # Command-line interface
│   ├── picker_overlay.py    # Main overlay window
│   └── utils/
│       ├── capture.py       # X11 screen capture
│       ├── magnifier.py     # Magnifier widget
│       ├── clipboard.py     # Clipboard operations
│       ├── color.py         # RGB/hex conversion
│       └── theme.py         # UI colors and constants
├── scripts/
│   └── register_shortcut.sh # Keyboard shortcut registration
├── requirements.txt         # Python dependencies
├── install.sh              # Installation script
├── cpicker_wrapper.sh      # Launcher wrapper
└── README.md               # This file
```

### Technology Stack

- **PyQt6**: GUI framework for overlay and magnifier
- **python-xlib**: X11 screen capture and pixel reading
- **Pillow**: Image processing and pixel manipulation
- **xclip**: Clipboard text operations
- **gsettings**: GNOME keyboard shortcut registration

### Design Principles

1. **Lightweight**: Minimal dependencies, ~800 lines total
2. **Fast**: Captures only 21×21 pixels (441 pixels) per update
3. **Simple**: No window detection, file saving, or selection tools
4. **Reusable**: Modular architecture inspired by CaptiX

## Comparison with CaptiX

cPicker is inspired by [CaptiX](https://github.com/yourusername/captix), a screenshot tool. Here's how they differ:

| Feature | CaptiX | cPicker |
|---------|--------|---------|
| Purpose | Screenshot tool | Color picker |
| Screen capture | Full freeze | Live 21×21 regions |
| User action | Click/drag selection | Hover + release |
| Clipboard | PNG images | Hex text |
| Complexity | ~5,000 lines | ~800 lines |
| Shortcut | `Ctrl+Shift+X` | `Super+Shift+C` |

## Troubleshooting

### "Failed to connect to X11 display"

- Make sure you're running on X11 (not Wayland)
- Check: `echo $XDG_SESSION_TYPE` (should show "x11")
- Wayland users: Switch to X11 session or use Xwayland

### "xclip not found"

```bash
sudo apt install xclip
```

### Keyboard shortcut not working

1. Check registration:
```bash
gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings
```

2. Re-register:
```bash
./scripts/register_shortcut.sh
```

3. Verify binding:
```bash
gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/cpicker/ binding
```

### Colors are inaccurate

- Ensure your display color profile is correct
- Test with known colors (e.g., pure red `#FF0000`)
- Check if color management software is interfering

### Magnifier is laggy

- Reduce update frequency by editing `picker_overlay.py`:
```python
self.update_timer.start(50)  # Increase from 30ms to 50ms
```

## Development

### Run from source

```bash
python3 -m cpicker
```

### Run tests

```bash
# Test color conversion
python3 -c "from cpicker.utils.color import rgb_to_hex; print(rgb_to_hex(58, 127, 189))"
# Expected: #3A7FBD

# Test screen capture (requires X11)
python3 -c "from cpicker.utils.capture import capture_screen_region; img = capture_screen_region(0, 0, 21, 21); print(img.size)"
# Expected: (21, 21)
```

### Code structure

- `cli.py`: Argument parsing and app initialization
- `picker_overlay.py`: Main transparent overlay window
- `utils/magnifier.py`: Magnified view widget with color display
- `utils/capture.py`: X11 screen region capture
- `utils/clipboard.py`: Text clipboard operations
- `utils/color.py`: RGB ↔ Hex conversion
- `utils/theme.py`: UI colors and constants

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Credits

- Inspired by [CaptiX](https://github.com/yourusername/captix) screenshot tool
- Built with PyQt6, python-xlib, and Pillow

## Changelog

### v1.0.0 (2024-01-XX)

- Initial release
- Live color picking with magnifier
- Hex code and RGB display
- Clipboard integration
- GNOME keyboard shortcut support
- X11 screen capture

---

**Made with ❤️ for the Linux community**

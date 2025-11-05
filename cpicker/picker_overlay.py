"""Main color picker overlay window."""

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
from Xlib import display as xlib_display

from .utils.capture import capture_screen_region
from .utils.magnifier import MagnifierWidget
from .utils.clipboard import copy_text_to_clipboard
from .utils.color import rgb_to_hex
from .utils.theme import SOURCE_SIZE


class PickerOverlay(QWidget):
    """
    Transparent fullscreen overlay for color picking.

    Workflow: Press Super+Shift+C to activate, hold keys to keep active,
    release keys (or click) to copy color and close.
    """

    def __init__(self):
        """Initialize picker overlay."""
        super().__init__()

        # Window configuration
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.CrossCursor)

        # Fullscreen
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        # State
        self.cursor_x = 0
        self.cursor_y = 0
        self.current_hex = "#000000"
        self.current_r = 0
        self.current_g = 0
        self.current_b = 0

        # Keyboard state tracking for press-hold-release workflow
        self.x_display = None
        self.shortcut_keys_held = False
        self.monitoring_release = True

        # Initialize X11 display for keyboard state monitoring
        try:
            self.x_display = xlib_display.Display()
        except Exception as e:
            print(f"Warning: Cannot monitor keyboard state: {e}")
            self.monitoring_release = False

        # Create magnifier widget
        self.magnifier = MagnifierWidget()
        self.magnifier.show()

        # Update timer to limit capture frequency (30ms = ~33 FPS)
        # Only captures 21×21 pixels = 441 pixels per frame (very efficient)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_color)
        self.update_timer.start(30)

        # Keyboard state monitoring timer (check every 50ms)
        if self.monitoring_release:
            self.key_monitor_timer = QTimer()
            self.key_monitor_timer.timeout.connect(self._check_shortcut_release)
            self.key_monitor_timer.start(50)

        # Show and activate
        self.show()
        self.activateWindow()
        self.setFocus()

        # Initial position (center of screen)
        self.cursor_x = screen.width() // 2
        self.cursor_y = screen.height() // 2

    def mouseMoveEvent(self, event):
        """
        Handle mouse movement to update cursor position.

        Args:
            event: Mouse move event
        """
        self.cursor_x = event.pos().x()
        self.cursor_y = event.pos().y()

    def _update_color(self):
        """Update color from current cursor position (called by timer)."""
        # Capture 21×21 pixel area around cursor
        # This is very efficient - only 441 pixels per frame
        half_size = SOURCE_SIZE // 2
        source_image = capture_screen_region(
            self.cursor_x - half_size,
            self.cursor_y - half_size,
            SOURCE_SIZE,
            SOURCE_SIZE
        )

        if source_image:
            # Get center pixel color (middle of 21×21 grid)
            center = SOURCE_SIZE // 2
            try:
                r, g, b = source_image.getpixel((center, center))
                self.current_r = r
                self.current_g = g
                self.current_b = b
                self.current_hex = rgb_to_hex(r, g, b)

                # Update magnifier
                self.magnifier.update_source(source_image)
                self.magnifier.set_color(self.current_hex, r, g, b)
                self.magnifier.position_near_cursor(self.cursor_x, self.cursor_y)

            except Exception as e:
                print(f"Error getting pixel color: {e}")

    def _check_shortcut_release(self):
        """Monitor keyboard state and copy when Super+Shift+C is released."""
        if not self.x_display:
            return

        try:
            # Query current keyboard state from X11
            keyboard_state = self.x_display.query_keymap()

            # Convert byte array to set of pressed keycodes
            pressed_keys = set()
            for byte_idx, byte_val in enumerate(keyboard_state):
                for bit_idx in range(8):
                    if byte_val & (1 << bit_idx):
                        keycode = byte_idx * 8 + bit_idx
                        pressed_keys.add(keycode)

            # Get keycodes for Super, Shift, and C keys
            super_l = self.x_display.keysym_to_keycode(0xffeb)  # Super_L
            super_r = self.x_display.keysym_to_keycode(0xffec)  # Super_R
            shift_l = self.x_display.keysym_to_keycode(0xffe1)  # Shift_L
            shift_r = self.x_display.keysym_to_keycode(0xffe2)  # Shift_R
            c_key = self.x_display.keysym_to_keycode(0x63)      # c

            # Check if shortcut keys are currently pressed
            super_pressed = super_l in pressed_keys or super_r in pressed_keys
            shift_pressed = shift_l in pressed_keys or shift_r in pressed_keys
            c_pressed = c_key in pressed_keys

            # All three keys must be pressed for combo to be active
            shortcut_combo_pressed = super_pressed and shift_pressed and c_pressed

            # Mark when we first detect the shortcut being held
            if shortcut_combo_pressed:
                self.shortcut_keys_held = True

            # When shortcut was held and now ANY key is released, copy and close
            # (shortcut_combo_pressed becomes False when ANY of the three keys is released)
            if self.shortcut_keys_held and not shortcut_combo_pressed:
                self._copy_and_close()

        except Exception as e:
            # If monitoring fails, disable it
            print(f"Error monitoring keyboard: {e}")
            self.monitoring_release = False
            if hasattr(self, 'key_monitor_timer'):
                self.key_monitor_timer.stop()

    def keyReleaseEvent(self, event):
        """
        Handle key release events.

        Args:
            event: Key release event
        """
        # Escape always closes without copying
        if event.key() == Qt.Key.Key_Escape:
            self._close_picker()
        # If not monitoring keyboard state, any key release copies
        elif not self.monitoring_release:
            self._copy_and_close()
        # Otherwise, let the keyboard monitor handle shortcut release

    def mouseReleaseEvent(self, event):
        """
        Handle mouse click to copy color.

        Args:
            event: Mouse release event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._copy_and_close()
        elif event.button() == Qt.MouseButton.RightButton:
            # Right click: close without copying
            self._close_picker()

    def paintEvent(self, event):
        """Paint the overlay (transparent)."""
        painter = QPainter(self)
        # Overlay is fully transparent - magnifier is a separate widget

    def _copy_and_close(self):
        """Copy current color to clipboard and close overlay."""
        # Copy to clipboard
        success = copy_text_to_clipboard(self.current_hex)

        if success:
            # Show notification using notify-send if available
            try:
                import subprocess
                subprocess.Popen(
                    [
                        'notify-send',
                        '-i', 'color-select',
                        '-t', '2000',
                        'Color Copied',
                        f'{self.current_hex}\nRGB({self.current_r}, {self.current_g}, {self.current_b})'
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception:
                pass  # Notification is optional

        self._close_picker()

    def _close_picker(self):
        """Close the picker overlay."""
        # Stop timers
        self.update_timer.stop()
        if hasattr(self, 'key_monitor_timer'):
            self.key_monitor_timer.stop()

        # Close X11 display connection
        if self.x_display:
            try:
                self.x_display.close()
            except Exception:
                pass

        # Close magnifier
        self.magnifier.close()

        # Close overlay
        self.close()

        # Quit application
        QApplication.quit()

    def closeEvent(self, event):
        """Handle window close event."""
        # Ensure magnifier is closed
        self.magnifier.close()
        event.accept()

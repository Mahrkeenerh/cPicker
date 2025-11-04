"""Main color picker overlay window."""

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter

from .utils.capture import capture_screen_region
from .utils.magnifier import MagnifierWidget
from .utils.clipboard import copy_text_to_clipboard
from .utils.color import rgb_to_hex
from .utils.theme import SOURCE_SIZE


class PickerOverlay(QWidget):
    """
    Transparent fullscreen overlay for color picking.

    Displays a magnifier following the cursor and captures color on key release.
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

        # Create magnifier widget
        self.magnifier = MagnifierWidget()
        self.magnifier.show()

        # Update timer to limit capture frequency (30ms = ~33 FPS)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_color)
        self.update_timer.start(30)

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

    def keyReleaseEvent(self, event):
        """
        Handle key release events.

        Args:
            event: Key release event
        """
        # Copy color on any key release (including Super+Shift+C)
        if event.key() == Qt.Key.Key_Escape:
            # Escape: close without copying
            self._close_picker()
        else:
            # Any other key: copy and close
            self._copy_and_close()

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
        # Stop timer
        self.update_timer.stop()

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

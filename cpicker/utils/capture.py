"""Screen capture utilities using X11."""

from typing import Optional
from Xlib import X, display
from PIL import Image


class ScreenCapture:
    """Handle X11 screen capture operations."""

    def __init__(self):
        """Initialize X11 display connection."""
        try:
            self.display = display.Display()
            self.root = self.display.screen().root
            self.screen_width = self.root.get_geometry().width
            self.screen_height = self.root.get_geometry().height
        except Exception as e:
            raise RuntimeError(f"Failed to connect to X11 display: {e}")

    def capture_region(self, x: int, y: int, width: int, height: int) -> Optional[Image.Image]:
        """
        Capture a rectangular region of the screen.

        Args:
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            width: Width of region to capture
            height: Height of region to capture

        Returns:
            PIL Image of the captured region, or None if capture failed
        """
        try:
            # Clamp coordinates to screen boundaries
            x = max(0, min(x, self.screen_width - width))
            y = max(0, min(y, self.screen_height - height))
            width = max(1, min(width, self.screen_width - x))
            height = max(1, min(height, self.screen_height - y))

            # Get raw image data from X11
            raw = self.root.get_image(x, y, width, height, X.ZPixmap, 0xffffffff)

            # Convert to PIL Image
            # X11 get_image always returns 4 bytes per pixel (BGRX) regardless of depth
            # Using "BGR" for depth==24 causes stride mismatch and RGB decomposition
            if raw.depth == 24:
                image = Image.frombytes("RGB", (width, height), raw.data, "raw", "BGRX")
            else:  # depth == 32
                image = Image.frombytes("RGB", (width, height), raw.data, "raw", "BGRX")

            return image

        except Exception as e:
            print(f"Failed to capture screen region: {e}")
            return None

    def close(self):
        """Close X11 display connection."""
        if hasattr(self, 'display'):
            self.display.close()


# Global instance for reuse
_screen_capture = None


def get_screen_capture() -> ScreenCapture:
    """Get or create the global ScreenCapture instance."""
    global _screen_capture
    if _screen_capture is None:
        _screen_capture = ScreenCapture()
    return _screen_capture


def capture_screen_region(x: int, y: int, width: int, height: int) -> Optional[Image.Image]:
    """
    Convenience function to capture a screen region.

    Args:
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Width of region to capture
        height: Height of region to capture

    Returns:
        PIL Image of the captured region, or None if capture failed
    """
    return get_screen_capture().capture_region(x, y, width, height)

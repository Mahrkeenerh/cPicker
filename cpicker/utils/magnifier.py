"""Magnifier widget for cPicker color display."""

from typing import Optional
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QImage, QPixmap, QPen, QFont, QColor
from PIL import Image

from .theme import (
    MAGNIFIER_SIZE, MAGNIFIER_OFFSET, ZOOM_FACTOR, SOURCE_SIZE,
    THEME_BLUE, DARK_BG, WHITE_TEXT, SUBTLE_GRID,
    HEX_FONT_SIZE, RGB_FONT_SIZE, FONT_FAMILY
)


class MagnifierWidget(QWidget):
    """
    Widget that displays a magnified view of screen area with color information.

    Shows:
    - 21×21 pixel area magnified 10x (210×210 display)
    - Grid overlay for pixel visualization
    - Center pixel highlight
    - Hex color code (large text)
    - RGB values (smaller text)
    - Color swatch
    """

    def __init__(self, parent=None):
        """Initialize magnifier widget."""
        super().__init__(parent)

        # Window configuration
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(MAGNIFIER_SIZE, MAGNIFIER_SIZE + 80)  # Extra space for text

        # State
        self.source_pixmap: Optional[QPixmap] = None
        self.current_hex: str = "#000000"
        self.current_r: int = 0
        self.current_g: int = 0
        self.current_b: int = 0
        self.cursor_x: int = 0
        self.cursor_y: int = 0

        # Screen geometry
        self.screen_geometry = QApplication.primaryScreen().geometry()

    def update_source(self, source_image: Image.Image):
        """
        Update the source image to magnify.

        Args:
            source_image: PIL Image of 21×21 pixels to magnify
        """
        if source_image:
            # Convert PIL RGB to QImage
            data = source_image.tobytes("raw", "RGB")
            qimage = QImage(
                data,
                source_image.width,
                source_image.height,
                source_image.width * 3,
                QImage.Format.Format_RGB888
            )

            # Convert to QPixmap (store source, not scaled version)
            self.source_pixmap = QPixmap.fromImage(qimage)

        self.update()

    def set_color(self, hex_code: str, r: int, g: int, b: int):
        """
        Set the current color information.

        Args:
            hex_code: Hex color code (e.g., "#3A7FBD")
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
        """
        self.current_hex = hex_code
        self.current_r = r
        self.current_g = g
        self.current_b = b
        self.update()

    def position_near_cursor(self, cursor_x: int, cursor_y: int):
        """
        Position magnifier near cursor with adaptive placement.

        Args:
            cursor_x: Cursor X coordinate
            cursor_y: Cursor Y coordinate
        """
        # Default: bottom-left of cursor
        mag_x = cursor_x - MAGNIFIER_SIZE - MAGNIFIER_OFFSET
        mag_y = cursor_y + MAGNIFIER_OFFSET

        # Adaptive positioning - flip to opposite sides if off-screen
        if mag_x < 0:
            mag_x = cursor_x + MAGNIFIER_OFFSET  # Right side of cursor

        if mag_y + self.height() > self.screen_geometry.height():
            mag_y = cursor_y - self.height() - MAGNIFIER_OFFSET  # Above cursor

        # Final boundary clamping
        mag_x = max(0, min(mag_x, self.screen_geometry.width() - self.width()))
        mag_y = max(0, min(mag_y, self.screen_geometry.height() - self.height()))

        self.move(mag_x, mag_y)

    def paintEvent(self, event):
        """Paint the magnifier display."""
        painter = QPainter(self)
        # Disable antialiasing and smooth transform for sharp pixel edges
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)

        # Draw magnified view
        if self.source_pixmap:
            # Background
            painter.fillRect(0, 0, MAGNIFIER_SIZE, MAGNIFIER_SIZE, Qt.GlobalColor.black)

            # Define source and target rectangles
            source_rect = QRect(0, 0, SOURCE_SIZE, SOURCE_SIZE)
            target_rect = QRect(0, 0, MAGNIFIER_SIZE, MAGNIFIER_SIZE)

            # Draw the magnified image - Qt handles scaling efficiently
            # With SmoothPixmapTransform disabled, uses nearest-neighbor (no interpolation)
            painter.drawPixmap(target_rect, self.source_pixmap, source_rect)

            # Draw grid
            self._draw_grid(painter)

            # Draw center pixel highlight
            self._draw_center_highlight(painter)

        # Draw color information panel
        self._draw_color_info(painter)

    def _draw_grid(self, painter: QPainter):
        """Draw grid overlay on magnified view."""
        pen = QPen(SUBTLE_GRID)
        pen.setWidth(1)
        painter.setPen(pen)

        # Calculate pixel size after magnification
        pixel_size = MAGNIFIER_SIZE / SOURCE_SIZE

        # Vertical lines
        for i in range(SOURCE_SIZE + 1):
            x = int(i * pixel_size)
            painter.drawLine(x, 0, x, MAGNIFIER_SIZE)

        # Horizontal lines
        for i in range(SOURCE_SIZE + 1):
            y = int(i * pixel_size)
            painter.drawLine(0, y, MAGNIFIER_SIZE, y)

    def _draw_center_highlight(self, painter: QPainter):
        """Draw highlight around center pixel."""
        pen = QPen(THEME_BLUE)
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)

        # Center pixel is at index 10 (middle of 21×21 grid)
        pixel_size = MAGNIFIER_SIZE / SOURCE_SIZE
        center_index = SOURCE_SIZE // 2

        x = int(center_index * pixel_size)
        y = int(center_index * pixel_size)
        size = int(pixel_size)

        painter.drawRect(x, y, size, size)

    def _draw_color_info(self, painter: QPainter):
        """Draw color information panel below magnifier."""
        # Background panel
        info_y = MAGNIFIER_SIZE
        info_height = 80

        painter.fillRect(0, info_y, MAGNIFIER_SIZE, info_height, DARK_BG)

        # Color swatch (small square showing actual color)
        swatch_size = 30
        swatch_x = 10
        swatch_y = info_y + 10

        swatch_color = QColor(self.current_r, self.current_g, self.current_b)
        painter.fillRect(swatch_x, swatch_y, swatch_size, swatch_size, swatch_color)

        # Draw border around swatch
        painter.setPen(QPen(WHITE_TEXT, 1))
        painter.drawRect(swatch_x, swatch_y, swatch_size, swatch_size)

        # Hex code (large text)
        hex_font = QFont(FONT_FAMILY, HEX_FONT_SIZE, QFont.Weight.Bold)
        painter.setFont(hex_font)
        painter.setPen(WHITE_TEXT)

        hex_x = swatch_x + swatch_size + 15
        hex_y = info_y + 35
        painter.drawText(hex_x, hex_y, self.current_hex)

        # RGB values (smaller text)
        rgb_font = QFont(FONT_FAMILY, RGB_FONT_SIZE)
        painter.setFont(rgb_font)

        rgb_text = f"R:{self.current_r:3d}  G:{self.current_g:3d}  B:{self.current_b:3d}"
        rgb_y = info_y + 60
        painter.drawText(10, rgb_y, rgb_text)

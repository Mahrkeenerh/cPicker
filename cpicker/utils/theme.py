"""Theme colors and styling constants for cPicker."""

from PyQt6.QtGui import QColor


# UI Colors (consistent with CaptiX theme)
THEME_BLUE = QColor(0, 150, 255, 200)           # Highlights and center pixel border
DARK_BG = QColor(40, 40, 40, 240)               # Dark background for info display
WHITE_TEXT = QColor(255, 255, 255, 255)         # Text color
SUBTLE_GRID = QColor(255, 255, 255, 60)         # Grid lines in magnifier


# Magnifier constants
MAGNIFIER_SIZE = 210        # Display size in pixels (21×21 source at 10x zoom)
MAGNIFIER_OFFSET = 30       # Distance from cursor
ZOOM_FACTOR = 10            # Each source pixel = 10×10 display pixels
SOURCE_SIZE = 21            # Number of source pixels to capture (21×21)


# Text styling
HEX_FONT_SIZE = 24          # Large hex code display
RGB_FONT_SIZE = 12          # Smaller RGB values display
FONT_FAMILY = "monospace"   # Monospace font for color codes

"""Color conversion utilities for cPicker."""

from typing import Tuple


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values to hex color code.

    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)

    Returns:
        Hex color code string (e.g., "#3A7FBD")
    """
    return f"#{r:02x}{g:02x}{b:02x}".upper()


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """
    Convert hex color code to RGB values.

    Args:
        hex_code: Hex color code string (with or without '#')

    Returns:
        Tuple of (r, g, b) values (0-255)
    """
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

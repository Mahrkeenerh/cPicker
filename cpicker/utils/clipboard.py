"""Clipboard operations for cPicker."""

import subprocess
import shutil


def copy_text_to_clipboard(text: str) -> bool:
    """
    Copy text to clipboard using xclip.

    Args:
        text: Text string to copy to clipboard

    Returns:
        True if successful, False otherwise
    """
    # Check if xclip is available
    if not shutil.which('xclip'):
        print("Error: xclip not found. Please install xclip: sudo apt install xclip")
        return False

    try:
        # Use xclip to copy text to clipboard
        process = subprocess.Popen(
            ['xclip', '-selection', 'clipboard'],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        process.communicate(input=text.encode('utf-8'), timeout=1)
        return process.returncode == 0

    except subprocess.TimeoutExpired:
        process.kill()
        print("Error: xclip timed out")
        return False
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False

"""Command-line interface for cPicker."""

import sys
import argparse
from PyQt6.QtWidgets import QApplication

from . import __version__
from .picker_overlay import PickerOverlay
from .utils.instance_lock import InstanceLock


def main():
    """Main entry point for cPicker."""
    parser = argparse.ArgumentParser(
        description='cPicker - Lightweight Linux color picker tool',
        prog='cpicker'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'cPicker {__version__}'
    )

    parser.add_argument(
        '--ui',
        action='store_true',
        help='Launch color picker overlay (default action)'
    )

    args = parser.parse_args()

    # Default action is to launch UI
    launch_picker()


def launch_picker():
    """Launch the color picker overlay."""
    # Use instance lock to prevent multiple instances
    with InstanceLock():
        try:
            # Create QApplication
            app = QApplication(sys.argv)
            app.setApplicationName("cPicker")
            app.setOrganizationName("cPicker")

            # Create and show picker overlay
            picker = PickerOverlay()

            # Run application
            sys.exit(app.exec())

        except Exception as e:
            print(f"Error launching cPicker: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

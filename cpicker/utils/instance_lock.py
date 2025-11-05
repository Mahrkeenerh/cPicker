"""Instance locking to prevent multiple cPicker instances."""

import os
import sys
import time
import fcntl
from pathlib import Path


class InstanceLock:
    """
    Ensure only one instance of cPicker runs at a time.

    Uses file locking to prevent multiple simultaneous instances.
    """

    def __init__(self):
        """Initialize instance lock."""
        # Use a lock file in /tmp
        self.lock_file_path = Path("/tmp/cpicker.lock")
        self.timestamp_file_path = Path("/tmp/cpicker.timestamp")
        self.lock_file = None
        self.lock_acquired = False
        # Debounce period: prevent launches within 100ms of last instance
        self.debounce_ms = 100

    def acquire(self) -> bool:
        """
        Acquire the instance lock.

        Returns:
            True if lock acquired successfully, False if another instance is running
        """
        # Check if a recent instance just exited (debounce check)
        if self.timestamp_file_path.exists():
            try:
                with open(self.timestamp_file_path, 'r') as f:
                    last_timestamp = float(f.read().strip())
                    current_time = time.time()
                    time_since_last = (current_time - last_timestamp) * 1000  # ms

                    if time_since_last < self.debounce_ms:
                        # Too soon after last instance - prevent rapid re-launch
                        return False
            except (ValueError, IOError):
                # Invalid or missing timestamp, ignore
                pass

        try:
            # Open/create the lock file
            self.lock_file = open(self.lock_file_path, 'w')

            # Try to acquire exclusive lock (non-blocking)
            fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

            # Write our PID to the lock file
            self.lock_file.write(f"{os.getpid()}\n")
            self.lock_file.flush()

            self.lock_acquired = True
            return True

        except (IOError, OSError):
            # Lock is already held by another instance
            if self.lock_file:
                try:
                    self.lock_file.close()
                except Exception:
                    pass
            return False

    def release(self):
        """Release the instance lock."""
        if self.lock_acquired and self.lock_file:
            try:
                # Write timestamp to prevent immediate re-launch
                with open(self.timestamp_file_path, 'w') as f:
                    f.write(f"{time.time()}\n")

                fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
                self.lock_file.close()
                # Clean up lock file
                if self.lock_file_path.exists():
                    self.lock_file_path.unlink()
            except Exception:
                pass
            finally:
                self.lock_acquired = False

    def __enter__(self):
        """Context manager entry."""
        if not self.acquire():
            print("cPicker is already running.", file=sys.stderr)
            sys.exit(0)  # Exit silently
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()

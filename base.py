"""
SegLCD Base Module for MicroPython
Abstract base class for segment LCD displays
"""

from micropython import const


# Drive mode constants
MODE_DRIVE_STATIC = const(1)  # Static drive (1/1 duty)
MODE_DRIVE_12 = const(2)       # 1/2 multiplexing
MODE_DRIVE_13 = const(3)       # 1/3 multiplexing
MODE_DRIVE_14 = const(0)       # 1/4 multiplexing

# Bias mode constants (not used in static drive)
MODE_BIAS_13 = const(0)        # 1/3 bias
MODE_BIAS_12 = const(1)        # 1/2 bias


class SegLCD:
    """
    Abstract base class for LCD segment display drivers.

    This class defines the generic interface required by all LCD segment drivers,
    including display control, character output, and data writing methods.
    """

    def __init__(self):
        """Initialize cursor position."""
        self._cursor_row = 0
        self._cursor_col = 0

    # ===================================================================
    # LCD API 1.0 Mandatory Methods
    # ===================================================================

    def init(self):
        """
        Initialize the display driver, clear display and set position to 0,0.
        """
        pass

    def clear(self):
        """
        Clear all visible segments on the display.
        """
        self.home()

    def home(self):
        """
        Set cursor to 0, 0 without clearing display.
        """
        self.set_cursor(0, 0)

    def set_cursor(self, row, col):
        """
        Set cursor to exact digit position.

        Because LCD API is mainly used for character displays, in segment displays
        this works differently:
        - Most segment LCDs have only one row (row 0)
        - Column represents the digit position

        For multi-row displays (e.g., T1T2 LCD):
        - Row 0: clock part
        - Row 1: T1 part
        - Row 2: T2 part

        Args:
            row: Row position (0 to MAX_ROWS-1)
            col: Column position (0 to MAX_DIGITS-1)
        """
        self._cursor_row = row
        self._cursor_col = col

    def write(self, data):
        """
        Write character or string to display at cursor position.

        Args:
            data: Character (str/int) or string to write

        Returns:
            Number of characters written
        """
        if isinstance(data, str):
            count = 0
            for ch in data:
                if self._write_char(ord(ch) if len(ch) == 1 else ch):
                    count += 1
            return count
        elif isinstance(data, int):
            return 1 if self._write_char(data) else 0
        else:
            return 0

    def _write_char(self, ch):
        """
        Write single character (to be implemented by subclass).

        Args:
            ch: Character code (int)

        Returns:
            True if successful
        """
        pass

    def command(self, cmd):
        """
        Send RAW command to controller.

        Args:
            cmd: Raw command byte
        """
        pass

    # ===================================================================
    # LCD API 1.0 Optional Methods
    # ===================================================================

    def on(self):
        """Turn the display on."""
        pass

    def off(self):
        """Turn the display off."""
        pass

    # ===================================================================
    # SegLCDLib Specific Methods
    # ===================================================================

    def _write_ram(self, data, address=0):
        """
        Low-level method to write data to display RAM.

        Args:
            data: Single byte (int) or bytes object to write
            address: RAM address to start writing
        """
        pass

    # Convenience methods for print-like usage
    def print(self, *args, sep=' ', end=''):
        """
        Print-like method for writing to display.

        Args:
            *args: Values to print
            sep: Separator between values (default: ' ')
            end: End character (default: '')
        """
        text = sep.join(str(arg) for arg in args) + end
        return self.write(text)

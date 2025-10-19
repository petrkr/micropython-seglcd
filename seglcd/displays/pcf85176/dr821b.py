"""
PCF85176 4DR821B Display Driver for MicroPython
Tesla 4DR821B 4-digit 7-segment LCD with clock colon

Display layout: XX:XX (4 digits + colon)
- Static drive mode (1/1 duty)
- 4 digits (0-3)
- Decimal points on digits 0, 1, 2
- Clock colon between digits 1 and 2
"""

from micropython import const
from seglcd.drivers.pcf85176 import PCF85176Driver
from seglcd.charset import get_char_value
from seglcd.base import MODE_DRIVE_STATIC, MODE_BIAS_13

# Address mapping
_ADDR_SYMBOLS = const(0x00)
_ADDR_SEGS = const(0x01)

# Constants
_DIGITS = const(4)
_DECIMAL_POINT_BIT = const(0x01)
_MIDDLE_COLON_BIT  = const(0x01)
_ARROW_BIT         = const(0x10)
_LEFT_COLON_BIT    = const(0x20)
_MINUS_BIT         = const(0x40)
_TILDA_BIT         = const(0x80)
_DECIMAL_MIN_COL   = const(0)
_DECIMAL_MAX_COL   = const(2)


class PCF85176_4DR821B(PCF85176Driver):
    """
    Tesla 4DR821B 4-digit clock display.

    Features:
    - 4 digits (7-segment)
    - Clock colon (:)
    - Decimal points on first 3 digits
    - Static drive mode

    Example:
        from machine import I2C, Pin
        from displays.pcf85176.dr821b import PCF85176_4DR821B

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        lcd = PCF85176_4DR821B(i2c)
        lcd.init()
        lcd.print("12:54")
    """

    def __init__(self, i2c, address=0x38, subaddress=0x00):
        """
        Initialize 4DR821B display.

        Args:
            i2c: machine.I2C instance
            address: I2C address (default 0x38)
            subaddress: Subaddress (default 0x00)
        """
        super().__init__(i2c, address, subaddress)
        self._buffer = bytearray(5)  # 1 symbol byte + 4 digit bytes
        self._previous_dot = False
        self._colon_displayed = False
        self._col0_overlay_active = False


    def _set_symbol(self, symbol, state):
        """
        Set symbol

        Args:
            symbol: Symbol bit
            state: True to show symbol, False to hide
        """
        if state:
            self._buffer[_ADDR_SYMBOLS] |= symbol
        else:
            self._buffer[_ADDR_SYMBOLS] &= ~symbol

        self._write_ram(self._buffer[_ADDR_SYMBOLS], _ADDR_SYMBOLS)

    def init(self):
        """Initialize display with static drive mode."""
        super().init()
        self._set_mode(1, MODE_DRIVE_STATIC, MODE_BIAS_13)  # 1 = enabled

    def clear(self):
        """Clear all segments and buffer."""
        # Clear buffer
        for i in range(len(self._buffer)):
            self._buffer[i] = 0x00

        # Clear display RAM
        super().clear()

    def set_clock_colon(self, row, col, state):
        """
        Set clock colon (between digits 1 and 2).

        Args:
            row: Row (not used, for API compatibility)
            col: Column (not used, for API compatibility)
            state: True to show colon, False to hide
        """

        if col == 0:
            if state: # If we want colon, we can not have minus here
                self._set_symbol(_MINUS_BIT, False)

            self._set_symbol(_LEFT_COLON_BIT, state)

        if col == 1:
            self._set_symbol(_MIDDLE_COLON_BIT, state)


    def set_decimal(self, row, col, state):
        """
        Set decimal point on specific digit.

        Args:
            row: Row number (must be 0)
            col: Column/digit number (0-2, digits 0, 1, 2 have decimal points)
            state: True to show decimal, False to hide
        """
        if row != 0:
            return  # Invalid row

        if col < _DECIMAL_MIN_COL or col > _DECIMAL_MAX_COL:
            return  # Invalid column

        if state:
            self._buffer[_ADDR_SEGS + col] |= _DECIMAL_POINT_BIT
        else:
            self._buffer[_ADDR_SEGS + col] &= ~_DECIMAL_POINT_BIT

        # Write to display RAM
        # Static drive: address = byte_position * 8
        self._write_ram(self._buffer[_ADDR_SEGS + col], (_ADDR_SEGS + col) * 8)

    def set_tilda(self, state):
        """
        Set tilda symbol at column 0.

        Args:
            state: True to show tilda, False to hide
        """
        self._set_symbol(_TILDA_BIT, state)

    def set_arrow(self, state):
        """
        Set arrow symbol at column 0.

        Args:
            state: True to show arrow, False to hide
        """
        self._set_symbol(_ARROW_BIT, state)

    def set_cursor(self, row, col):
        if row == 0 and col <= 2:
            self._colon_displayed = False

        if row == 0 and col == 0:
            self._col0_overlay_active = False

        super().set_cursor(row, col)

    def _write_char(self, ch):
        """
        Write single character at cursor position.

        Handles special characters:
        - '.' sets decimal point on previous digit
        - ':' sets clock colon at middle position
        - '-', '+', ':' at col=0 set overlay symbols

        Returns:
            True if successful
        """
        if self._cursor_col < 0 or self._cursor_col > _DIGITS:
            return False  # Invalid position

        # Handle decimal point
        if ch == ord('.'):
            self.set_decimal(self._cursor_row, self._cursor_col - 1, True)
            return True

        # Handle clock/middle colon
        if ch != ord(':') and self._cursor_col == 2 and not self._colon_displayed:
            self.set_clock_colon(self._cursor_row, self._cursor_col - 1, False)
            self._colon_displayed = False

        if ch == ord(':') and self._cursor_col == 2 and not self._colon_displayed:
            self.set_clock_colon(self._cursor_row, self._cursor_col - 1, True)
            self._colon_displayed = True
            return True

        # Symbols at column zero
        if self._cursor_col == 0:
            # Sign characters for overlay
            if ch in (ord('-'), ord('+'), ord(':')):
                # clean up
                self._set_symbol(_MINUS_BIT, False)
                self._set_symbol(_LEFT_COLON_BIT, False)

                if ch == ord('-'):
                    self._set_symbol(_MINUS_BIT, True)
                elif ch == ord(':'):
                    self._set_symbol(_LEFT_COLON_BIT, True)
                elif ch == ord('+'):
                    self._set_symbol(_MINUS_BIT, True)
                    self._set_symbol(_LEFT_COLON_BIT, True)
                else:
                    return False  # Should not happen

                # Col 0 overlay
                self._col0_overlay_active = True
                return True  # Do not increment cursor

            # first char after overlay, disable overlay
            if self._col0_overlay_active:
                self._col0_overlay_active = False
            else:
                # no overlay active, ensure symbols are off
                self._set_symbol(_MINUS_BIT, False)
                self._set_symbol(_LEFT_COLON_BIT, False)

        # Get segment data for character
        segment_data = get_char_value(ch)

        # Update buffer
        self._buffer[_ADDR_SEGS + self._cursor_col] = segment_data

        # Write to display RAM
        # Static drive: address = byte_position * 8
        self._write_ram(
            self._buffer[_ADDR_SEGS + self._cursor_col],
            (_ADDR_SEGS + self._cursor_col) * 8
        )

        # Advance cursor
        self._cursor_col += 1
        return True

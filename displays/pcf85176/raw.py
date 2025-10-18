"""
PCF85176 RAW Display - Direct RAM access for testing
"""

from drivers.pcf85176 import PCF85176Driver
from base import MODE_DRIVE_14, MODE_BIAS_13


class PCF85176_Raw(PCF85176Driver):
    """
    RAW LCD implementation for PCF85176.

    This class provides direct access to display RAM for testing and
    prototyping new LCD displays before creating dedicated classes.

    Example:
        from machine import I2C, Pin
        from displays.pcf85176.raw import PCF85176_Raw

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        lcd = PCF85176_Raw(i2c)
        lcd.init(MODE_DRIVE_14, MODE_BIAS_13)
        lcd.write_ram(0xFF, 0)  # Write 0xFF to address 0
    """

    def __init__(self, i2c, address=0x38, subaddress=0x00):
        """
        Initialize RAW display.

        Args:
            i2c: machine.I2C instance
            address: I2C address (default 0x38)
            subaddress: Subaddress (default 0x00)
        """
        super().__init__(i2c, address, subaddress)

    def init(self, drive=MODE_DRIVE_14, bias=MODE_BIAS_13):
        """
        Initialize display with specific drive and bias mode.

        Args:
            drive: Drive mode (MODE_DRIVE_*)
            bias: Bias mode (MODE_BIAS_*)
        """
        super().init()
        self._set_mode(1, drive, bias)  # 1 = enabled
        self.clear()

    def write_ram(self, data, address=0):
        """
        Public interface to write RAW data to display RAM.

        Args:
            data: Single byte (int) or bytes/bytearray to write
            address: Starting RAM address (0-39 for PCF85176)

        Example:
            lcd.write_ram(0b10000000, 0)     # Single byte at address 0
            lcd.write_ram([0xFF, 0xFF], 0)   # Multiple bytes starting at 0
        """
        self._write_ram(data, address)

    def _write_char(self, ch):
        """
        RAW display doesn't implement character writing.

        Use write_ram() instead for direct RAM access.
        """
        return False

"""
PCF85176 I2C LCD Segment Driver for MicroPython
"""

from micropython import const
from seglcd.base import SegLCD, MODE_DRIVE_14, MODE_BIAS_13


# PCF85176 Commands
_CMD_LOAD_POINTER = const(0x00)
_CMD_MODE = const(0x40)
_CMD_DEVICE_SELECT = const(0x60)
_CMD_BLINK = const(0x70)
_CMD_BANK_SELECT = const(0x78)
_CMD_LAST_COMMAND = const(0x80)

# Hardware constants
_DEFAULT_I2C_ADDRESS = const(0x38)  # 56 decimal
_DEFAULT_SUBADDRESS = const(0x00)
_MAX_HW_ADDRESS = const(39)

# Display status
_MODE_STATUS_BLANK = const(0)
_MODE_STATUS_ENABLED = const(1)

# Blink frequency
BLINK_FREQUENCY_OFF = const(0)
BLINK_FREQUENCY_2HZ = const(1)   # ~2Hz
BLINK_FREQUENCY_1HZ = const(2)   # ~1Hz
BLINK_FREQUENCY_05HZ = const(3)  # ~0.5Hz

# Blink mode
BLINK_MODE_NORMAL = const(0)
BLINK_MODE_ALTRAM = const(1)


class PCF85176Driver(SegLCD):
    """
    PCF85176 I2C LCD segment display driver.

    This driver implements I2C communication with PCF85176 controller
    and provides methods for display control.
    """

    def __init__(self, i2c, address=_DEFAULT_I2C_ADDRESS, subaddress=_DEFAULT_SUBADDRESS):
        """
        Initialize PCF85176 driver.

        Args:
            i2c: machine.I2C instance
            address: I2C address (default 0x38, selected by SA0 pins)
            subaddress: Subaddress (default 0x00, selected by A0-A2 pins)
        """
        super().__init__()
        self._i2c = i2c
        self._address = address
        self._subaddress = subaddress
        self._drive = MODE_DRIVE_14
        self._bias = MODE_BIAS_13
        self._max_address = _MAX_HW_ADDRESS

    def init(self):
        """Initialize the display driver."""
        self._device_select()
        self.clear()

    def command(self, cmd):
        """
        Send RAW command to controller.

        Args:
            cmd: Command byte
        """
        self._i2c.writeto(self._address, bytes([cmd | _CMD_LAST_COMMAND]))

    def clear(self):
        """Clear all segments on the display."""
        # Calculate buffer size based on drive mode
        if self._drive == MODE_DRIVE_14:
            # 1/4 drive: each address controls 4 segments (nibbles)
            # Need (MAX_ADDRESS / 2) + 1 bytes
            size = (_MAX_HW_ADDRESS // 2) + 1
        else:
            # Static drive: each address controls 8 segments
            # Need (MAX_ADDRESS / 8) + 1 bytes
            size = (_MAX_HW_ADDRESS // 8) + 1

        buffer = bytearray(size)
        self._write_ram(buffer, 0)
        super().clear()

    def on(self):
        """Turn the display on."""
        self._set_mode(_MODE_STATUS_ENABLED, self._drive, self._bias)

    def off(self):
        """Turn the display off (blank)."""
        self._set_mode(_MODE_STATUS_BLANK, self._drive, self._bias)

    def bank_select(self, input_bank, output_bank):
        """
        Select bank for input and output.

        The bank-select command controls where data is written to RAM
        and where it is displayed from.

        Args:
            input_bank: Input bank selection (0 or 1) - storage of arriving data
            output_bank: Output bank selection (0 or 1) - retrieval of display data
        """
        data = _CMD_BANK_SELECT | (input_bank << 1) | output_bank | _CMD_LAST_COMMAND
        self._i2c.writeto(self._address, bytes([data]))

    def blink(self, frequency=BLINK_FREQUENCY_OFF, mode=BLINK_MODE_NORMAL):
        """
        Set blink frequency and mode.

        Args:
            frequency: Blink frequency (BLINK_FREQUENCY_*)
            mode: Blink mode (BLINK_MODE_*)
        """
        data = _CMD_BLINK | (mode << 2) | frequency | _CMD_LAST_COMMAND
        self._i2c.writeto(self._address, bytes([data]))

    def _write_char(self, ch):
        """
        Write single character (implemented by display class).

        Args:
            ch: Character code

        Returns:
            True if successful
        """
        # Base driver doesn't implement character writing
        # This is done by specific display implementations
        return False

    def _write_ram(self, data, address=0):
        """
        Low-level method to write data to display RAM.

        Args:
            data: Single byte (int) or bytes/bytearray to write
            address: Starting RAM address
        """
        if isinstance(data, int):
            data = bytes([data])
        elif not isinstance(data, (bytes, bytearray)):
            data = bytes(data)

        # Write: address followed by data bytes
        self._i2c.writeto(self._address, bytes([address]) + data)

        # If we write to last address, re-select device
        # (PCF supports chaining, but we don't use it)
        if address + (len(data) * 8) >= _MAX_HW_ADDRESS - 8:
            self._device_select()

    def _device_select(self):
        """
        Select the device for communication.

        Used to set the device by subaddress. If address during writing
        overflows one device's address, next device is selected.
        This re-selects the current device.
        """
        data = _CMD_DEVICE_SELECT | self._subaddress | _CMD_LAST_COMMAND
        self._i2c.writeto(self._address, bytes([data]))

    def _set_mode(self, status, drive=MODE_DRIVE_14, bias=MODE_BIAS_13):
        """
        Set the mode of the display.

        Args:
            status: Display status (enabled or blanked)
            drive: Drive mode (MODE_DRIVE_*)
            bias: Bias mode (MODE_BIAS_*)
        """
        self._drive = drive
        self._bias = bias

        data = _CMD_MODE | (status << 3) | (bias << 2) | drive | _CMD_LAST_COMMAND
        self._i2c.writeto(self._address, bytes([data]))

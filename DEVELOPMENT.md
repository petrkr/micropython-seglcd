# Development Guide - MicroPython SegLCD

Guide for further development and library extension.

## Current Implementation Status

### ✅ Complete (Phase 1 - PCF85176 RAW)

- [x] `base.py` - Abstract LCD API class (~170 lines)
- [x] `charset.py` - 7-seg and 16-seg conversions (~270 lines)
- [x] `drivers/pcf85176.py` - I2C driver (~170 lines)
- [x] `displays/pcf85176/raw.py` - RAW display (~60 lines)
- [x] Examples and documentation
- [x] Syntax tests

**Total:** ~673 lines of code, ~8-10KB flash after compilation

## Next Steps

### Phase 2: PCF85176 Specific Displays

Template for new display (e.g. TempHum):

```python
# displays/pcf85176/temphum.py

from drivers.pcf85176 import PCF85176Driver
from charset import get_char_value
from base import MODE_DRIVE_14, MODE_BIAS_13

class PCF85176_TempHum(PCF85176Driver):
    """Temperature/Humidity 5+4 digit display"""

    def __init__(self, i2c, address=0x38):
        super().__init__(i2c, address)
        self._digits_row0 = 5  # Temperature digits
        self._digits_row1 = 4  # Humidity digits

    def init(self):
        super().init()
        self._set_mode(1, MODE_DRIVE_14, MODE_BIAS_13)
        self.clear()

    def _write_char(self, ch):
        """Write character at current cursor position"""
        segments = get_char_value(ch)

        # Mapping for specific LCD
        if self._cursor_row == 0:
            # Temperature row
            address = self._map_digit_to_address_row0(self._cursor_col)
        else:
            # Humidity row
            address = self._map_digit_to_address_row1(self._cursor_col)

        self._write_ram(segments, address)
        self._cursor_col += 1
        return True

    def _map_digit_to_address_row0(self, digit):
        # TODO: Determine from hardware testing
        mapping = [0, 2, 4, 6, 8]  # Example
        return mapping[digit] if digit < len(mapping) else 0

    def _map_digit_to_address_row1(self, digit):
        # TODO: Determine from hardware testing
        mapping = [10, 12, 14, 16]  # Example
        return mapping[digit] if digit < len(mapping) else 0

    def set_signal_level(self, level):
        """Set signal indicator (0-4)"""
        # TODO: Implement based on segment mapping
        pass

    def set_battery_level(self, level):
        """Set battery indicator (0-4)"""
        # TODO: Implement based on segment mapping
        pass
```

**Process for new display:**

1. Create `displays/pcf85176/mydisplay.py`
2. Use RAW display to determine segment mapping
3. Implement `_write_char()` with concrete mapping
4. Add special methods (battery, signal, etc.)
5. Create example in `examples/`
6. Test on hardware

### Phase 3: HT1621 3-wire Driver

```python
# drivers/ht1621.py

from drivers.wire3 import Wire3Driver  # Common 3-wire base
from base import MODE_DRIVE_14, MODE_BIAS_13

# HT1621 specific commands
CMD_SYS_DIS = const(0b00000000)
CMD_SYS_EN = const(0b00000001)
CMD_LCD_OFF = const(0b00000010)
CMD_LCD_ON = const(0b00000011)
# ... more commands

class HT1621Driver(Wire3Driver):
    """HT1621 3-wire LCD driver"""

    def __init__(self, cs_pin, data_pin, wr_pin):
        super().__init__(cs_pin, data_pin, wr_pin)
        self._max_address = 31  # HT1621 has 32×4 bit RAM

    def init(self):
        super().init()
        self.command(CMD_SYS_EN)
        self._set_mode(MODE_DRIVE_14, MODE_BIAS_13)
        self.command(CMD_LCD_ON)

    def _set_mode(self, drive, bias):
        # TODO: Build command byte based on drive/bias
        cmd = self._build_mode_command(drive, bias)
        self.command(cmd)
```

**Will need to create:**
- `drivers/wire3.py` - Common 3-wire base class with bit-banging
- Pin timing using `machine.Pin` and `time.sleep_us()`

### Phase 4: VK0192 Driver

Similar to HT1621, but:
- Different timing requirements (4μs pulses)
- 48×4-bit addressing (addresses 0-47)
- Irregular segment mapping

## Hardware Testing

### 1. RAW Display Test

```python
# test_raw.py
from machine import I2C, Pin
from displays.pcf85176.raw import PCF85176_Raw

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
lcd = PCF85176_Raw(i2c)
lcd.init()

# Test each address sequentially
for addr in range(40):
    lcd.clear()
    lcd.write_ram(0xFF, addr)
    print(f"Address {addr}: which segments lit?")
    input("Press Enter for next...")
```

### 2. Segment Mapping Discovery

Create a table:

| Address | Segments | Digit | Note |
|---------|----------|-------|------|
| 0       | All A    | 0     | Top segment |
| 1       | ...      | ...   | ...  |

### 3. Character Test

```python
lcd.set_cursor(0, 0)
lcd.print("0123456789")
# Check if all digits display correctly
```

## Code Style

- **snake_case** for functions and variables (MicroPython convention)
- **PascalCase** for classes
- **UPPER_CASE** for constants
- Docstrings in Google style
- Type hints if possible (but not mandatory for MicroPython)

## File Organization

```
displays/
├── pcf85176/
│   ├── __init__.py
│   ├── raw.py           # Always first
│   ├── temphum.py       # Sort alphabetically
│   ├── dig6.py
│   └── ...
├── ht1621/
│   └── ...
```

## Optimization Tips

1. **Use `const()`** for constants → RAM savings
2. **Avoid large lookup tables** in RAM
3. **Prefer `bytearray`** for buffers instead of lists
4. **Frozen modules** - precompile into ESP32 firmware for even more savings

## Testing

### Unit Tests (without HW)

```bash
cd micropython-seglcd
micropython test_syntax.py
```

We use **native MicroPython** (not Python + mocks)!

### Testing Checklist

- [ ] Syntax test (`test_syntax.py` passes)
- [ ] RAW test on HW (all addresses work)
- [ ] Character mapping correct (digits 0-9 readable)
- [ ] Cursor positioning works
- [ ] `clear()` clears entire display
- [ ] `on()`/`off()` works
- [ ] Blinking works (if display supports it)

## Useful Commands

```bash
# Upload to ESP32
ampy -p /dev/ttyUSB0 put micropython-seglcd /seglcd

# Run REPL
screen /dev/ttyUSB0 115200

# Or use Thonny IDE
```

## Next Priorities

1. ✅ PCF85176 RAW (DONE)
2. 🔄 PCF85176 TempHum display (example from Arduino port)
3. 🔄 PCF85176 6-digit display
4. ⏭️ HT1621 3-wire base
5. ⏭️ HT1621 6SegBat display
6. ⏭️ VK0192 driver

## Questions?

Check Arduino implementation:
- `/home/petrkr/git/SegLCDLib/src/`
- Examples: `/home/petrkr/git/SegLCDLib/examples/`

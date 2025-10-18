# SegLCD for MicroPython

Modular library for segment LCD displays and controllers for MicroPython (primarily ESP32).

MicroPython port of Arduino library [SegLCDLib](https://github.com/petrkr/SegLCDLib) with focus on modularity and memory efficiency.

## Features

- **Modular design** - import only what you need
- **LCD API 1.0 compatible** - standardized interface
- **Flash memory savings** - only used modules are loaded (~8-10KB typically)
- **ESP32 optimized** - native `machine.I2C` and `machine.Pin`

## Supported Controllers

| Controller | Communication | Status |
|-----------|-----------|--------|
| PCF85176  | I2C       | ✅ Implemented |
| HT1621    | 3-wire    | 🔜 Planned |
| HT1622    | 3-wire    | 🔜 Planned |
| VK0192    | 3-wire    | 🔜 Planned |

## Project Structure

```
micropython-seglcd/
├── base.py                   # Abstract base class
├── charset.py                # Character to segment conversion
├── drivers/
│   ├── pcf85176.py          # PCF85176 I2C driver (~3KB)
│   ├── ht1621.py            # HT1621 3-wire driver (TODO)
│   └── ...
├── displays/
│   ├── pcf85176/
│   │   ├── raw.py           # RAW - direct RAM access
│   │   ├── temphum.py       # Temp/Humidity display (TODO)
│   │   └── ...
│   └── ...
└── examples/
    └── pcf85176_raw_example.py
```

## Quick Start

### Installation

1. Upload entire `micropython-seglcd` directory to ESP32:
```bash
# Using ampy
ampy -p /dev/ttyUSB0 put micropython-seglcd /seglcd

# Or using Thonny IDE
# Simply copy the folder to ESP32
```

2. Or upload only required files (minimal installation):
```bash
# For PCF85176 RAW you need:
ampy -p /dev/ttyUSB0 put base.py
ampy -p /dev/ttyUSB0 put drivers/pcf85176.py drivers/pcf85176.py
ampy -p /dev/ttyUSB0 put displays/pcf85176/raw.py displays/pcf85176_raw.py
```

### Basic Usage - RAW Display

```python
from machine import I2C, Pin
from displays.pcf85176.raw import PCF85176_Raw
from base import MODE_DRIVE_14, MODE_BIAS_13

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Create LCD instance
lcd = PCF85176_Raw(i2c)

# Initialize (1/4 duty, 1/3 bias)
lcd.init(MODE_DRIVE_14, MODE_BIAS_13)

# Turn on display
lcd.on()

# Write RAW data to address 0
lcd.write_ram(0xFF, 0)

# Write multiple bytes
lcd.write_ram([0xFF, 0xFF, 0x00], 0)

# Clear
lcd.clear()

# Blink
from drivers.pcf85176 import BLINK_FREQUENCY_2HZ
lcd.blink(BLINK_FREQUENCY_2HZ)

# Turn off
lcd.off()
```

## Hardware Setup

### PCF85176 Wiring

```
ESP32        PCF85176
─────────────────────
GPIO21 (SDA) → SDA
GPIO22 (SCL) → SCL
3.3V         → VDD
GND          → VSS
```

**I2C Address:** 0x38 (default, configurable via SA0 pin)

## Modular Structure Benefits

### Arduino version (links everything):
```cpp
#include <SegLCDLib.h>  // ~60KB flash!
```

### MicroPython version (links only needed):
```python
from displays.pcf85176.raw import PCF85176_Raw  # ~8KB flash
```

**Savings: ~85%**

## Drive and Bias Modes

| LCD Type | Drive | Bias |
|---------|-------|------|
| Static (1 segment) | `MODE_DRIVE_STATIC` | `MODE_BIAS_13` |
| 1/2 duty | `MODE_DRIVE_12` | `MODE_BIAS_12` |
| 1/3 duty | `MODE_DRIVE_13` | `MODE_BIAS_13` |
| 1/4 duty | `MODE_DRIVE_14` | `MODE_BIAS_13` |

Most LCDs use **1/4 duty, 1/3 bias**.

## Testing

Library uses **native MicroPython** for testing (not Python mocks):

```bash
cd micropython-seglcd
micropython test_syntax.py
```

Tests verify:
- ✅ Correct imports of all modules
- ✅ Character mapping (7-seg + 16-seg)
- ✅ I2C communication (with mock)
- ✅ RAW display functions
- ✅ Memory usage

## Development

### Adding a New Display

1. Create file in `displays/pcf85176/mydisplay.py`
2. Inherit from `PCF85176Driver`
3. Implement `_write_char()` method
4. Add segment mapping

Example:
```python
from drivers.pcf85176 import PCF85176Driver
from charset import get_char_value

class MyDisplay(PCF85176Driver):
    def __init__(self, i2c):
        super().__init__(i2c)
        self._digits = 6

    def _write_char(self, ch):
        segments = get_char_value(ch)
        # Map segments to RAM addresses
        self._write_ram(segments, address_for_digit)
        return True
```

## Roadmap

- [x] Base abstract class
- [x] Charset (7-segment + 16-segment)
- [x] PCF85176 I2C driver
- [x] PCF85176 RAW display
- [ ] PCF85176 TempHum display
- [ ] PCF85176 6-digit display
- [ ] HT1621 3-wire driver
- [ ] HT1621 displays
- [ ] VK0192 driver
- [ ] API documentation
- [ ] Unit tests

## Links

- [Arduino version](https://github.com/petrkr/SegLCDLib)
- [API documentation](https://petrkr.github.io/SegLCDLib/)
- [LCD API 1.0 spec](https://playground.arduino.cc/Code/LCDAPI/)

## License

Same as Arduino version (MIT)

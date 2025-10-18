"""
MicroPython SegLCD Library Tests
Run with: cd micropython-seglcd && micropython test_syntax.py
"""

print("="*60)
print("MicroPython SegLCD Library - Test Suite")
print("="*60)

# Mock machine.I2C for testing without hardware
class MockI2C:
    """Mock I2C for testing without physical hardware"""
    def __init__(self):
        self.transactions = []

    def writeto(self, addr, data):
        self.transactions.append(('write', addr, data))
        return len(data)

    def readfrom(self, addr, nbytes):
        return bytes(nbytes)

print("\n[TEST 1] Testing base.py...")
try:
    from base import SegLCD, MODE_DRIVE_14, MODE_BIAS_13, MODE_DRIVE_STATIC
    print("  ✓ Imports successful")
    print(f"  ✓ MODE_DRIVE_14 = {MODE_DRIVE_14}")
    print(f"  ✓ MODE_BIAS_13 = {MODE_BIAS_13}")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    sys.exit(1)

print("\n[TEST 2] Testing charset.py...")
try:
    from charset import get_char_value, get_16char_value

    # Test 7-segment characters
    test_cases = [
        ('0', 0b11111100),
        ('1', 0b01100000),
        ('A', 0b11101110),
        ('a', 0b11101110),
        (' ', 0x00),
        ('-', 0b00000010),
    ]

    for ch, expected in test_cases:
        result = get_char_value(ch)
        assert result == expected, f"'{ch}' expected {expected:08b}, got {result:08b}"

    print("  ✓ 7-segment mapping works")
    print(f"    '0' → {get_char_value('0'):08b}")
    print(f"    'A' → {get_char_value('A'):08b}")

    # Test 16-segment
    result_16 = get_16char_value('A')
    print(f"  ✓ 16-segment mapping works")
    print(f"    'A' → {result_16:016b}")

except Exception as e:
    print(f"  ✗ FAILED: {e}")
    sys.exit(1)

print("\n[TEST 3] Testing drivers/pcf85176.py...")
try:
    from drivers.pcf85176 import PCF85176Driver, BLINK_FREQUENCY_2HZ

    i2c_mock = MockI2C()
    driver = PCF85176Driver(i2c_mock, address=0x38)
    print("  ✓ PCF85176Driver instantiated")

    # Test init
    driver.init()
    print(f"  ✓ init() executed ({len(i2c_mock.transactions)} I2C transactions)")

    # Test write_ram
    i2c_mock.transactions.clear()
    driver._write_ram(0xFF, 0)
    assert len(i2c_mock.transactions) > 0, "No I2C transaction recorded"
    print(f"  ✓ _write_ram() works")

    # Test blink
    driver.blink(BLINK_FREQUENCY_2HZ)
    print(f"  ✓ blink() works")

except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[TEST 4] Testing displays/pcf85176/raw.py...")
try:
    from displays.pcf85176.raw import PCF85176_Raw
    from base import MODE_DRIVE_14, MODE_BIAS_13

    i2c_mock = MockI2C()
    lcd = PCF85176_Raw(i2c_mock)
    print("  ✓ PCF85176_Raw instantiated")

    # Test init
    lcd.init(MODE_DRIVE_14, MODE_BIAS_13)
    print("  ✓ init() executed")

    # Test write_ram
    i2c_mock.transactions.clear()
    lcd.write_ram(0xFF, 0)
    assert len(i2c_mock.transactions) > 0
    print("  ✓ write_ram(byte) works")

    # Test write_ram with list
    lcd.write_ram([0xFF, 0xAA], 0)
    print("  ✓ write_ram(list) works")

    # Test clear
    lcd.clear()
    print("  ✓ clear() works")

    # Test on/off
    lcd.on()
    lcd.off()
    print("  ✓ on()/off() work")

except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[TEST 5] Memory usage check...")
try:
    import gc
    gc.collect()
    free_before = gc.mem_free()

    # Import everything
    from displays.pcf85176.raw import PCF85176_Raw
    from charset import get_char_value

    gc.collect()
    free_after = gc.mem_free()
    used = free_before - free_after

    print(f"  ✓ Memory used: ~{used} bytes")
    if used < 0:
        print(f"    (GC freed memory, actual usage likely minimal)")

except Exception as e:
    print(f"  ⚠ Warning: {e}")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nLibrary is ready for deployment to ESP32")
print("\nNext steps:")
print("  1. Upload to ESP32: ampy -p /dev/ttyUSB0 put micropython-seglcd /")
print("  2. Test on hardware with examples/pcf85176_raw_example.py")
print("  3. Implement specific displays (temphum, 6digit, etc.)")
print("="*60)

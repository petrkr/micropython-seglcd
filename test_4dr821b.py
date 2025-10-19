"""
Test 4DR821B display implementation
Run with: micropython test_4dr821b.py
"""

print("="*60)
print("4DR821B Display Test")
print("="*60)

# Mock I2C for testing without hardware
class MockI2C:
    def __init__(self):
        self.transactions = []

    def writeto(self, addr, data):
        self.transactions.append(('write', addr, data))
        return len(data)

print("\n[TEST 1] Import and instantiate...")
try:
    from seglcd.displays.pcf85176.dr821b import PCF85176_4DR821B

    i2c_mock = MockI2C()
    lcd = PCF85176_4DR821B(i2c_mock)
    print("  ✓ PCF85176_4DR821B instantiated")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import sys
    sys.print_exception(e)
    sys.exit(1)

print("\n[TEST 2] Initialize...")
try:
    lcd.init()
    print("  ✓ init() executed")
    print(f"    I2C transactions: {len(i2c_mock.transactions)}")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import sys
    sys.exit(1)

print("\n[TEST 3] Clear...")
try:
    i2c_mock.transactions.clear()
    lcd.clear()
    print("  ✓ clear() executed")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import sys
    sys.exit(1)

print("\n[TEST 4] Write characters...")
try:
    i2c_mock.transactions.clear()
    lcd.home()
    lcd.write(ord('1'))
    lcd.write(ord('2'))
    print(f"  ✓ Wrote '12' ({len(i2c_mock.transactions)} transactions)")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import sys
    sys.exit(1)

print("\n[TEST 5] Clock colon...")
try:
    i2c_mock.transactions.clear()
    lcd.set_clock_colon(0, 0, True)
    assert len(i2c_mock.transactions) > 0
    print("  ✓ set_clock_colon() works")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import sys
    sys.exit(1)

print("\n[TEST 6] Decimal point...")
try:
    i2c_mock.transactions.clear()
    lcd.set_decimal(0, 0, True)
    assert len(i2c_mock.transactions) > 0
    print("  ✓ set_decimal() works")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import sys
    sys.exit(1)

print("\n[TEST 7] Print string with colon...")
try:
    i2c_mock.transactions.clear()
    lcd.home()
    count = lcd.print("12:54")
    print(f"  ✓ print('12:54') returned {count}")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import sys
    sys.exit(1)

print("\n[TEST 8] Print string with decimal...")
try:
    i2c_mock.transactions.clear()
    lcd.home()
    count = lcd.print("12.34")
    print(f"  ✓ print('12.34') returned {count}")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import sys
    sys.exit(1)

print("\n" + "="*60)
print("✅ ALL 4DR821B TESTS PASSED!")
print("="*60)
print("\nReady for hardware testing!")
print("Upload to ESP32 and run examples/4dr821b_clock_example.py")

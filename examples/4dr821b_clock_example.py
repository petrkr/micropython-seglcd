"""
Example: Tesla 4DR821B Clock Display
Demonstrates 4-digit clock display with colon
"""

from machine import I2C, Pin, RTC
import time

from seglcd.displays.pcf85176.dr821b import PCF85176_4DR821B

# Initialize I2C
# ESP32 defaults: SDA=Pin(21), SCL=Pin(22)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

# Create LCD instance
lcd = PCF85176_4DR821B(i2c)

print("Initializing 4DR821B display...")
lcd.init()

# Clear display
lcd.clear()
print("Display cleared")

time.sleep(1)

# Example 1: Simple time display
print("\nExample 1: Static time display")
lcd.home()
lcd.print("12:54")
time.sleep(3)

# Example 2: Time with decimal point
print("\nExample 2: With decimal point")
lcd.clear()
lcd.home()
lcd.print("23.45")
time.sleep(3)

# Example 3: Manual digit control
print("\nExample 3: Manual control")
lcd.clear()
lcd.set_cursor(0, 0)
lcd.write(ord('8'))
lcd.set_cursor(0, 1)
lcd.write(ord('8'))
lcd.set_clock_colon(0, 0, True)  # Show colon
lcd.set_cursor(0, 2)
lcd.write(ord('8'))
lcd.set_cursor(0, 3)
lcd.write(ord('8'))
time.sleep(3)

# Example 4: Decimal point animation
print("\nExample 4: Decimal point animation")
lcd.clear()
lcd.home()
lcd.print("1234")
for i in range(3):
    lcd.set_decimal(0, i, True)
    time.sleep(0.5)

    lcd.set_decimal(0, i, False)
    time.sleep(0.5)

# Example 5: Clock display with RTC (if available)
print("\nExample 5: Real-time clock")
try:
    rtc = RTC()
    # Set example time if needed
    # rtc.datetime((2025, 1, 1, 0, 12, 34, 0, 0))  # (year, month, day, weekday, hours, minutes, seconds, subseconds)

    for _ in range(10):
        now = rtc.datetime()
        hours = now[4]
        minutes = now[5]

        lcd.home()
        lcd.print(f"{hours:02d}:{minutes:02d}")

        time.sleep(1)
except Exception as e:
    print(f"RTC not available: {e}")
    print("Showing static time instead")
    lcd.home()
    lcd.print("12:00")
    time.sleep(3)

# Example 6: Blinking colon (clock effect)
print("\nExample 6: Blinking colon")
for i in range(10):
    lcd.home()
    lcd.print("12:34")
    time.sleep(0.5)

    lcd.home()
    lcd.print("1234")
    time.sleep(0.5)

print("\nExamples complete!")
lcd.clear()

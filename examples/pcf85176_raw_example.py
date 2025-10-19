"""
Example: PCF85176 RAW Display
Demonstrates direct RAM access to PCF85176 LCD controller
"""

from machine import I2C, Pin
import time

# Import the RAW display class (files must be uploaded to ESP32 first)
from seglcd.displays.pcf85176.raw import PCF85176_Raw
from seglcd.base import MODE_DRIVE_STATIC, MODE_DRIVE_14, MODE_BIAS_13

# Initialize I2C
# ESP32: SDA=Pin(21), SCL=Pin(22) are default
# Adjust pins as needed for your setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

# Create LCD instance
# Default I2C address is 0x38 (can be changed with SA0 pin)
lcd = PCF85176_Raw(i2c)

print("Initializing LCD...")

# Initialize with 1/4 duty, 1/3 bias (common for most LCDs)
# Use MODE_DRIVE_STATIC for static (1/1 duty) displays
lcd.init(MODE_DRIVE_14, MODE_BIAS_13)

# Clear display
lcd.clear()
print("LCD cleared")

time.sleep(1)

# Turn on display
lcd.on()
print("Display ON")

# Example 1: Write single byte to address 0
print("Writing 0b10000000 to address 0...")
lcd.write_ram(0b10000000, 0)
time.sleep(2)

# Example 2: Write single byte to address 8
print("Writing 0b01000000 to address 8...")
lcd.write_ram(0b01000000, 8)
time.sleep(2)

# Example 3: Write multiple bytes starting at address 0
print("Writing multiple bytes...")
data = [0b11111111, 0b11111111]
lcd.write_ram(data, 0)
time.sleep(2)

# Example 4: Clear display
print("Clearing display...")
lcd.clear()
time.sleep(1)

# Example 5: Blink test (if supported by your LCD)
from drivers.pcf85176 import BLINK_FREQUENCY_2HZ, BLINK_MODE_NORMAL

print("Testing blink at 2Hz...")
lcd.write_ram(0xFF, 0)
lcd.blink(BLINK_FREQUENCY_2HZ, BLINK_MODE_NORMAL)
time.sleep(5)

# Stop blinking
from drivers.pcf85176 import BLINK_FREQUENCY_OFF
lcd.blink(BLINK_FREQUENCY_OFF)

# Turn off display
print("Display OFF")
lcd.off()

print("Example complete!")

"""
SegLCD - Modular Segment LCD Library for MicroPython

Example usage:
    from seglcd.displays.pcf85176.raw import PCF85176_Raw
    from machine import I2C, Pin

    i2c = I2C(0, scl=Pin(22), sda=Pin(21))
    lcd = PCF85176_Raw(i2c)
    lcd.init()
    lcd.on()
"""

__version__ = '0.0.1'
__author__ = 'Petr Kracik'

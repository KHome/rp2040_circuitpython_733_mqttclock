# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example uses adafruit_display_text.label to display text using a custom font
loaded by adafruit_bitmap_font
"""

import board
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
import time
import board
import busio
#import adafruit_ssd1306
import digitalio
import displayio
import adafruit_displayio_ssd1306
import microcontroller
# Create the I2C interface.
try:
    i2c = busio.I2C(board.GP19, board.GP18)
except:
    #microcontroller.reset()
    print('i2c geblock')
    
led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT
led.value = 1
# Create the SSD
# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
# The I2C address for these displays is 0x3d or 0x3c, change to match
# A reset line may be required if there is no auto-reset circuitry
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C, reset=led)
display_bus = displayio.I2CDisplay(i2c,device_address=0x3c)
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, display_bus)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=64, height=128)
# try uncommenting different font files if you like
#font_file = "/fonts/LeagueSpartan-Bold-16.bdf"
#font_file = "fonts/crevice100.bdf"
font_file = "fonts/Junction-regular-24.bdf"
# Set text, font, and color
text = "1"
font = bitmap_font.load_font(font_file)
color = 0xFFFFFF

# Create the tet label
text_area = label.Label(font, text=text, color=color)

# Set the location
text_area.x = 0
text_area.y = 20

# Show it
display.rotation=1
display.show(text_area)
time.sleep(1)
text_area.text = "2"
time.sleep(1)
text_area.text = "11:11"
time.sleep(2)
i2c.deinit()
time.sleep(2)

#while True:
#    pass


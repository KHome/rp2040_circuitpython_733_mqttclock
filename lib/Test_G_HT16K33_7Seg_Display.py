# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of setting digits on a LED segment display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

import time

# Import all board pins.
import board
import busio

# Import the HT16K33 LED segment module.
from adafruit_ht16k33 import segments

# Create the I2C interface.
import adafruit_tsl2561
import adafruit_ds3231

# Lookup table for names of days (nicer printing).
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")



#i2c = busio.I2C(board.GP19, board.GP18)
i2c = busio.I2C(board.GP21, board.GP20)
#while not i2c.try_lock():
#    pass##

#try:
#    while True:
#        print(
#            "I2C addresses found:",
#            [hex(device_address) for device_address in i2c.scan()],
#        )
#        time.sleep(2)##
#
#finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
#    i2c.unlock()
    
# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)

#rtc = adafruit_ds3231.DS3231(i2c)

# Create the TSL2561 instance, passing in the I2C bus
#tsl = adafruit_tsl2561.TSL2561(i2c)

# Or this creates a 14 segment alphanumeric 4 character display:
# display = segments.Seg14x4(i2c)
# Or this creates a big 7 segment 4 character display
# display = segments.BigSeg7x4(i2c)
# Finally you can optionally specify a custom I2C address of the HT16k33 like:
# display = segments.Seg7x4(i2c, address=0x70)

# Clear the display.
display.brightness=0.01
display.fill(0)

# Can just print a number
#display.print(42)
#time.sleep(2)

# Or, can print a hexadecimal value
#display.print_hex(0xFF23)
#time.sleep(2)

# Or, print the time
display.print("12:30")
time.sleep(.5)
display.colon = False
time.sleep(.5)
display.colon = True
time.sleep(.5)
display.colon = False
time.sleep(.5)
display.colon = True
display.print("    ")
display.colon = False
# Or, can set indivdual digits / characters
# Set the first character to '1':
##display[0] = "1"
# Set the second character to '2':
##display[1] = "2"
# Set the third character to 'A':
#display[2] = "A"
# Set the forth character to 'B':
#display[3] = "B"
#time.sleep(2)

# Or, can even set the segments to make up characters
#display.set_digit_raw(0, 0xFF)
#display.set_digit_raw(1, 0b11111111)
#display.set_digit_raw(2, 0x79)
#display.set_digit_raw(3, 0b01111001)
#time.sleep(2)

# Show a looping marquee
#display.marquee("Deadbeef 192.168.100.102... ", 0.2, False)
# Print chip info

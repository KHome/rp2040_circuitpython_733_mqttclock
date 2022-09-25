# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example uses AnimationsSequence to display multiple animations in sequence, at a five second
interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.

This example does not work on SAMD21 (M0) boards.
"""
import time
import board
import neopixel

# Update to match the pin connected to your NeoPixels
pixel_pin = board.GP15
# Update to match the number of NeoPixels you have connected
pixel_num = 32

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.009, auto_write=True, pixel_order="GRBW")

#R, G, B, W

pixels.fill((0,0,0,0))
pixels.fill((245,250,5,0))
time.sleep(1)
pixels.fill((255,0,0,0))
time.sleep(1)
pixels.fill((0,255,0,0))
time.sleep(1)
pixels.fill((0,0,255,0))
time.sleep(1)
pixels.fill((0,0,0,255))
time.sleep(1)
pixels.fill((255,255,255,0))
time.sleep(1)

pixels.fill((0,0,0,0))


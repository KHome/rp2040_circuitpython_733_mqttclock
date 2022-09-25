# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board
import busio
import adafruit_apds9960.apds9960
i2c = busio.I2C(board.GP27, board.GP26)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

#apds.enable_color = True
sensor.enable = True
sensor.enable_proximity = True
sensor.enable_gesture = True
#sensor.enable_color = True
sensor.gesture_gain = 0
#sensor.proximity
sensor.enable_proximity = True

while True:

    gesture = sensor.gesture()

    if gesture == 0x01:
        print("up")
    elif gesture == 0x02:
        print("down")
    elif gesture == 0x03:
        print("left")
    elif gesture == 0x04:
        print("right")
    time.sleep(0.2)

#int_pin = digitalio.DigitalInOut(board.D5)
#int_pin.switch_to_input(pull=digitalio.Pull.UP)
#apds = APDS9960(i2c)

## set the interrupt threshold to fire when proximity reading goes above 175
#apds.proximity_interrupt_threshold = (0, 175)

## assert the interrupt pin when the proximity interrupt is triggered
#apds.enable_proximity_interrupt = True

## enable the sensor's proximity engine
#apds.enable_proximity = True

#while True:
#    # print the proximity reading when the interrupt pin goes low
#    if not int_pin.value:
#        print(apds.proximity)
#
#        # clear the interrupt
#        apds.clear_interrupt()

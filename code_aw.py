# (c) Kreft-inG 2022
# GPL v3
# ---------------
# Pinout
# Module B
#GP13 = yellow = CS (SCNn)
#GP12 = orange = MISO
#GP11 = lila = MOSI
#GP10 = green = SCLK
#####################
# Module C
# i2c = busio.I2C(board.GP21, board.GP20)
#####################
# Module D
# i2c_gesture = busio.I2C(board.GP27, board.GP26)
#####################
# Module E
# same i2c bus as Module C
#####################
# Module F
# same i2c bus as Module C & E
#####################
# Module G
# same i2c bus as Module C & E & F
#####################
# Module H#
# issue
# https://www.hackster.io/mr-alam/how-to-use-i2c-pins-in-raspberry-pi-pico-i2c-scanner-code-8f489f
# JUST 2 pair can be be used
# i2cdisplay = busio.I2C(board.GP19, board.GP18)
# enabledisplay_pin = digitalio.DigitalInOut(board.GP16)
#####################
# Module I, J, K
# spi=busio.SPI(clock=board.GP2,MOSI=board.GP3,MISO=board.GP4)
# cs=board.GP5
#
# sdcard = sdcardio.SDCard(spi, cs)
#
# audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP6)
####################
# Module L
# InnerHexagon NEOPIXEL = board.GP22 #NEOPIXEL
####################
# Module L2
# OuterHexagon NEOPIXEL = board.GP15 #NEOPIXEL
####################

# ---------------
# To be done checklist
# 1. Logic by AWTRIX , binary controls
# 2. Logic by K-inG ,  binary controls add-on
# 3. Feature Extension: RTC ?
# 4. Testing, Error Debouncing
# 5. Watchdog
# 6. MQTT disconnect warning on Matrix
#  
# ? Pico-Bug? .Can't handle "B" 256 values, just "b" up to 127, and also not string type. Reduce call with framebuffer, do directly
# ? Loudness Workaround. Save relevant files with less volume digital and convert filename to include this
# ----------------------------------
# -----------------------PARAMETER 
matrixname = 'awtrixmatre3x'
is_reduced_power_due_to_debug = True
# -------------------------------
# ---------------------- MODULE A --
# Import secrets for MQTT
import secrets
secrets = secrets.secrets

# ---------------------- MODULE B --
import board
import busio
import digitalio
import time
from adafruit_wiznet5k.adafruit_wiznet5k import *
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import neopixel
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from secrets import secrets

print("Wiznet5k Fixed IP")
# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0x00, 0x01, 0x02, 0x03, 0x04, 0x66)
IP_ADDRESS = (192, 168, 178, 66)
SUBNET_MASK = (255, 255, 255, 0)
GATEWAY_ADDRESS = (192, 168, 178, 2)
DNS_SERVER = (192, 168, 178, 2)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

cs = digitalio.DigitalInOut(board.GP13)
# For Particle Ethernet FeatherWing
# cs = digitalio.DigitalInOut(board.D5)

#spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#GP13 = yellow = CS (SCNn)
#GP12 = orange = MISO
#GP11 = lila = MOSI
#GP10 = green = SCLK
spi_bus = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)

# # Initialize ethernet interface without DHCP
# eth = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=MY_MAC, debug=False)
# # Set network configuration
# eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)

# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=MY_MAC, debug=False)

eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)

print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

# Setup a feed named 'color_feed' for publishing to a feed
color_feed = matrixname + "/command"
### Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT! Listening for topic changes on %s" % color_feed)
    # Subscribe to all changes on the onoff_feed.
    client.subscribe(color_feed)

def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT!")


# Initialize MQTT interface with the ethernet interface
MQTT.set_socket(socket, eth)

# Set up a MiniMQTT Client
# NOTE: We'll need to connect insecurely for ethernet configurations.
mqtt_client = MQTT.MQTT(
    broker="192.168.178.26",
    username=secrets["aio_username"],
    password=secrets["aio_key"],
    is_ssl=False,
)

# Setup the callback methods above
##mqtt_client.on_connect = connected
##mqtt_client.on_disconnect = disconnected
##mqtt_client.on_message = message

# Connect the client to the MQTT broker.
print("Connecting to MQTT...")
mqtt_client.connect()


#---------------------------

#---------------------- MODULE C
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of reading and writing the time for the DS3231 real-time clock.
# Change the if False to if True below to set the time, otherwise it will just
# print the current date and time every second.  Notice also comments to adjust
# for working with hardware vs. software I2C.

###import time
###import board
###import busio

import adafruit_ds3231

i2c = busio.I2C(board.GP21, board.GP20)
rtc = adafruit_ds3231.DS3231(i2c)

# Lookup table for names of days (nicer printing).
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


#### pylint: disable-msg=using-constant-test
###if False:  # change to True if you want to set the time!
###    #                     year, mon, date, hour, min, sec, wday, yday, isdst
###    t = time.struct_time((2022, 09, 24, 00, 1, 0, 0, -1, -1))
###    # you must set year, mon, date, hour, min, sec and weekday
###    # yearday is not supported, isdst can be set but we don't do anything with it at this time
###    print("Setting time to:", t)  # uncomment for debugging
###    rtc.datetime = t
###    print()
#### pylint: enable-msg=using-constant-test

# Main loop:
#while True:
mytime = rtc.datetime

def c_31_writeRTCtime(hour,minu,year,month,day):
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((int(year), int(month), int(day), int(hour), int(minu), 0, 0, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t
    #print()
    # print(t)     # uncomment for debugging
###print(
###    "The date is {} {}/{}/{}".format(
###        days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
###    )
###)
###print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
#    time.sleep(1)  # wait a second
###print("Temperature {}".format(rtc.temperature))
# ---------------------------


#---------------------- MODULE D
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
###import time
###import board
###import busio
use_gesture = False
if use_gesture == True:
    import adafruit_apds9960.apds9960
    i2c_gesture = busio.I2C(board.GP27, board.GP26)
    sensor = adafruit_apds9960.apds9960.APDS9960(i2c_gesture)
    
    #apds.enable_color = True
    sensor.enable = True
    sensor.enable_proximity = True
    sensor.enable_gesture = True
    #sensor.enable_color = True
    sensor.gesture_gain = 0
    #sensor.proximity
    sensor.enable_proximity = True
    gesture = sensor.gesture()
###while True:
###    gesture = sensor.gesture()
###
###    if gesture == 0x01:
###        print("up")
###    elif gesture == 0x02:
###        print("down")
###    elif gesture == 0x03:
###        print("left")
###    elif gesture == 0x04:
###        print("right")
###    time.sleep(0.2)

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
# ---------------------------


#---------------------- MODULE E
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

###import time
###import board
###import busio
import adafruit_tsl2561

# Create the I2C bus
###i2c = busio.I2C(board.GP21, board.GP20)

# Create the TSL2561 instance, passing in the I2C bus
tsl = adafruit_tsl2561.TSL2561(i2c)

# Print chip info
print("Chip ID = {}".format(tsl.chip_id))
print("Enabled = {}".format(tsl.enabled))
print("Gain = {}".format(tsl.gain))
print("Integration time = {}".format(tsl.integration_time))

print("Configuring TSL2561...")

# Enable the light sensor
tsl.enabled = True
time.sleep(1)

# Set gain 0=1x, 1=16x
tsl.gain = 1

# Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
tsl.integration_time = 2

print("Getting readings...")

# Get raw (luminosity) readings individually
broadband = tsl.broadband
infrared = tsl.infrared

# Get raw (luminosity) readings using tuple unpacking
# broadband, infrared = tsl.luminosity

# Get computed lux value (tsl.lux can return None or a float)
lux = tsl.lux

# Print results
print("Enabled = {}".format(tsl.enabled))
print("Gain = {}".format(tsl.gain))
print("Integration time = {}".format(tsl.integration_time))
print("Broadband = {}".format(broadband))
print("Infrared = {}".format(infrared))
if lux is not None:
    print("Lux = {}".format(lux))
else:
    print("Lux value is None. Possible sensor underrange or overrange.")

# Disble the light sensor (to save power)
###tsl.enabled = False
def getlux():
    tsl.gain = 0
    lux = tsl.lux
    if lux is not None:
        return lux
    else:
        tsl.gain = 8
        lux = tsl.lux
        if lux is not None:
            return lux
        else:
            return -1

# ---------------------------


#---------------------- MODULE F
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
###
###"""
###Example showing how the BME280 library can be used to set the various
###parameters supported by the sensor.
###Refer to the BME280 datasheet to understand what these parameters do
###"""
###import time
###import board
###import busio
import adafruit_bme280.advanced as adafruit_bme280

# Create sensor object, using the board's default I2C bus.
#i2c = board.I2C()  # uses board.SCL and board.SDA
###i2c = busio.I2C(board.GP21, board.GP20)

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# OR create sensor object, using the board's default SPI bus.
# SPI setup
# from digitalio import DigitalInOut
# spi = board.SPI()
# bme_cs = digitalio.DigitalInOut(board.D10)
# bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# Change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1014.25
bme280.mode = adafruit_bme280.MODE_NORMAL
bme280.standby_period = adafruit_bme280.STANDBY_TC_1000
bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X16
# The sensor will need a moment to gather initial readings
time.sleep(1)

#while True:
if True:
    print("\nTemperature: %0.1f C" % bme280.temperature)
    print("Humidity: %0.1f %%" % bme280.relative_humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude = %0.2f meters" % bme280.altitude)
    #time.sleep(2)

# ---------------------------


#---------------------- MODULE G
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of setting digits on a LED segment display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

###import time

# Import all board pins.
###import board
###import busio

# Import the HT16K33 LED segment module.
from adafruit_ht16k33 import segments
# Lookup table for names of days (nicer printing).
###days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
###i2c = busio.I2C(board.GP21, board.GP20)
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
display.print("12:34")
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

def display7seg_string(mystring):
    global display
    if len(mystring) > 3 and len(mystring) <6 :
        display.print(mystring)
        display.show()
    
def display7seg_blink(blinkrate):
    global display
    if blinkrate > -1 and blinkrate < 4:
        display.blink_rate = blinkrate
        display.show()
    
def display7seg_brightness(value):
    global display
    if value >= 0 and value <=1.0:
        display.brightness = value

# ---------------------------


#---------------------- MODULE H
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

#"""
#This example uses adafruit_display_text.label to display text using a custom font
#loaded by adafruit_bitmap_font
#"""

#import board
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
#import time
#import board
#import busio
#import adafruit_ssd1306
import digitalio
import displayio
import adafruit_displayio_ssd1306
import microcontroller
# Create the I2C interface.
try:
    i2cdisplay = busio.I2C(board.GP19, board.GP18)
except:
    #microcontroller.reset()
    print('i2c display geblock')
    
enabledisplay_pin = digitalio.DigitalInOut(board.GP16)
enabledisplay_pin.direction = digitalio.Direction.OUTPUT
enabledisplay_pin.value = 1
# Create the SSD
# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
# The I2C address for these displays is 0x3d or 0x3c, change to match
# A reset line may be required if there is no auto-reset circuitry
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C, reset=led)
display_bus = displayio.I2CDisplay(i2cdisplay,device_address=0x3c)
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, display_bus)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=64, height=128)
# try uncommenting different font files if you like
#font_file = "/fonts/LeagueSpartan-Bold-16.bdf"
#font_file = "fonts/crevice100.bdf"
font_file24 = "fonts/Junction-regular-24.bdf"
font_file48 = "fonts/Junction-regular-24.bdf"
# Set text, font, and color
text = "1"
font = bitmap_font.load_font(font_file24)
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
#text_area.text = "2"
#time.sleep(1)
text_area.text = "Startup"
#time.sleep(2)
#i2c.deinit()
#time.sleep(2)

#while True:
#    pass

# ---------------------------


#---------------------- MODULE I,J,K
#"""
#CircuitPython I2S MP3 playback example.
#Plays a single MP3 once.
#"""
###import board
import audiomp3
import audiobusio

###import busio
import sdcardio
import storage

###import time

# # MicroSD SPI Pins
# * MicroSD MISO pin to Pico GPIO-12
# * MicroSD MOSI pin to Pico GPIO-11
# * MicroSD SCK pin to Pico GPIO-10
# * MicroSD CS pin to Pico GPIO-13
 
spi=busio.SPI(clock=board.GP2,MOSI=board.GP3,MISO=board.GP4)
cs=board.GP5

sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP6)
#001_32kbps_fs24kHz_mono.mp3 - Dong. tunes 
#002_32kbps_fs24kHz_mono.mp3 - Dong, dong, waser hintergrund
#003_32kbps_fs24kHz_mono.mp3
#004_32kbps_fs24kHz_mono.mp3
#005_32kbps_fs24kHz_mono.mp3
#006_32kbps_fs24kHz_mono.mp3
#007_32kbps_fs24kHz_mono.mp3
#008_32kbps_fs24kHz_mono.mp3
#009_32kbps_fs24kHz_mono.mp3
#010_32kbps_fs24kHz_mono.mp3
#011_32kbps_fs24kHz_mono.mp3
#012_32kbps_fs24kHz_mono.mp3
#013_32kbps_fs24kHz_mono.mp3
#014_32kbps_fs24kHz_mono.mp3
#015_32kbps_fs24kHz_mono.mp3
#016_32kbps_fs24kHz_mono.mp3
#017_32kbps_fs24kHz_mono.mp3
#018_32kbps_fs24kHz_mono.mp3
#019_32kbps_fs24kHz_mono.mp3

mp3 = audiomp3.MP3Decoder(open("/sd/014_32kbps_fs24kHz_mono.mp3", "rb"))

audio.play(mp3)
#while audio.playing:
#    pass
time.sleep(1)
audio.stop()
mp3=0
#print("Done playing!")

        
def song_stop():
    global audio
    audio.stop()


def song_play(songnr, vol):
    global audio
    if songnr > 2 and songnr < 20:
        nrstring = ""
        if songnr < 10:
            nrstring="00"+str(songnr)
        else:
            nrstring="0"+str(songnr)
        filename="/sd/" + nrstring + "_32kbps_fs24kHz_mono.mp3"
        mp3 = audiomp3.MP3Decoder(open(filename, "rb"))
        audio.play(mp3)
    if songnr == 1:
        song_stop()
    
def status_audioplaying():
    global audio
    if audio.playing:
        return True
    else:
        return False

# ---------------------------


#---------------------- MODULE M
use_watchdog = False
if use_watchdog == True:
    from microcontroller import watchdog as w
    from watchdog import WatchDogMode
    # wait time to catch a debugging session
    time.sleep(10)

    w.timeout=8 # Set a timeout of 8 seconds
    w.mode = WatchDogMode.RESET
    w.feed()
    print('feed_wd');
    for i in range(1, 8): # cnt from 1 to incl 7
        print(i)
        time.sleep(1)
    w.feed()
###w.deinit()
###print('after 7 sec no reset, ok')
###print('No dont feed')
###for i in range(1, 11):
###    print(i)
###    time.sleep(1)
###print(' If you can read this, than Watchdog failed to bite')

# ---------------------------


#---------------------- MODULE L
# SPDX-FileCopyrightText: 2022 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

#"""Demonstrate background writing with NeoPixels####
#
#The NeoPixelBackground class defined here is largely compatible with the
#standard NeoPixel class, except that the ``show()`` method returns immediately,
#writing data to the LEDs in the background, and setting `auto_write` to true
#causes the data to be continuously sent to the LEDs all the time.##
#
#Writing the LED data in the background will allow more time for your
#Python code to run, so it may be possible to slightly increase the refresh
#rate of your LEDs or do more complicated processing.####
#
#Because the pixelbuf storage is also being written out 'live', it is possible
#(even with auto-show 'false') to experience tearing, where the LEDs are a
#combination of old and new values at the same time.#
#
#The demonstration code, under ``if __name__ == '__main__':`` is intended
#for the Adafruit MacroPad, with 12 NeoPixel LEDs. It shows a cycling rainbow
#pattern across all the LEDs.
#"""

import struct
import adafruit_pixelbuf
from rp2pio import StateMachine
from adafruit_pioasm import Program
#from adafruit_led_animation.animation.rainbowcomet import RainbowComet
#from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
#from adafruit_led_animation.animation.sparklepulse import SparklePulse
#from adafruit_led_animation.animation.sparkle import Sparkle
#from adafruit_led_animation.color import AMBER

#from adafruit_led_animation.sequence import AnimationSequence

###import time

# Pixel color order constants
RGB = "RGB"
"""Red Green Blue"""
GRB = "GRB"
"""Green Red Blue"""
RGBW = "RGBW"
"""Red Green Blue White"""
GRBW = "GRBW"
"""Green Red Blue White"""

# NeoPixels are 800khz bit streams. We are choosing zeros as <312ns hi, 936 lo>
# and ones as <700 ns hi, 556 ns lo>.
_program = Program(
    """
.side_set 1 opt
.wrap_target
    pull block          side 0
    out y, 32           side 0      ; get count of NeoPixel bits

bitloop:
    pull ifempty        side 0      ; drive low
    out x 1             side 0 [5]
    jmp !x do_zero      side 1 [3]  ; drive high and branch depending on bit val
    jmp y--, bitloop    side 1 [4]  ; drive high for a one (long pulse)
    jmp end_sequence    side 0      ; sequence is over

do_zero:
    jmp y--, bitloop    side 0 [4]  ; drive low for a zero (short pulse)

end_sequence:
    pull block          side 0      ; get fresh delay value
    out y, 32           side 0      ; get delay count
wait_reset:
    jmp y--, wait_reset side 0      ; wait until delay elapses
.wrap
        """
)

###minbright= 0.008
setbright= 0.02

class NeoPixelBackground(  # pylint: disable=too-few-public-methods
    adafruit_pixelbuf.PixelBuf
):
    def __init__(
        self, pin, n, *, bpp=3, brightness=setbright, auto_write=True, pixel_order=None
    ):
        if not pixel_order:
            pixel_order = GRB if bpp == 3 else GRBW
        elif isinstance(pixel_order, tuple):
            order_list = [RGBW[order] for order in pixel_order]
            pixel_order = "".join(order_list)

        byte_count = bpp * n
        bit_count = byte_count * 8
        padding_count = -byte_count % 4

        # backwards, so that dma byteswap corrects it!
        header = struct.pack(">L", bit_count - 1)
        trailer = b"\0" * padding_count + struct.pack(">L", 3840)

        self._sm = StateMachine(
            _program.assembled,
            auto_pull=False,
            first_sideset_pin=pin,
            out_shift_right=False,
            pull_threshold=32,
            frequency=12_800_000,
            **_program.pio_kwargs,
        )

        self._first = True
        super().__init__(
            n,
            brightness=brightness,
            byteorder=pixel_order,
            auto_write=False,
            header=header,
            trailer=trailer,
        )

        self._auto_write = False
        self._auto_writing = False
        self.auto_write = auto_write

    @property
    def auto_write(self):
        return self._auto_write

    @auto_write.setter
    def auto_write(self, value):
        self._auto_write = bool(value)
        if not value and self._auto_writing:
            self._sm.background_write()
            self._auto_writing = False
        elif value:
            self.show()

    def _transmit(self, buf):
        if self._auto_write:
            if not self._auto_writing:
                self._sm.background_write(loop=memoryview(buf).cast("L"), swap=True)
                self._auto_writing = True
        else:
            self._sm.background_write(memoryview(buf).cast("L"), swap=True)


###if __name__ == "__main__":
###    import board
import rainbowio
import supervisor

NEOPIXEL = board.GP22 #NEOPIXEL
NUM_PIXELS_inner = 96
pixels_inner = NeoPixelBackground(NEOPIXEL, NUM_PIXELS_inner)
   # while True:
   
   # Around 1 cycle per second
# ---------------------------


#---------------------- MODULE N
if True:
    hourarray = [[ 3, 18, 19, 21, 4, 14, 23, 22, 24, 13, 27, 42, 43 ],
        [ 0, 18, 17, 23, 24 ],
        [ 0, 1, 18, 17, 16, 15, 24, 25 ],
        [ 0, 1, 18, 17, 16, 23, 24, 25 ],
        [ 2, 18, 17, 16, 23, 24 ],
        [ 0, 1, 2, 17, 16, 23, 24, 25 ],
        [ 0, 1, 2, 17, 16, 15, 23, 24, 25 ],
        [ 0, 1, 2, 18, 17, 23, 24 ],
        [ 0, 1, 2, 18, 17, 16, 15, 23, 24, 25 ],
        [ 0, 1, 2, 18, 17, 16, 23, 24, 25 ],
        [ 3, 18, 19, 21, 17, 4, 14, 44, 24, 13, 27, 42, 43 ],
        [ 3, 18, 17, 4, 14, 23, 24, 13, 27, 42 ]]
    #pixels.fill(rainbowio.colorwheel(supervisor.ticks_ms() // 4))
    minarray = [[ 58, 57, 69, 70, 80, 68, 67, 59, 91, 83, 84, 64, 86, 85, 89, 90 ], 
        [ 58, 57, 67, 59, 64, 86, 85, 84, 69, 68, 82, 83, 89 ], 
        [ 58, 57, 67, 59, 64, 86, 85, 84, 69, 70, 80, 82, 81, 83, 89, 90 ],
        [ 58, 57, 67, 59, 64, 86, 85, 84, 69, 70, 80, 82, 81, 91, 89, 90 ],
        [ 58, 57, 67, 59, 64, 86, 85, 84, 80, 68, 82, 81, 91, 90 ],
        [ 58, 57, 67, 59, 64, 86, 85, 84, 69, 70, 68, 82, 81, 91, 89, 90 ],
        [ 58, 57, 67, 59, 64, 86, 85, 84, 69, 70, 68, 82, 81, 91, 83, 89, 90 ],
        [ 58, 57, 67, 59, 64, 86, 85, 84, 69, 70, 80, 68, 81, 91, 90 ],
        [ 58, 57, 67, 59, 64, 86, 85, 84, 69, 70, 80, 68, 82, 81, 91, 83, 89, 90 ],
        [ 58, 57, 67, 59, 64, 86, 85, 84, 69, 70, 80, 68, 82, 81, 91, 89, 90 ],
        [ 58, 69, 70, 80, 68, 59, 65, 91, 83, 64, 86, 89, 90 ],
        [ 58, 69, 68, 59, 65, 82, 83, 64, 86, 89 ],
        [ 58, 69, 70, 80, 59, 65, 82, 81, 83, 64, 86, 89, 90 ],
        [ 58, 69, 70, 80, 59, 65, 82, 81, 91, 64, 86, 89, 90 ],
        [ 58, 80, 68, 59, 65, 82, 81, 91, 64, 86, 90 ],
        [ 58, 69, 70, 68, 59, 65, 82, 81, 91, 64, 86, 89, 90 ],
        [ 58, 69, 70, 68, 59, 65, 82, 81, 91, 83, 64, 86, 89, 90 ],
        [ 58, 69, 70, 80, 68, 59, 65, 81, 91, 64, 86, 90 ],
        [ 58, 69, 70, 80, 68, 59, 65, 82, 81, 91, 83, 64, 86, 89, 90 ],
        [ 58, 69, 70, 80, 68, 59, 65, 82, 81, 91, 64, 86, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 67, 65, 66, 91, 83, 64, 86, 85, 89, 90 ],
        [ 58, 57, 70, 80, 67, 65, 66, 81, 91, 64, 86, 85, 90 ],
        [ 58, 57, 69, 70, 80, 67, 65, 66, 82, 81, 83, 64, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 67, 65, 66, 82, 81, 91, 64, 86, 85, 89, 90 ],
        [ 58, 57, 80, 68, 67, 65, 66, 82, 81, 91, 64, 86, 85, 90 ],
        [ 58, 57, 69, 70, 68, 67, 65, 66, 82, 81, 91, 64, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 68, 67, 65, 66, 82, 81, 91, 83, 64, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 67, 65, 66, 81, 91, 64, 86, 85, 90 ],
        [ 58, 57, 69, 70, 80, 68, 67, 65, 66, 82, 81, 91, 83, 64, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 67, 65, 66, 82, 81, 91, 64, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 67, 65, 66, 91, 83, 84, 86, 85, 89, 90 ],
        [ 58, 57, 70, 80, 67, 65, 66, 81, 91, 84, 86, 85, 90 ],
        [ 58, 57, 69, 70, 80, 67, 65, 66, 82, 81, 83, 84, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 67, 65, 66, 82, 81, 91, 84, 86, 85, 89, 90 ],
        [ 58, 57, 80, 68, 67, 65, 66, 82, 81, 91, 84, 86, 85, 90 ],
        [ 58, 57, 69, 70, 68, 67, 65, 66, 82, 81, 91, 84, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 68, 67, 65, 66, 82, 81, 91, 83, 84, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 67, 65, 66, 81, 91, 84, 86, 85, 90 ],
        [ 58, 57, 69, 70, 80, 68, 67, 65, 66, 82, 81, 91, 83, 84, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 67, 65, 66, 82, 81, 91, 84, 86, 85, 89, 90 ],
        [ 69, 70, 80, 68, 67, 59, 65, 66, 91, 83, 84, 85, 89, 90 ],
        [ 70, 80, 67, 59, 65, 66, 81, 91, 84, 85, 90 ],
        [ 69, 70, 80, 67, 59, 65, 66, 82, 81, 83, 84, 85, 89, 90 ],
        [ 69, 70, 80, 67, 59, 65, 66, 82, 81, 91, 84, 85, 89, 90 ],
        [ 80, 68, 67, 59, 65, 66, 82, 81, 91, 84, 85, 90 ],
        [ 69, 70, 68, 67, 59, 65, 66, 82, 81, 91, 84, 85, 89, 90 ],
        [ 69, 70, 68, 67, 59, 65, 66, 82, 81, 91, 83, 84, 85, 89, 90 ],
        [ 69, 70, 80, 68, 67, 59, 65, 66, 81, 91, 84, 85, 90 ],
        [ 69, 70, 80, 68, 67, 59, 65, 66, 82, 81, 91, 83, 84, 85, 89, 90 ],
        [ 69, 70, 80, 68, 67, 59, 65, 66, 82, 81, 91, 84, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 59, 65, 66, 91, 83, 84, 86, 85, 89, 90 ],
        [ 58, 57, 70, 80, 59, 65, 66, 81, 91, 84, 86, 85, 90 ],
        [ 58, 57, 69, 70, 80, 59, 65, 66, 82, 81, 83, 84, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 59, 65, 66, 82, 81, 91, 84, 86, 85, 89, 90 ],
        [ 58, 57, 80, 68, 59, 65, 66, 82, 81, 91, 84, 86, 85, 90 ],
        [ 58, 57, 69, 70, 68, 59, 65, 66, 82, 81, 91, 84, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 68, 59, 65, 66, 82, 81, 91, 83, 84, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 59, 65, 66, 81, 91, 84, 86, 85, 90 ],
        [ 58, 57, 69, 70, 80, 68, 59, 65, 66, 82, 81, 91, 83, 84, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 59, 65, 66, 82, 81, 91, 84, 86, 85, 89, 90 ],
        [ 58, 57, 69, 70, 80, 68, 59, 65, 66, 91, 83, 84, 64, 86, 85, 89, 90 ]]
    
    minutetick = [[0],
        [0],
        [19],
        [19],
        [20],
        [20],
        [47],
        [47],
        [48],
        [48],
        [75],
        [75],
        [76],
        [76],
        [95],
        [95],
        [94],
        [94],
        [92],
        [92],
        [90],
        [90],
        [88],
        [88],
        [86],
        [86],
        [63],
        [63],
        [62],
        [62],
        [33],
        [33],
        [32],
        [32],
        [9],
        [9],
        [8],
        [8],
        [7],
        [7],
        [5],
        [5],
        [3],
        [3],
        [1],
        [1]]
        
    hourtick = [2,18,21,46,49,74,77,93,91,89,85, 64,61,34,31,10,6,4,4]
    #rainbow_comet = RainbowComet(pixels, speed=1, tail_length=80, bounce=True)
    #rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=70)
    #sparkle_pulse = SparklePulse(pixels, speed=0.1, period=3, color=AMBER)
    #sparkle = Sparkle(pixels, speed=0.01, color=AMBER, num_sparkles=80)

    #animations1 = AnimationSequence(
    #    sparkle,
    #    auto_clear=True,
    #)

pixels_inner.fill(0)
time.sleep(1)
for cnt in range(1,96):
    pixels_inner.fill(rainbowio.colorwheel(supervisor.ticks_ms() // 4))
        
###        pixels[cnt] = (255,255,255)
###        pixels[cnt-1] = (0,0,0)
    time.sleep(0.05)
pixels_inner.fill(0)

    #sparkle_pulse.animate()
if False:
    maxbrightnessbackground= 0.05 #
    for hour in range(12):
        #sparkle = Sparkle(pixels, speed=0.01, color=(255,hour*10,0), num_sparkles=80)
            
        for miniute in range(60):
            if not(pixels_inner.brightness == minbright):
                #pixels.auto_write=False
                pixels_inner.fill(rainbowio.colorwheel(supervisor.ticks_ms() // 4))
                for cntb in range(NUM_PIXELS):
                    r = round(pixels[cntb][0]* maxbrightnessbackground,0)
                    g = round(pixels[cntb][1]* maxbrightnessbackground,0)
                    b = round(pixels[cntb][2]* maxbrightnessbackground,0)
                    pixels_inner[cntb]=(r,g,b)
                pixels_inner.auto_write=True    
            else:
                pixels_inner.fill(0)
            #sparkle.draw()
            #pixels.fill(AMBER)
            #animations1.animate()
            #time.sleep(0.01)
            mycolor =(0,255,0)
            mycolor=(255,255,255)
            for cnt1 in hourarray[hour] :
                pixels_inner[cnt1]=mycolor
            for cnt2 in minarray[miniute]:
                pixels_inner[cnt2]=mycolor
            
            if not(pixels_inner.brightness == minbright):
                pixels_inner[hourtick[int(round(hour*1.6,0))]]=(5,5,5)
                pixels_inner[minutetick[int(round(miniute*3/4,0))][0]]=(0,0,0)
            
            time.sleep(1)
        #time.sleep(.5)
    pixels_inner.fill(0)

def c1_drawBMP():
    print('not implemented')

def c2_drawCircle(x,y,radius,color):
    print('not implemented')
    ###global pixel_framebuf
    ###pixel_framebuf.circle(x,y,radius,int(color,16))
    #uint16_t x0_coordinate = int(payload[1] << 8) + int(payload[2]);
    #uint16_t y0_coordinate = int(payload[3] << 8) + int(payload[4]);
    #uint16_t radius = payload[5];
    #matrix->drawCircle(x0_coordinate, y0_coordinate, radius, matrix->Color(payload[6], payload[7], payload[8]));

def c3_drawCircleFill(x,y,radius,color):
    print('not implemented')
    ###global pixel_framebuf
    ###pixel_framebuf.circle(x,y,radius,int(color,16))
    ###for cnt in range(radius):
    ###    pixel_framebuf.circle(x,y,cnt,int(color,16))

def c4_drawPixel(cntb,r,g,b):
    global pixels_inner
    pixels_inner[cntb]=(r,g,b)
    #global pixel_framebuf
    #pixel_framebuf.pixel(x,y,int(color,16))
    #//Prepare the coordinates
    #uint16_t x0_coordinate = int(payload[1] << 8) + int(payload[2]);
    #uint16_t y0_coordinate = int(payload[3] << 8) + int(payload[4]);
    #matrix->drawPixel(x0_coordinate, y0_coordinate, matrix->Color(payload[5], payload[6], payload[7]));
		
def c5_drawRect(x,y,w,h,color):
    print('not implemented')
    ###global pixel_framebuf
    ###pixel_framebuf.rect(x,y,w,h,int(color,16))
    #uint16_t x0_coordinate = int(payload[1] << 8) + int(payload[2]);
    #uint16_t y0_coordinate = int(payload[3] << 8) + int(payload[4]);
    #int16_t width = payload[5];
    #int16_t height = payload[6];
    #matrix->drawRect(x0_coordinate, y0_coordinate, width, height, matrix->Color(payload[7], payload[8], payload[9]));

def c6_drawLine(x0,y0,x1,y1,color):
    print('not implemented')
    ###global pixel_framebuf
    ###pixel_framebuf.line(x0,y0,x1,y1,int(color,16))
    #uint16_t x0_coordinate = int(payload[1] << 8) + int(payload[2]);
    #uint16_t y0_coordinate = int(payload[3] << 8) + int(payload[4]);
    #uint16_t x1_coordinate = int(payload[5] << 8) + int(payload[6]);
    #uint16_t y1_coordinate = int(payload[7] << 8) + int(payload[8]);
    #matrix->drawLine(x0_coordinate, y0_coordinate, x1_coordinate, y1_coordinate, matrix->Color(payload[9], payload[10], payload[11]));	
    
def c7_drawScreen(r,g,b):
    global pixels_inner
    pixels_inner.fill((r,g,b))
    ###global pixel_framebuf
    ###pixel_framebuf.fill(int(color,16))
    
def c8_drawDisplay():
    print('not implemented - permanent write is true')
    #global pixel_framebuf
    #pixel_framebuf.display()
    
def c9_drawClear():
    global pixels_inner
    pixels_inner.fill(0)
    ###global pixel_f
    ###global pixel_framebuf
    ###pixel_framebuf.fill(0x000000)
    
def c13_drawBrightness(value):
    global pixels_inner
    pixels_inner.brightess(value)
    ###global pixels
    ###pixels.brightness=value
   
def c0_drawText(x,y,mytext,color):
    print('not implemented')
    ###global pixel_framebuf
    ####pixel_framebuf.text(mytext,x,y,int(color,16))

def c20_drawText(x,y,mytext,color):
    print('not implemented')
    ###global pixel_framebuf
    ###pixel_framebuf.text(mytext,x,y,int(color,16))
    
def c_30_updateInnerTime():
    global mytime
    global pixels_inner
    global NUM_PIXELS_inner
    maxbrightnessbackground= 0.05 #
    h=mytime.tm_hour
    m=mytime.tm_min
    #mytime.tm_sec
    if not(pixels_inner.brightness == minbright):
                #pixels.auto_write=False
        pixels_inner.fill(rainbowio.colorwheel(supervisor.ticks_ms() // 4))
        for cntb in range(NUM_PIXELS_inner):
            r = round(pixels_inner[cntb][0]* maxbrightnessbackground,0)
            g = round(pixels_inner[cntb][1]* maxbrightnessbackground,0)
            b = round(pixels_inner[cntb][2]* maxbrightnessbackground,0)
            pixels_inner[cntb]=(r,g,b)
            #pixels_inner.auto_write=True    
    else:
        pixels_inner.fill(0)
    #sparkle.draw()

    #mycolor =(0,255,0)
    mycolor=(255,255,255)
    for cnt1 in hourarray[hour] :
        pixels_inner[cnt1]=mycolor
    for cnt2 in minarray[miniute]:
        pixels_inner[cnt2]=mycolor
    
    #
    #        if not(pixels_inner.brightness == minbright):
    #            pixels_inner[hourtick[int(round(hour*1.6,0))]]=(5,5,5)
    #            pixels_inner[minutetick[int(round(miniute*3/4,0))][0]]=(0,0,0)
     #       
    #        time.sleep(1)
# ------------------------------


            
#--------------------------------


def update_icon(x0,y0,nr):
    print('not implemented, use transformer?')
    #global pixel_framebuf
    #onebmp = RGB_bmp[nr]
    #for x in range(8):
    #   for y in range(8):
    #       pixel_framebuf.pixel(x0+x,y0+y,onebmp[x*8+y])

#for cnticon in range(len(RGB_bmp)):
#    pixel_framebuf.fill(0x000000)
#    update_icon(cnticon)
#    time.sleep(1)
#    pixel_framebuf.display()      

# ----------------------------
# re-define messages
def rgb_to_hex(rgb):
    return '0x%02x%02x%02x' % rgb


def message(client, topic, message):
    global w
    global use_watchdog
    if use_watchdog == True:
        w.feed()
    # This method is called when a topic the client is subscribed to
    # has a new message.
    command=struct.unpack('B',message[0])[0]
    print(command)

###w.deinit()
 
    if command == 0:
        print('Do: 0, draw text, not implemented')
        (command_show_text,x,timeoffset_x,y,timeoffset_y,red_value,green_value,blue_value,timebyte) = struct.unpack('bbbbbBBB5s',message)
        newx = int(x << 8) + int(timeoffset_x)
        newy = int(y << 8) + int(timeoffset_y)       
        color = rgb_to_hex((red_value, green_value, blue_value))
        mytext=timebyte.decode()
        #print(newx, newy, color,mytext)
        c0_drawText(newx,newy,mytext,color)
    if command == 1:
        print('NA 1, draw bitmap, not implemented')
    if command == 2:
        print('Do: 2, draw circle, not implemented')
        (command_show_text,x,timeoffset_x,y,timeoffset_y,radius, red_value,green_value,blue_value) = struct.unpack('bbbbbBBBB',message)
        newx = int(x << 8) + int(timeoffset_x)
        newy = int(y << 8) + int(timeoffset_y)
        color = rgb_to_hex((red_value, green_value, blue_value))
        mradius=int(radius)
        #print(newx,newy,mradius,color)
        c2_drawCircle(newx,newy,mradius,color)    
    if command == 3:
        print('Do: 3, draw fill circle, not implemented')
        (command_show_text,x,timeoffset_x,y,timeoffset_y,radius, red_value,green_value,blue_value) = struct.unpack('bbbbbBBBB',message)
        newx = int(x << 8) + int(timeoffset_x)
        newy = int(y << 8) + int(timeoffset_y)
        color = rgb_to_hex((red_value, green_value, blue_value))
        mradius=int(radius)
        #print(newx,newy,mradius,color)
        c3_drawCircleFill(newx,newy,mradius,color) 
    if command == 4:
        print('Do: 4, draw pixel')
        (command_show_text,x,timeoffset_x,y,timeoffset_y, red_value,green_value,blue_value) = struct.unpack('bbbbbBBB',message)
        newx = int(x << 8) + int(timeoffset_x)
        newy = int(y << 8) + int(timeoffset_y)
        color = rgb_to_hex((red_value, green_value, blue_value))
        #print(newx,newy,color)
        ###c4_drawPixel(newx,newy,color)
        c4_drawPixel(newx, red_value, green_value, blue_value)
    if command == 5:
        print('Do: 5, draw Rect, not implemented')
        (command_show_text,x,timeoffset_x,y,timeoffset_y, width, height,red_value,green_value,blue_value) = struct.unpack('bbbbbBBBBB',message)
        newx = int(x << 8) + int(timeoffset_x)
        newy = int(y << 8) + int(timeoffset_y)
        w=int(width)
        h=int(height)
        color = rgb_to_hex((red_value, green_value, blue_value))
        #print(newx,newy,w,h,color)
        c5_drawRect(newx,newy,w,h,color)
    if command == 6:
        print('Do: 6, draw line, not implemented')
        (command_show_text,x,timeoffset_x,y,timeoffset_y,x0,timeoffset_x0,y0,timeoffset_y0,red_value,green_value,blue_value) = struct.unpack('bbbbbbbbbBBB',message)
        newx = int(x << 8) + int(timeoffset_x)
        newy = int(y << 8) + int(timeoffset_y)
        newx0 = int(x0 << 8) + int(timeoffset_x0)
        newy0 = int(y0 << 8) + int(timeoffset_y0)  
        color = rgb_to_hex((red_value, green_value, blue_value))
        #print(newx,newy,newx0,newy0,color)
        c6_drawLine(newx,newy,newx0,newy0,color)
    if command == 7:
        print('Do: 7, draw screen fill complete')
        command_show_fill,red_fill,green_fill,blue_fill = struct.unpack('bBBB',message)
        color = rgb_to_hex((red_fill, green_fill, blue_fill))
        #print(color)
        c7_drawScreen(red_fill,green_fill,blue_fill) 
    if command == 8:
        print('Do: 8, draw Display framebuffer, not implemented')
        c8_drawDisplay()
    if command == 9:
        print('Do: 9, draw Clear all')
        c9_drawClear()    
    if command == 10:
        print('10, play song')
        (command_playmp3,playtrack,playvolume)=struct.unpack('bbB',message)
        #print(type(playtrack))
        #print(type(playvolume))
        #print(type(command_playmp3))
        #print(playtrack, playvolume)
        ##print('Track: %d'% playtrack) 
        ##print('Vol: %d'% playvolume) 
        #mp3track = int(playtrack)
        #mp3vol = int(playvolume)
        song_play(playtrack, playvolume)
        
    if command == 11:
        print('NA 11, ECU Reset')
        microcontroller.reset()
    if command == 12:
        print('NA 12, Get Info, not implemented')
    if command == 13:
        print('Do: 13, draw Matrix brightness')
        command_change_brihtness,controllux=struct.unpack('bB',message)
        value=int(controllux)
        #print(value)
        c13_drawBrightness(value/255)
    if command == 14:
        print('NA 14, Save config, not implemented')                
    if command == 15:
        print('NA 15, Reset WiFi, not implemented')
    if command == 16:
        print('NA 16, Ping server, not implemented')                
    if command == 17:
        print('Do 17, 7Seg Display Update')
        (command_change_alarmtime,brightness,blinkrate,ascii1,ascii2,ascii3,ascii4,asciicolon) = struct.unpack('bBbbbbbb',message)
        display7seg_brightness(int(brightness))
        display7seg_blink(int(blinkrate))
        mycol=int(asciicolon)
        #print(type(ascii1))
        mystring=""
        if not(ascii1 == 23):
            if mycol==0:
                mystring=chr(ascii1) + chr(ascii2)  + chr(ascii3)  + chr(ascii4)
            else:
                 mystring=chr(ascii1) + chr(ascii2)  + ":" + chr(ascii3)  + chr(ascii4)
        print(mystring)
        display7seg_string(mystring)
    if command == 18:
        print('Do: 18, draw weather icon, not implemented, use OLED instead?')
        (command_showicon,timeoffset_x,iconx,timeoffset_y,icony,myicon) = struct.unpack('bbbBBb',message)
        newx = int(timeoffset_x << 8) + int(iconx)
        newy = int(timeoffset_y << 8) + int(icony)
        nr=int(myicon)
        #print(newx,newy,nr)
        update_icon(newx,newy,nr)
    if command == 19:
        print('NA, 19, na, not implemented')
    if command == 20:
        print('NA, 20, Draw text with different fonts, not implemented')                
    if command == 21:
        print('NA, 21, na, not implemented')#
    if command == 22:
        print('22, FLickercounter??? Matrix flicker - TBD')
    if command == 23:
        print('23, Sound enable amp')
        song_stop()
    if command == 24:
        print('24, Sound disable amp')
        song_stop()
    if command == 30:
        print('30, show clock')
        c_30_updateInnerTime()
    if command == 31:
        #(command_showicon,timeoffset_x,iconx,timeoffset_y,icony,myicon) = struct.unpack('bbbBBb',message)
        #newx = int(timeoffset_x << 8) + int(iconx)
        #newy = int(timeoffset_y << 8) + int(icony)
        #nr=int(myicon)
        hour=2
        minu=3
        year=2022
        month=10
        day=4
        c_31_writeRTCtime(hour,minu,year,month,day)

# -------------------------------- INIT
# Clear display 
pixels_inner.fill(0)
text_area.text = " "

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
print("Connecting to MQTT...")
mqtt_client.connect()

mytick=0
perform_main_loop = True
while perform_main_loop == True:
    if use_watchdog == True:
        w.feed()
        
    mytick=mytick+1
    if mytick > 60:
        mytick=mytime.tm_sec
    elif mytick == 0:
        c_30_updateInnerTime()
    #- Module 1
    # Poll the message queue
    try:
        mqtt_client.loop()
    except Exception as err:
        print('mqtt schrott: %s' % str(err))

    if use_gesture == True:
        gesture = sensor.gesture()

        if gesture == 0x01:
            print("up")
        elif gesture == 0x02:
            print("down")
        elif gesture == 0x03:
            print("left")
        elif gesture == 0x04:
            print("right")

    ##- Module 5
    ## Get raw (luminosity) readings individually
    #broadband = tsl.broadband
    #infrared = tsl.infrared
    ## Get computed lux value (tsl.lux can return None or a float)
    #lux = tsl.lux
    ## Print results
    #print("Enabled = {}".format(tsl.enabled))
    #print("Gain = {}".format(tsl.gain))
    #print("Integration time = {}".format(tsl.integration_time))
    #print("Broadband = {}".format(broadband))
    #print("Infrared = {}".format(infrared))
    #if lux is not None:
    #    print("Lux = {}".format(lux))
    #else:
    #    print("Lux value is None. Possible sensor underrange or overrange.")
           

      
    # Send a new message
    # print("Sending photocell value: %d..." % photocell_val)
    # mqtt_client.publish(photocell_feed, photocell_val)
    # print("Sent!")
    # photocell_val += 1
    
    
    time.sleep(0.1)
    perform_main_loop = False
print("Done!")



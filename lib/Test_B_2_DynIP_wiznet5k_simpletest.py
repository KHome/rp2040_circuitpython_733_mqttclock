# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
import digitalio
import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

print("Wiznet5k WebClient Test")

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_URL = "http://api.coindesk.com/v1/bpi/currentprice/USD.json"

# For Adafruit Ethernet FeatherWing
cs = digitalio.DigitalInOut(board.GP13)
# For Particle Ethernet FeatherWing
# cs = digitalio.DigitalInOut(board.D5)

#spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#GP13 = yellow = CS (SCNn)
#GP12 = orange = MISO
#GP11 = lila = MOSI
#GP10 = green = SCLK
spi_bus = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)

# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs)

# Initialize a requests object with a socket and ethernet interface
requests.set_socket(socket, eth)

print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))
print(
    "IP lookup adafruit.com: %s" % eth.pretty_ip(eth.get_host_by_name("adafruit.com"))
)


# eth._debug = True
print("Fetching text from", TEXT_URL)
r = requests.get(TEXT_URL)
print("-" * 40)
print(r.text)
print("-" * 40)
r.close()

print()
print("Fetching json from", JSON_URL)
r = requests.get(JSON_URL)
print("-" * 40)
print(r.json())
print("-" * 40)
r.close()

print("Done!")

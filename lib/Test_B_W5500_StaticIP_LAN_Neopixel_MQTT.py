import board
import busio
import digitalio
import time
from adafruit_wiznet5k.adafruit_wiznet5k import *
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import neopixel
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from secrets import secrets


pixel_pin = board.GP22
num_pixels = 2

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

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)

# Setup a feed named 'color_feed' for publishing to a feed
color_feed = secrets["aio_username"] + "/feeds/color"
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

def message(client, topic, message):
    # This method is called when a topic the client is subscribed to
    # has a new message.
    print(message[1:3], message[3:5], message[5:])
    red = int("0x" + message[1:3])
    green = int("0x" + message[3:5])
    blue = int("0x" + message[5:])
    print(red)
    print(green)
    print(blue)
    pixels.fill((red,green,blue))
    pixels.show()
    print("New message on topic {0}: {1}".format(topic, message))

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
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
print("Connecting to MQTT...")
mqtt_client.connect()

photocell_val = 0
while True:
    # Poll the message queue
    mqtt_client.loop()
    # Send a new message
    # print("Sending photocell value: %d..." % photocell_val)
    # mqtt_client.publish(photocell_feed, photocell_val)
    # print("Sent!")
    # photocell_val += 1
    time.sleep(1)

print("Done!")
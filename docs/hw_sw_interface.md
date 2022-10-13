# Wiznet5k
cs = digitalio.DigitalInOut(board.GP13)
spi_bus = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
- GP13 (SPI CS)
- GP10 (SPI)
- GP11 (SPI MOSI)
- GP12 (SPI MISO)

# RTC DS32311
i2c = busio.I2C(board.GP21, board.GP20)
rtc = adafruit_ds3231.DS3231(i2c)
- GP20 (I2C)
- GP21 (I2C)

# Lux TSL2561
tsl = adafruit_tsl2561.TSL2561(i2c)
- Re-use I2C (GP21, GP20)

# Temperature, rH BME280
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
- Re-use I2C (GP21, GP20)

# Display 7 Segment , HT16K33
display = segments.Seg7x4(i2c)
- Re-use I2C (GP21, GP20)

# MP3 Amp, SD Card
spi=busio.SPI(clock=board.GP2,MOSI=board.GP3,MISO=board.GP4)
cs=board.GP5
- GP5 (SPI2 CS)
- GP2 (SPI2)
- GP3 (SPI2 MOSI)
- GP4 (SPI MISO)

# Neopixels
## Neopixel Clock in Hexagon
NEOPIXEL = board.GP22
- GP22 = Neopixel RGB (Pico RP2040, Statemachine Driven)

## Neopixel South Inner
pixel_pin_si = board.GP15
- GP15 = Neopixel RGBW

## Neopixel South Outer
pixel_pin_so = board.GP14
- GP14 = Neopixel RGBW

## Neopxiel East Top
pixel_pin_eo = board.GP18
- GP18 = Neopixel RGBW

## Neopixel East Outer
pixel =
- GP16 = Neopixel RGB

## Neopixel East Table
pixel_pin_et = board.GP19
- GP19 = Neopixel RGB

# NOT USED (Since not further SPI available)
   OLED SD1309
   i2c = busio.I2C(board.GP19, board.GP18) 
   led = digitalio.DigitalInOut(board.GP16)

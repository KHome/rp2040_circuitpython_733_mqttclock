# rp2040_circuitpython_733_mqttclock
Raspberry Pico with Circuitpython 7.3.3. as a Mulit-Sensor MQTT Neopixel Hex-Clock

HW used:
- Raspberry Pico W with µC: RP2040 & WLAN
- W5500: SPI Interface for LAN
- DS3231: I2C for Realtime Clock incl. Buffer-Battery
- ADPS9960: Gesture Sensor for Human-Machine-Interface (HMI)
- TSL2561: Light Sensor to control Display and Neopixel Brightness
- BME280: Pressure, Temperature, Humidity Sensor for room feedback
- HT16K33 7-Segment I2C: Display
- SDD1309, [2,42" OLED Yellow Display,](https://www.diymore.cc/collections/hot-sale/products/2-42-inch-12864-oled-display-module-iic-i2c-spi-serial-for-arduino-c51-stm32-green-white-blue-yellow) modified for I2C
- SD-Card Reader incl. SD-Card with MP3-files
- MAX98357: Audio-Amplifier with I2S Interface
- Small Loudspeaker connected to Audio-Amp.
- Neopixel WS2811 (RP2040 PIO driven)
- 5V Main Power Supply 

MD used:
- Thingiverse: [HexMatrix Slim](https://www.thingiverse.com/thing:4848896)

FIrmware used:
- Circuitpython 7.3.3

SW used:
- Asyncio control of main loop

SW controls class
- tbd (Ideo include everything which interacts between async-tasks
-        self.luxbrigtness = 0.0 # read value by sensor
 -       self.luxautomaticclock = False # switch if clock bright is auto
  -      self.luxautomaticmiddleneo = False # switch for middle neopixel
   -     self.neomode = 1 # 1= constant
    -    self.neocolor = (255,0,0,0)

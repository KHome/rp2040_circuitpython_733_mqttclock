"""
CircuitPython I2S MP3 playback example.
Plays a single MP3 once.
"""
import board
import audiomp3
import audiobusio

import busio
import sdcardio
import storage

import time

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
time.sleep(6)
audio.stop()
#print("Done playing!")




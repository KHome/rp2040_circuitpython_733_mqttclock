import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
import time

pixel_pin = board.GP15
pixel_width = 6
pixel_height = 6

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height,
    brightness=0.02,
    auto_write=False,
)

pixel_framebuf = PixelFramebuffer(
    pixels,
    6,
    6,
    reverse_x=False,
    alternating=False,
    rotation=2
)
#blue
pixel_framebuf.fill(0x0000FF)
pixel_framebuf.display()

time.sleep(0.3)
#green
pixel_framebuf.fill(0x00FF00)
pixel_framebuf.display()

time.sleep(0.3)
#red
pixel_framebuf.fill(0xFF0000)
pixel_framebuf.display()

time.sleep(0.3)
pixel_framebuf.fill(0x000000)
pixel_framebuf.display()

pixel_framebuf.pixel(4, 6, 0xFF0000)
pixel_framebuf.display()

time.sleep(1)
pixel_framebuf.fill(0x000000)
pixel_framebuf.display()

pixel_framebuf.line(0, 0, 7, 9, 0xFF0000)
pixel_framebuf.display()

time.sleep(1)
pixel_framebuf.fill(0x000000)
pixel_framebuf.display()

pixel_framebuf.hline(2, 3, 5, 0xFF0000)
pixel_framebuf.vline(2, 3, 5, 0xFF0000)
pixel_framebuf.display()


time.sleep(1)
#pixel_framebuf.fill(0x000000)
#pixel_framebuf.display()

pixel_framebuf.rect(2, 2, 8, 12, 0xFFFF00)
pixel_framebuf.display()

time.sleep(1)
pixel_framebuf.fill(0x000000)
pixel_framebuf.display()

pixel_framebuf.rect(2, 2, 8, 12, 0xFFFF00)
pixel_framebuf.display()

time.sleep(1)
pixel_framebuf.fill(0x000000)
pixel_framebuf.display()

pixel_framebuf.text("Hi", 0, 0, 0x00FF00)
pixel_framebuf.display()

time.sleep(1)
pixel_framebuf.fill(0x000000)
pixel_framebuf.display()


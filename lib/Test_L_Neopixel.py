# SPDX-FileCopyrightText: 2022 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Demonstrate background writing with NeoPixels

The NeoPixelBackground class defined here is largely compatible with the
standard NeoPixel class, except that the ``show()`` method returns immediately,
writing data to the LEDs in the background, and setting `auto_write` to true
causes the data to be continuously sent to the LEDs all the time.

Writing the LED data in the background will allow more time for your
Python code to run, so it may be possible to slightly increase the refresh
rate of your LEDs or do more complicated processing.

Because the pixelbuf storage is also being written out 'live', it is possible
(even with auto-show 'false') to experience tearing, where the LEDs are a
combination of old and new values at the same time.

The demonstration code, under ``if __name__ == '__main__':`` is intended
for the Adafruit MacroPad, with 12 NeoPixel LEDs. It shows a cycling rainbow
pattern across all the LEDs.
"""

import struct
import adafruit_pixelbuf
from rp2pio import StateMachine
from adafruit_pioasm import Program
#from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
#from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.color import AMBER

#from adafruit_led_animation.sequence import AnimationSequence

import time

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

minbright= 0.008

setbright= 0.01

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


if __name__ == "__main__":
    import board
    import rainbowio
    import supervisor

    NEOPIXEL = board.GP15 #NEOPIXEL
    NUM_PIXELS = 36
    pixels = NeoPixelBackground(NEOPIXEL, NUM_PIXELS)
   # while True:
   
   # Around 1 cycle per second
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

    pixels.fill(0)
    time.sleep(1)
    for cnt in range(1,96):
        pixels.fill(rainbowio.colorwheel(supervisor.ticks_ms() // 4))
        
        pixels[cnt] = (255,255,255)
        pixels[cnt-1] = (0,0,0)
        time.sleep(0.05)
    pixels.fill(0)
    #sparkle_pulse.animate()
    maxbrightnessbackground= 0.05 #
    for hour in range(12):
        #sparkle = Sparkle(pixels, speed=0.01, color=(255,hour*10,0), num_sparkles=80)
            
        for miniute in range(60):
            if not(pixels.brightness == minbright):
                #pixels.auto_write=False
                pixels.fill(rainbowio.colorwheel(supervisor.ticks_ms() // 4))
                for cntb in range(NUM_PIXELS):
                    r = round(pixels[cntb][0]* maxbrightnessbackground,0)
                    g = round(pixels[cntb][1]* maxbrightnessbackground,0)
                    b = round(pixels[cntb][2]* maxbrightnessbackground,0)
                    pixels[cntb]=(r,g,b)
                pixels.auto_write=True    
            else:
                pixels.fill(0)
            #sparkle.draw()
            #pixels.fill(AMBER)
            #animations1.animate()
            #time.sleep(0.01)
            mycolor =(0,255,0)
            mycolor=(255,255,255)
            for cnt1 in hourarray[hour] :
                pixels[cnt1]=mycolor
            for cnt2 in minarray[miniute]:
                pixels[cnt2]=mycolor
            
            if not(pixels.brightness == minbright):
                pixels[hourtick[int(round(hour*1.6,0))]]=(5,5,5)
                pixels[minutetick[int(round(miniute*3/4,0))][0]]=(0,0,0)
            
            time.sleep(1)
        #time.sleep(.5)
    pixels.fill(0)

        
    
            
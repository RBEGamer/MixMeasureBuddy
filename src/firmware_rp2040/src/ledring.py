import neopixel
import machine
import config
import neopixel
import random
import helper
import math
from singleton import singleton

@singleton
class ledring:
    @staticmethod
    def hsv_to_rgb(self, hsv_color):
        # https://github.com/Warringer/micropython-rgbled/blob/master/rgbled.py
        (h, s, v) = hsv_color
        i = math.floor(h*6)
        f = h*6 - i
        p = v * (1-s)
        q = v * (1-f*s)
        t = v * (1-(1-f)*s)

        r, g, b = [
            (v, t, p),
            (q, v, p),
            (p, v, t),
            (p, q, v),
            (t, p, v),
            (v, p, q),
        ][int(i%6)]
        r = int(255 * r)
        g = int(255 * g)
        b = int(255 * b)
        return r, g, b


    neopixelring: neopixel.NeoPixel = None
   
    def __init__(self):
        self.neopixelring = neopixel.NeoPixel(machine.Pin(config.CFG_NEOPIXEL_PIN), config.CFG_NEOPIXEL_LED_COUNT)
   
    def clear(self):
        self.set_neopixel_full(0, 0, 0)


    def set_neopixel_percentage(self, _percentage: float, _start_color: float = 0.0, _target_color: float = 1.0, _off_color: tuple[int, int ,int] = (0, 0, 10)):
        _percentage = min(_percentage, 1.0)
        
        disp_value: int = int(min([helper.imap(_percentage * 100, 0, 100, 0 , config.CFG_NEOPIXEL_LED_COUNT), config.CFG_NEOPIXEL_LED_COUNT]))
        print(disp_value)
        
        for i in range(config.CFG_NEOPIXEL_LED_COUNT):
            color_value = helper.fmap(i, 0, config.CFG_NEOPIXEL_LED_COUNT, _start_color , _target_color)
        #    # APPLY START INDEX OFFSET
            led_index = int((i+config.CFG_NEOPIXEL_LED_START_OFFSET) % config.CFG_NEOPIXEL_LED_COUNT)
        #    # ABOVE TARGET PERCENTAGE SET OFF OR ON LOW COLOR
            if i > disp_value:
                self.neopixelring[led_index] = _off_color
                continue
            
            rgb = ledring.hsv_to_rgb([color_value, 255, 255])
            self.neopixelring[led_index] = (rgb[0], rgb[1], rgb[2])
          
        self.neopixelring.write()


    def set_neopixel_full(self, _r: int, _g: int, _b: int):
        for i in range(config.CFG_NEOPIXEL_LED_COUNT):
            self.neopixelring[i] = (min(_r, 255), min(_g, 255), min(_b, 255))
        self.neopixelring.write()

    def set_neopixel_random(self, _er: bool = False, _eg: bool = False, _eb: bool = True):
        r: int = int(128* random.random()) * _er
        g: int = int(128* random.random()) * _eg
        b: int = int(128* random.random()) * _eb
        self.set_neopixel_full(r, g, b)


    def set_neopixel_full_hsv(self, _h: float):
        rgb = ledring.hsv_to_rgb([min(_h, 1.0), 255, 255])
        self.set_neopixel_full(rgb[0], rgb[1], rgb[2])


if __name__ == "__main__":
    ledring().clear()
    ledring().set_neopixel_percentage(0.5)
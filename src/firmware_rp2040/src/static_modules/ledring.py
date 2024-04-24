import neopixel
import machine
import config
import neopixel
import random
import helper
import math
import time
from singleton import singleton

@singleton
class ledring:

    COLOR_PRESET_HSV_H__BLUE: float = 0.66
    COLOR_PRESET_HSV_H__PINK: float = 0.88
    COLOR_PRESET_HSV_H__GREEN: float = 0.36
    COLOR_PRESET_HSV_H__BLACK: float = -1.0

    def hsv_to_rgb(self, hsv_color):
        # https://github.com/Warringer/micropython-rgbled/blob/master/rgbled.py
        (h, s, v) = hsv_color

        if h < 0.0:
            return 0, 0, 0
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

    def rgb_to_hsv(self, rgb_color):
        (r, g, b) = rgb_color
        r = float(1 / 255 * r)
        g = float(1 / 255 * g)
        b = float(1 / 255 * b)
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, v = high, high, high

        d = high - low
        s = 0 if high == 0 else d/high

        if high == low:
            h = 0.0
        else:
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6

        return h, s, v

    neopixelring: neopixel.NeoPixel = None
   
    def __init__(self):
        self.neopixelring = neopixel.NeoPixel(machine.Pin(config.CFG_NEOPIXEL_PIN), config.CFG_NEOPIXEL_LED_COUNT)
   
    def clear(self):
        self.set_neopixel_full(
            0, 0, 0)


    def set_neopixel_spinner(self, _current_segment: int, _no_segment: int, _on_color: float = 0.0, _off_color: float = 0.6):
        if _current_segment < 0:
            _current_segment = 0
        
        if _no_segment <= 0:
            _no_segment = config.CFG_NEOPIXEL_LED_COUNT / 6
            
        
        leds_per_segment: int = config.CFG_NEOPIXEL_LED_COUNT / _no_segment
        
        on_color = self.hsv_to_rgb([_on_color, config.CFG_NEOPIXEL_MAX_BRIGHTNESS, config.CFG_NEOPIXEL_MAX_BRIGHTNESS])
        off_color = self.hsv_to_rgb([_off_color, config.CFG_NEOPIXEL_MAX_BRIGHTNESS, config.CFG_NEOPIXEL_MAX_BRIGHTNESS])

        for i in range(config.CFG_NEOPIXEL_LED_COUNT):
            
            if i > _current_segment*leds_per_segment and i < (_current_segment+1)*leds_per_segment:
                self.neopixelring[i] = (on_color[0], on_color[1], on_color[2])
            else:
                self.neopixelring[i] = (off_color[0], off_color[1], off_color[2])
            
        self.neopixelring.write()



    def set_neopixel_percentage(self, _percentage: float, _start_color: float = 0.0, _target_color: float = 0.4, _off_color: float = 0.6, _independent_coloring: bool = False):
        _percentage = min(_percentage, 1.0)
        
        disp_value: int = int(min([helper.imap(_percentage * 100, 0, 100, 0 , config.CFG_NEOPIXEL_LED_COUNT), config.CFG_NEOPIXEL_LED_COUNT]))
        #print(disp_value)
        

        color_value: float = helper.fmap(disp_value, 0, config.CFG_NEOPIXEL_LED_COUNT, _start_color , _target_color)
        
        off_color = self.hsv_to_rgb([_off_color, config.CFG_NEOPIXEL_MAX_BRIGHTNESS, config.CFG_NEOPIXEL_MAX_BRIGHTNESS])
            
        
        for i in range(config.CFG_NEOPIXEL_LED_COUNT):
            
            if _independent_coloring:
                color_value = helper.fmap(i, 0, config.CFG_NEOPIXEL_LED_COUNT, _start_color , _target_color)
        #    # APPLY START INDEX OFFSET
            led_index = int((i+config.CFG_NEOPIXEL_LED_START_OFFSET) % config.CFG_NEOPIXEL_LED_COUNT)
        #    # ABOVE TARGET PERCENTAGE SET OFF OR ON LOW COLOR
            if i > disp_value:
                self.neopixelring[led_index] = (off_color[0], off_color[1], off_color[2])
                continue
            
            rgb = self.hsv_to_rgb([color_value, 1.0, config.CFG_NEOPIXEL_MAX_BRIGHTNESS])
            self.neopixelring[led_index] = (rgb[0], rgb[1], rgb[2])
        
        
        self.neopixelring.write()


    def set_neopixel_full_hsv(self, _hsv_color: float = 0.0):
        self.set_neopixel_percentage(1.0, _hsv_color, _hsv_color, _hsv_color)

    def set_neopixel_random(self, _er: bool = False, _eg: bool = False, _eb: bool = True):
        r: int = int(128* random.random()) * _er
        g: int = int(128* random.random()) * _eg
        b: int = int(128* random.random()) * _eb
        self.set_neopixel_full(r, g, b)


    def set_neopixel_full(self, _r: int, _g: int, _b: int):
        h, _, _ = self.rgb_to_hsv([_r, _g, _b])
        self.set_neopixel_full_hsv(h)

if __name__ == "__main__":
    while True:
        segments: int = config.CFG_NEOPIXEL_LED_COUNT / 5
        for i in range(segments):
            ledring().set_neopixel_spinner(i, segments, ledring().COLOR_PRESET_HSV_H__BLUE, ledring().COLOR_PRESET_HSV_H__PINK)
            time.sleep(0.1)



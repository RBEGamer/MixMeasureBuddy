import neopixel
import machine
import config
import neopixel
import random
from singleton import singleton

@singleton
class ledring:


    neopixelring: neopixel.NeoPixel = None
   
    def __init__(self):
        self.neopixelring = neopixel.NeoPixel(machine.Pin(config.CFG_NEOPIXEL_PIN), config.CFG_NEOPIXEL_LED_COUNT)
   
    def clear(self):
        self.set_neopixel_full(0, 0, 0)

    def set_neopixel_full(self, _r: int, _g: int, _b: int):
        for i in range(config.CFG_NEOPIXEL_LED_COUNT):
            self.neopixelring[i] = (_r, _g, _b)
        self.neopixelring.write()

    def set_neopixel_random(self, _er: bool = False, _eg: bool = False, _eb: bool = True):
        r: int = int(128* random.random()) * _er
        g: int = int(128* random.random()) * _eg
        b: int = int(128* random.random()) * _eb
        self.set_neopixel_full(r, g, b)
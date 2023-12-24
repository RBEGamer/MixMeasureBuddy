import time
import ubinascii
import machine
import config
import neopixel
import random
import sys

def millis():
    return round(time.time() * 1000)

def fmap(s, a1, a2, b1, b2) -> float:
    return b1 + (s - a1) * (b2 - b1) / (a2 - a1)

def imap(s, a1, a2, b1, b2) -> int:
    return b1 + (s - a1) * (b2 - b1) / (a2 - a1)

def get_system_id():
    return ubinascii.hexlify(machine.unique_id()).decode('utf-8')

def set_neopixel_full(_neopixelring, _r, _g, _b):
    for i in range(config.CFG_NEOPIXEL_LED_COUNT):
        _neopixelring[i] = (_r, _g, _b)
    _neopixelring.write()

def set_neopixel_random(_neopixelring, _er: bool = False, _eg: bool = False, _eb: bool = True):
    r: int = int(128* random.random()) * _er
    g: int = int(128* random.random()) * _eg
    b: int = int(128* random.random()) * _eb
    set_neopixel_full(_neopixelring, r, g, b)

def has_wifi():
    if 'Raspberry Pi Pico W' in str(sys.implementation):
        return True
    return False

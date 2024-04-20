import time
import ubinascii
import machine
import sys

def millis():
    return round(time.time() * 1000)

def fmap(s, a1, a2, b1, b2) -> float:
    return b1 + (s - a1) * (b2 - b1) / (a2 - a1)

def imap(s, a1, a2, b1, b2) -> int:
    return b1 + (s - a1) * (b2 - b1) / (a2 - a1)

def get_system_id():
    return ubinascii.hexlify(machine.unique_id()).decode('utf-8')

def has_wifi():
    if 'Raspberry Pi Pico W' in str(sys.implementation):
        return True
    return False

from utime import sleep_us
import uasyncio as aio
from aiobutton import AIOButton


import machine
import time
import math

import random
import helper
#import Scales
import config
import recipe_loader
import ui
import settings
import menu_manager
import menu_entry
import ledring
import system_command
print("main: __entry__")



BUTTON_INDEX_LEFT = 0
BUTTON_INDEX_RIGHT = 1

BUTTON_PRESSED = 0
BUTTON_HOLD = 1
BUTTON_RELEASED = 2

last_left_button_state: int = 0
button_state_dict: list = [-1, -1]



# GENERATED SYSTEM EVENTS DEPENING ON THE PRESSED BUTTON TO NAVIGATE THOUGHT MENUS
def generate_button_state(_button_index: int, _button_event: int, _button_state: bool):
    #print("Button {} type {} state {}".format(_button_index,_button_event,_button_state))
    
    if button_state_dict[_button_index] == BUTTON_PRESSED and _button_event == BUTTON_RELEASED:
        #print("short press")
        cmd: system_command.system_command = system_command.system_command()
        if _button_index == BUTTON_INDEX_LEFT:
            cmd.action = system_command.system_command.NAVIGATION_LEFT
        elif _button_index == BUTTON_INDEX_RIGHT:
            cmd.action = system_command.system_command.NAVIGATION_RIGHT
        cmd.type = system_command.system_command.COMMAND_TYPE_NAVIGATION
        menu_manager.menu_manager().process_user_commands(cmd)

    elif _button_event == BUTTON_HOLD:
        #print("short press")
        cmd: system_command.system_command = system_command.system_command()
        if _button_index == BUTTON_INDEX_LEFT:
            cmd.action = system_command.system_command.NAVIGATION_EXIT
        elif _button_index == BUTTON_INDEX_RIGHT:
            cmd.action = system_command.system_command.NAVIGATION_ENTER
        cmd.type = system_command.system_command.COMMAND_TYPE_NAVIGATION
        menu_manager.menu_manager().process_user_commands(cmd)
    
    button_state_dict[_button_index] = _button_event
   
   
   
if __name__ == "__main__":
    
    # INIT RECIPE LOADER AND INIT SD CARD
    settings.settings().list_files()
    # RECIPE STORAGE
    recipe = recipe_loader.recipe_loader()
    # INIT LED RING
    ledring.ledring().set_neopixel_full(10, 10, 10)
    
    

    # INIT USER INPUT BUTTONS
    left_button_pin: machine.Pin = machine.Pin(config.CFG_BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    left_button = AIOButton(lambda btn: not left_button_pin.value())
    # Register button event handlers
    left_button.set_hold_handler(lambda btn: generate_button_state(BUTTON_INDEX_LEFT, BUTTON_HOLD, btn.get_debounced()))   
    left_button.set_press_handler(lambda btn: generate_button_state(BUTTON_INDEX_LEFT, BUTTON_PRESSED, btn.get_debounced()))
    left_button.set_release_handler(lambda btn: generate_button_state(BUTTON_INDEX_LEFT, BUTTON_RELEASED, btn.get_debounced())) 
    
    right_button_pin: machine.Pin = machine.Pin(config.CFG_BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    right_button = AIOButton(lambda btn: not right_button_pin.value())
    # Register button event handlers
    right_button.set_hold_handler(lambda btn: generate_button_state(BUTTON_INDEX_RIGHT, BUTTON_HOLD, btn.get_debounced()))   
    right_button.set_press_handler(lambda btn: generate_button_state(BUTTON_INDEX_RIGHT, BUTTON_PRESSED, btn.get_debounced()))
    right_button.set_release_handler(lambda btn: generate_button_state(BUTTON_INDEX_RIGHT, BUTTON_RELEASED, btn.get_debounced())) 
    



    
    
    
   







    # INIT DISPLAY / UI INSTANCE
    #ui.ui.instance().show_titlescreen()
    #time.sleep(2)

    # INIT MENU SYSTEM
    a = menu_entry.menu_entry("a" , "aaa")
    b = menu_entry.menu_entry("b" , "aaa")
    c = menu_entry.menu_entry("c" , "aaa")

    menu_manager.menu_manager().add_subentries(a)
    menu_manager.menu_manager().add_subentries(b)
    menu_manager.menu_manager().add_subentries(c)


    # INIT SCALE
    #scales = Scales.Scales(d_out=config.CFG_HX711_DOUT_PIN, pd_sck=config.CFG_HX711_SCK_PIN)
    #scales.tare()
    # LOAD SCALE CALIBTATION VALUES
    #calibration_factor = settings_instance.get_scale_calibration_factor()
    #print("calibration_factor {}".format(calibration_factor))
    #scales.set_scale(calibration_factor)
    #scales.tare()
    
    
    #system_state = SYSTATE_IDLE #SYSTEMSTATE_ENTER_MAINMENU #SYSTEMSTATE_UPDATE_MODE
    #user_cmd: menu_manager.menu_command = menu_manager.menu_command()


    async def main_task():
        # CREATE TASKS FOR USER INPUT
        task_left = aio.create_task(left_button.coro_check())
        task_right = aio.create_task(right_button.coro_check())


        while True:
            await aio.sleep_ms(1)
    
    aio.run(main_task())

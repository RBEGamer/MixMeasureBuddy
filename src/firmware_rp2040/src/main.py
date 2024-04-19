from utime import sleep_us
import machine
import time
import math
import neopixel
import random
import helper
import Scales
import config
import recipe_loader
import ui
import settings
import menu_manager
import menu_entry
print("main: __entry__")


# SYSTEM STATES
SYSTATE_IDLE = 0
# MENU
SYSTEMSTATE_ENTER_MAINMENU = 1
SYSTEMSTATE_MAINMENU = 2

# MISC MODES
SYSTEMSTATE_SCALE_MODE = 3
SYSTEMSTATE_UPDATE_MODE = 4
SYSTEMSTATE_CALIBRATION_MODE_ENTRY = 5
SYSTEMSTATE_RAW_MODE = 6

SYSTEMSTATE_CALIBRATION_MODE_ZERO = 7
SYSTEMSTATE_CALIBRATION_MODE_FULL = 8
# SCALE ENABLED
SYSTATE_RECIPE_START = 10
SYSTATE_RECIPE_SHOW_INGREDIENTS = 11
SYSTATE_RECIPE_PLACEGLASS = 12
SYSTATE_RECIPE_RUNNING = 13
SYSTATE_RECIPE_FINISHED = 14

SYSTEMSTATE_UPDATE_MODE_QR_START = 20
SYSTEMSTATE_UPDATE_MODE_QR_RUNNING = 21

UB_NONE = 0
UB_RELEASE = 1
UB_UP = 2
UB_UPLONG = 3
UB_DOWN = 4


if __name__ == "__main__":
        
    system_state = SYSTATE_IDLE
    # INIT RECIPE LOADER AND INIT SD CARD
    settings_instance: settings.settings = settings.settings()
    recipe = recipe_loader.recipe_loader(settings_instance)
        
    # INIT NEOPIXEL RING
    neopixelring = neopixel.NeoPixel(machine.Pin(config.CFG_NEOPIXEL_PIN), config.CFG_NEOPIXEL_LED_COUNT)
    helper.set_neopixel_random(neopixelring)
    
    # INIT MENU SYSTEM
    menu: menu_manager.menu_manager = menu_manager.menu_manager()





    menu.add_subentries()




    # INIT DISPLAY7
    #gui = ui.ui()
    # INIT SCALE
    #scales = Scales.Scales(d_out=config.CFG_HX711_DOUT_PIN, pd_sck=config.CFG_HX711_SCK_PIN)
    #scales.tare()
    # LOAD SCALE CALIBTATION VALUES
    #calibration_factor = settings_instance.get_scale_calibration_factor()
    #print("calibration_factor {}".format(calibration_factor))
    #scales.set_scale(calibration_factor)
    #scales.tare()
    
    
    
    #system_state = SYSTATE_IDLE #SYSTEMSTATE_ENTER_MAINMENU #SYSTEMSTATE_UPDATE_MODE
    while True:
       pass 

       # RESOLVE POSSIBLE BUTTON PRESSES


       # READ SCALE

       # 
       
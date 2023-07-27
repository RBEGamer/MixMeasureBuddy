from utime import sleep_us
import machine
import time, math
import neopixel
import random
import sdcard
import uos
from utime import sleep_us


from helper import millis, fmap, imap
from Scales import Scales
import recipe_loader
import ui

print("main: __entry__")











def tare_drink(_scale, _iterations = 5):
    print("scale_tarebegin")
    tare_value = 0
    scale_value = 0
    for i in range(_iterations):
        scale_value = scales.stable_value()
        time.sleep(0.5)
        tare_value = tare_value + scale_value
    tare_value = tare_value / _iterations
    return tare_value





# SYSTEM STATES
SYSTATE_INIT = 0
SYSTATE_RECIPE_START = 1
SYSTATE_RECIPE_PLACEGLASS = 2
SYSTATE_RECIPE_RUNNING = 3
 
if __name__ == "__main__":
    
    
    
    system_state = SYSTATE_INIT
    # INIT RECIPE LOADER AND INIT SD CARD
    recipe = recipe_loader.recipe_loader()
        
    # INIT NEOPIXEL RING
    NEOPIXEL_COUNT = 60
    neopixelring = neopixel.NeoPixel(machine.Pin(3), NEOPIXEL_COUNT)
    for i in range(NEOPIXEL_COUNT):
        neopixelring[i] = (0, 0, int(128* random.random()))
    neopixelring.write()
    
    # INIT DISPLAY
    gui = ui.ui()
    gui.show_titlescreen()
    
    # INIT SCALE
    scales = Scales()
    scales.tare()
    tare_value = tare_drink(scales, 1)
    scale_value = 0
    
    # CALIBTATION VALUES
    map_value_0g = 1288
    maps_value_50g = 11400
    
          
          
    
    
    #pin_tare = machine.Pin(3, machine.Pin.IN)
    #pin_calibrate = machine.Pin(6, machine.Pin.IN)
    if recipe.load_recipe("Tequila_Sunrise"):
        print("loaded recipe: Tequila Sunrise")
        system_state = SYSTATE_RECIPE_START
        
        information = recipe.get_recipe_information()
        gui.show_recipe_information(information[0], information[1])
        last_systate_update = millis()
    else:
        print("recipe loading failed")
    
    
           
           
    target_value = 100
    scale_value_before_glass_added = 0
    
    
    
    
    
    last_display_update = millis()
    last_systate_update = millis()
    while True:
        
        
        # READ SCALE
        scale_value = scales.stable_value()
        scale_value_tared = scale_value - tare_value
        scale_value_g = fmap(scale_value_tared, map_value_0g, maps_value_50g, 0 , 50)
        
        
        
        
        
        
        if system_state == SYSTATE_RECIPE_START:
            if  abs(last_systate_update - millis()) > 1000:
                last_systate_update = millis()
                system_state = SYSTATE_RECIPE_PLACEGLASS
                scale_value_before_glass_added = scale_value_g
                
        elif system_state == SYSTATE_RECIPE_PLACEGLASS:
            gui.show_msg("PLACE GLASS")
            print(scale_value_g)
            if  abs(last_systate_update - millis()) > 7000 or scale_value_g > (scale_value_before_glass_added + 50):
                
                gui.show_msg("SYSTEM TARE")
                tare_value = tare_drink(scales, 1)
                
                system_state = SYSTATE_RECIPE_RUNNING
                last_systate_update = millis()
                
        elif system_state == SYSTATE_RECIPE_RUNNING:
            
            # UPDATE UI
            if  abs(last_display_update - millis()) > 1000:
                last_display_update = millis()
                gui.show_recipe_step("ADD", "TEQUILA", scale_value_g, target_value)
               
                
            # UPDATE NEOPIXEL
            disp_value = imap(scale_value_g, 0, target_value, 0 , NEOPIXEL_COUNT)
            for i in range(NEOPIXEL_COUNT):
                color_value = imap(i, 0, NEOPIXEL_COUNT, 0 , 1.0)
                
                if target_value < 0:
                    neopixelring[i] = (0, 0, 128)
                elif scale_value_g >= target_value:
                    neopixelring[i] = (0, 255, 0)
                elif i < disp_value:
                    #       R  G  B
                    neopixelring[i] = (int((1.0 - color_value) * 255), int(color_value*255), 0)
                else:
                    neopixelring[i] = (0, 0, 0)
            neopixelring.write()
        else:
            for i in range(NEOPIXEL_COUNT):
                neopixelring[i] = (0, 0, int(128* random.random()))
            neopixelring.write()
        
        
       
        time.sleep(0.2)



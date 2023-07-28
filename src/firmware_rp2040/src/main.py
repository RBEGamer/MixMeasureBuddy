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
SYSTATE_IDLE = 0

# SCALE ENABLED
SYSTATE_RECIPE_START = 1
SYSTATE_RECIPE_PLACEGLASS = 2
SYSTATE_RECIPE_RUNNING = 3
SYSTATE_RECIPE_FINISHED = 4


if __name__ == "__main__":
    
    
    
    system_state = SYSTATE_IDLE
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
    #gui.show_titlescreen()
    
    # INIT SCALE
    scales = Scales()
    scales.tare()
    tare_value = tare_drink(scales, 1)
    scale_value = 0
    
    # CALIBTATION VALUES
    map_value_0g = 1288
    maps_value_50g = 11400
    
    
    # CONFIGURE USER BUTTONS
    push_button_up = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)  # 23 number pin is input
    push_button_down = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)  # 23 number pin is input
    
    
    
    
    
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
    
    
    delay_value = None # FOR USER TIMER      
           
    target_value = None
    scale_offset = 0.0
    scale_value_before_glass_added = 0
    
    
    
    
    
    last_display_update = millis()
    last_systate_update = millis()
    last_recipe_step_update = millis()
    last_userbutton_update = None
    
    UB_NONE = 0
    UB_UP = 1
    UB_DOWN = 2
    last_button_pressed = None
    time_elapsed = 0
    load_next_step = False
        
    while True:
        
        
        # READ USER_BUTTONS
        if push_button_up.value() and not push_button_down.value() and last_userbutton_update is None:
            last_userbutton_update = millis()
            last_button_pressed = UB_UP
        
        elif push_button_up.value() and push_button_down.value():
            if last_userbutton_update is not None and abs(last_userbutton_update - millis()) > 1:
                last_userbutton_update = None
        
        # READ SCALE
        if system_state >= SYSTATE_RECIPE_START:
            scale_value = scales.raw_value() #stable_value()
            scale_value_tared = scale_value - tare_value
            scale_value_g = fmap(scale_value_tared, map_value_0g, maps_value_50g, 0 , 50)
        
            if scale_value_g <= 0.0:
                scale_offset = -scale_value_g
            scale_value_g =  scale_value_g + scale_offset
        
        
        
        
        
        if system_state == SYSTATE_RECIPE_START:
            if  abs(last_systate_update - millis()) > 1000:
                last_systate_update = millis()
                system_state = SYSTATE_RECIPE_PLACEGLASS
                scale_value_before_glass_added = scale_value_g
                
        elif system_state == SYSTATE_RECIPE_PLACEGLASS:
            gui.show_msg("PLACE GLASS")
            print(scale_value_g)
            if  abs(last_systate_update - millis()) > 7000 or scale_value_g > (scale_value_before_glass_added + 50):
                
                gui.show_msg("CALIBRATING")
                tare_value = tare_drink(scales, 1)
                
                system_state = SYSTATE_RECIPE_RUNNING
                last_systate_update = millis()
                last_recipe_step_update = millis()
        
        elif system_state == SYSTATE_RECIPE_FINISHED:
            for i in range(NEOPIXEL_COUNT):
                neopixelring[i] = (0, int(128* random.random()), 0)
            neopixelring.write()
            gui.show_msg("DRINK READY TO SERVE")
            
            if  abs(last_systate_update - millis()) > 1000:
                last_systate_update = millis()
                system_state = SYSTATE_IDLE
                
        elif system_state == SYSTATE_RECIPE_RUNNING:
            
            # GET RECIPE STEP
            rsr = recipe.get_current_recipe_step() # (action, ingredient, current_step, max_steps, target_weight, finished)
            user_move = rsr[0]
            action  = rsr[1]
            ingredient = rsr[2]
            current_step = rsr[3]
            max_steps = rsr[4]
            amount = rsr[5]
            finished = rsr[6]
            print(rsr)
            
            
            # UPDATE VARIABLES
            if user_move == recipe_loader.USER_INTERACTION_MODE.SCALE:
                target_value = amount
                delay_value = None
            elif user_move == recipe_loader.USER_INTERACTION_MODE.WAIT:
                delay_value = amount
                target_value = None
                time_elapsed = ((millis() - last_recipe_step_update))/1000
                print(time_elapsed)
            else:
                target_value = None
                delay_value = None
                
            # CHECK OK ACTION OK
            if finished:
                last_systate_update = millis()
                # GOTO MAIN MENU IF GLASS IS REMOVED
                if scale_value_g < scale_value_before_glass_added:
                    gui.show_msg("REMOVE GLASS")
                    system_state = SYSTATE_RECIPE_FINISHED
                    continue
            elif user_move == recipe_loader.USER_INTERACTION_MODE.SCALE and scale_value_g > target_value:
                load_next_step = True
            elif user_move == recipe_loader.USER_INTERACTION_MODE.WAIT and time_elapsed > delay_value:
                load_next_step = True
            elif user_move == recipe_loader.USER_INTERACTION_MODE.CONFIRM and last_button_pressed == UB_UP:
                load_next_step = True
            else:
                load_next_step = False
                
                
            if load_next_step:
                load_next_step = False
                recipe.switch_next_step()
                gui.set_full_refresh()
                last_recipe_step_update = millis()
                # IS THE NEW STEP THE FINISH STEP => SKIP TARE PROCESS
                if not recipe.get_current_recipe_step()[6]:
                    gui.show_msg("CALIBRATING")
                    tare_value = tare_drink(scales, 1)
                    scale_value_before_glass_added = tare_value
                continue
            
                
            # UPDATE UI
            if  abs(last_display_update - millis()) > 1000:
                last_display_update = millis()
                gui.show_recipe_step(action, ingredient, current_step, max_steps)
               
            
            # UPDATE NEOPIXEL
            
            if user_move == recipe_loader.USER_INTERACTION_MODE.SCALE and scale_value_g is not None and target_value is not None:
                disp_value = min([imap(scale_value_g, 0, target_value, 0 , NEOPIXEL_COUNT), NEOPIXEL_COUNT])
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
            elif user_move == recipe_loader.USER_INTERACTION_MODE.CONFIRM:
                for i in range(NEOPIXEL_COUNT):
                    neopixelring[i] = (100, 100, 0)
                neopixelring.write()
            
            elif user_move == recipe_loader.USER_INTERACTION_MODE.WAIT and delay_value is not None and time_elapsed is not None:
                lightup = min([imap(time_elapsed, 0, delay_value, 0 , NEOPIXEL_COUNT), NEOPIXEL_COUNT])
                #print("lightup {} {} {}".format(lightup, time_elapsed, delay_value)
                for i in range(NEOPIXEL_COUNT):
                    if i < lightup:
                        neopixelring[i] = (10, 10, 10)
                    elif i == lightup:
                        neopixelring[i] = (100, 100, 100)
                    else:
                        neopixelring[i] = (0, 0, 0)
                neopixelring.write()
                
            else:
                for i in range(NEOPIXEL_COUNT):
                    neopixelring[i] = (int(128* random.random()), 0, 0)
                neopixelring.write()
            
            
            
            
        else:
            for i in range(NEOPIXEL_COUNT):
                neopixelring[i] = (0, 0, 50)
            neopixelring.write()
        
        
       
        #time.sleep(0.2)



from utime import sleep_us
import machine
import time, math
import neopixel
import random
import network

import helper
from Scales import Scales
import config
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


def get_stable_raw_scale_value(_iterations = 10):
    print("get_stable_raw_scale_value_begin")
    tare_value = 0
    scale_value = 0
    for i in range(_iterations):
        scale_value = scales.raw_value()
        time.sleep(0.5)
        tare_value = tare_value + scale_value
    tare_value = tare_value / _iterations
    return tare_value



# SYSTEM STATES
SYSTATE_IDLE = 0
# MENU
SYSTEMSTATE_ENTER_MAINMENU = 1
SYSTEMSTATE_MAINMENU = 2

# MISC MODES
SYSTEMSTATE_SCALE_MODE = 3
SYSTEMSTATE_UPDATE_MODE = 4
SYSTEMSTATE_CALIBRATION_MODE_ENTRY = 5
SYSTEMSTATE_CALIBRATION_MODE_ZERO = 6
SYSTEMSTATE_CALIBRATION_MODE_FULL = 7
# SCALE ENABLED
SYSTATE_RECIPE_START = 10
SYSTATE_RECIPE_SHOW_INGREDIENTS = 11
SYSTATE_RECIPE_PLACEGLASS = 12
SYSTATE_RECIPE_RUNNING = 13
SYSTATE_RECIPE_FINISHED = 14




if __name__ == "__main__":
    
    # SETUP NETWORK IF PICO W
    if helper.has_wifi():
        network.country(config.CFG_NETWORK_WIFICOUNTRY)
        network.hostname(config.CFG_NETWORK_HOSTNAME)
    
    system_state = SYSTATE_IDLE
    # INIT RECIPE LOADER AND INIT SD CARD
    recipe = recipe_loader.recipe_loader()
        
    # INIT NEOPIXEL RING
    neopixelring = neopixel.NeoPixel(machine.Pin(config.CFG_NEOPIXEL_PIN), config.CFG_NEOPIXEL_LED_COUNT)
    helper.set_neopixel_random(neopixelring)
    
    # INIT DISPLAY
    gui = ui.ui()
    # INIT SCALE

    scales = Scales(d_out=config.CFG_HX711_DOUT_PIN, pd_sck=config.CFG_HX711_SCK_PIN)
    scales.tare()
    tare_value = tare_drink(scales, 1)
    scale_value = 0
    
    # CALIBTATION VALUES
    # TODO LOAD FFROM SETTINGS
    rt = recipe_loader.get_calibration_values()
    map_value_0g = rt[0]
    maps_value_50g = rt[1]
    print("loaded scale calibration valued 0g:{} 50g:{}".format(map_value_0g, maps_value_50g))
    
    
    # CONFIGURE USER BUTTONS
    push_button_up = machine.Pin(config.CFG_BUTTON_UP_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    push_button_down = machine.Pin(config.CFG_BUTTON_DOWN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    
    
   
    
    delay_value = None # FOR USER TIMER      
           
    target_value = None
    scale_offset = 0.0
    scale_value_before_glass_added = 0
    
    
    
    
    
    last_display_update = helper.millis()
    last_systate_update = helper.millis()
    last_recipe_step_update = helper.millis()
    last_userbutton_update = None
    
    UB_NONE = 0
    UB_UP = 1
    UB_UPLONG = 2
    UB_DOWN = 3
    
    
    last_button_pressed = None
    button_pressed = UB_NONE
    time_elapsed = 0
    load_next_step = False
    
    
  

    
    
    found_recipes = []
    mainmenu_recipe_index = 0
    
    system_state = SYSTEMSTATE_ENTER_MAINMENU #SYSTEMSTATE_UPDATE_MODE
    while True:
        
        
        # READ USER_BUTTONS
        if push_button_up.value() and not push_button_down.value() and last_userbutton_update is None and button_pressed is UB_NONE:
            last_userbutton_update = helper.millis()
            last_button_pressed = UB_UP
        
     
        elif push_button_up.value() and push_button_down.value():
            if last_userbutton_update is not None and last_button_pressed is not None:
                
                btn_duration = abs(last_userbutton_update - helper.millis())
                if last_button_pressed == UB_UP: #and  btn_duration >1 and btn_duration < 1000:
                    print("UB_UP")
                    button_pressed = UB_UP
                else:
                    button_pressed = UB_NONE
     
                
                last_userbutton_update = None
                last_button_pressed = None   


        if last_button_pressed == UB_UP and abs(last_userbutton_update - helper.millis()) > 1000:
            button_pressed = UB_UPLONG
            last_userbutton_update = None
            last_button_pressed = None
            print("UB_UPLONG")
           


        
        
        # READ SCALE
        if system_state >= SYSTATE_RECIPE_START or system_state == SYSTEMSTATE_SCALE_MODE:
            scale_value = scales.raw_value() #stable_value()
            scale_value_tared = scale_value - tare_value
            scale_value_g = helper.fmap(scale_value_tared, map_value_0g, maps_value_50g, 0 , 50)
        
            if scale_value_g <= 0.0:
                scale_offset = -scale_value_g
            scale_value_g =  scale_value_g + scale_offset
        
        
            
            
            
        # RETURN BUTTON
        if system_state > SYSTEMSTATE_MAINMENU and (button_pressed == UB_UPLONG or button_pressed == UB_DOWN):
            button_pressed = UB_NONE
            system_state = SYSTEMSTATE_ENTER_MAINMENU
        
        # GLOBAL STATE MACHIENE
        if system_state == SYSTATE_IDLE: # INITIAL SYSTEMSTATE
            gui.show_titlescreen()
            last_systate_update = helper.millis()
            system_state = SYSTEMSTATE_ENTER_MAINMENU
            
        elif system_state == SYSTEMSTATE_ENTER_MAINMENU: # RELOAD RECIPES
            helper.set_neopixel_full(neopixelring, 0, 0, 100)
            found_recipes = recipe.list_recpies()
            mainmenu_recipe_index = -1 # TO TRIGGER FIRST TIME DISPLAY UPDATE AFTER ENTERING THE STATE
            print(found_recipes)
            last_systate_update = helper.millis()
            system_state = SYSTEMSTATE_MAINMENU
                
                
        elif system_state == SYSTEMSTATE_MAINMENU: # DISPLAY MANIMENU
            
            # DISPLAY NEXT MENU

            if button_pressed == UB_UP or mainmenu_recipe_index == -1:
                button_pressed = UB_NONE
                # TO TRIGGER FIRST TIME DISPLAY UPDATE AFTER ENTERING THE STATE
                if mainmenu_recipe_index == -1:
                    mainmenu_recipe_index = 0
                
            
        
                if mainmenu_recipe_index >= (len(found_recipes)-1) + 2: # +2 for UPDATE_RECIPES, SCALE_MODE
                    mainmenu_recipe_index = 0
                else:
                    mainmenu_recipe_index = mainmenu_recipe_index + 1
                    
                # SHOW RECIPES
                if mainmenu_recipe_index < len(found_recipes):
                    rec_name = found_recipes[mainmenu_recipe_index][0]
                    print(rec_name)
                    if recipe.load_recipe(rec_name):
                        gui.set_full_refresh()
                        information = recipe.get_recipe_information()
                        print(information)
                        gui.show_recipe_information(information[0], information[1])
                   
                        
                else:
                    recipe.unload_recipe()
                    
                    if mainmenu_recipe_index == (len(found_recipes)-1)+1:
                        gui.set_full_refresh()
                        gui.show_recipe_information("SCALE MODE", "like a normal kitchen scale")
                    elif mainmenu_recipe_index == (len(found_recipes)-1)+2:
                        gui.set_full_refresh()
                        gui.show_recipe_information("RECIPE UPDATE", "updates all recipes using the webapp")
                    elif mainmenu_recipe_index == (len(found_recipes)-1)+3:
                        gui.set_full_refresh()
                        gui.show_recipe_information("CALIBRATE", "run a scale calibration program. A 50g weight is needed")
                        
                    print("extra menu {}".format(mainmenu_recipe_index))
                        
                        
            elif button_pressed == UB_UPLONG or button_pressed == UB_DOWN:
                button_pressed = UB_NONE
                last_systate_update = helper.millis()
                
                if recipe.is_recipe_loaded():
                    pass
                    #system_state = SYSTATE_RECIPE_START
                elif mainmenu_recipe_index == (len(found_recipes)-1)+1:
                    system_state = SYSTEMSTATE_SCALE_MODE
                    # UPDATE NEOPIXEL
                    helper.set_neopixel_full(neopixelring, 0, 100, 100)

                elif mainmenu_recipe_index == (len(found_recipes)-1)+2:
                    system_state = SYSTEMSTATE_UPDATE_MODE
                    # UPDATE NEOPIXEL
                    helper.set_neopixel_full(neopixelring, 100, 0, 100)

                elif mainmenu_recipe_index == (len(found_recipes)-1)+3:
                    system_state = SYSTEMSTATE_CALIBRATION_MODE_ENTRY
                    # UPDATE NEOPIXEL
                    helper.set_neopixel_full(neopixelring, 100, 0, 100)


                
                
        elif system_state == SYSTEMSTATE_CALIBRATION_MODE_ENTRY:
                gui.show_msg("REMOVE EVERYTHING FROM SCALE")
                if  abs(last_systate_update - helper.millis()) > 20000 or button_pressed == UB_UP:
                    gui.show_msg("PLEASE WAIT")
                    map_value_0g = get_stable_raw_scale_value()
                    system_state = SYSTEMSTATE_CALIBRATION_MODE_FULL

        elif system_state == SYSTEMSTATE_CALIBRATION_MODE_FULL:
                gui.show_msg("PLEASE PLACE 50g WEIGHT")
                if  abs(last_systate_update - helper.millis()) > 20000 or button_pressed == UB_UP:
                    gui.show_msg("PLEASE WAIT")
                    map_value_50g = get_stable_raw_scale_value()

                    recipe_loader.save_calibration_values(map_value_0g, maps_value_50g)
                    gui.show_msg("CALIBRATION SAVED")
                    system_state = SYSTATE_IDLE
                    


        elif system_state == SYSTEMSTATE_SCALE_MODE:
            # UPDATE DISPLAY WITH SCALE READING
            gui.show_scale(int(scale_value_g))
            
            if button_pressed == UB_UP:
                button_pressed = UB_NONE
                tare_value = tare_drink(scales, 1)
            elif button_pressed == UB_UPLONG or button_pressed == UB_DOWN:
                last_button_pressed = UB_NONE
                last_systate_update = helper.millis()
                system_state = SYSTATE_IDLE
                
        elif system_state == SYSTEMSTATE_UPDATE_MODE:
            gui.show_msg("LOADING UPDATE MANAGER")
            recipe.unload_recipe()
            if recipe.update_recipes(gui):
                helper.set_neopixel_full(neopixelring, 0, 0, 100)
                gui.show_msg("RECIPE UPDATE SUCCESS")
            else:
                helper.set_neopixel_full(neopixelring, 100, 0, 0)
                gui.show_msg("RECIPE UPDATE FAILED")
            
            if button_pressed == UB_UP or button_pressed == UB_UPLONG or button_pressed == UB_DOWN:
                button_pressed = UB_NONE
                last_systate_update = helper.millis()
                system_state = SYSTATE_IDLE
            
        
        
        elif system_state == SYSTATE_RECIPE_START: # START RECIPE
            if  abs(last_systate_update - helper.millis()) > 1000:
                last_systate_update = helper.millis()
                system_state = SYSTATE_RECIPE_SHOW_INGREDIENTS
                
                
        elif system_state == SYSTATE_RECIPE_SHOW_INGREDIENTS:
            gui.show_recipe_ingredients(recipe.get_ingredient_list())
            helper.set_neopixel_full(neopixelring, 100, 100, 0)

            if  abs(last_systate_update - helper.millis()) > 20000 or button_pressed == UB_UP:
                button_pressed = UB_NONE
                scale_value_before_glass_added = scale_value_g
                last_systate_update = helper.millis()
                system_state = SYSTATE_RECIPE_PLACEGLASS
            
        elif system_state == SYSTATE_RECIPE_PLACEGLASS:
            gui.show_msg("PLACE GLASS")
            #print(scale_value_g)
            if  abs(last_systate_update - helper.millis()) > 10000 or scale_value_g > (scale_value_before_glass_added + 50):
                
                gui.show_msg("CALIBRATING")
                tare_value = tare_drink(scales, 1)
                
                system_state = SYSTATE_RECIPE_RUNNING
                last_systate_update = helper.millis()
                last_recipe_step_update = helper.millis()
        
        elif system_state == SYSTATE_RECIPE_FINISHED:
            helper.set_neopixel_random(neopixelring, False, True, False)
            gui.show_msg("DRINK READY TO SERVE")
            
            if button_pressed == UB_UP or abs(last_systate_update - helper.millis()) > 7000:
                last_systate_update = helper.millis()
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
                time_elapsed = ((helper.millis() - last_recipe_step_update))/1000
                print(time_elapsed)
            else:
                target_value = None
                delay_value = None
                
            # CHECK OK ACTION OK
            if finished:
                last_systate_update = helper.millis()
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
                last_recipe_step_update = helper.millis()
                # IS THE NEW STEP THE FINISH STEP => SKIP TARE PROCESS
                if not recipe.get_current_recipe_step()[6]:
                    gui.show_msg("CALIBRATING")
                    tare_value = tare_drink(scales, 1)
                    scale_value_before_glass_added = tare_value
                continue
            
                
            # UPDATE UI
            if  abs(last_display_update - helper.millis()) > 1000:
                last_display_update = helper.millis()
                gui.show_recipe_step(action, ingredient, current_step, max_steps)
               
            
            # UPDATE NEOPIXEL  
            if user_move == recipe_loader.USER_INTERACTION_MODE.SCALE and scale_value_g is not None and target_value is not None:
                disp_value = min([helper.imap(scale_value_g, 0, target_value, 0 , config.CFG_NEOPIXEL_LED_COUNT), config.CFG_NEOPIXEL_LED_COUNT])
                for i in range(config.CFG_NEOPIXEL_LED_COUNT):
                    color_value = helper.imap(i, 0, config.CFG_NEOPIXEL_LED_COUNT, 0 , 1.0)
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
                helper.set_neopixel_full(neopixelring, 100, 100, 0)
            
            elif user_move == recipe_loader.USER_INTERACTION_MODE.WAIT and delay_value is not None and time_elapsed is not None:
                lightup = min([helper.imap(time_elapsed, 0, delay_value, 0 , config.CFG_NEOPIXEL_LED_COUNT), config.CFG_NEOPIXEL_LED_COUNT])
                #print("lightup {} {} {}".format(lightup, time_elapsed, delay_value)
                for i in range(config.CFG_NEOPIXEL_LED_COUNT):
                    if i < lightup:
                        neopixelring[i] = (10, 10, 10)
                    elif i == lightup:
                        neopixelring[i] = (100, 100, 100)
                    else:
                        neopixelring[i] = (0, 0, 0)
                neopixelring.write()
                
            else:
                helper.set_neopixel_random(neopixelring, True, False, False)
            
        else:
            helper.set_neopixel_full(neopixelring, 0, 0, 100)


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
    recipe = recipe_loader.recipe_loader()
        
    # INIT NEOPIXEL RING
    neopixelring = neopixel.NeoPixel(machine.Pin(config.CFG_NEOPIXEL_PIN), config.CFG_NEOPIXEL_LED_COUNT)
    helper.set_neopixel_random(neopixelring)
    
    # INIT DISPLAY7
    gui = ui.ui()
    # INIT SCALE

    scales = Scales.Scales(d_out=config.CFG_HX711_DOUT_PIN, pd_sck=config.CFG_HX711_SCK_PIN)
    scales.tare()
    
    
    
    # CALIBTATION VALUES
    # TODO LOAD FFROM SETTINGS
    calibration_factor = recipe.get_calibration_factor()
    print("calibration_factor {}".format(calibration_factor))
    map_value_0g = 0
    map_value_50g = 0
    
    scales.set_scale(calibration_factor)
    scales.tare()
    
    
    tare_value = scales.get_unit(True) # STABLE READ
    tare_value_initial = tare_value
    print("tare_value:{}".format(tare_value))
    scale_value = 0
    print("loaded scale calibration valued cal_w{} cal-fact{}".format(config.CFG_CALIBRATION_WEIGHT_WEIGHT, calibration_factor))
    
    
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
    last_recipe_ing_update = helper.millis()
    last_userbutton_update = None
    
    ingredient_counter = 0
    
    
    last_button_pressed = None
    button_pressed = UB_NONE
    time_elapsed = 0
    load_next_step = False
    
    
  

    
    target_value = 0.0
    found_recipes = []
    mainmenu_recipe_index = 0
    
    system_state = SYSTATE_IDLE #SYSTEMSTATE_ENTER_MAINMENU #SYSTEMSTATE_UPDATE_MODE
    while True:
        
        
        # READ USER_BUTTONS
        if not push_button_up.value() and not push_button_down.value() and button_pressed is UB_RELEASE:
            #print()
            #last_userbutton_update = helper.millis()
            #last_button_pressed = UB_DOWN
            if last_userbutton_update is not None and(helper.millis() - last_userbutton_update) > 100:
                button_pressed = UB_UPLONG
            else:
                last_userbutton_update = helper.millis()
                
        elif push_button_up.value() and not push_button_down.value() and button_pressed is UB_RELEASE:
            
            
            if last_userbutton_update is not None and(helper.millis() - last_userbutton_update) > 500:
                button_pressed = UB_UP
            else:
                last_userbutton_update = helper.millis()
                
            #last_button_pressed = UB_UP
                #button_pressed = UB_UP
        elif not push_button_up.value() and push_button_down.value() and button_pressed is UB_RELEASE:
            if last_userbutton_update is not None and(helper.millis() - last_userbutton_update) > 500:
                button_pressed = UB_DOWN
            else:
                last_userbutton_update = helper.millis()
            

            
            
            
        elif push_button_up.value() and push_button_down.value() and button_pressed is UB_NONE:
            if last_userbutton_update is not None and(helper.millis() - last_userbutton_update) > 100:
                button_pressed = UB_RELEASE
            else:
                last_userbutton_update = helper.millis()
            
        

        time.sleep(0.01)

        
        
        # READ SCALE
        if system_state >= SYSTATE_RECIPE_START or system_state == SYSTEMSTATE_SCALE_MODE or system_state == SYSTEMSTATE_RAW_MODE or system_state == SYSTEMSTATE_CALIBRATION_MODE_FULL or system_state == SYSTEMSTATE_CALIBRATION_MODE_ZERO:
            scale_value_g = scales.get_unit(True) - tare_value

            

        
            
            
            
        # RETURN BUTTON
        if system_state > SYSTEMSTATE_MAINMENU and button_pressed == UB_UPLONG:
            button_pressed = UB_NONE
            system_state = SYSTATE_IDLE
            last_systate_update = helper.millis()
            
        
        # GLOBAL STATE MACHIENE
        if system_state == SYSTATE_IDLE: # INITIAL SYSTEMSTATE
            gui.show_titlescreen()
            if  abs(last_systate_update - helper.millis()) > 20000 or button_pressed != UB_NONE:
                button_pressed = UB_NONE
                
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
                
            
        
                if mainmenu_recipe_index >= (len(found_recipes)-1) + 4: # +2 for UPDATE_RECIPES, SCALE_MODE
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
                        if helper.has_wifi():
                            gui.set_full_refresh()
                            gui.show_recipe_information("SCALE MODE", "like a normal kitchen scale")
                        else:
                            mainmenu_recipe_index = (len(found_recipes)-1)+3
                    elif mainmenu_recipe_index == (len(found_recipes)-1)+2:
                        if helper.has_wifi():
                            gui.set_full_refresh()
                            gui.show_recipe_information("RECIPE UPDATE", "updates all recipes using the webapp")
                        else:
                            mainmenu_recipe_index = (len(found_recipes)-1)+3
                            
                    elif mainmenu_recipe_index == (len(found_recipes)-1)+3:
                        gui.set_full_refresh()
                        gui.show_recipe_information("CALIBRATE", "run a scale calibration program. A 50g weight is needed")
                    elif mainmenu_recipe_index == (len(found_recipes)-1)+4:
                        gui.set_full_refresh()
                        gui.show_recipe_information("HARDWARE TEST", "test internal hardware")
                        
                    print("extra menu {}".format(mainmenu_recipe_index))
                        
                        
            elif button_pressed == UB_UPLONG or button_pressed == UB_DOWN:
                button_pressed = UB_NONE
                last_systate_update = helper.millis()
                
                if recipe.is_recipe_loaded():
                    system_state = SYSTATE_RECIPE_START
                elif mainmenu_recipe_index == (len(found_recipes)-1)+1:
                    system_state = SYSTEMSTATE_SCALE_MODE
                    # UPDATE NEOPIXEL
                    helper.set_neopixel_full(neopixelring, 0, 100, 100)

                elif mainmenu_recipe_index == (len(found_recipes)-1)+2:
                    system_state = SYSTEMSTATE_UPDATE_MODE_QR_START
                    # UPDATE NEOPIXEL
                    helper.set_neopixel_full(neopixelring, 100, 0, 100)

                elif mainmenu_recipe_index == (len(found_recipes)-1)+3:
                    system_state = SYSTEMSTATE_CALIBRATION_MODE_ENTRY
                    # UPDATE NEOPIXEL
                    helper.set_neopixel_full(neopixelring, 100, 10, 50)
                elif mainmenu_recipe_index == (len(found_recipes)-1)+4:
                    system_state = SYSTEMSTATE_RAW_MODE
                    # UPDATE NEOPIXEL
                    helper.set_neopixel_full(neopixelring, 100, 0, 100)


        elif system_state == SYSTEMSTATE_RAW_MODE:
                gui.show_msg("SRV:{}\nPBU:{}\nPBD:{}\nSS:{}\nTRE:{}\nID:{}".format(scales.stable_raw_value(without_offset=True), push_button_up.value(), push_button_down.value(), system_state, tare_value, helper.get_system_id()))
                
                if button_pressed == UB_UP:
                    button_pressed = UB_NONE
                    user_portal_url: str = recipe.check_update_url()
                    if user_portal_url != "":
                        gui.show_device_qr_code(user_portal_url)
                        time.sleep(10)
         
                
                
        elif system_state == SYSTEMSTATE_CALIBRATION_MODE_ENTRY:
                gui.show_msg("REMOVE EVERYTHING FROM SCALE")
                if  button_pressed == UB_UP:
                    button_pressed = UB_NONE
                    gui.show_msg("PLEASE WAIT")
                    map_value_0g = scales.stable_raw_value(without_offset=True)
                    print("map_value_0g:{}".format(map_value_0g))
                    system_state = SYSTEMSTATE_CALIBRATION_MODE_FULL

        elif system_state == SYSTEMSTATE_CALIBRATION_MODE_FULL:
                gui.show_msg("PLEASE PLACE {}g WEIGHT".format(config.CFG_CALIBRATION_WEIGHT_WEIGHT))
                if  button_pressed == UB_UP:
                    button_pressed = UB_NONE
                    gui.show_msg("PLEASE WAIT")
                    map_value_50g = scales.stable_raw_value(without_offset=True)
                    # FLIP MIN MAX IF LOADCELL IS INVERTED
                    if map_value_0g > map_value_50g:
                       t = map_value_0g
                       map_value_0g = map_value_50g
                       map_value_50g = t
                
                    recipe.save_calibration_values(map_value_0g, map_value_50g)
                    print("CALIBRATION SAVED map_value_0g:{} map_value_50g:{}".format(map_value_0g, map_value_50g))
                    calibration_factor = recipe.get_calibration_factor()
                    scales.set_scale(calibration_factor)
                    system_state = SYSTATE_IDLE
                    


        elif system_state == SYSTEMSTATE_SCALE_MODE:
            # UPDATE DISPLAY WITH SCALE READING
            print("scale_value_g:{}g".format(scale_value_g))
            gui.show_scale(int(scale_value_g))
            
            if button_pressed == UB_UP:
                button_pressed = UB_NONE
                tare_value = scales.get_unit(True)
            elif button_pressed == UB_DOWN:
                button_pressed = UB_NONE
                target_value = 0.0
                
            elif button_pressed == UB_UPLONG:
                last_button_pressed = UB_NONE
                last_systate_update = helper.millis()
                system_state = SYSTATE_IDLE
            
            # UPDATE NEOPIXEL RING FROM TAREVALUE TO MAX MEASURED VALUE
            target_value = max([scale_value_g, target_value, 10])
            disp_value = min([helper.imap(scale_value_g, tare_value, target_value, 0 , config.CFG_NEOPIXEL_LED_COUNT), config.CFG_NEOPIXEL_LED_COUNT])
            for i in range(config.CFG_NEOPIXEL_LED_COUNT):
                color_value = helper.imap(i, 0, config.CFG_NEOPIXEL_LED_COUNT, 0 , 1.0)
                # APPLY START indEX OFFSET
                led_index = int((i+config.CFG_NEOPIXEL_LED_START_OFFSET) % config.CFG_NEOPIXEL_LED_COUNT)

                if target_value < 0:
                    neopixelring[led_index] = (10, 0, 10)
                elif scale_value_g >= target_value:
                    neopixelring[led_index] = (255, 0, 255)
                elif i < disp_value:
                    #       R  G  B
                    neopixelring[led_index] = (int(color_value*255), 0, int((1.0 - color_value) * 255))
                else:
                    neopixelring[led_index] = (10, 10, 10)
            neopixelring.write()
            
            
            
        elif system_state == SYSTEMSTATE_UPDATE_MODE_QR_START:
            if config.CFG_DISPLAY_USER_QR_CODE:
                user_portal_url: str = recipe.check_update_url()
                if user_portal_url != "":
                    gui.show_device_qr_code(user_portal_url)
                    system_state = SYSTEMSTATE_UPDATE_MODE_QR_RUNNING
                else:
                    system_state = SYSTEMSTATE_UPDATE_MODE
            else:
                system_state = SYSTEMSTATE_UPDATE_MODE
            
            
        elif system_state == SYSTEMSTATE_UPDATE_MODE_QR_RUNNING:
            gui.show_msg("LOADING UPDATE MANAGER")
            if button_pressed == UB_DOWN or button_pressed == UB_UP:
                button_pressed = UB_NONE
                system_state = SYSTEMSTATE_UPDATE_MODE
                
        elif system_state == SYSTEMSTATE_UPDATE_MODE:
            gui.show_msg("UPDATING RECIPES")
            
        
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
                last_recipe_ing_update = helper.millis()
                
                helper.set_neopixel_full(neopixelring, 100, 100, 0)
                
                # ENTER SHOW INGREDIENTS IF THERE ARE SOME PRESENT ELSE SKIP THIS STEP
                ingredient_counter = -1
                if len(recipe.get_ingredient_list()) > 0:
                    ingredient_counter = 0
                    gui.show_recipe_ingredients([recipe.get_ingredient_list()[ingredient_counter]])
                    system_state = SYSTATE_RECIPE_SHOW_INGREDIENTS
                else:
                    system_state = SYSTATE_RECIPE_PLACEGLASS
                
        elif system_state == SYSTATE_RECIPE_SHOW_INGREDIENTS:
            if button_pressed == UB_DOWN:
                button_pressed = UB_NONE
                ingredient_counter = ingredient_counter + 1
                if ingredient_counter >= len(recipe.get_ingredient_list()):
                    ingredient_counter = 0
                    

                gui.show_recipe_ingredients([recipe.get_ingredient_list()[ingredient_counter]])
            


            if  abs(last_systate_update - helper.millis()) > 20000 or button_pressed == UB_UP:
                button_pressed = UB_NONE
                scale_value_before_glass_added = scale_value_g
                last_systate_update = helper.millis()
                system_state = SYSTATE_RECIPE_PLACEGLASS
            
        elif system_state == SYSTATE_RECIPE_PLACEGLASS:
            gui.show_msg("PLACE GLASS")
            #print(scale_value_g)
            if  abs(last_systate_update - helper.millis()) > 10000 or scale_value_g > (scale_value_before_glass_added + config.CFG_SCALE_GLASS_ADDITION_NEXT_STEP_WEIGHT):
                
                gui.show_msg("CALIBRATING")
                tare_value = scales.get_unit(True)
                
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
                    # RESTORE INITIAL TARE VALUE
                    tare_value = tare_value_initial
                    continue
            elif user_move == recipe_loader.USER_INTERACTION_MODE.SCALE and scale_value_g > target_value:
                load_next_step = True
            elif user_move == recipe_loader.USER_INTERACTION_MODE.WAIT and time_elapsed > delay_value:
                load_next_step = True
            elif user_move == recipe_loader.USER_INTERACTION_MODE.CONFIRM and (button_pressed == UB_UP or button_pressed == UB_DOWN):
                button_pressed == UB_NONE
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
                    tare_value = scales.get_unit(True)
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
                    # APPLY START indEX OFFSET
                    led_index = int((i+config.CFG_NEOPIXEL_LED_START_OFFSET) % config.CFG_NEOPIXEL_LED_COUNT)

                    if target_value < 0:
                        neopixelring[led_index] = (0, 0, 128)
                    elif scale_value_g >= target_value:
                        neopixelring[led_index] = (0, 255, 0)
                    elif i < disp_value:
                        #       R  G  B
                        neopixelring[led_index] = (int((1.0 - color_value) * 255), int(color_value*255), 0)
                    else:
                        neopixelring[led_index] = (10, 0, 0)
                neopixelring.write()
                
            elif user_move == recipe_loader.USER_INTERACTION_MODE.CONFIRM:
                helper.set_neopixel_full(neopixelring, 100, 100, 0)
            
            elif user_move == recipe_loader.USER_INTERACTION_MODE.WAIT and delay_value is not None and time_elapsed is not None:
                lightup = min([helper.imap(time_elapsed, 0, delay_value, 0 , config.CFG_NEOPIXEL_LED_COUNT), config.CFG_NEOPIXEL_LED_COUNT])
                #print("lightup {} {} {}".format(lightup, time_elapsed, delay_value)
                for i in range(config.CFG_NEOPIXEL_LED_COUNT):
                    led_index = int((i+config.CFG_NEOPIXEL_LED_START_OFFSET) % config.CFG_NEOPIXEL_LED_COUNT)
                    if i < lightup:
                        neopixelring[led_index] = (10, 10, 10)
                    elif i == lightup:
                        neopixelring[led_index] = (100, 100, 100)
                    else:
                        neopixelring[led_index] = (10, 10, 10)
                neopixelring.write()
                
            else:
                helper.set_neopixel_random(neopixelring, True, False, False)
            
        else:
            helper.set_neopixel_full(neopixelring, 0, 0, 100)



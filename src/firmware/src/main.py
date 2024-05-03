from utime import sleep_us
import uasyncio as aio
from aiobutton import AIOButton
import machine
import helper
from Scales import ScaleInterface
from ledring import ledring
import system_command
# NEEDED FOR ENCODER
from sys import platform
if 'esp' in platform: 
    from rotary_irq_esp import RotaryIRQ
elif 'rp' in platform:
    from rotary_irq_rp2 import RotaryIRQ
else:
    from rotary_irq_pyb import RotaryIRQ


import config
import recipe_loader
import recipe_updater
from ui import ui
import settings
import menu_manager
# PLUGINS
import menu_entry_submenu
import menu_entry_recipe_update
import menu_entry_recipe_editor
import menu_entry_scale
import menu_entry_info
import menu_entry_recipe
import menu_entry_hardwaretest
import menu_entry_calibration
import menu_entry_restore


TIME_ELAPSED_DIVIDER: int = 2
print("main: __entry__")

BUTTON_INDEX_LEFT = 0
BUTTON_INDEX_RIGHT = 1
BUTTON_INDEX_MENU = 2

BUTTON_PRESSED = 0
BUTTON_HOLD = 1
BUTTON_RELEASED = 2

last_left_button_state: int = 0
button_state_dict: list = [-1, -1, -1]
encoder_middle_point: int = 1
current_button_cmd: system_command.system_command = system_command.system_command()
current_button_cmd.type = system_command.system_command.COMMAND_TYPE_NAVIGATION
# GENERATED SYSTEM EVENTS DEPENING ON THE PRESSED BUTTON TO NAVIGATE THOUGHT MENUS
def generate_button_state(_button_index: int, _button_event: int, _button_state: bool):

    if button_state_dict[_button_index] == BUTTON_PRESSED and _button_event == BUTTON_RELEASED:
        if _button_index == BUTTON_INDEX_LEFT:
            current_button_cmd.action = system_command.system_command.NAVIGATION_LEFT
        elif _button_index == BUTTON_INDEX_RIGHT:
            current_button_cmd.action = system_command.system_command.NAVIGATION_RIGHT
        elif _button_index == BUTTON_INDEX_MENU:
            current_button_cmd.action = system_command.system_command.NAVIGATION_ENTER

        menu_manager.menu_manager().process_user_commands(current_button_cmd)

    elif _button_event == BUTTON_HOLD:
        if _button_index == BUTTON_INDEX_LEFT:
            current_button_cmd.action = system_command.system_command.NAVIGATION_EXIT
        elif _button_index == BUTTON_INDEX_RIGHT:
            current_button_cmd.action = system_command.system_command.NAVIGATION_ENTER
        elif _button_index == BUTTON_INDEX_MENU:
            current_button_cmd.action = system_command.system_command.NAVIGATION_EXIT

        
        menu_manager.menu_manager().process_user_commands(current_button_cmd)
    
    button_state_dict[_button_index] = _button_event
   
   
   



if __name__ == "__main__":
    
    # INIT RECIPE LOADER AND INIT SD CARD
    settings.settings().list_files()
    # RECIPE STORAGE
    recipe_loader.recipe_loader().list_recpies()
    # INIT LED RING
    ledring().set_neopixel_full_hsv(ledring().COLOR_PRESET_HSV_H__BLUE)
    # INIT UI
    ui().clear()
    # INIT SCALE
    ScaleInterface().tare()

    # INIT USER INPUT BUTTONS
    left_button_pin: machine.Pin = machine.Pin(config.CFG_BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    left_button = AIOButton(lambda btn: not left_button_pin.value())
    left_button.set_hold_ms(config.CFG_USER_LONG_BUTTON_PRESS_TIME)
    # Register button event handlers
    left_button.set_hold_handler(lambda btn: generate_button_state(BUTTON_INDEX_LEFT, BUTTON_HOLD, btn.get_debounced()))   
    left_button.set_press_handler(lambda btn: generate_button_state(BUTTON_INDEX_LEFT, BUTTON_PRESSED, btn.get_debounced()))
    left_button.set_release_handler(lambda btn: generate_button_state(BUTTON_INDEX_LEFT, BUTTON_RELEASED, btn.get_debounced())) 
    
    right_button_pin: machine.Pin = machine.Pin(config.CFG_BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    right_button = AIOButton(lambda btn: not right_button_pin.value())
    right_button.set_hold_ms(config.CFG_USER_LONG_BUTTON_PRESS_TIME)
    # Register button event handlers
    right_button.set_hold_handler(lambda btn: generate_button_state(BUTTON_INDEX_RIGHT, BUTTON_HOLD, btn.get_debounced()))   
    right_button.set_press_handler(lambda btn: generate_button_state(BUTTON_INDEX_RIGHT, BUTTON_PRESSED, btn.get_debounced()))
    right_button.set_release_handler(lambda btn: generate_button_state(BUTTON_INDEX_RIGHT, BUTTON_RELEASED, btn.get_debounced())) 
    

    
    ## REGISTER ENCODER BUTTON EVENTS BY REMAPPING THE ENCODER SWITCH 
    encoder_button_pin: machine.Pin = machine.Pin(config.CFG_ENCODER_SW_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    #while True:
    #    print(encoder_button_pin.value())
    
    encoder_button = AIOButton(lambda btn: not encoder_button_pin.value())
    encoder_button.set_hold_handler(lambda btn: generate_button_state(BUTTON_INDEX_MENU, BUTTON_HOLD, btn.get_debounced()))   
    encoder_button.set_press_handler(lambda btn: generate_button_state(BUTTON_INDEX_MENU, BUTTON_PRESSED, btn.get_debounced()))
    encoder_button.set_release_handler(lambda btn: generate_button_state(BUTTON_INDEX_MENU, BUTTON_RELEASED, btn.get_debounced())) 
    
    # CONFIGURE ENCODER
    encoder: RotaryIRQ = RotaryIRQ(pin_num_clk=config.CFG_ENCODER_CLK_PIN, pin_num_dt=config.CFG_ENCODER_DT_PIN, min_val=encoder_middle_point-encoder_middle_point, max_val=encoder_middle_point*2, reverse=config.CFG_ENCODER_INVERT, range_mode=RotaryIRQ.RANGE_WRAP)
    encoder.set_current_value(encoder_middle_point)
    # INIT MENU SYSTEM
    
    # ADD RECIPES
    for r in recipe_loader.recipe_loader().list_recpies(_include_description=True):
        filename, name, description = r
        print("adding recipe entry: {}".format(filename))
        # name description are only used for menu entries, recipe will be loaded again by filename
        menu_manager.menu_manager().add_subentries(menu_entry_recipe.menu_entry_recipe(filename, name, description))

    
    
    # ADD FURTHER SYSTEM MENUS
    menu_manager.menu_manager().add_subentries(menu_entry_scale.menu_entry_scale())

    # ADD SYSTEM MENUS
    system_menu: menu_entry_submenu.menu_entry_submenu = menu_entry_submenu.menu_entry_submenu("SYSTEM", "ACCESS SYSTEM SETTINGS")
    system_menu.add_subentries(menu_entry_calibration.menu_entry_calibration())
    system_menu.add_subentries(menu_entry_info.menu_entry_info())
    system_menu.add_subentries(menu_entry_restore.menu_entry_restore())
    if config.CFG_DEBUG:
        system_menu.add_subentries(menu_entry_hardwaretest.menu_entry_hardwaretest())
    
    # ADD RECIPE UPDATE FUNCTIONS
    if recipe_updater.recipe_update_helper.has_network_capabilities():
        system_menu.add_subentries(menu_entry_recipe_update.menu_entry_recipe_update())
        # EDITOR IS CURRENTLY UNDER DEVELOPMENT
        if config.CFG_DEBUG:
            system_menu.add_subentries(menu_entry_recipe_editor.menu_entry_recipe_editor())


    menu_manager.menu_manager().add_subentries(system_menu)

    async def main_task():
        
        last_scale_update = helper.millis()
        last_timer_update = helper.millis()

        # DECLEARE SOME SYSTEM STATE MESSAGES IN ORDER TO ACVOID REALLOCATION
        current_scale_cmd: system_command.system_command = system_command.system_command(system_command.system_command.COMMAND_TYPE_SCALE_VALUE, system_command.system_command.SCALE_CURRENT_VALUE)
        current_timertick_cmd: system_command.system_command = system_command.system_command(system_command.system_command.COMMAND_TYPE_TIMER_IRQ, system_command.system_command.TIMER_TICK)

        # CREATE TASKS FOR USER INPUT
        task_left = aio.create_task(left_button.coro_check())
        task_right = aio.create_task(right_button.coro_check())
        task_menu = aio.create_task(encoder_button.coro_check())
        
        current_encoder_cmd: system_command.system_command = system_command.system_command()
        current_encoder_cmd.type = system_command.system_command.COMMAND_TYPE_NAVIGATION
       
        while True:
            await aio.sleep_ms(1)


            # QUERY ENCODER AND DETERM USER INTPUT STATE
            current_encoder_value = encoder.value()
            if current_encoder_value != encoder_middle_point:
                current_encoder_cmd.value = current_encoder_value
                
                if current_encoder_value > encoder_middle_point:
                    encoder.set_current_value(encoder_middle_point)
                    current_encoder_cmd.action = system_command.system_command.NAVIGATION_LEFT
                    menu_manager.menu_manager().process_user_commands(current_encoder_cmd)
                elif current_encoder_value < encoder_middle_point:
                    encoder.set_current_value(encoder_middle_point)
                    current_encoder_cmd.action = system_command.system_command.NAVIGATION_RIGHT
                    menu_manager.menu_manager().process_user_commands(current_encoder_cmd)
              

            # PERIODIC READ OF THE SCALE
            if  abs(last_scale_update - helper.millis()) > (10/TIME_ELAPSED_DIVIDER):
                last_scale_update = helper.millis()
                # UPDATE SCALE VALUE AND SEND TO PROCESS
                current_scale_cmd.value = ScaleInterface().get_current_weight()
                menu_manager.menu_manager().process_system_commands(current_scale_cmd)

            # SYSTEM TICK TO IMPLEMENT TIMERS SUCH AS WAITING FOR X SECONDS IN RECIPES
            if  abs(last_timer_update - helper.millis()) > (1000/TIME_ELAPSED_DIVIDER):
                current_timertick_cmd.value = abs(last_timer_update - helper.millis())
                menu_manager.menu_manager().process_system_commands(current_timertick_cmd)
                last_timer_update = helper.millis()

    aio.run(main_task())


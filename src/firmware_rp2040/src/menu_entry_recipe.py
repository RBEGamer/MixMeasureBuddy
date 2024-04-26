from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from menu_manager import menu_manager
import recipe_loader
import recipe
import time
from Scales import ScaleInterface
import config

class menu_entry_recipe(menu_entry.menu_entry):
    RECIPE_STATE_INIT = 0
    RECIPE_STATE_OVERVIEW = 1
    RECIPES_STATE_DRINK_MULTIPLIER = 2
    RECIPE_STATE_INITIAL_TARE = 3
    RECIPE_RUNNING_INIT = 4
    RECIPE_RUNNING_GET_CURRENT_STEP = 5
    RECIPE_RUNNING_GET_NEXT_STEP = 6
    RECIPE_RUNNING = 7
    RECIPE_END_CHECK = 8
    RECIPE_END = 9


   
    recipe_filename: str = ""
    loaded_recipe: recipe.recipe = None
    last_scale_value: float = 0.0
    last_time_value : float = 0.0
    recipe_state: int = RECIPE_STATE_OVERVIEW
    current_recipe_step: recipe.recipe_step = None
    is_end_step: bool = False
    drink_multiplier: int = 1

    def __init__(self, _recipe_filename: str, _recipe_name: str, _recipe_desciption: str):
        super().__init__(_recipe_name, _recipe_desciption)
        self.recipe_filename = _recipe_filename

    def preview(self):
        print("preview c{}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        print("activate {}".format(self.name))
        ui().clear()
        # LOAD RECIPE
        if len(self.recipe_filename) <= 0:
            ui().show_msg("Recipe filename empty. Please check file")
            time.sleep(2)
            menu_manager.exit_current_menu()
            return
        
        self.loaded_recipe = recipe_loader.recipe_loader().get_recipe_by_filename(self.recipe_filename)

        if self.loaded_recipe is None or not self.loaded_recipe.is_valid():
            ui().show_msg("Recipe loading failed. Please check file structure")
            time.sleep(2)
            menu_manager.exit_current_menu()
            return



        # SHOW RECIPE OVERVIEW PAGE
        self.recipe_state = self.RECIPE_STATE_INIT
        ui().show_recipe_ingredients(self.loaded_recipe.get_ingredients_as_names_list(), True)

        # TARE SCALE
        ScaleInterface().tare()

        # RESET RECIPE
        self.loaded_recipe.reset_steps()

    def teardown(self):
        print("teardown {}".format(self.name))
        # UNLOAD RECIPE
        if self.loaded_recipe is not None:
            del self.loaded_recipe
            self.loaded_recipe = None


    def tare_scale(self):
            ScaleInterface().tare()
            time.sleep(1)
            ScaleInterface().tare()
            self.last_time_value = 0.0


    def update(self, _system_command: system_command.system_command):
        if self.loaded_recipe is None:
            menu_manager.exit_current_menu()

        # 1st WAIT FOR INITIAL SCALE VALUE
        if self.recipe_state == self.RECIPE_STATE_INIT and _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
            self.last_scale_value = _system_command.value
            self.recipe_state = self.RECIPE_STATE_OVERVIEW
            
        # IF USER IS IN OVERVIEW SCREEN SWITCH TO FIRST RECIPE STEP IF USER PRESSED OK
        elif self.recipe_state == self.RECIPE_STATE_OVERVIEW:
            if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
                ui().show_recipe_ingredients("DRINK QUANTITY","{}x".format(self.drink_multiplier))
                self.recipe_state = self.RECIPES_STATE_DRINK_MULTIPLIER
            
            elif _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
                self.last_scale_value = _system_command.value

        elif self.recipe_state == self.RECIPES_STATE_DRINK_MULTIPLIER:

            
            if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
                if _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                    ui().show_msg("Please place glass and press ok to begin")
                    self.drink_multiplier = max(1, self.drink_multiplier)
                    self.recipe_state = self.RECIPE_STATE_INITIAL_TARE

                elif _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION and _system_command.action == system_command.system_command.NAVIGATION_LEFT:
                    self.drink_multiplier = self.drink_multiplier - 1
                    self.drink_multiplier = max(1, self.drink_multiplier)

                elif _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION and _system_command.action == system_command.system_command.NAVIGATION_RIGHT:
                    self.drink_multiplier = self.drink_multiplier + 1

                ui().show_recipe_ingredients("DRINK QUANTITY","{}x".format(self.drink_multiplier))
            elif _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
                self.last_scale_value = _system_command.value

        elif self.recipe_state == self.RECIPE_STATE_INITIAL_TARE:
            # USER PLACES GLASS AND CLICKED A BUTTON 
            if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
                self.tare_scale()
                self.recipe_state = self.RECIPE_RUNNING_INIT
            # SYSTEM WAITS FOR INCREASING LOAD ON THE SCALE AND CONTINOUES AUTOMATICALLY
            elif _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
                if _system_command.value > (self.last_scale_value + config.CFG_SCALE_GLASS_ADDITION_NEXT_STEP_WEIGHT):
                    self.tare_scale()
                    self.recipe_state = self.RECIPE_RUNNING_INIT

        # LOAD FIRST STEP
        elif self.recipe_state == self.RECIPE_RUNNING_INIT:
            self.loaded_recipe.reset_steps()
            self.recipe_state = self.RECIPE_RUNNING_GET_CURRENT_STEP

        elif self.recipe_state == self.RECIPE_RUNNING_GET_NEXT_STEP:
            self.loaded_recipe.switch_next_step()
            print("RECIPE_RUNNING_GET_NEXT_STEP")
            self.recipe_state = self.RECIPE_RUNNING_GET_CURRENT_STEP

        elif self.recipe_state == self.RECIPE_RUNNING_GET_CURRENT_STEP:
        
            self.tare_scale()
            self.current_recipe_step, self.is_end_step = self.loaded_recipe.get_current_recipe_step()
            
            self.recipe_state = self.RECIPE_RUNNING

            if self.current_recipe_step.action == recipe.USER_INTERACTION_MODE.SCALE:
                ui().show_recipe_step("ADD", self.current_recipe_step.ingredient_name)
                self.current_recipe_step.target_value = self.current_recipe_step * self.drink_multiplier
            elif self.current_recipe_step.action == recipe.USER_INTERACTION_MODE.CONFIRM:
                self.current_recipe_step.target_value = self.current_recipe_step * self.drink_multiplier
            elif self.current_recipe_step.action == recipe.USER_INTERACTION_MODE.WAIT or self.current_recipe_step.action == recipe.USER_INTERACTION_MODE.CONFIRM:
                ui().show_recipe_step(self.current_recipe_step.current_step_text, self.current_recipe_step.ingredient_name)
            else:
                ui().show_recipe_step("DO SOMETHING", self.current_recipe_step.ingredient_name)

            time.sleep(1)

        elif self.recipe_state == self.RECIPE_RUNNING:
            
            if self.current_recipe_step.action == recipe.USER_INTERACTION_MODE.SCALE:
                if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION and _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                    self.recipe_state = self.RECIPE_END_CHECK
                elif _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
                    # UPDAT LED RING
                    if _system_command.value > (self.current_recipe_step.target_value * 0.9):
                        ledring().set_neopixel_percentage(_system_command.value / (self.current_recipe_step.target_value*1.0),_independent_coloring = False)
                    else:
                        ledring().set_neopixel_percentage(_system_command.value / (self.current_recipe_step.target_value*1.0),_independent_coloring = True)
                    # IF TARGET VALUE REACHED GOTO NEXT STEP
                    if _system_command.value > self.current_recipe_step.target_value:
                        self.recipe_state = self.RECIPE_END_CHECK
            elif self.current_recipe_step.action == recipe.USER_INTERACTION_MODE.WAIT:
                # ON EACH SYSTEM TIMER TICK COUNT UP THE TIME IN THIS STEP
                if _system_command.type == system_command.system_command.COMMAND_TYPE_TIMER_IRQ:
                    self.last_time_value = self.last_time_value + (_system_command.value / 1000.0)

                ledring().set_neopixel_percentage(self.last_time_value / (self.current_recipe_step.target_value*1.0),_independent_coloring = False)
                # IF TARGET PASSED TIME VALUE REACHED -> GOTO NEXT STEP
                if self.last_time_value > self.current_recipe_step.target_value:
                    self.recipe_state = self.RECIPE_END_CHECK

            # ON ANY BUTTON CLICK SWITCH TO NEXT STEP
            elif self.current_recipe_step.action == recipe.USER_INTERACTION_MODE.CONFIRM:
                ledring().set_neopixel_full(20, 20, 20)
                if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
                    self.recipe_state = self.RECIPE_END_CHECK
            else:
                self.recipe_state = self.RECIPE_END_CHECK

        # CHECK IF THIS THE LAST STEP IN RECIPE
        # TODO REWORK
        elif self.recipe_state == self.RECIPE_END_CHECK:
            self.recipe_state = self.RECIPE_RUNNING_GET_NEXT_STEP
            # CHECK IF LAST STEP
            if self.is_end_step:
                self.recipe_state = self.RECIPE_END
        # SHOW END SCREEN
        elif self.recipe_state == self.RECIPE_END:
            ui().show_msg("ENJOY")
            ledring().set_neopixel_full_hsv(ledring().COLOR_PRESET_HSV_H__GREEN)
            time.sleep(2)
            menu_manager().exit_current_menu()
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
class menu_entry_recipe(menu_entry.menu_entry):

    RECIPE_STATE_OVERVIEW = 0
    RECIPE_STATE_INITIAL_TARE = 1
    RECIPE_RUNNING = 2


   
    recipe_filename: str = ""
    loaded_recipe: recipe.recipe = None
    last_scale_value: float = 0
    recipe_state: int = RECIPE_STATE_OVERVIEW


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

        
        self.loaded_recipe = recipe_loader.recipe_loader().get_recipe_by_filename(self.recipe_filename)

        if self.loaded_recipe is None or not self.loaded_recipe.is_valid():
            ui().show_msg("Recipe loading failed. Please check file structure")



        # SHOW RECIPE OVERVIEW PAGE
        self.recipe_state = self.RECIPE_STATE_OVERVIEW
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


    def tare_scale():
            ScaleInterface().tare()
            time.sleep(1)
            ui().show_msg("-- TARE SCALE --")
            ScaleInterface().tare()


    def update(self, _system_command: system_command.system_command):
        if self.loaded_recipe is None:
            menu_manager.exit_current_menu()

        # IF USER IS IN OVERVIEW SCREEN SWITCH TO FIRST RECIPE STEP
        if self.recipe_state == self.RECIPE_STATE_OVERVIEW:
            if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
                ui().show_msg("Please place glass and press a button")
                self.recipe_state = self.RECIPE_STATE_INITIAL_TARE
            
            elif _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
                self.last_scale_value = _system_command.value

        if self.recipe_state == self.RECIPE_STATE_INITIAL_TARE:
            # USER PLACES GLASS AND CLICKED A BUTTON 
            if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
                self.tare_scale()
                self.recipe_state = self.RECIPE_RUNNING
            # SYSTEM WAITS FOR INCREASING LOAD ON THE SCALE AND CONTINOUES AUTOMATICALLY
            elif _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
                if _system_command.value > self.last_scale_value:
                    self.tare_scale()
                    self.recipe_state = self.RECIPE_RUNNING




        #if _system_command.type == system_command.system_command.COMMAND_TYPE_TIMER_IRQ:
        #   self.last_timer_event = _system_command
        #elif _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
        #   self.last_scale_event = _system_command
        #elif _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
        #    self.last_user_event = _system_command
        
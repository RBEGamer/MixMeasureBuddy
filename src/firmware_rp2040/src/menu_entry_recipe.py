from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from menu_manager import menu_manager
import recipe_loader
import recipe

class menu_entry_recipe(menu_entry.menu_entry):


   
    recipe_filename: str = ""
    loaded_recipe: recipe.recipe = None

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
        ui().show_recipe_ingredients(self.loaded_recipe.get_ingredients_as_names_list(), True)




    def teardown(self):
        print("teardown {}".format(self.name))
        # UNLOAD RECIPE
        if self.loaded_recipe is not None:
            del self.loaded_recipe
            self.loaded_recipe = None



    def update(self, _system_command: system_command.system_command):
        if self.loaded_recipe is None:
            menu_manager.exit_current_menu()


        #if _system_command.type == system_command.system_command.COMMAND_TYPE_TIMER_IRQ:
        #   self.last_timer_event = _system_command
        #elif _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
        #   self.last_scale_event = _system_command
        #elif _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
        #    self.last_user_event = _system_command
        
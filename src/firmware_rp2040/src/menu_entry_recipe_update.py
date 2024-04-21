from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from recipe_updater import recipe_updater
from menu_manager import menu_manager

class menu_entry_recipe_update(menu_entry.menu_entry):


   

    def __init__(self):
        super().__init__("RECIPE UPDATE", "Update recipes over MixMeasureBuddy API")

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        print("activate {}".format(self.name))
        ui().show_msg("CHECK FOR WIFI CONNECTION")
        if recipe_updater.check_update_url():
            ui().show_msg("WIFI SUCCESS")
        else:
            ui().show_msg("ERROR: CHECK CREDENTIALS")
            return

        ui().show_msg("RECIPE FETCHING STARTED")
        recipe_updater.update_recipes()


        ui().show_msg("DONE: EXIT WITH ANYKEY")

    def teardown(self):
        print("teardown {}".format(self.name))
        recipe_updater.disable_wifi()


    def update(self, _system_command: system_command.system_command):
        if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
            # UPDATE DOES NOTHING EXCEPT GOING BACK TO MAIN MENU
            menu_manager().exit_current_menu()
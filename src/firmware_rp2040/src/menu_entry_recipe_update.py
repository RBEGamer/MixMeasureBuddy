from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from recipe_updater import recipe_updater
from menu_manager import menu_manager
import time
class menu_entry_recipe_update(menu_entry.menu_entry):


    update_ok: bool = False

    def __init__(self):
        super().__init__("RECIPE UPDATE", "Update recipes over MixMeasureBuddy API")

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        self.update_ok = False
        
        print("activate {}".format(self.name))
        try:
            ui().show_msg("CHECK FOR WIFI CONNECTION")
            if recipe_updater.check_update_url():
                ui().show_msg("WIFI SUCCESS")
            else:
                ui().show_msg("ERROR: CHECK CREDENTIALS")
                time.sleep(2)
                menu_manager().exit_current_menu()

            ui().show_msg("RECIPE FETCHING STARTED")
            self.update_ok = recipe_updater.update_recipes()
            if self.update_ok:
                ui().show_recipe_information("PLEASE POWERCYCLE THE DEVICE", "Press NEXT/PREV to show QR Code or URL")
            else:
                ui().show_recipe_information("UPDATE FAILED", "Press NEXT/PREV to show QR Code or URL")

        except Exception as e:
            print(e)
            ui().show_msg("ERROR: UPDATE ERROR")
            time.sleep(2)
            menu_manager().exit_current_menu()


        

    def teardown(self):
        print("teardown {}".format(self.name))
        try:
            recipe_updater.disable_wifi()
        except Exception as e:
            print(e)



    def update(self, _system_command: system_command.system_command):
        if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
            # UPDATE DOES NOTHING EXCEPT GOING BACK TO MAIN MENU
            if not self.update_ok:
                menu_manager().exit_current_menu()
        if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
            if _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                menu_manager().exit_current_menu()
            elif _system_command.action == system_command.system_command.NAVIGATION_LEFT:
                ui().show_device_qr_code(recipe_updater.get_api_url())
            elif _system_command.action == system_command.system_command.NAVIGATION_RIGHT:
                ui().show_url(recipe_updater.get_api_url())
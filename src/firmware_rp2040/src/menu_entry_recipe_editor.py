from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from recipe_updater import recipe_updater
from menu_manager import menu_manager
class menu_entry_recipe_editor(menu_entry.menu_entry):


   

    def __init__(self):
        super().__init__("RECIPE EDITOR", "Shows recipe editor URL")

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        print("activate {}".format(self.name))
        ui().show_recipe_information("PLEASE WAIT", "Press NEXT/PREV to show QR Code or URL")
        

    def teardown(self):
        print("teardown {}".format(self.name))


    def update(self, _system_command: system_command.system_command):
        if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
            if _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                menu_manager().exit_current_menu()
            elif _system_command.action == system_command.system_command.NAVIGATION_LEFT:
                ui().show_device_qr_code(recipe_updater.get_api_url())
            elif _system_command.action == system_command.system_command.NAVIGATION_RIGHT:
                ui().show_url(recipe_updater.get_api_url())
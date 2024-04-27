from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from recipe_updater import recipe_updater
from static_modules.menu_manager import menu_manager
class menu_entry_info(menu_entry.menu_entry):


   

    def __init__(self):
        super().__init__("INFO", "Have a nice day :)")

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        print("activate {}".format(self.name))
        ui().show_titlescreen()


    def teardown(self):
        print("teardown {}".format(self.name))


    def update(self, _system_command: system_command.system_command):
        if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
                menu_manager().exit_current_menu()
           
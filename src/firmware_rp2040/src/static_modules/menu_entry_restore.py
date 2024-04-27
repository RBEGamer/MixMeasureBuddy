from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from recipe_updater import recipe_updater
from static_modules.menu_manager import menu_manager
class menu_entry_restore(menu_entry.menu_entry):

    def __init__(self):
        super().__init__("RESTORE FIRMWARE", "Restore system firmware")

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        print("activate {}".format(self.name))
        ui().show_recipe_information("SURE ?", "Press ok to reset the firmnware. Custom recipes will be deleted")
        ledring().set_neopixel_full(50, 0, 0)

    def teardown(self):
        print("teardown {}".format(self.name))


    def update(self, _system_command: system_command.system_command):
        if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
            if _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                ledring().set_neopixel_full(50, 0, 50)
                try:
                    import machine
                    import fsdatareconstructor
                    fsdatareconstructor.restore(True)
                    machine.reset()
                except Exception as e:
                    print(e)
            else:
                menu_manager().exit_current_menu()
           
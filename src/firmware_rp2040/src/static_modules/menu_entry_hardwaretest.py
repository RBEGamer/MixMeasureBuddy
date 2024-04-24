from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from menu_manager import menu_manager
class menu_entry_hardwaretest(menu_entry.menu_entry):


   
    last_timer_event: system_command.system_command = system_command.system_command()
    last_scale_event: system_command.system_command = system_command.system_command()
    last_user_event: system_command.system_command = system_command.system_command()

    def __init__(self):
        super().__init__("HARDWARE TEST", "Tests the internal hardware")

    def preview(self):
        print("preview c{}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        print("activate {}".format(self.name))
        ui().clear()
        


    def teardown(self):
        print("teardown {}".format(self.name))


    def update(self, _system_command: system_command.system_command):
       
        if _system_command.type == system_command.system_command.COMMAND_TYPE_TIMER_IRQ:
           self.last_timer_event = _system_command
        elif _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
           self.last_scale_event = _system_command
        elif _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
            self.last_user_event = _system_command
            
        ui().show_msg("t:{} a:{} b:{} t:{} s:{}".format(self.last_user_event.type, self.last_user_event.action, self.last_user_event.value, self.last_timer_event.value, self.last_scale_event.value))
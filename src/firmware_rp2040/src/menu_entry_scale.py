from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from Scales import ScaleInterface

class menu_entry_scale(menu_entry.menu_entry):


    WIGHT_CHANGE_DISPLAY_UPDATE: float = 1.0 # UPDAT DISPLAY AFTERLEAST Xg CHANGES
    max_scale_value: float = 0.0
    last_scale_value: float = 0.0
    def __init__(self):
        super().__init__("SCALE", "A normal kitchen scale")

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        print("activate {}".format(self.name))
        ScaleInterface().tare()
        ui().show_scale(ScaleInterface().get_current_weight())
        self.max_scale_value = 10.0
        self.last_scale_value = 0.0
        ledring().set_neopixel_full(10, 10, 10)



    def teardown(self):
        print("teardown {}".format(self.name))


    def update(self, _system_command: system_command.system_command):

        # UPDATE SCALE VALUE
        if _system_command.type == system_command.system_command.COMMAND_TYPE_SCALE_VALUE:
            if abs(_system_command.value - self.last_scale_value) > 0.2:
                self.last_scale_value = _system_command.value
                self.max_scale_value = max(self.max_scale_value, _system_command.value + 10.0)
                ui().show_scale(_system_command.value) 
                
                # ADD SOME NEOPIXEL LIGHTNING
                ledring().set_neopixel_percentage(min(1.0, abs(_system_command.value / self.max_scale_value)))

        # TARE SCALE ON OK BUTTON
        elif _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
            if _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                ScaleInterface().tare()
                self.max_scale_value = 10.0
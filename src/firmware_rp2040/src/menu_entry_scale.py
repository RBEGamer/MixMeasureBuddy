from abc import ABC, abstractmethod
import menu_entry

class menu_entry_scale(menu_entry):

    def __init__():
        super().__init__("SCALE", "A normal kitchen scale")


    @abstractmethod
    def preview(self):
        print("preview {}".format(self.name))
        #ui.ui.show_recipe_information(self.name, self.description)

    @abstractmethod
    def activate(self):
        print("activate {}".format(self.name))

    @abstractmethod
    def teardown(self):
        print("teardown {}".format(self.name))

    @abstractmethod
    def update(self, _system_command: system_command.system_command):
        pass
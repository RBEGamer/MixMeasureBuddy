from abc import ABC, abstractmethod
import ui
import system_command
class menu_entry(ABC):
    


    name: str = ""
    description: str = ""
    def __init__(self, _name: str, _description: str = ""):
        self.name = _name
        self.description = _description
    


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
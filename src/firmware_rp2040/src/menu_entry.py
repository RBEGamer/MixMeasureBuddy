import ui
import system_command
class menu_entry:
    


    name: str = ""
    description: str = ""
    def __init__(self, _name: str, _description: str = ""):
        self.name = _name
        self.description = _description
    



    def preview(self):
        print("preview {}".format(self.name))
        #ui.ui.show_recipe_information(self.name, self.description)

    def activate(self):
        print("activate {}".format(self.name))

    def teardown(self):
        print("teardown {}".format(self.name))

    def update(self, _system_command: system_command.system_command):
        pass
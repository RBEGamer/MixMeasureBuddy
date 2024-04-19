import menu_entry


class menu_command:
    pass

class menu_manager:

    menu_entires: [menu_entry.menu_entry] = []

    current_active_entry: menu_entry.menu_entry = None
    def __init__(self):
        pass

    
    def add_subentries(self, _entry: menu_entry.menu_entry):
        pass



    def process_menu_commands(self, _menu_command: menu_command):
        pass
import menu_entry
import system_command
from singleton import singleton


@singleton
class menu_manager:

    menu_entires: [menu_entry.menu_entry] = []

    current_active_entry: menu_entry.menu_entry = None

    def __init__(self):
        pass

    
    def add_subentries(self, _entry: menu_entry.menu_entry):
        pass


    def process_user_commands(self, _system_command: system_command):
        pass
    
    def process_system_commands(self, _system_command: system_command):
        pass
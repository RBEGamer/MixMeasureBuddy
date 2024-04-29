from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from recipe_updater import recipe_updater
from menu_manager import menu_manager
class menu_entry_submenu(menu_entry.menu_entry):


    MENU_STATE_INACTIVE = 0
    MENU_STATE_ACTIVE = 1

    menu_entires: [menu_entry.menu_entry] = []
    current_active_entry_index: int = -1
    current_menu_state: int = MENU_STATE_INACTIVE

    def __init__(self, _submenu_name: str, _submenu_description: str = ""):
        super().__init__(_submenu_name,_submenu_description)

    def add_subentries(self, _entry: menu_entry.menu_entry):
        self.menu_entires.append(_entry)

        

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)

    def display_preview(self):
        self.get_menu_entry().preview()
        # OPTIONAL DISPLAY LED STATE
        ledring().set_neopixel_spinner(self.current_active_entry_index, len(self.menu_entires), ledring().COLOR_PRESET_HSV_H__PINK, ledring().COLOR_PRESET_HSV_H__BLUE)
    


    def activate(self):
        print("activate {}".format(self.name))

        if len(self.menu_entires) <= 0:
            self.teardown()
            menu_manager().exit_current_menu()

        if self.current_active_entry_index < 0:
            self.current_active_entry_index = 0
            
        self.display_preview()
        self.current_menu_state: int = self.MENU_STATE_INACTIVE

    def teardown(self):
        print("teardown {}".format(self.name))
        if self.get_menu_entry() is not None:
            self.get_menu_entry().teardown()

            
    def get_menu_entry(self) -> menu_entry.menu_entry:
        if self.current_active_entry_index < 0:
            print("no menu_entries added ?")
            return None
        elif self.current_active_entry_index >= len(self.menu_entires):
            self.current_active_entry_index = 0

        return self.menu_entires[self.current_active_entry_index]
    
    def exit_current_menu(self):
        if self.get_menu_entry() is not None:
            self.get_menu_entry().teardown()
            self.display_preview()
        else:
            self.current_active_entry_index = 0

        self.current_menu_state = self.MENU_STATE_INACTIVE

    def update(self, _system_command: system_command.system_command):
        if self.get_menu_entry() is None:
            menu_manager().exit_current_menu()
        
        
        if self.current_menu_state == self.MENU_STATE_INACTIVE:
            if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:

                # SCROL THOUGH MENUS
                if _system_command.action == system_command.system_command.NAVIGATION_LEFT:
                    self.current_active_entry_index = (self.current_active_entry_index + 1) % len(self.menu_entires)
                    print(self.current_active_entry_index)
                    self.display_preview()
                elif _system_command.action == system_command.system_command.NAVIGATION_RIGHT:
                    self.current_active_entry_index = (self.current_active_entry_index - 1) % len(self.menu_entires)
                    self.display_preview()
                # ENTER MENU
                elif _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                    self.get_menu_entry().activate()
                    self.current_menu_state = self.MENU_STATE_ACTIVE

        elif self.current_menu_state == self.MENU_STATE_ACTIVE:
                self.get_menu_entry().update(_system_command)
        else:
            menu_manager().exit_current_menu()


    def process_system_commands(self, _system_command: system_command):
        if self.current_menu_state == self.MENU_STATE_ACTIVE:
            self.get_menu_entry().update(_system_command)
           
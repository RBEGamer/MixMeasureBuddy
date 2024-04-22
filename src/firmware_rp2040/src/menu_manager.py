import menu_entry
import system_command
import ledring
from singleton import singleton


@singleton
class menu_manager:


    MENU_STATE_INACTIVE = 0
    MENU_STATE_ACTIVE = 1

    menu_entires: [menu_entry.menu_entry] = []

    current_active_entry_index: int = -1
    current_menu_state: int = MENU_STATE_INACTIVE

    def __init__(self):
        pass

    
    def add_subentries(self, _entry: menu_entry.menu_entry):

        self.menu_entires.append(_entry)

        # THE FIRST ENTRY ADDED IS THE STARTING ENTRY
        if self.current_active_entry_index < 0:
            self.current_active_entry_index = 0
            self.display_preview()
            
    



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
            self.get_menu_entry().preview()
        else:
            self.current_active_entry_index = 0

        self.current_menu_state = self.MENU_STATE_INACTIVE


    def display_preview(self):
        self.get_menu_entry().preview()

        # OPTIONAL DISPLAY LED STATE
        ledring.ledring().set_neopixel_spinner(self.current_active_entry_index, len(self.menu_entires), ledring.ledring().COLOR_PRESET_HSV_H__PINK, ledring.ledring().COLOR_PRESET_HSV_H__BLUE)
        
    def process_user_commands(self, _system_command: system_command.system_command):
        if self.get_menu_entry() is None:
            return
        
        
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
            if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION and _system_command.action == system_command.system_command.NAVIGATION_EXIT:
                # LEAVE MENU
                self.exit_current_menu()
            # ALL OTHER INPUT WILL BE PASSED TO THE MENU ENTRY ITSELF
            else:
                self.get_menu_entry().update(_system_command)
        else:
            self.exit_current_menu()    


    def process_system_commands(self, _system_command: system_command):
        if self.current_menu_state == self.MENU_STATE_ACTIVE:
            self.get_menu_entry().update(_system_command)

import menu_entry
import system_command
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
            _entry.preview()
            
    



    def get_menu_entry(self) -> menu_entry.menu_entry:
        return self.menu_entires[self.current_active_entry_index]


    def process_user_commands(self, _system_command: system_command.system_command):
        if self.current_active_entry_index is None or self.current_active_entry_index < 0:
            return
        
        
        if self.current_menu_state == self.MENU_STATE_INACTIVE:
            if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:

                # SCROL THOUGH MENUS
                if _system_command.action == system_command.system_command.NAVIGATION_LEFT:
                    self.current_active_entry_index = (self.current_active_entry_index + 1) % len(self.menu_entires)
                    self.get_menu_entry().preview()
                elif _system_command.action == system_command.system_command.NAVIGATION_RIGHT:
                    self.current_active_entry_index = (self.current_active_entry_index - 1) % len(self.menu_entires)
                    self.get_menu_entry().preview()
                # ENTER MENU
                elif _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                    self.get_menu_entry().activate()
                    self.current_menu_state = self.MENU_STATE_ACTIVE

        elif self.current_menu_state == self.MENU_STATE_ACTIVE:
            if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
                # LEAVE MENU
                if _system_command.action == system_command.system_command.NAVIGATION_EXIT:
                    self.get_menu_entry().teardown()
                    self.get_menu_entry().preview()
                    self.current_menu_state = self.MENU_STATE_INACTIVE
                # ALL OTHER INPUT WILL BE PASSED TO THE MENU ENTRY ITSELF
                else:
                    self.get_menu_entry().update(_system_command)
            

    def process_system_commands(self, _system_command: system_command):
        pass
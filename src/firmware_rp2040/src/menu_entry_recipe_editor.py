import menu_entry
import system_command
from ui import ui
from ledring import ledring
from recipe_updater import recipe_updater
from menu_manager import menu_manager
from recipe_editor import recipe_editor
import helper
import config
class menu_entry_recipe_editor(menu_entry.menu_entry):


    
    editor: recipe_editor = None
    init_success: bool = False
    def __init__(self):
        super().__init__("RECIPE EDITOR", "Enable Wifi based online recipe editor")

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        print("activate {}".format(self.name))
        if self.editor is not None:
            self.teardown()

        self.editor = recipe_editor()

        if not self.editor.has_capabilities():
            self.init_success = True
            ui().show_msg("Wifi access point is not supported")
            return
        
        #  CFG_EDITOR_WIFI_STA_SSID CFG_EDITOR_WIFI_STA_PSK
        ssid: str = config.CFG_EDITOR_WIFI_STA_SSID.format(helper.get_system_id())
        psk: str =  config.CFG_EDITOR_WIFI_STA_PSK.format(helper.get_system_id())

        ip: str= self.editor.open_accesspoint(ssid, psk)    
        ui().show_recipe_information(self.name, ip)

        self.editor.setup_webserver()

        self.init_success = True


    def teardown(self):
        print("teardown {}".format(self.name))
        self.editor.stop_webserver()
        self.editor.disable_wifi()
        del editor


    def update(self, _system_command: system_command.system_command):
        if self.init_success:
            self.editor.handle_connection()
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from recipe_updater import recipe_updater
from menu_manager import menu_manager
from recipe_editor import recipe_editor
import helper
import config
import time

class menu_entry_recipe_editor(menu_entry.menu_entry):

    editor: recipe_editor = None
    init_success: bool = False
    def __init__(self):
        super().__init__("RECIPE EDITOR", "Enable Wifi based online recipe editor")

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)

    def exit(self, _reason: str):
        ui().show_msg(_reason)
        time.sleep(2)
        self.teardown()
        menu_manager().exit_current_menu()


    def activate(self):
        print("activate {}".format(self.name))
        if self.editor is not None:
            self.exit("Editor init failed, please report")
            return

        self.editor = recipe_editor()

        if not self.editor.has_capabilities():
            self.init_success = True
            self.exit("Wifi access point is not supported")
            return

        ip: str = ""
        if config.CFG_EDITOR_OPEN_ACCESSPOINT:
            ssid: str = config.CFG_EDITOR_WIFI_STA_SSID.format(helper.get_system_id())
            psk: str =  config.CFG_EDITOR_WIFI_STA_PSK.format(helper.get_system_id())
            ip = self.editor.open_accesspoint(ssid, psk)   
        else:
            ip, success = self.editor.connect_wifi() 
            if not success:
                self.exit("Cant connect to wifi")
                return

        ui().show_recipe_information("Please connect using :", "IP:{}\nSSID:{}\nPSK:{}".format(ip, ssid, psk))

        self.editor.setup_webserver()

        self.init_success = True


    def teardown(self):
        print("teardown {}".format(self.name))
        if self.editor is not None:
            self.editor.stop_webserver()
            self.editor.disable_wifi()
        del editor

    def update(self, _system_command: system_command.system_command):
        if self.init_success:
            self.editor.handle_connection()
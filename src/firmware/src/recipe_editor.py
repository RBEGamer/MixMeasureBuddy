import config
import settings
import time
import helper
import json
import recipe_loader


try:
    import network
    import micropyserver

    class recipe_editor:
        

        server: micropyserver.MicroPyServer = micropyserver.MicroPyServer(port=config.CFG_EDITOR_HTTP_PORT)
        
        def serve_index(self, request):
            self.server.send("THIS IS INDEX PAGE!")

        def serve_recipe(self, request):
            params = micropyserver.get_request_query_params(request)	
            json_repsonse: dict = {}
            if 'filename' in params:
                json_repsonse = recipe_loader.recipe_loader.get_recipe_file_content(params['filename'])
            
            
            self.server.send("HTTP/1.0 200 OK\r\n")
            self.server.send("Content-Type: application/json\r\n\r\n")
            self.server.send(json.dumps(json_repsonse))

        def serve_recipes(self, request):
            json_repsonse: dict = {}
            

            for r in recipe_loader.recipe_loader().list_recpies(_include_description=True):
                filename, name, description = r
                link: str = "/recipe?filename={}".format(filename)
                json_repsonse[filename] = {"name": name, "description": description, "link": link}

            self.server.send("HTTP/1.0 200 OK\r\n")
            self.server.send("Content-Type: application/json\r\n\r\n")
            self.server.send(json.dumps(json_repsonse))


        def __init__(self):
            pass
        

        def has_capabilities(self) -> bool:
            return True
        
        def disable_wifi(self):
            wlan = network.WLAN(network.AP_IF)
            wlan.active(False)
        

        def setup_webserver(self):
            
            # ADD ROUTES
            self.server.add_route("/", self.serve_index)
            self.server.add_route("/index", self.serve_index)
            self.server.on_not_found(self.serve_index) # 404

            self.server.add_route("/recipe", self.serve_recipe)
            self.server.add_route("/recipes", self.serve_recipes)


            self.server.loop_init()

        def stop_webserver(self):
            self.server.stop()

        def handle_connection(self):
            self.server.loop()
   

        def open_accesspoint(self, _ssid: str, _psk: str = None) -> str:

            network.country(config.CFG_NETWORK_WIFICOUNTRY)
            network.hostname(config.CFG_EDITOR_WIFI_STA_HOSTNAME.format("_" + helper.get_system_id()))

            wlan = network.WLAN(network.AP_IF)
            wlan.config(essid=_ssid, password=_psk)
            wlan.active(True)
            
            return wlan.ifconfig()
        
        def connect_wifi() -> tuple(str, bool):
            network.country(config.CFG_NETWORK_WIFICOUNTRY)
            network.hostname(config.CFG_NETWORK_HOSTNAME) #.format(helper.get_system_id()))

            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            
            
            ssid = settings.settings().get_settings_entry(settings.SETTINGS_ENTRIES.NETWORK_WIFI_SSID)
            psk = settings.settings().get_settings_entry(settings.SETTINGS_ENTRIES.NETWORK_WIFI_PSK)
            
            if ssid is None or psk is None:
                print("SSID OR PSK FOR WIFI CONNECTION NOT SET")
                return wlan.ifconfig(), False


            print("CONNECTING TO: {}".format(ssid))
            wlan.connect(ssid, psk)
            timer = 0
            while wlan.isconnected() == False:
                print('Waiting for connection...')
                time.sleep(1)
                timer = timer + 1

                if timer > 10:
                    wlan.active(False)
                    return wlan.ifconfig()
            
            if wlan.isconnected():
                return wlan.ifconfig(), True
            return wlan.ifconfig(), False

      
        

except Exception as e:
        
    class recipe_editor:
        
        def __init__(self):
            pass

        def has_capabilities(self) -> bool:
            return False

        def disable_wifi(self):
            pass
        
        def setup_webserver(self):
            pass
        
        def stop_webserver(self):
            pass

        def handle_connection(self):
            pass

        def open_accesspoint(self, _ssid: str, _psk: str = None) -> str:
            return ""
        
        def connect_wifi() -> tuple(str, bool):
            return False
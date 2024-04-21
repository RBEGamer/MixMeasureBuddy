import config
import settings
import time
import helper
import json

from micropyserver import MicroPyServer


try:
    import network
    import micropyserver

    class recipe_editor:
        

        server: micropyserver.MicroPyServer = micropyserver.MicroPyServer(port=config.CFG_EDITOR_HTTP_PORT)
        
        def serve_index(self, request):
            self.server.send("THIS IS INDEX PAGE!")

        def serve_recipe(self, request):
            params = micropyserver.get_request_query_params(request)

            json_str = json.dumps({"param_one": 1, "param_two": 2})
            self.server.send("HTTP/1.0 200 OK\r\n")
            self.server.send("Content-Type: application/json\r\n\r\n")
            self.server.send(json_str)

        def serve_recipes(self, request):
            params = micropyserver.get_request_query_params(request)

            json_str = json.dumps({"param_one": 1, "param_two": 2})
            self.server.send("HTTP/1.0 200 OK\r\n")
            self.server.send("Content-Type: application/json\r\n\r\n")
            self.server.send(json_str)


        def __init__():
            pass
        

        def has_capabilities(self) -> bool:
            return True
        
        def disable_wifi(self):
            wlan = network.WLAN(network.STA_IF)
            wlan.active(False)
        

        def setup_webserver(self):
            
            # ADD ROUTES
            self.server.add_route("/", self.serve_index)
            self.server.add_route("/index", self.serve_index)

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

            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            wlan.config(essid=_ssid, password=_psk)
            
           
            return wlan.ifconfig()
        


      
        

except Exception as e:
        
    class recipe_updater:
        
        def __init__():
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
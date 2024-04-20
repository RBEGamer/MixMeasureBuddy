import config
import settings
import time
import helper

try:
    import network
    import socket
    import urequests

    class recipe_updater:
        
        @staticmethod
        def disable_wifi():
            wlan = network.WLAN(network.STA_IF)
            wlan.active(False)
        
        @staticmethod
        def connect_wifi() -> bool:
            network.country(config.CFG_NETWORK_WIFICOUNTRY)
            network.hostname(config.CFG_NETWORK_HOSTNAME)

            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            
            
            ssid = settings.settings().set_settings_entry(settings.SETTINGS_ENTRIES.NETWORK_WIFI_SSID)
            psk = settings.settings().set_settings_entry(settings.SETTINGS_ENTRIES.NETWORK_WIFI_PSK)
            
            if ssid is None or psk is None:
                print("SSID OR PSK FOR WIFI CONNECTION NOT SET")
                return False


            print("CONNECTING TO: {}".format(ssid))
            wlan.connect(ssid, psk)
            timer = 0
            while wlan.isconnected() == False:
                print('Waiting for connection...')
                time.sleep(1)
                timer = timer + 1

                if timer > 10:
                    wlan.active(False)
                    return False
            
            if wlan.isconnected():
                return True
            return False
        

        @staticmethod
        def check_update_url() -> str:
            if not recipe_updater.connect_wifi():
                return ""
        
            
            api_endpoint: str = settings.settings.instance().set_settings_entry(settings.SETTINGS_ENTRIES.NETWORK_API_ENPOINT)
            if api_endpoint is None:
                return None

            if 'http://' not in api_endpoint:
                api_endpoint = 'http://' + api_endpoint
            print("check_update_url: set api endpoint url {}".format(api_endpoint))
            
            try:
                # GET LIST OF RECIPES
                final = "{}/{}".format(api_endpoint, str(helper.get_system_id()))
                r = urequests.get(final)
                r.close()
                return api_endpoint        
            except Exception as e:
                print(str(e))
                return None

            
        @staticmethod   
        def update_recipes() -> bool:
            
            api_endpoint: str = recipe_updater.check_update_url()
        
            print("API: {}".format(api_endpoint))
            time.sleep(2)
            try:
                # GET LIST OF RECIPES
                r = urequests.get("{}/{}/recipes".format(api_endpoint, str(helper.get_system_id())),  headers=headers)
                recipe_list = r.json() # ["resipe_file_uri_relative"]
                r.close()
                if recipe_list is not None:
                    # DONWLOAD EACH RECIPE
                    for recipe in recipe_list:
                        r = urequests.get("{}/{}/recipe/{}".format(api_endpoint, str(helper.get_system_id()), recipe),  headers=headers)
                        dl_recipe = r.json() # [{filename_without_ending, recipe}]
                        r.close()

                        if 'recipe' in dl_recipe:
                            settings.settings.instance().write_json_file(dl_recipe['name'] + ".recipe", dl_recipe['recipe'])
                        else:
                            print("cant store reciped data block due to missing recipe dict block")
                        
            except Exception as e:
                print(str(e))
    
                    
                
            recipe_updater.disable_wifi()
            return True
        

except Exception as e:
        
    class recipe_updater:
        
        def disable_wifi():
            pass
        
        def check_update_url() -> str:
            pass

        def connect_wifi() -> bool:
            pass

        def update_recipes() -> bool:
            pass
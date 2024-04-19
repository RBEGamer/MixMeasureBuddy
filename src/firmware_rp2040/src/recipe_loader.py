import machine
import os
import time
import json

from ui import ui
import config
import helper
import example_recipes
import settings


if helper.has_wifi():
    import network
    import socket
    import urequests



class USER_INTERACTION_MODE:
    SCALE = 0
    CONFIRM = 1
    WAIT = 2






class recipe_loader:
    
  
    loaded_recipe = None
    current_recipe_step = None
    settings_instance: settings.settings = None


    def __init__(self, _settings: settings.settings):
        print("recipe_loader: __init__")
         
        self.settings_instance = _settings
        
         
        self.write_initial_settings()
        self.unload_recipe()
        self.create_initial_recipe()
        
    def get_recipe_information(self) -> (str, str):
        if self.loaded_recipe is None:
            return ("invalid", "---")
        
        return (self.loaded_recipe['name'], self.loaded_recipe['description'])
    
    def switch_next_step(self):
        if self.loaded_recipe is None:
            return
        if self.current_recipe_step is None:
            self.current_recipe_step = 0
        steps = self.loaded_recipe['steps']
        n_steps = len(steps)
        if self.current_recipe_step < n_steps:
            self.current_recipe_step = self.current_recipe_step + 1
                  
    def switch_prev_step(self):
        pass
    
    def is_recipe_loaded(self):
        if self.loaded_recipe is not None:
            return True
        return False
        
    def get_current_recipe_step(self) -> (USER_INTERACTION_MODE, str, str, int, int, int, bool): # (action, ingredient, current_step, max_steps, target_weight, finished)
        if self.loaded_recipe is None:
            return (None, None, None, None, None, None, True)
        steps = self.loaded_recipe['steps']
        n_steps = len(steps)
        if self.current_recipe_step is None:
            self.current_recipe_step = 0
        
        if self.current_recipe_step >= n_steps:
             return (None, None, None, None, None, None, True)
            
        step = steps[self.current_recipe_step]
        if step['action'] == 'scale':
            ingredient_name = self.loaded_recipe['ingredients'][step['ingredient']]
            return (USER_INTERACTION_MODE.SCALE, step['action'], ingredient_name, self.current_recipe_step+1, n_steps, step['amount'], False)
        elif step['action'] == 'confirm':     
            return (USER_INTERACTION_MODE.CONFIRM, step['action'], step['text'], self.current_recipe_step+1, n_steps, 0, False)
        elif step['action'] == 'wait':     
            return (USER_INTERACTION_MODE.WAIT, step['action'], step['text'], self.current_recipe_step+1, n_steps, step['amount'], False)
        else:
            return (None, None, None, None, None, None, True)
                    
    def unload_recipe(self):
        self.loaded_recipe = None
        
    def get_ingredient_list(self) -> [str]:
        if self.loaded_recipe is None:
            return []
        rt = []
        ing = self.loaded_recipe['ingredients']
        if ing is None:
            return []
        for k in ing:
            rt.append(ing[k])
        return rt
    
    def get_ingredient_str(self) -> str:
        rt = ""
        for item in self.get_ingredient_list():
            rt = rt + item + "\n"
        return rt
        


    def create_initial_recipe(self):
        for k in example_recipes.EXAMPLE_RECIPES_COLLECTION:
            sefl.settings_instance.write_json_file(k + ".recipe", example_recipes.EXAMPLE_RECIPES_COLLECTION[k])
            with open(self.RECIPE_BASE_DIR + "/" + k, "w") as file:
                file.write(json.dumps(example_recipes.EXAMPLE_RECIPES_COLLECTION[k]))
            
        

    
    

    
    def list_recpies(self) -> (str, str):
        res = []
        for f in self.settings_instance.list_files():
            if f.endswith('.recipe'):
                # f = tequila_sunrise.recipe
                name = f.replace('.recipe', '').replace('_', ' ')
                res.append((f,name))
        return res
    
    def load_recipe(self, _filename: str) -> bool:
         
        if '.recipe' not in _filename:
            _filename = _filename + ".recipe"
            
        if _filename not in self.settings_instance.list_files():
            return False
        
        json_recipe = settings_instance.load_json_file(_filename)
        
        if json_recipe:
            self.loaded_recipe = json_recipe
            return True
    

    def disable_wifi(self):
        if not helper.has_wifi():
            return False
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        
    def connect_wifi(self) -> bool:
        if not helper.has_wifi():
            return False

        network.country(config.CFG_NETWORK_WIFICOUNTRY)
        network.hostname(config.CFG_NETWORK_HOSTNAME)

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        
        
        ssid = self.settings_instance.set_settings_entry(SETTINGS_ENTRIES.NETWORK_WIFI_SSID)
        psk = self.settings_instance.set_settings_entry(SETTINGS_ENTRIES.NETWORK_WIFI_PSK)
        
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
    
    

        
    def check_update_url(self) -> str:
        if not self.connect_wifi():
            return ""
       
        
        api_endpoint: str = self.settings_instance.set_settings_entry(NETWORK_API_ENPOINT.NETWORK_WIFI_SSID)
        if api_endpoint is None:
            return None

        if 'http://' not in api_endpoint:
            api_endpoint = 'http://' + api_endpoint
        print("check_update_url: set api endpoint url {}".format(api_endpoint))
        
        try:
            # GET LIST OF RECIPES
            final = "{}/{}".format(url, str(helper.get_system_id()))
            r = urequests.get(final)
            r.close()
            return api_endpoint        
        except Exception as e:
            print(str(e))
            retrun None

        
        
    def update_recipes(self, _gui: ui.ui) -> bool:
        if not self.connect_wifi():
            return False
        
        api_endpoint: str = self.check_update_url()
        
        _gui.show_msg("API: {}".format(api_endpoint))
        time.sleep(2)
        try:
            # GET LIST OF RECIPES
            r = urequests.get("{}/{}/recipes".format(api_endpoint, str(helper.get_system_id())),  headers=headers)
            recipe_list = r.json() # ["resipe_file_uri_relative"]
            r.close()
            if recipe_list is not None:
                # DONWLOAD EACH RECIPE
                for recipe in recipe_list:
                    _gui.show_msg("recipe update: {}".format(recipe))
                    r = urequests.get("{}/{}/recipe/{}".format(api_endpoint, str(helper.get_system_id()), recipe),  headers=headers)
                    dl_recipe = r.json() # [{filename_without_ending, recipe}]
                    r.close()

                    if 'recipe' in dl_recipe:
                        sefl.settings_instance.write_json_file(dl_recipe['name'] + ".recipe", dl_recipe['recipe'])
                    else:
                        print("cant store reciped data block due to missing recipe dict block")
                    
        except Exception as e:
            _gui.show_msg(str(e))
            print(str(e))
  
                
            
        self.disable_wifi()
        return True
    

    
    
    

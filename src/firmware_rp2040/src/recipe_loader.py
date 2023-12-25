import machine
import sdcard
import uos
import os
import time
import json

from ui import ui
import config
import helper
import example_recipes

if helper.has_wifi():
    import network
    import socket
    import urequests



class USER_INTERACTION_MODE():
    SCALE = 0
    CONFIRM = 1
    WAIT = 2
    
class recipe_loader:
    
    INITIAL_SETTINGS_DATA: dict = {"calibration":
                                   {"sc_min":"0", "sc_full":"50", "sc_weight": config.CFG_CALIBRATION_WEIGHT_WEIGHT},
                                   "wificredentials": [
                                       {"ssid":"Makerspace", "psk": "MS8cCvpE"},
                                       {"ssid":"ProDevMo", "psk": "6226054527192856"}
                                    ],
                                   "api_endpoint": ["mixmeasurebuddy.com/api/mmb", "mixmeasurebuddy.local/api/mmb"]
                                   }
        
    RECIPE_BASE_DIR = "/data"
    loaded_recipe = None
    current_recipe_step = None
    sd = None # sdcard class instance


    def __init__(self, _spi = None, cs_pin = config.CFG_SDCARD_CS_PIN):
        print("recipe_loader: __init__")
        if _spi is None:
            _spi = machine.SPI(config.CFG_SDCARD_SPIINSTANCE, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=machine.SPI.MSB, sck=machine.Pin(config.CFG_SDCARD_SCK_PIN), mosi=machine.Pin(config.CFG_SDCARD_MOSI_PIN), miso=machine.Pin(config.CFG_SDCARD_MISO_PIN))
        # Assign chip select (CS) pin (and start it high)
        self.cs = machine.Pin(cs_pin, machine.Pin.OUT)

        self.sd = None
        try:
            self.sd = sdcard.SDCard(_spi, self.cs)

         # Mount filesystem
            self.vfs = uos.VfsFat(self.sd)
            uos.mount(self.vfs, self.RECIPE_BASE_DIR)
        except Exception as e:
            print("sdcard init failed using local filesystem on /data", str(e))


        if self.sd is None:
            try: 
                os.mkdir(self.RECIPE_BASE_DIR) 
                print("Directory '%s' created successfully" % self.RECIPE_BASE_DIR) 
            except OSError as error: 
                print("Directory '%s' can not be created" % self.RECIPE_BASE_DIR) 
        
        
        print(os.listdir(self.RECIPE_BASE_DIR))
        
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
            with open(self.RECIPE_BASE_DIR + "/" + k, "w") as file:
                file.write(json.dumps(example_recipes.EXAMPLE_RECIPES_COLLECTION[k]))
            
        

    
    def save_calibration_values(self, _scale_calibration_0g: float, _scale_calibration_50g: float):
        cred = {}
        with open(self.RECIPE_BASE_DIR + "/" + "SETTINGS.json", "r") as file:
            cred = json.loads(file.read())
        
        if 'calibration' not in cred:
            self.write_initial_settings()

        cred['calibration']['sc_min'] = str(_scale_calibration_0g)
        cred['calibration']['sc_full'] = str(_scale_calibration_50g)
        cred['calibration']['sc_weight'] = str(config.CFG_CALIBRATION_WEIGHT_WEIGHT)
        print(cred['calibration'])
    
        with open(self.RECIPE_BASE_DIR + "/" + "SETTINGS.json", "w") as file:
            file.write(json.dumps(cred))

    def get_calibration_factor(self):
        cred = {}
        with open(self.RECIPE_BASE_DIR + "/" + "SETTINGS.json", "r") as file:
            cred = json.loads(file.read())
        
        if 'calibration' not in cred:
            self.write_initial_settings()
        
        calibration_values = cred['calibration']
        print(calibration_values)
        sc_min = float(cred['calibration']['sc_min'])
        sc_full = float(cred['calibration']['sc_full'])
        sc_weight = float(cred['calibration']['sc_weight'])
        
        calibration_factor =  (sc_min-sc_full) / sc_weight
        print("get_calibration_factor using ({}-{}) / {} = {}".format(sc_min, sc_full, sc_weight, calibration_factor))
        return calibration_factor

    def write_initial_settings(self):
        if "SETTINGS.json" in os.listdir(self.RECIPE_BASE_DIR):
            return
        with open(self.RECIPE_BASE_DIR + "/" + "SETTINGS.json", "w") as file:
            file.write(json.dumps(self.INITIAL_SETTINGS_DATA))
    
    def list_recpies(self) -> (str, str):
        res = []
        for f in os.listdir(self.RECIPE_BASE_DIR):
            if f.endswith('.recipe'):
                # f = tequila_sunrise.recipe
                name = f.replace('.recipe', '').replace('_', ' ')
                res.append((f,name))
        return res
    
    def load_recipe(self, _filename: str) -> bool:
         
        if '.recipe' not in _filename:
            _filename = _filename + ".recipe"
            
        if _filename not in os.listdir(self.RECIPE_BASE_DIR):
            return False
        
        json_recipe = None
        with open(self.RECIPE_BASE_DIR + "/" + _filename, "r") as file:
            json_recipe = json.loads(file.read())
        
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

        cred = {}
        with open(self.RECIPE_BASE_DIR + "/" + "SETTINGS.json", "r") as file:
            cred = json.loads(file.read())
        
        if "wificredentials" not in cred or len(cred["wificredentials"]) <= 0:
            return False
        
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        
        for wifi in cred["wificredentials"]:
            print(wifi)
            ssid = wifi["ssid"]
            psk = wifi["psk"]
            
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
                break
        return True
    
    

        
    def check_update_url(self) -> str:
        if not self.connect_wifi():
            return ""
        ok_url:str = ""
        
        cred = {}
        with open(self.RECIPE_BASE_DIR + "/" + "SETTINGS.json", "r") as file:
            cred = json.loads(file.read())
        print(cred["api_endpoint"])
        for url in cred["api_endpoint"]:
            if 'http://' not in url:
                url = 'http://' + url
            print(url)
            
            try:
                # GET LIST OF RECIPES
                final = "{}/{}".format(url, str(helper.get_system_id()))
                r = urequests.get(final)
                r.close()
                ok_url = final
                    
            except Exception as e:
                print(str(e))
                
        return ok_url
        
    def update_recipes(self, _gui: ui.ui) -> bool:
        if not self.connect_wifi():
            return False
        
        time.sleep(2)
        
        cred = {}
        with open(self.RECIPE_BASE_DIR + "/" + "SETTINGS.json", "r") as file:
            cred = json.loads(file.read())
        headers={}
        print(cred["api_endpoint"])
        for url in cred["api_endpoint"]:
            if 'http://' not in url:
                url = 'http://' + url
            print(url)
            _gui.show_msg("API: {}".format(url))
            time.sleep(2)
            try:
                # GET LIST OF RECIPES
                r = urequests.get("{}/{}/recipes".format(url, str(helper.get_system_id())),  headers=headers)
                recipe_list = r.json() # ["resipe_file_uri_relative"]
                r.close()
                if recipe_list is not None:
                    # DONWLOAD EACH RECIPE
                    for recipe in recipe_list:
                        _gui.show_msg("recipe update: {}".format(recipe))
                        r = urequests.get("{}/{}/recipe/{}".format(url, str(helper.get_system_id()), recipe),  headers=headers)
                        dl_recipe = r.json() # [{filename_without_ending, recipe}]
                        r.close()
                        with open(self.RECIPE_BASE_DIR + "/" + dl_recipe['name'] + ".recipe", "w") as file:
                            file.write(json.dumps( dl_recipe['recipe']))
                    
            except Exception as e:
                _gui.show_msg(str(e))
                print(str(e))
  
                
            
        self.disable_wifi()
        return True
    

    
    
    

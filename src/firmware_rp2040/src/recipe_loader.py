import machine
import sdcard
import uos
import network
import network
import socket
import os
from utime import sleep_us
import json
import urequests
from helper import get_system_id

class recipe_loader:
    RECIPE_BASE_DIR = "/sd"
    loaded_recipe = None
    
    
    def __init__(self, _spi = None, cs_pin = 9):
        print("recipe_loader: __init__")
        if _spi is None:
            _spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=machine.SPI.MSB, sck=machine.Pin(10), mosi=machine.Pin(11), miso=machine.Pin(8))
        # Assign chip select (CS) pin (and start it high)
        self.cs = machine.Pin(cs_pin, machine.Pin.OUT)

        # Intialize SPI peripheral (start with 1 MHz)
        

        # Initialize SD card
        self.sd = sdcard.SDCard(_spi, self.cs)

        # Mount filesystem
        self.vfs = uos.VfsFat(self.sd)
        uos.mount(self.vfs, self.RECIPE_BASE_DIR)
        
        print(os.listdir(self.RECIPE_BASE_DIR))
        
        
        self.write_initial_settings()
        self.unload_recipe()
        self.create_initial_recipe()
        
    
    def get_recipe_information(self) -> (str, str):
        if self.loaded_recipe is None:
            return ("invalid", "---")
        
        return (self.loaded_recipe['name'], self.loaded_recipe['description'])
        
    def unload_recipe(self):
        self.loaded_recipe = None
        

    def create_initial_recipe(self):
        print("create_initial_recipe: Tequila Sunrise")
        name:str = "Tequila Sunrise"
        filename: str = name.replace(" ","_") + ".recipe"
        recipe: dict = dict()
        
        recipe['name'] = "Tequila Sunrise"
        recipe['description'] = "A nice Tequila Sunrise Cocktail"
        recipe['version'] = "1.0.0"
        recipe['ingredients'] = {'0': 'weißer Tequila','1': 'Orangensaft, ', '2': 'Grenadine'}
        
        steps = []
        steps.append( {'action':'scale', 'ingredient': '0', 'amount': 10}) # scale -> amount in g
        steps.append( {'action':'scale', 'ingredient': '1', 'amount': 120})
        steps.append( {'action':'scale', 'ingredient': '2', 'amount': 20})
        #steps.append( {'action':'confirm', 'text': 'MIX EVERYTHING'})
        recipe['steps'] = steps
       
        
        with open(self.RECIPE_BASE_DIR + "/" + filename, "w") as file:
            file.write(json.dumps(recipe))
    
    def write_initial_settings(self):
        if "SETTINGS.json" in os.listdir(self.RECIPE_BASE_DIR):
            return
        cred = {"wificredentials": [{"ssid":"ProDevMoDev", "psk": "6226054527192856"}], "api_endpoint": ["mixmeasurebuddy.com/api", "marcelochsendorf.com:4243"]}
        with open(self.RECIPE_BASE_DIR + "/" + "WIFI_CREDENTIALS.json", "w") as file:
            file.write(json.dumps(cred))
    
    
    def list_recpies(self) -> (str, str):
        res = []
        for f in os.listdir(self.RECIPE_BASE_DIR):
            if f.endswith('.recipe'):
                # f = tequila_sunrise.recipe
                name = ""
                res.append((f,name))
        return res
    
    def load_recipe(self, _filename: str) -> bool:
         
        # Open the file we just created and read from it
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
    
    def update_recipes(self):
        
        cred = {}
        with open(self.RECIPE_BASE_DIR + "/" + "SETTINGS.json", "r") as file:
            cred = json.loads(file.read())
        
        if "wificredentials" not in cred or len(cred["wificredentials"]) <= 0:
            return False
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        
        connect_ok = False
        for wifi in cred:
            wlan.connect(cred["wificredentials"]["ssid"], cred["wificredentials"]["psk"])
            timer = 0
            while wlan.isconnected() == False:
                print('Waiting for connection...')
                sleep(1)
                timer = timer + 1
                if timer > 5:
                    break
            if wlan.isconnected():
                connect_ok = True
                break
        print(wlan.ifconfig())
        
          
        for url in cred["api_endpoint"]:
            try:
                # GET LIST OF RECIPES
                r = urequests.get("{}/{}/recipes".format(cred["api_endpoint"], str(get_system_id())),  headers=headers)
                recipe_list = r.json() # ["resipe_file_uri_relative"]
                r.close
                
                # DONWLOAD EACH RECIPE
                for recipe in recipe_list:
                    r = urequests.get("{}/{}/{}".format(cred["api_endpoint"], str(get_system_id()), recipe),  headers=headers)
                    dl_recipe = r.json() # [{filename_without_ending, recipe}]
                    r.close
                    with open(self.RECIPE_BASE_DIR + "/" + dl_recipe['name'] + ".recipe", "w") as file:
                        file.write(json.dumps( dl_recipe['recipe']))
                    
            except Exception as e:
                print(str(e))
            
        
        
        
        
        
        # DISABLE WIFI
        wlan.active(False)
    

    
    
    

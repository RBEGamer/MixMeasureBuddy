import sdcard
import machine
import uos
import json
import config
import os
from singleton import singleton

class SETTINGS_ENTRIES(object):
    SCALE_CALIBRATION_MIN_VALUE: str = "scale_min"
    SCALE_CALIBRATION_MAX_VALUE: str = "scale_full"
    SCALE_CALIBRATION_CALIBRATION_WEIGHT: str = "scale_weight"
    SCALE_CALIBRATION_CALIBRATION_WEIGHT: str = "scale_weight"
    SCALE_CALIBRATION_CALIBRATION_INVERT: str = "scale_invert_factor"
    NETWORK_WIFI_SSID: str = "wifi_ssid"
    NETWORK_WIFI_PSK: str = "wifi_psk"
    NETWORK_API_ENPOINT: str = "api_enpoint"



@singleton
class settings(object):

   

    sd = None # sdcard class instance

    RECIPE_BASE_DIR: str = "/data" # FOLDER OF THE SETTINGS FILES STORAGE IF SD CARD FOUND SD CARD WILL BE MOUNTED THERE
    SETTINGS_FILENAME: str = "SETTINGS.json"
     
    def __init__(self, _spi = None, _cs_pin = config.CFG_SDCARD_CS_PIN, _data_dir: str = "/data"):
        self.RECIPE_BASE_DIR = _data_dir

        if _spi is None:
            _spi = machine.SPI(config.CFG_SDCARD_SPIINSTANCE, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=machine.SPI.MSB, sck=machine.Pin(config.CFG_SDCARD_SCK_PIN), mosi=machine.Pin(config.CFG_SDCARD_MOSI_PIN), miso=machine.Pin(config.CFG_SDCARD_MISO_PIN))
        # Assign chip select (CS) pin (and start it high)
        self.cs = machine.Pin(_cs_pin, machine.Pin.OUT)

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


        self.create_settings_file()
        self.create_initial_config()

    def create_settings_file(self):
        settings_dict: dict = {}
        if not self.SETTINGS_FILENAME in self.list_files():
            self.write_json_file(self.RECIPE_BASE_DIR + "/" + self.SETTINGS_FILENAME, settings_dict)

    def create_initial_config(self):
        members = [attr for attr in dir(SETTINGS_ENTRIES) if not callable(getattr(SETTINGS_ENTRIES, attr)) and not attr.startswith("__")]
        # POPULATE CONFIG FILE WITH ALL POSSIBLE KEYS
        for m in members:
            if self.get_settings_entry(m) is not None:
                continue
            self.set_settings_entry(m, None)  


        # ADD SOME DEFAULT VALUES FROM CONFIG

        if self.get_settings_entry(SETTINGS_ENTRIES.NETWORK_WIFI_SSID) is None:
            self.set_settings_entry(SETTINGS_ENTRIES.NETWORK_WIFI_SSID, config.CFG_NETWORK_WIFI_SSID)

        if self.get_settings_entry(SETTINGS_ENTRIES.NETWORK_WIFI_PSK) is None:
            self.set_settings_entry(SETTINGS_ENTRIES.NETWORK_WIFI_PSK, config.CFG_NETWORK_WIFI_PSK)

        if self.get_settings_entry(SETTINGS_ENTRIES.NETWORK_API_ENPOINT) is None:
            self.set_settings_entry(SETTINGS_ENTRIES.NETWORK_API_ENPOINT, config.CFG_NETWORK_API_ENDPOINT)


        if self.get_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_CALIBRATION_INVERT) is None:
            self.set_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_CALIBRATION_INVERT, config.CFG_SCALE_INVERT_WEIGHT_MEASURED_VALUE)
        


        


    def get_settings_entry(self, _key: str) -> any:
        settings_dict: dict = self.load_json_file(self.RECIPE_BASE_DIR + "/" + self.SETTINGS_FILENAME)

        if _key in settings_dict:
            return settings_dict[_key]

        print("get_settings_entry key: {} not found in settings file".format(_key))
        return None
    


    def set_settings_entry(self, _key: str, _value: any):
        settings_dict: dict = self.load_json_file(self.RECIPE_BASE_DIR + "/" + self.SETTINGS_FILENAME)

        settings_dict[str(_key)] = _value

        self.write_json_file(self.RECIPE_BASE_DIR + "/" + self.SETTINGS_FILENAME, settings_dict)



    def get_settings_base_folder_path(self) -> str:
        return self.RECIPE_BASE_DIR

    def list_files(self) ->list[str]:
        return os.listdir(self.RECIPE_BASE_DIR)


    
    def write_json_file(self, _path:str, _dict_content: dict):
        # ADD SETTINGS STORAGE DIRECTORY IF REL PATH IS REQUESTED
        if not _path.startswith("/"):
            _path = self.RECIPE_BASE_DIR + "/" + _path

        with open(_path, "w") as file:
            file.write(json.dumps(_dict_content))


    def load_json_file(self, _path: str) -> dict:

        if not _path.startswith("/"):
            _path = self.RECIPE_BASE_DIR + "/" + _path
        
        # TODO ADD CHECK FOR FILE EXSITS
        try:
            settings_dict: dict = {}
            with open(_path, "r") as file:
                settings_dict = json.loads(file.read())
            return settings_dict
        except Exception as e:
            print(e)
            return {}

    ################ SPECIFIC SETTINGS LOADING FUCTIONS ####################################################


    def save_scale_calibration_values(self, _scale_calibration_0g: float, _scale_calibration_50g: float, _scale_calibration_weight_weight: float = config.CFG_CALIBRATION_WEIGHT_WEIGHT, _scale_invert_factor: float = config.CFG_SCALE_INVERT_WEIGHT_MEASURED_VALUE):
        self.set_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_MIN_VALUE, _scale_calibration_0g)
        self.set_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_MAX_VALUE, _scale_calibration_50g)
        self.set_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_CALIBRATION_WEIGHT, _scale_calibration_weight_weight)
        self.set_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_CALIBRATION_INVERT, _scale_invert_factor)

    
        print("save_scale_calibration_values ({}-{}) / {} with invert factor of: {}".format(_scale_calibration_0g, _scale_calibration_50g, _scale_calibration_weight_weight, _scale_invert_factor))


    
    def get_scale_calibration_factor(self):
        sc_min = 3000.0
        sc_full = 5000.0
        sc_weight = config.CFG_CALIBRATION_WEIGHT_WEIGHT
        sc_invert = config.CFG_SCALE_INVERT_WEIGHT_MEASURED_VALUE
        try:
            sc_min = float(self.get_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_MIN_VALUE))
            sc_full = float(self.get_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_MAX_VALUE))
            sc_weight = float(self.get_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_CALIBRATION_WEIGHT))
            sc_invert = float(self.get_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_CALIBRATION_INVERT))
        except Exception as e:
            self.save_scale_calibration_values(sc_min, sc_full)


        calibration_factor =  (sc_min - sc_full) / sc_weight
        print("get_scale_calibration_factor using ({}-{}) / {} = {} with invert factor of: {}".format(sc_min, sc_full, sc_weight, calibration_factor, sc_invert))
        return calibration_factor * sc_invert
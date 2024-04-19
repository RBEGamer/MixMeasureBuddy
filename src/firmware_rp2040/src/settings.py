import sdcard
import machine
import uos

import config

class SETTINGS_ENTRIES:
    SCALE_CALIBRATION_MIN_VALUE = "sc_min"
    SCALE_CALIBRATION_MAX_VALUE = "sc_full"
    SCALE_CALIBRATION_CALIBRATION_WEIGHT = "sc_weight"

    NETWORK_WIFI_SSID = "ssid"
    NETWORK_WIFI_PSK = "psk"
    NETWORK_API_ENPOINT = "mmb_api_enpoint"




class settings:

    sd = None # sdcard class instance

    RECIPE_BASE_DIR: str = "/data" # FOLDER OF THE SETTINGS FILES STORAGE IF SD CARD FOUND SD CARD WILL BE MOUNTED THERE
    SETTINGS_FILENAME: str = "SETTINGS.json"
    def __init__(_spi = None, _cs_pin = config.CFG_SDCARD_CS_PIN, _data_dir: str = "/data"):
        self.RECIPE_BASE_DIR = _data_dir

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


        self.create_settings_file()


    def create_settings_file():
        settings_dict = {}
        if not self.SETTINGS_FILENAME in self.list_files():
            with open(self.RECIPE_BASE_DIR + "/" + self.SETTINGS_FILENAME, "w") as file:
            file.write(json.dumps(settings_dict))


    def get_settings_entry(_key: str) -> str:
         settings_dict: dict = {}
        with open(self.RECIPE_BASE_DIR + "/" + self.SETTINGS_FILENAME, "r") as file:
            settings_dict = json.loads(file.read())

        if _key in settings_dict:
            return settings_dict[_key]

        print("get_settings_entry key: {} not found in settings file".format(_key))
        return None
    


    def set_settings_entry(_key: str, _value: str):
        settings_dict: dict = {}

        with open(self.RECIPE_BASE_DIR + "/" + self.SETTINGS_FILENAME, "r") as file:
            settings_dict = json.loads(file.read())

        settings_dict[str(_key)] = _value

        with open(self.RECIPE_BASE_DIR + "/" + self.SETTINGS_FILENAME, "w") as file:
            file.write(json.dumps(settings_dict))



    def get_settings_base_folder_path() -> str:
        return self.RECIPE_BASE_DIR

    def list_files() ->[str]:
        return os.listdir(self.RECIPE_BASE_DIR)


    
    def write_json_file(_path:str, _dict_0content: dict):
        # ADD SETTINGS STORAGE DIRECTORY IF REL PATH IS REQUESTED
        if not _path.startswith("/"):
            _path = self.RECIPE_BASE_DIR + "/" + _path

        with open(_path, "w") as file:
            file.write(json.dumps( _dict_0content))


    def load_json_file(_path: str) -> dict:

        if not _path.startswith("/"):
            _path = self.RECIPE_BASE_DIR + "/" + _path
        
        # TODO ADD CHECK FOR FILE EXSITS
        try:
            settings_dict: dict = {}
            with open(self.RECIPE_BASE_DIR + "/" + self.SETTINGS_FILENAME, "r") as file:
                settings_dict = json.loads(file.read())
            return settings_dict
        except Exception as e:
            return None
    ################ SPECIFIC SETTINGS LOADING FUCTIONS ####################################################


    def save_scale_calibration_values(self, _scale_calibration_0g: float, _scale_calibration_50g: float):
        self.set_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_MIN_VALUE, str(_scale_calibration_0g))
        self.set_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_MAX_VALUE, str(_scale_calibration_50g))
        self.set_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_CALIBRATION_WEIGHT, str(config.CFG_CALIBRATION_WEIGHT_WEIGHT))

        print("save_scale_calibration_values ({}-{}) / {}".format(_scale_calibration_0g, _scale_calibration_50g, config.CFG_CALIBRATION_WEIGHT_WEIGHT))


    
    def get_scale_calibration_factor(self):
        sc_min = 0.0
        sc_full = 5000.0
        sc_weight = config.CFG_CALIBRATION_WEIGHT_WEIGHT
        try:
            sc_min = float(self.get_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_MIN_VALUE))
            sc_full = float(self.get_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_MAX_VALUE))
            sc_weight = float(self.get_settings_entry(SETTINGS_ENTRIES.SCALE_CALIBRATION_CALIBRATION_WEIGHT))
        except Exception as e:
            self.save_scale_calibration_values(sc_min, sc_full)


        calibration_factor =  (sc_min-sc_full) / sc_weight
        print("get_scale_calibration_factor using ({}-{}) / {} = {}".format(sc_min, sc_full, sc_weight, calibration_factor))
        return calibration_factor
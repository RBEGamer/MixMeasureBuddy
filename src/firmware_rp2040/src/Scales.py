from singleton import singleton
import time
import math

import hx711
import config
import settings


class Scales(hx711.HX711):

    SCALE_FACTOR: float = 1.0
    def __init__(self, d_out = 5, pd_sck = 12):
        super(Scales, self).__init__(d_out, pd_sck)
        self.offset = 0

    def reset(self):
        self.power_off()
        self.power_on()

    def set_tare_value(self, _offset: float = 0.0):
        self.offset = _offset

    def tare(self):
        self.offset = self.read()

    def raw_value(self):
        return self.read() - self.offset

    def stable_raw_value(self, without_offset: bool = False, reads=10, delay_us=10):     
        stable_values = []
        for i in range(reads):
            if without_offset:
                stable_values.append(self.read())
            else:   
                
                stable_values.append(self.raw_value())
            time.sleep_ms(10)
        
        tare_value = 0.0
        for v in stable_values:
            tare_value = tare_value + v
        
        return tare_value / reads
    
 
    def set_scale(self, _scale_factor: float):
        if _scale_factor is None or _scale_factor == 0.0:
            _scale_factor = 1.0
            print("set _scale_factor to 1.0 due parameter _scale_factor is None or Zero")
        self.SCALE_FACTOR = _scale_factor
        
    def get_unit(self, _stable: bool = False) -> float:
        if self.SCALE_FACTOR == 0.0:
            self.SCALE_FACTOR = 1.0
            
        if _stable:
            return self.raw_value() / self.SCALE_FACTOR
        
        return self.stable_raw_value() / self.SCALE_FACTOR
        

@singleton        
class ScaleInterface:

    scale: Scales = None
    calibration_factor: float = 1.0
    current_tare_value: float = 0
    def __init__(self):
        self.scale = Scales(d_out=config.CFG_HX711_DOUT_PIN, pd_sck=config.CFG_HX711_SCK_PIN)

        self.current_tare_value = 0.0
        self.reload_calibration()
        self.scale.tare() # HARDWARE TARE
        self.tare()
    
    def tare(self):
        self.current_tare_value = self.get_untared_weight()

    def reset_calibration(self):
        self.scale.set_scale(1.0)
        self.scale.set_tare_value(0.0)

    def reload_calibration(self):
        self.calibration_factor = settings.settings().get_scale_calibration_factor()
        print("calibration_factor {}".format(self.calibration_factor))
        self.scale.set_scale(self.calibration_factor)

    def get_untared_weight(self) -> float:
        try:
            return self.scale.get_unit(True)
        except Exception as e:
            return 0.0

    def get_current_weight(self):
        return self.get_untared_weight() - self.current_tare_value

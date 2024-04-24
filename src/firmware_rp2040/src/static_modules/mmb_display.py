import config
import machine


class mmb_display():

    @staticmethod
    def display_instance_creator():
                   
        if config.CFG_DISPLAY_TYPE == "sh1106":
            import sh1106
            i2c = machine.I2C(config.CFG_OLED_I2CINSTANCE, scl=machine.Pin(config.CFG_OLED_SCL_PIN), sda=machine.Pin(config.CFG_OLED_SDA_PIN), freq=400000)
            disp = sh1106.SH1106_I2C(config.SCR_WIDTH, config.SCR_HEIGHT, i2c, None, config.CFG_OLED_ADDR)
            disp.sleep(False)
            return disp

        elif config.CFG_DISPLAY_TYPE == "ssd1306":
            import ssd1306
            i2c = machine.I2C(config.CFG_OLED_I2CINSTANCE, scl=machine.Pin(config.CFG_OLED_SCL_PIN), sda=machine.Pin(config.CFG_OLED_SDA_PIN), freq=400000)
            disp = ssd1306.SSD1306_I2C(config.SCR_WIDTH, config.SCR_HEIGHT, i2c, config.CFG_OLED_ADDR)
            return disp
        return None

    

    
    def __init__(self) -> None:
        pass

    def pixel(self, x, y, value):
        pass
 
    def show():
        pass
      
    def fill_rect(self, x, y, w, h, v):
        pass
    
    def print(self, _str):
        pass

    def write(self, _str):
        pass
    
    def erase(self):
        pass

    def text(self, text, x, y, color=1):
        pass
import config
import machine
import ili934xnew, tt14, sh1106, ssd1306

class mmb_display():

    @staticmethod
    def display_instance_creator():
        
        if config.CFG_DISPLAY_TYPE == "ili934":
            SCR_ROT = 7
            _spi = machine.SPI(config.CFG_ILI9341_SPIINSTANCE, baudrate=15625000, sck=machine.Pin(config.CFG_ILI9341_SCK_PIN), mosi=machine.Pin(config.CFG_ILI9341_MOSI_PIN), miso=machine.Pin(config.CFG_ILI9341_MISO_PIN))
            disp = ili934xnew.ILI9341(_spi, cs=machine.Pin(config.CFG_ILI9341_CS_PIN), dc=machine.Pin(config.CFG_ILI9341_DC_PIN), rst=machine.Pin(config.CFG_ILI9341_RST_PIN), w=config.SCR_WIDTH, h=config.SCR_HEIGHT, r=SCR_ROT)
            disp.set_color(ili934xnew.ILI9341.color565(255, 255, 255), ili934xnew.ILI9341.color565(0, 0, 0))
            disp.display.set_font(tt14)
            return disp

        elif config.CFG_DISPLAY_TYPE == "sh1106":
            i2c = machine.I2C(config.CFG_OLED_I2CINSTANCE, scl=machine.Pin(config.CFG_OLED_SCL_PIN), sda=machine.Pin(config.CFG_OLED_SDA_PIN), freq=400000)
            disp = sh1106.SH1106_I2C(config.SCR_WIDTH, config.SCR_HEIGHT, i2c, None, config.CFG_OLED_ADDR)
            disp.sleep(False)
            disp.fill(0)
            return disp

        elif config.CFG_DISPLAY_TYPE == "ssd1306":
            i2c = machine.I2C(config.CFG_OLED_I2CINSTANCE, scl=machine.Pin(config.CFG_OLED_SCL_PIN), sda=machine.Pin(config.CFG_OLED_SDA_PIN), freq=400000)
            disp = ssd1306.SSD1306_I2C(config.SCR_WIDTH, config.SCR_HEIGHT, i2c, config.CFG_OLED_ADDR)
            return disp

    


    def __init__(self) -> None:
        pass

    # OK
    def pixel(self, x, y, value):
        pass

    # ok
    def show():
        pass

    # OK    
    def fill_rect(self, x, y, w, h, v):
        pass
    
    def print(self, _str):
        pass


    def write(self, _str):
        pass
    
    # ok
    def erase(self):
        pass

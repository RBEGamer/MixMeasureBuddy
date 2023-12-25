import config
import machine


class mmb_display():

    @staticmethod
    def display_instance_creator():
        
        if config.CFG_DISPLAY_TYPE == "ili934":
            import ili934xnew
            import tt14
            SCR_ROT = 7
            _spi = machine.SPI(config.CFG_ILI9341_SPIINSTANCE, baudrate=15625000, sck=machine.Pin(config.CFG_ILI9341_SCK_PIN), mosi=machine.Pin(config.CFG_ILI9341_MOSI_PIN), miso=machine.Pin(config.CFG_ILI9341_MISO_PIN))
            disp = ili934xnew.ILI9341(_spi, cs=machine.Pin(config.CFG_ILI9341_CS_PIN), dc=machine.Pin(config.CFG_ILI9341_DC_PIN), rst=machine.Pin(config.CFG_ILI9341_RST_PIN), w=config.SCR_WIDTH, h=config.SCR_HEIGHT, r=SCR_ROT)
            disp.set_color(ili934xnew.ILI9341.color565(255, 255, 255), ili934xnew.ILI9341.color565(0, 0, 0))
            disp.display.set_font(tt14)
            return disp

        elif config.CFG_DISPLAY_TYPE == "st7789":
            import st7789
            import vga2_8x8
            SCR_ROT = 7
            _spi = machine.SPI(config.CFG_ST7789_SPIINSTANCE, baudrate=60000000, sck=machine.Pin(config.CFG_ST7789_SCK_PIN), mosi=machine.Pin(config.CFG_ST7789_MOSI_PIN), miso=machine.Pin(config.CFG_ST7789_MISO_PIN))
            disp = st7789.ST7789(_spi, config.SCR_WIDTH, config.SCR_HEIGHT, reset=machine.Pin(config.CFG_ST7789_RST_PIN), dc=machine.Pin(config.CFG_ST7789_DC_PIN), rotation=SCR_ROT, cs=machine.Pin(config.CFG_ST7789_CS_PIN))
            disp.display.set_font(vga2_8x8)
            return disp
            
        elif config.CFG_DISPLAY_TYPE == "sh1106":
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
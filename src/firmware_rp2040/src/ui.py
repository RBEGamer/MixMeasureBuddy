import config

#if config.CFG_DISPLAY_TYPE == "ili934":
from ili934xnew import ILI9341, color565
#elif config.CFG_DISPLAY_TYPE == "ssd1306":
import ssd1306
#elif config.CFG_DISPLAY_TYPE == "sh1106":
import sh1106


import glcdfont
import tt14
import tt24
import tt32
import machine
from helper import get_system_id
class ui:
    
    def display_write(self, _str:str):
        s = _str.replace("ß", "ss").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue")
        self.display.write(s)
        
    def display_print(self, _str:str):
        s = _str.replace("ß", "ss").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue")
        self.display.print(s)
    
    
    

    def erase(self):
        # with used lib ili934 needs two rease commands....
        if config.CFG_DISPLAY_TYPE == "ili934":
            self.display.erase()
            self.display.erase()
        elif config.CFG_DISPLAY_TYPE == "ssd1306":
            self.fill(0)
            self.show()
        elif config.CFG_DISPLAY_TYPE == "sh1106":
            self.fill(0)
            self.show()



    def __init__(self):

        
           

        # DISPLAY SETTINGS
        if config.CFG_DISPLAY_TYPE == "ili934":
            self.SCR_WIDTH = 160
            self.SCR_HEIGHT = 128
            SCR_ROT = 7
            _spi = machine.SPI(config.CFG_ILI9341_SPIINSTANCE, baudrate=15625000, sck=machine.Pin(config.CFG_ILI9341_SCK_PIN), mosi=machine.Pin(config.CFG_ILI9341_MOSI_PIN), miso=machine.Pin(config.CFG_ILI9341_MISO_PIN))
            self.display = ILI9341(_spi, cs=machine.Pin(config.CFG_ILI9341_CS_PIN), dc=machine.Pin(config.CFG_ILI9341_DC_PIN), rst=machine.Pin(config.CFG_ILI9341_RST_PIN), w=self.SCR_WIDTH, h=self.SCR_HEIGHT, r=SCR_ROT)
            # SET COLOR AN COLOR DISPLAY TO BLACK WHITE
            self.display.set_color(color565(255, 255, 255), color565(0, 0, 0))
        elif config.CFG_DISPLAY_TYPE == "sh1106":
            self.SCR_WIDTH = 128
            self.SCR_HEIGHT = 64
            i2c = machine.I2C(config.CFG_OLED_I2CINSTANCE, scl=machine.Pin(config.CFG_OLED_SCL_PIN), sda=machine.Pin(config.CFG_OLED_SDA_PIN), freq=400000)
            self.display = sh1106.SH1106_I2C(self.SCR_WIDTH, self.SCR_HEIGHT, i2c, None, config.CFG_OLED_ADDR)


        elif config.CFG_DISPLAY_TYPE == "ssd1306":
            self.SCR_WIDTH = 128
            self.SCR_HEIGHT = 64
            i2c = machine.I2C(config.CFG_OLED_I2CINSTANCE, scl=machine.Pin(config.CFG_OLED_SCL_PIN), sda=machine.Pin(config.CFG_OLED_SDA_PIN), freq=400000)
            self.display = ssd1306.SSD1306_I2C(self.SCR_WIDTH, self.SCR_HEIGHT, i2c, config.CFG_OLED_ADDR)

       

         
        self.erase()
       
        self.display.set_font(tt24)
        
        self.last_display_source: int = -1
        
        self.last_display_content = "."
    
  
    
    def show_msg(self, _message: str = ""):
        full_refresh = False
        if self.last_display_source != 0 or _message != self.last_display_content:
            self.last_display_content = _message
            full_refresh = True
            self.erase()
            self.last_display_source = 0

            self.display.set_pos(10,40)
            
            if len(_message) > 12:
                    self.display.set_font(tt14)
            else:
                self.display.set_font(tt24)
            
            self.display_print("{}".format(_message))
        
  
        
    def show_recipe_information(self, _name:str, _description: str = ""):
        full_refresh = False
        if self.last_display_source != 1:
            full_refresh = True
        self.last_display_source = 1
        
        if full_refresh:
            self.erase()

            self.display.set_pos(0, 10)
            self.display.set_font(tt24)
            self.display_print("{}".format(_name))
            
            
            #self.display.set_pos(0, 90)
            self.display.set_font(tt14)
            self.display_print("{}".format(_description))
    
    
    def set_full_refresh(self):
        self.last_display_source = -1
        
        
    def show_recipe_step(self, _action: str, _ingredient: str, _current_step: int, _max_steps: int):
        full_refresh = False
        if self.last_display_source != 2:
            full_refresh = True
        self.last_display_source = 2
        if full_refresh:
            self.erase()

            
            
            self.display.set_pos(50, 10)
            self.display_print("{}".format(_action))
            self.display.set_font(tt24)
            
            self.display.set_pos(0, 35)
            
            chars_row = 30
            if _ingredient is None:
                pass
            elif len(_ingredient) < 11:
                chars_row =10
                self.display.set_font(tt32)
            elif len(_ingredient) < 15:
                chars_row = 15
                self.display.set_font(tt24)
            else:
                chars_row = 30
                self.display.set_font(tt14)
            self.display_print("{}".format(_ingredient))
            
            # SHOW STEPS
            self.display.set_pos(60, 90)
            self.display.set_font(tt24)
            self.display_print("{} / {}".format(_current_step, _max_steps))
             
         
        
              
        
    def show_titlescreen(self):
        self.last_display_source = 3
        self.erase()
        self.display.set_font(tt32)
        self.display.set_pos(25,10)
        self.display_write("   Mix")
        self.display.set_pos(25,45)
        self.display_write("Measure")
        self.display.set_pos(25,80)
        self.display_write(" Buddy")
        
        self.display.set_font(tt14)
        self.display.set_pos(10,115)
        self.display_write("ID: {}".format(get_system_id()))
    
    
    def show_recipe_ingredients(self, _ingredients: [str]):
        full_refresh = False
        if self.last_display_source != 4:
            full_refresh = True
        self.last_display_source = 4
        
        if full_refresh:
            self.display.erase()
            self.display.set_font(tt24)
            self.display.set_pos(5,10)
            self.display_write("Ingredients")
            
            self.display.set_font(tt14)
            y = 30
            step = 15
            for item in _ingredients:
                y = y + step
                self.display.set_pos(0,y)
                self.display_print("* {}".format(item))
    
      
    def show_scale(self, _value: int):
        full_refresh = False
        if self.last_display_source != 5:
            full_refresh = True
        self.last_display_source = 5
        
        if full_refresh:
            self.display.erase()
            self.display.set_pos(0, 10)
            self.display.set_font(tt24)
            self.display_print("{}".format("SCALE MODE"))
            

        self.display.set_pos(40, 60)

        self.display_print("{:04d}g".format(_value))
       

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
    


    def display_text(self, _str:str, _wrap:bool = False, _pos_x_percentage:int = 0, _pos_y_percentage:int = 0):

        _str = _str.replace("ß", "ss").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue")

         #if len(_message) > 12:
         #           self.display.set_font(tt14)
         #   else:
         #       self.display.set_font(tt24)
        x: int = int((self.SCR_WIDTH / 100.0) * _pos_x_percentage)
        y: int = int((self.SCR_HEIGHT / 100.0) * _pos_y_percentage)

       
        
        if config.CFG_DISPLAY_TYPE == "ili934":

            self.display.set_pos(x, y)
            
            if _wrap:
                 self.display.print(_str)
            else:
                 self.display.write(_str)
        
        elif config.CFG_DISPLAY_TYPE == "ssd1306" or config.CFG_DISPLAY_TYPE == "sh1106":
            if not _wrap:
                self.display.text(_str, x, y)
                self.display.show()
                return
            

            # WRAP TEXT
            words = []
            new_lines = _str.split(" ")
            for l in new_lines:
                if not l == " ": 
                    for w in str(l).split(" "):
                        if not w == " ":
                            words.append(w)
            
            chars_left = 1 + (self.SCR_WIDTH - x)/ int(config.CFG_DISPLAY_CHAR_WIDTH)
            print("chars_left: {}".format(chars_left))
            words_written = 0
            line_y = y
            print(words)
            for w in words:
                w_space = "{} ".format(w)


                if (words_written+len(w_space)) >= chars_left:
                    print("line_y:{}".format(line_y))
                    words_written = 0
                    line_y = line_y + int(config.CFG_DISPLAY_LINE_SPACING)


                print("w: {}".format(w_space, line_y)) 
                xpos = x + words_written * int(config.CFG_DISPLAY_CHAR_WIDTH)
                self.display.text(w_space, xpos, line_y)

                words_written = words_written + len(w_space)

                if words_written >= chars_left:
                    print("line_y:{}".format(line_y))
                    words_written = 0
                    line_y = line_y + int(config.CFG_DISPLAY_LINE_SPACING)
                
            self.display.show()
           



    
    
    

    def erase(self):
        # with used lib ili934 needs two rease commands....
        if config.CFG_DISPLAY_TYPE == "ili934":
            self.display.erase()
            self.display.erase()
        elif config.CFG_DISPLAY_TYPE == "ssd1306":
            self.display.fill(0)
            self.display.show()
        elif config.CFG_DISPLAY_TYPE == "sh1106":
            self.display.fill(0)
            self.display.show()



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
            self.display.set_font(tt14)
        elif config.CFG_DISPLAY_TYPE == "sh1106":
            self.SCR_WIDTH = 128
            self.SCR_HEIGHT = 64
            i2c = machine.I2C(config.CFG_OLED_I2CINSTANCE, scl=machine.Pin(config.CFG_OLED_SCL_PIN), sda=machine.Pin(config.CFG_OLED_SDA_PIN), freq=400000)
            self.display = sh1106.SH1106_I2C(self.SCR_WIDTH, self.SCR_HEIGHT, i2c, None, config.CFG_OLED_ADDR)
            self.display.sleep(False)
            self.display.fill(0)

        elif config.CFG_DISPLAY_TYPE == "ssd1306":
            self.SCR_WIDTH = 128
            self.SCR_HEIGHT = 64
            i2c = machine.I2C(config.CFG_OLED_I2CINSTANCE, scl=machine.Pin(config.CFG_OLED_SCL_PIN), sda=machine.Pin(config.CFG_OLED_SDA_PIN), freq=400000)
            self.display = ssd1306.SSD1306_I2C(self.SCR_WIDTH, self.SCR_HEIGHT, i2c, config.CFG_OLED_ADDR)

       

         
        self.erase()

        self.last_display_source: int = -1
        self.last_display_content = "."
    
  
    
    def show_msg(self, _message: str = ""):

        if self.last_display_source != 0 or _message != self.last_display_content:
            self.last_display_content = _message

            self.erase()
            self.display_text("{}".format(_message), True, 0, 0)

            self.last_display_source = 0
 
        
  
        
    def show_recipe_information(self, _name:str, _description: str = ""):
        full_refresh = False
        if self.last_display_source != 1:
            full_refresh = True
        self.last_display_source = 1
        
        if full_refresh:
            self.erase()

            self.display_text("{}".format(_name), True, 0, 7)
            self.display_text("{}".format(_description), True, 0, 35)
          
    
    
    def set_full_refresh(self):
        self.last_display_source = -1
        
        
    def show_recipe_step(self, _action: str, _ingredient: str, _current_step: int, _max_steps: int):
        full_refresh = False
        if self.last_display_source != 2:
            full_refresh = True
        self.last_display_source = 2
        if full_refresh:
            self.erase()

            
            
           
            self.display_text("{}".format(_action), True, 31, 7)
           
            
            chars_row = 30
            if _ingredient is None:
                pass
            elif len(_ingredient) < 11:
                chars_row =10
                #self.display.set_font(tt32)
            elif len(_ingredient) < 15:
                chars_row = 15
                #self.display.set_font(tt24)
            else:
                chars_row = 30
                #self.display.set_font(tt14)


            self.display_text("{}".format(_ingredient), True, 0, 27)
            
            # SHOW STEPS
            self.display_text("{} / {}".format(_current_step, _max_steps), True, 37, 70)


             
         
        
              
        
    def show_titlescreen(self):
        self.last_display_source = 3
        self.erase()

        self.display_text("MIX", True, 15, 7)
        self.display_text("MEASURE", True, 15, 35)
        self.display_text("BUDDY", True, 15, 62)
        self.display_text("ID: {}".format(get_system_id()), True, 7, 89)
    
    
    def show_recipe_ingredients(self, _ingredients: [str]):
        full_refresh = False
        if self.last_display_source != 4:
            full_refresh = True
        self.last_display_source = 4
        
        if full_refresh:
            self.display.erase()

            self.display_text("Ingredients", True, 3, 7)
 
            y = 23
            step = 11
            for item in _ingredients:
                y = y + step
                self.display_text("* {}".format(item), True, 0, y)

    
      
    def show_scale(self, _value: int):
        self.last_display_source = 5
        self.erase()
        self.display_text("SCALE MODE", True, 0, 7)
        self.display_text("      ", True, 25, 50)
        self.display_text("{:04d}g".format(_value), True, 25, 50)
       

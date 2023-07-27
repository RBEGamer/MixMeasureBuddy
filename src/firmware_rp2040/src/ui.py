from ili934xnew import ILI9341, color565
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
    
    
  
    
    def __init__(self, _spi = None, _cs_pin = 13, _rst_pin = 14, _dc_pin = 15):

        if _spi is None:
            _spi = machine.SPI(0, baudrate=15625000, sck=machine.Pin(6), mosi=machine.Pin(7), miso=machine.Pin(4))

        # DISPLAY SETTINGS
        self.SCR_WIDTH = 160
        self.SCR_HEIGHT = 128
        SCR_ROT = 7


        self.display = ILI9341(_spi, cs=machine.Pin(13), dc=machine.Pin(15), rst=machine.Pin(14), w=self.SCR_WIDTH, h=self.SCR_HEIGHT, r=SCR_ROT)
        self.display.erase()
        # leeren des Displays
        self.display.erase()
        # setzen der Schriftgröße  
        self.display.set_font(tt24)
        
        self.last_display_source: int = -1
        
        self.last_display_content = "."
    
    
    #def show_error(self, _errmsg: str = ""):
    #    self.last_display_source = 0
    
    
    def show_msg(self, _message: str = ""):
        full_refresh = False
        if self.last_display_source != 0 or _message != self.last_display_content:
            self.last_display_content = _message
            full_refresh = True
            self.display.erase()
            self.last_display_source = 0
            self.display.set_color(color565(255, 255, 255), color565(0, 0, 0))
            self.display.set_pos(0,0)
            
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
            self.display.erase()
            self.display.set_color(color565(255, 255, 255), color565(0, 0, 0))
            self.display.set_pos(0, 10)
            self.display.set_font(tt24)
            self.display_print("{}".format(_name))
            
            
            #self.display.set_pos(0, 90)
            self.display.set_font(tt14)
            self.display_print("{}".format(_description))
        
    def show_recipe_step(self, _action: str, _ingredient: str, _scale_val: int, _target_val: int):
        full_refresh = False
        if self.last_display_source != 2:
            full_refresh = True
        self.last_display_source = 2
        if full_refresh:
            self.display.erase()
            self.display.set_color(color565(255, 255, 255), color565(0, 0, 0))
            self.display.set_pos(0, 10)
            
            chars_row = 30
            if len(_ingredient) < 11:
                chars_row =10
                self.display.set_font(tt32)
            elif len(_ingredient) < 15:
                chars_row = 15
                self.display.set_font(tt24)
            else:
                chars_row = 30
                self.display.set_font(tt14)
            self.display_print("{}".format(_ingredient))
         
         
        
        #color_value =  -1.0
        #if _target_val is not None:
        #    color_value = 1.0 - (_scale_val / _target_val) # 0-1.0
        #if not full_refresh:
        #    self.display.fill_rectangle(45, 50, self.SCR_WIDTH, 32)
        #self.display.set_pos(45, 50)
        # B G R
        #if color_value < 1.0 and color_value > 0.0:
        #    self.display.set_color(color565(0, int((1.0 - color_value) * 255), int(color_value*255)), color565(0, 0, 0))
        #else:
        #    self.display.set_color(color565(255, 255, 255), color565(0, 0, 0))
            
            
        #self.display.set_font(tt32)
        #if _target_val is not None:
        #    self.display_print("{} / {}g".format(int(_scale_val), int(_target_val)))
        #else:
        #    self.display_print("{}g".format(int(_scale_val)))
        

        
        
    def show_titlescreen(self):
        self.last_display_source = 3
        self.display.erase()
        self.display.set_color(color565(255, 255, 255), color565(0, 0, 0))
        self.display.set_font(tt32)
        self.display.set_pos(25,10)
        self.display_write("   Mix")
        self.display.set_pos(25,40)
        self.display_write("Measure")
        self.display.set_pos(25,80)
        self.display_write(" Buddy")
        
        self.display.set_font(tt14)
        self.display.set_pos(0,110)
        self.display_write("ID: {}".format(get_system_id()))
        
        
       

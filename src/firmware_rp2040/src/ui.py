from singleton import singleton
import config
import mmb_display
import uQR
import helper

@singleton
class ui:
    
  
    

    display: mmb_display



    def pixel(self, x, y, value):
        self.display.pixel(x, y, value)
        
    def show(self):
            self.display.show()
        
    def display_rect(self, _pos_x_percentage:int, _pos_y_percentage:int, _pos_x_end_perc:int, _pos_y_end_perc):
        x: int = int((config.SCR_WIDTH / 100.0) * _pos_x_percentage)
        y: int = int((config.SCR_HEIGHT / 100.0) * _pos_y_percentage)
        
        xe: int = int((config.SCR_WIDTH / 100.0) * _pos_x_end_perc)
        ye: int = int((config.SCR_HEIGHT / 100.0) * _pos_y_end_perc)
        

        self.display.fill_rect(x, y, abs(x-xe), abs(y-ye), 0) # 0 = BG COLOR
        self.display.show()
        
        
    def display_text(self, _str:str, _wrap:bool = False, _pos_x_percentage:int = 0, _pos_y_percentage:int = 0):
        _str = _str.replace("ß", "ss").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue")

        x: int = int((config.SCR_WIDTH / 100.0) * _pos_x_percentage)
        y: int = int((config.SCR_HEIGHT / 100.0) * _pos_y_percentage)

        if not _wrap:
            self.display.text(_str, x, y)
            self.display.show()
            return
            

        # WRAP TEXT
        words = []
        new_lines = _str.split("\n")
        for l in new_lines:
            if not l == " ": 
                for w in str(l).split(" "):
                    if not w == " ":
                        words.append(w)
        
        chars_left = 1 + (config.SCR_WIDTH - x)/ int(config.CFG_DISPLAY_CHAR_WIDTH)
        #print("chars_left: {}".format(chars_left))
        words_written = 0
        line_y = y
        #print(words)
        for w in words:
            w_space = "{} ".format(w)


            if (words_written+len(w_space)) >= chars_left:
                #print("line_y:{}".format(line_y))
                words_written = 0
                line_y = line_y + int(config.CFG_DISPLAY_LINE_SPACING)


            #print("w: {}".format(w_space, line_y)) 
            xpos = x + words_written * int(config.CFG_DISPLAY_CHAR_WIDTH)
            self.display.text(w_space, xpos, line_y)

            words_written = words_written + len(w_space)

            if words_written >= chars_left:
                #print("line_y:{}".format(line_y))
                words_written = 0
                line_y = line_y + int(config.CFG_DISPLAY_LINE_SPACING)
            
        self.display.show()
           


    def __init__(self):
        # CREATE A DISPLAY INSTANCE
        self.display = mmb_display.mmb_display.display_instance_creator()

        if self.display is None:
            print("invalid display config")

         
        self.display.erase()

        self.last_display_source: int = -1
        self.last_display_content = "."
    
    
    def clear(self):
        self.display.erase()
        self.set_full_refresh()
    
    def show_msg(self, _message: str = ""):

        if self.last_display_source != 0 or _message != self.last_display_content:
            self.last_display_content = _message

            self.display.erase()
            self.display_text("{}".format(_message), True, 0, 0)

            self.last_display_source = 0
 

    def show_url(self, _url: str = ""):
        
        splitted_url: str = ""
        index: int = 0
        split_after_chars = int((config.SCR_WIDTH / config.CFG_DISPLAY_CHAR_WIDTH) * 0.95)
        for w in _url:
            index = index + 1

            splitted_url = splitted_url + w

            if index >= split_after_chars:
                splitted_url = splitted_url + " "
                index = 0
        
        self.display.erase()
        self.display_text("{}".format(splitted_url), True, 0, 0)
        
        
    def show_recipe_information(self, _name:str, _description: str = ""):
        full_refresh = False
        if self.last_display_source != 1:
            full_refresh = True
        self.last_display_source = 1
        
        full_refresh = True
        if full_refresh:
            self.display.erase()

            self.display_text("{}".format(_name), True, 0, 7)
            self.display_text("{}".format(_description), True, 0, 35)
          
    
    
    def set_full_refresh(self):
        self.last_display_source = -1
        
     
    def show_recipe_step(self, _action: str, _ingredient: str, _current_step: int, _max_steps: int):
        full_refresh = False
        if self.last_display_source != 2:
            full_refresh = True
        self.last_display_source = 2

        full_refresh = True
        if full_refresh:
            self.display.erase()

            self.display_text("{}".format(_action), True, 31, 7)
           
            self.display_text("{}".format(_ingredient), True, 0, 27)    
            # SHOW STEPS
            self.display_text("{} / {}".format(_current_step, _max_steps), True, 37, 90)


             
         
        
              
        
    def show_titlescreen(self):
        full_refresh = False
        if self.last_display_source != 3:
            full_refresh = True
        self.last_display_source = 3
        
        full_refresh = True
        if full_refresh:
            self.display.erase()
            self.display_text("MIX", True, 25, 10)
            self.display_text("MEASURE", True, 25, 30)
            self.display_text("BUDDY", True, 25, 50)
            self.display_text("{}".format(helper.get_system_id()), True, 7, 70)
    
    
    def show_recipe_ingredients(self, _ingredients: [str], _force_refresh: bool = True):
        full_refresh = False
        if self.last_display_source != 4 or _force_refresh:
            full_refresh = True
        self.last_display_source = 4
        
        full_refresh = True
        if full_refresh:
            self.display.erase()
            self.display_text("Ingredients", True, 0, 7)
 
        text = ""
        for item in _ingredients:
            text = text + "{}\n".format(item)
                
            self.display_text(text, True, 0, 30)

    
      
    def show_scale(self, _value: int):
        _value = int(_value)
        full_refresh = False
        if self.last_display_source != 5:
            full_refresh = True
        self.last_display_source = 5
        
        full_refresh = True
        if full_refresh:
            self.display.erase()
            self.display_text("SCALE MODE", True, 0, 7)
        
        self.display_rect(25,50, 100, 60)
        self.display_text("{:04d}g".format(_value), True, 25, 50)
    

    def show_device_qr_code(self, _url:str = "", _offset_x:int = 0, _offset_y:int = 0):
        full_refresh = False
        if self.last_display_source != 6:
            full_refresh = True
        self.last_display_source = 6
        
        full_refresh = True
        if full_refresh:
            self.display.erase()
            
            qr = uQR.QRCode()
            if _url == "":
                qr.add_data("{}".format(helper.get_system_id()))
            else:
                qr.add_data("{}".format(_url))
            matrix = qr.get_matrix()
            for y in range(len(matrix)*2):                   
                for x in range(len(matrix[0])*2):            
                    value = not matrix[int(y/2)][int(x/2)]   
                    self.pixel(x + _offset_x, y + _offset_y, value)
        self.show()  


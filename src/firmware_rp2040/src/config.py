# DONT CHANGE
SCR_WIDTH = 0
SCR_HEIGHT = 0



# HARDWARE CONFIG STARTS HERE


# ssd1306 = 128x64 olded with ssd1306 controller
# sh1106 = 128x64 olded with ssh1106 controller
# ili934 =  TFT 3,2 Zoll, 240x320 with ILI934 controller
CFG_DISPLAY_TYPE = "st7789" # sh1106 sh1106 ssd1306 ili934
CFG_CALIBRATION_WEIGHT_WEIGHT = 50
CFG_SCALE_GLASS_ADDITION_NEXT_STEP_WEIGHT = 50 # Xg more on scale to trigger next step in recipe => 1/3 weight of a typical glass
CFG_USER_LONG_BUTTON_PRESS_TIME = 1000 # time to regsiter a long button press in ms
CFG_NETWORK_HOSTNAME = "mixandmeasureberry" # xXxX.local
CFG_NETWORK_WIFICOUNTRY = "DE" # DE US
CFG_DISPLAY_USER_QR_CODE = True # True False
CFG_NEOPIXEL_LED_COUNT = 26 #60
CFG_NEOPIXEL_LED_START_OFFSET = (CFG_NEOPIXEL_LED_COUNT/2) # MAX CFG_NEOPIXEL_LED_COUNT TO ROTATE THE STARTPOINT
# PIN CONFIG

CFG_NEOPIXEL_PIN = 28

CFG_BUTTON_UP_PIN = 22
CFG_BUTTON_DOWN_PIN = 2


CFG_HX711_DOUT_PIN = 5
CFG_HX711_SCK_PIN = 12


CFG_SDCARD_SPIINSTANCE = 1
CFG_SDCARD_SCK_PIN = 10
CFG_SDCARD_MOSI_PIN = 11
CFG_SDCARD_MISO_PIN = 8
CFG_SDCARD_CS_PIN = 9

# IF ili934 IS USED
CFG_ILI9341_SPIINSTANCE = 0
CFG_ILI9341_SCK_PIN = 6
CFG_ILI9341_MOSI_PIN = 7
CFG_ILI9341_MISO_PIN = 4
CFG_ILI9341_CS_PIN = 13
CFG_ILI9341_RST_PIN = 14
CFG_ILI9341_DC_PIN = 15
if CFG_DISPLAY_TYPE == "ili934":
    SCR_WIDTH = 160
    SCR_HEIGHT = 128


CFG_ST7789_SPIINSTANCE = 0
CFG_ST7789_SCK_PIN = 18
CFG_ST7789_MOSI_PIN = 19
CFG_ST7789_MISO_PIN = 16
CFG_ST7789_CS_PIN = 17
if CFG_DISPLAY_TYPE == "st7789":
    SCR_WIDTH = 240
    SCR_HEIGHT = 240


# IF ssd1306 OR sh1106 IS USED
CFG_OLED_I2CINSTANCE = 0
CFG_OLED_SCL_PIN = 17
CFG_OLED_SDA_PIN = 16
CFG_OLED_ADDR = 0x3c
CFG_DISPLAY_LINE_SPACING = 9 # pixel font width
CFG_DISPLAY_CHAR_WIDTH = 8
if CFG_DISPLAY_TYPE == "ssd1306" or CFG_DISPLAY_TYPE == "sh1106":
    SCR_WIDTH = 128
    SCR_HEIGHT = 64


    
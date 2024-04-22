# HARDWARE CONFIG STARTS HERE
# ssd1306 = 128x64 olded with ssd1306 controller
# sh1106 = 128x64 olded with ssh1106 controller
CFG_DISPLAY_TYPE = "sh1106" # sh1106 ssd1306
CFG_CALIBRATION_WEIGHT_WEIGHT = 50
CFG_SCALE_GLASS_ADDITION_NEXT_STEP_WEIGHT = 50 # Xg more on scale to trigger next step in recipe => 1/3 weight of a typical glass
CFG_USER_LONG_BUTTON_PRESS_TIME = 1000 # time to regsiter a long button press in ms
CFG_DISPLAY_USER_QR_CODE = True # True False
CFG_NEOPIXEL_LED_COUNT = 32 #60
CFG_NEOPIXEL_LED_START_OFFSET = (CFG_NEOPIXEL_LED_COUNT/2) # MAX CFG_NEOPIXEL_LED_COUNT TO ROTATE THE STARTPOINT
CFG_NEOPIXEL_MAX_BRIGHTNESS = 0.8 # 0 - 1.0

# DEFAULT WIFI SETTINGS
# CAN LATER BE CANGED IN THE SDCARD/SETTINGS.JSON FILE
CFG_NETWORK_HOSTNAME = "mixandmeasurebuddy{}" # xXxX.local {} will be replacd with device id:  _<id>
CFG_NETWORK_WIFICOUNTRY = "DE" # DE US
CFG_NETWORK_WIFI_SSID = "Makerspace"
CFG_NETWORK_WIFI_PSK = "MS8cCvpE"
CFG_NETWORK_API_ENDPOINT = "mixmeasurebuddy.com/api/mmb"


# SETTINGS FOR ACCESS POINT + LOCAL WEBEDITOR
CFG_EDITOR_WIFI_STA_HOSTNAME = "mixandmeasurebuddy"
CFG_EDITOR_WIFI_STA_SSID = "mixandmeasurebuddy{}" # {} will be replacd with device id:  _<id>
CFG_EDITOR_WIFI_STA_PSK = "{}"  # {} will be replacd with device id:  _<id>
CFG_EDITOR_HTTP_PORT = 80
############################
######## PIN CONFIG ########
############################
# NEOPIXEL RING
CFG_NEOPIXEL_PIN = 28
# BUTTONS
CFG_BUTTON_LEFT_PIN = 6 #22
CFG_BUTTON_RIGHT_PIN = 2
# HX711 MODULE
CFG_HX711_DOUT_PIN = 5
CFG_HX711_SCK_PIN = 4
# [OPTIONAL] SD CARD
CFG_SDCARD_SPIINSTANCE = 1
CFG_SDCARD_SCK_PIN = 10
CFG_SDCARD_MOSI_PIN = 11
CFG_SDCARD_MISO_PIN = 8
CFG_SDCARD_CS_PIN = 9
# [OPTIONAL] SSD1306 or SH1106
CFG_OLED_I2CINSTANCE = 0
CFG_OLED_SCL_PIN = 17
CFG_OLED_SDA_PIN = 16
CFG_OLED_ADDR = 0x3c
CFG_DISPLAY_LINE_SPACING = 9 # pixel font width
CFG_DISPLAY_CHAR_WIDTH = 8

SCR_WIDTH = 128
SCR_HEIGHT = 64


    

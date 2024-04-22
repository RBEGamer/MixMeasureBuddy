# HARDWARE CONFIG STARTS HERE
# ssd1306 = 128x64 olded with ssd1306 controller
# sh1106 = 128x64 olded with ssh1106 controller
CFG_DISPLAY_TYPE: str = "sh1106" # sh1106 ssd1306
CFG_CALIBRATION_WEIGHT_WEIGHT:float = 50.0
CFG_SCALE_INVERT_WEIGHT_MEASURED_VALUE: float = -1.0 # if the scale measurement is negative set this to 1.0 or -1.0
CFG_SCALE_GLASS_ADDITION_NEXT_STEP_WEIGHT:float = 50.0 # Xg more on scale to trigger next step in recipe => 1/3 weight of a typical glass
CFG_USER_LONG_BUTTON_PRESS_TIME: int = 700 # time to regsiter a long button press in ms

CFG_NEOPIXEL_LED_COUNT: int = 32 #60 how many leds for the ring are used
CFG_NEOPIXEL_LED_START_OFFSET: int = (CFG_NEOPIXEL_LED_COUNT/2) # MAX CFG_NEOPIXEL_LED_COUNT TO ROTATE THE STARTPOINT
CFG_NEOPIXEL_MAX_BRIGHTNESS: float = 0.8 # max led brighness modifier 0.0 - 1.0

# DEFAULT WIFI SETTINGS
# CAN LATER BE CANGED IN THE SDCARD/SETTINGS.JSON FILE
CFG_NETWORK_HOSTNAME: str = "mixandmeasurebuddy{}" # xXxX.local {} will be replacd with device id:  _<id>
CFG_NETWORK_WIFICOUNTRY: str = "DE" # DE US
CFG_NETWORK_WIFI_SSID: str = "Makerspace"
CFG_NETWORK_WIFI_PSK: str = "MS8cCvpE"
CFG_NETWORK_API_ENDPOINT: str = "mixmeasurebuddy.com/api/mmb"


# SETTINGS FOR ACCESS POINT + LOCAL WEBEDITOR
CFG_EDITOR_WIFI_STA_HOSTNAME: str = "mixandmeasurebuddy"
CFG_EDITOR_WIFI_STA_SSID: str = "mixandmeasurebuddy{}" # {} will be replacd with device id:  _<id>
CFG_EDITOR_WIFI_STA_PSK: str = "{}"  # {} will be replacd with device id:  _<id>
CFG_EDITOR_HTTP_PORT: int = 80 # WEBSERVER PORT FOR THE ONLINE EDITOR
############################
######## PIN CONFIG ########
############################
# NEOPIXEL RING
CFG_NEOPIXEL_PIN: int = 28
# BUTTONS
CFG_BUTTON_LEFT_PIN: int = 6 #22
CFG_BUTTON_RIGHT_PIN: int = 2
# HX711 MODULE
CFG_HX711_DOUT_PIN: int = 5
CFG_HX711_SCK_PIN: int = 4
# [OPTIONAL] SD CARD
CFG_SDCARD_SPIINSTANCE: int = 1 # ON RP2040 0 or 1 DEPENDING THE FOLLOWING USED SPI PINS
CFG_SDCARD_SCK_PIN: int = 10
CFG_SDCARD_MOSI_PIN: int = 11
CFG_SDCARD_MISO_PIN: int = 8
CFG_SDCARD_CS_PIN: int = 9
# [OPTIONAL] SSD1306 or SH1106
CFG_OLED_I2CINSTANCE: int = 0 # ON RP2040 0 or 1 DEPENDING THE FOLLOWING USED I2C PINS
CFG_OLED_SCL_PIN: int = 17
CFG_OLED_SDA_PIN: int = 16
CFG_OLED_ADDR: int = 0x3c
CFG_DISPLAY_CHAR_WIDTH: int = 8 # char width in pixels see vga2x8x as used fontfile
CFG_DISPLAY_LINE_SPACING: int = (CFG_DISPLAY_CHAR_WIDTH + 1) # pixel font height +  a bit extra space to make large text more readable

# DISPLAY RESOLUTION
SCR_WIDTH: int = 128
SCR_HEIGHT: int = 64


    

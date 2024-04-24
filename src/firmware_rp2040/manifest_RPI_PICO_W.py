include("$(MPY_DIR)/ports/rp2/boards/RPI_PICO_W/manifest.py")

# TO DECOMPRESS THE SYSTEM IMAGE LATER ON THE THIRD ADDED BOOTSTAGE BOOTSTAGE
#require("zlib")
require("abc")
# ADD NEEDED LIBRARIES HERE
package("neopixel", base_path="/var/build/src/thridparty_libs")
package("sdcard", base_path="/var/build/src/thridparty_libs")
package("urequests", base_path="/var/build/src/thridparty_libs")

#package("fsdatareconstructor", base_path="/var/build/src/lib")
package("mmb", base_path="/var/build/src/lib")


module("fsdatareconstructor.py", base_path="/var/build/src/lib/")

# ADD FURTHER MODULES HERE;
## WILL BE AUTOMATICLY ADDED BY prepare_manifest.sh





module("Scales.py", base_path="/var/build/src/src/static_modules")
module("aiobutton.py", base_path="/var/build/src/src/static_modules")
module("example_recipes.py", base_path="/var/build/src/src/static_modules")
module("glcdfont.py", base_path="/var/build/src/src/static_modules")
module("helper.py", base_path="/var/build/src/src/static_modules")
module("hx711.py", base_path="/var/build/src/src/static_modules")
module("ledring.py", base_path="/var/build/src/src/static_modules")
module("menu_entry.py", base_path="/var/build/src/src/static_modules")
module("micropyserver.py", base_path="/var/build/src/src/static_modules")
module("mmb_display.py", base_path="/var/build/src/src/static_modules")
module("rotary.py", base_path="/var/build/src/src/static_modules")
module("rotary_irq_esp.py", base_path="/var/build/src/src/static_modules")
module("rotary_irq_pyb.py", base_path="/var/build/src/src/static_modules")
module("rotary_irq_rp2.py", base_path="/var/build/src/src/static_modules")
module("sdcard.py", base_path="/var/build/src/src/static_modules")
module("sh1106.py", base_path="/var/build/src/src/static_modules")
module("singleton.py", base_path="/var/build/src/src/static_modules")
module("ssd1306.py", base_path="/var/build/src/src/static_modules")
module("system_command.py", base_path="/var/build/src/src/static_modules")
module("uQR.py", base_path="/var/build/src/src/static_modules")

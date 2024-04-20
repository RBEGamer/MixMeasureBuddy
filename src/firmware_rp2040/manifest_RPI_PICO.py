include("$(MPY_DIR)/ports/rp2/boards/manifest.py")

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




module("aiobutton.py", base_path="/var/build/src/src/static_modules")
module("glcdfont.py", base_path="/var/build/src/src/static_modules")
module("hx711.py", base_path="/var/build/src/src/static_modules")
module("sh1106.py", base_path="/var/build/src/src/static_modules")
module("singleton.py", base_path="/var/build/src/src/static_modules")
module("ssd1306.py", base_path="/var/build/src/src/static_modules")
module("uQR.py", base_path="/var/build/src/src/static_modules")
module("vga2_16x16.py", base_path="/var/build/src/src/static_modules")
module("vga2_8x8.py", base_path="/var/build/src/src/static_modules")

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
## WILL BE AUTOMATICLY ADDED BY prepare_manifest.shmodule("tt14.py", base_path="/var/build/src/src")
module("tt24.py", base_path="/var/build/src/src")
module("tt32.py", base_path="/var/build/src/src")
module("vga2_16x16.py", base_path="/var/build/src/src")
module("vga2_16x32.py", base_path="/var/build/src/src")
module("vga2_8x8.py", base_path="/var/build/src/src")
module("vga2_bold_16x16.py", base_path="/var/build/src/src")
module("vga2_bold_16x32.py", base_path="/var/build/src/src")

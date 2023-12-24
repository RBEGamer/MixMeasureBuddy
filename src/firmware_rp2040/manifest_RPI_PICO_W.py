include("$(MPY_DIR)/ports/rp2/boards/RPI_PICO_W/manifest.py")

# TO DECOMPRESS THE SYSTEM IMAGE LATER ON THE THIRD ADDED BOOTSTAGE BOOTSTAGE
#require("zlib")

# ADD NEEDED LIBRARIES HERE
package("neopixel", base_path="/var/build/src/thridparty_libs")
package("sdcard", base_path="/var/build/src/thridparty_libs")
package("urequests", base_path="/var/build/src/thridparty_libs")

#package("fsdatareconstructor", base_path="/var/build/src/lib")
package("mmb", base_path="/var/build/src/lib")


module("fsdatareconstructor.py", base_path="/var/build/src/lib/")

# ADD FURTHER MODULES HERE;
## WILL BE AUTOMATICLY ADDED BY prepare_manifest.sh
# CocktailScaler

![mixmeasurebuddy](./documentation/images/cropped_A003_11281139_S044.jpg)

MixMeasureBuddy's smart cocktail scale revolutionizes home bartending by offering accurate ingredient measurements and a vast library of cocktail recipes personalized to your liquor collection. Enjoy the art of mixology with ease and precision.

Discover the advanced features that set MixMeasureBuddy apart from traditional kitchen scales.



## FEATURES

Discover the advanced features that set MixMeasureBuddy apart from traditional kitchen scales:

* **Open-Source** MixMeasureBuddy is 100% open-source and can be build using a few simple and cheap parts.
* **Connectivity Features** Enjoy seamless integration with a companion webapp for sharing personalized cocktail recipes with other MixMeasureBuddy owners.
* **Offline Usage** Recipes are stored offline and locally on the MixMeasureBerry and can be edited using a text editor
* **User-Friendly Interface** Easily navigate the scale's intuitive interface for effortless cocktail making.
* **Customizable Recipes** Access a plethora of cocktail recipes tailored to your liquor cabinet for endless mixing possibilities.
* **Precision Measurements** Eliminate the guesswork and achieve consistent results with exact ingredient measurements every time.


## BOM


### 3D PRINTED PARTS

* 1x `ring.stl`
* 1x `breadboard_mount.stl`
* 1x `cellplate.stl`
* 1x `bottom.stl`

### FOR SSH1106 1.3" OLED DISPLAY
* 1x `display_clamp_SSH1106`

### FOR SSD1306 0.96" OlED DISPLAY
* 1x `display_mount_SSD1306`


### MECHANICAL

* 8x `Heat Inserts M3`
* 3x `M5 NUT`
* 4x `M4x10 BHCS`
* 4x `M3x10 BHCS`
* 3x `M5x60 SHCS`
* 8x `Cylindrical Magnet D5 H8`

### ELECTRICAL

* 1x `Raspberry Pi Pico` or `Raspberry Pi Pico W`
* 1x `LOAD CELL` with dimensions of `60x12x12mm` and at least `2kg`, for example `YZC-131`
* 1x `HX711`
* 1x `1.3" I2C OLED SSH1306` or `0.96" I2C OLED SSD1306`
* 1x `Encoder` e.g. `KY-040`
* 60cm `WS2812 Strip`
* Jumperwires
* 1x Breadboard with dimensions of `83 x 55mm`, for example `Mini Breadboard 400 Pin`






# HARDWARE BUILD

## SCHEMATIC

![MixMeasureBuddy Schematic](documentation/schematic/mmb_schematic_encoder_Steckplatine.png)

## NOTES

To fix accuracy issues on several `HX711` boards, two addional resistors are needed.
Please refer to this guide: [HX711 – Auswahl und Beschaltung](https://beelogger.de/sensoren/waegezellen_hx711/hx711_beschaltung/#:~:text=HX711%20Modul%20Auswahl,Wägezelle%20und%20einen%20einstellbaren%20Messbrückenverstärker.)


# SOFTWARE BUILD

Please check the `Releases` page of this repository for prebuild firmware archives.



## 



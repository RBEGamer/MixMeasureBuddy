# CocktailScaler

![mixmeasurebuddy](./documentation/images/cropped_A003_11281139_S044.jpg)




# BOM



## 3D PRINTED PARTS

* 1x `ring.stl`
* 1x `breadboard_mount.stl`
* 1x `cellplate.stl`
* 1x `bottom.stl`

### FOR SSH1106 1.3" OlED DISPLAY
* 1x `display_clamp_SSH1106`
* 1x `display_mount_SSH1106`


## MECHANICAL

* 8x `Heat Inserts M3`
* 3x `M5 NUT`
* 4x `M4x10 BHCS`
* 4x `M3x10 BHCS`
* 3x `M5x60 SHCS`
* 8x `Cylindrical Magnet D5 H8`

## ELECTRICAL

* 1x `Raspberry Pi Pico` or `Raspberry Pi Pico W`
* 1x `LOAD CELL 5kg` or `LOAD CELL 10kg`
* 1x `HX711`
* 1x `1.3" I2C OLED SSH1306`, `0.96" I2C OLED SSD1306`
* 2x `T 250A RT Miniatur-Pushbutton`
* 60cm `WS2812 Strip`
* Jumperwires


## MISC

* `Superglue`
* `small cable ties`






# REST API DEFINITION



* SCALE PING `mixmeasurebuddy.com/api/{scale_id}` -> should redirect to user interface, used for qr code generation
* LIST RECIPES FOR SCALE `mixmeasurebuddy.com/api/{scale_id}/recipes` -> ["recipe_filename_link_relative"]
* FETCH RECIPE FOR SCALE `mixmeasurebuddy.com/api/{scale_id}/recipe/{recipe_filename_link_relative}}` -> [{filename_without_ending, recipe_as_json}]
* 


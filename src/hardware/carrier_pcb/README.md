# MixMeasureBuddy carrier PCB (Raspberry Pi Pico 2 W)

A 2-layer, 83 × 70 mm board that replaces the breadboard and jumper-wire nest. The top 83 × 55 mm is the breadboard-sized area; the bottom 15 mm band holds the optional LiPo section.

* **Raspberry Pi Pico 2 W**: socketed on 2 × 20 pin headers (or soldered directly), with USB at the board edge
* **HX711** load-cell ADC: the bare chip and its datasheet reference circuit, mounted on the board
* **2 navigation buttons** (LEFT / RIGHT): 6 × 6 mm THT tactile switches on the board
* Headers for the **OLED**, **encoder**, **WS2812 ring**, **load cell**, optional **SD card** and optional **5 V battery shield**
* **Optional LiPo section**: charger, step-up converter, power switch header and battery-voltage sense

KiCad 10 project: `mmb_carrier/` (`.kicad_pro`, `.kicad_sch`, `.kicad_pcb`).
Status: ERC 0 violations, DRC 0 violations, 0 unconnected items, 0 schematic-parity issues.

| Top | Bottom |
|---|---|
| ![top](mmb_carrier/mmb_carrier_3d_top.png) | ![bottom](mmb_carrier/mmb_carrier_3d_bottom.png) |

## Pin mapping (matches `src/firmware/src/config.py`, so the firmware works unchanged)

| Function | Pico GPIO (pin) | Board connector |
|---|---|---|
| OLED SDA / SCL (I2C0) | GP16 (21) / GP17 (22) | J1: 1 GND, 2 VCC (3V3), 3 SCL, 4 SDA |
| Encoder CLK / DT / SW | GP20 (26) / GP19 (25) / GP18 (24) | J2: 1 CLK, 2 DT, 3 SW, 4 + (3V3), 5 GND, in KY-040 order |
| WS2812 data | GP28 (34), through 330 Ω R3 | J3: 1 +5V (VSYS), 2 DIN, 3 GND |
| Button LEFT / RIGHT | GP3 (5) / GP2 (4), switch to GND (internal pull-up) | SW1 / SW2 |
| HX711 PD_SCK / DOUT | GP4 (6) / GP5 (7) | on board (U2) |
| Load cell | n/a | J4: 1 A+ (green), 2 A- (white), 3 E- (black), 4 E+ (red) |
| SD card (SPI1, optional) | GP8 MISO, GP9 CS, GP10 SCK, GP11 MOSI | J5: 1 GND, 2 3V3, 3 MISO, 4 MOSI, 5 SCK, 6 CS |
| 5 V in (battery shield, optional) | VBUS (40) | J6: 1 +5V, 2 GND |
| LiPo cell (optional) | n/a | J7 JST-PH 2.0: 1 = **+**, 2 = − |
| Power switch (optional) | n/a | J8: external on/off switch, or a jumper for always-on |
| Battery voltage (optional) | GP26 / ADC0 (31) = VBAT / 2 | n/a |

## Optional LiPo section (bottom band)

Leave every part in the band unpopulated if you don't need a battery; the rest of the board works the same without it.

* **Charger, U3 (MCP73831-2-OT):** charges a single 3.7 V LiPo from USB at 500 mA (R4 = 2 kΩ; use 4.7 kΩ for about 200 mA with small cells). The red CHG LED is on while the cell is charging.
* **Load sharing (Q2 AO3401A + D1):** with USB plugged in, the step-up runs from USB and the battery only charges. Without USB, Q2 connects the battery.
* **Power switch, J8:** sits in series with the step-up input. Wire a slide switch from the enclosure to it, or fit a jumper. The battery still charges while the switch is off.
* **Step-up, U4 (MT3608):** makes 5.1 V with a 10 µH inductor and R7/R8 = 75k/10k. D3 feeds that into VSYS, the Pico's recommended way to add a second power source. The WS2812 header now runs from VSYS, so the ring works on battery too. The MT3608 handles roughly 0.8–1 A out of a LiPo, which is plenty for the 26 LEDs at the firmware's brightness limit.
* **Battery level:** R9/R10 (220k/220k) put VBAT/2 on GP26. The current firmware doesn't read it yet; in MicroPython, `machine.ADC(26).read_u16() * 3.3 / 65535 * 2` gives the battery voltage.
* **⚠ Check polarity:** JST-PH LiPo leads are not standardized. Before plugging in a cell, make sure its red wire lands on pin 1 (marked **+**).

## HX711 circuit notes

* VSUP comes from VSYS and DVDD from 3V3, so DOUT and PD_SCK use 3.3 V logic and are safe for the RP2350.
* AVDD (load-cell excitation, E+) is set to 1.25 V × (R1+R2)/R2 = **3.75 V** with the Q1 PNP pass transistor. This leaves headroom when VSYS sags to about 4.5 V on USB.
* E- is tied directly to AGND/GND. This is the fix that the README's "HX711 accuracy" note applies by hand to cheap modules.
* The step-up converter sits at the opposite corner from the HX711 and load-cell header, so its switching currents don't flow through the HX711 ground area.
* RATE = GND (10 SPS), internal oscillator (XI = GND), channel B is grounded.
* Because AVDD is 3.75 V instead of the module's ~4.3 V, the raw counts per gram change. Re-run the calibration menu once after the switch.

## Layout notes

* The Pico W/2 W antenna keepout from the footprint is respected: no copper or tracks under the antenna end.
* Both layers have a GND pour with stitching vias on a 5 mm grid.
* Four M3 mounting holes sit at 4 mm from each corner.
* Reference designators in the LiPo band are on the fab layer only (no space for silkscreen); see the schematic or the pick-and-place file.
* Signal tracks are 0.25 mm and supply tracks 0.4–0.5 mm, with 0.2 mm clearance and 0.6/0.3 mm vias. Any standard 2-layer fab can make this.

## Fabrication files (`mmb_carrier/fab/`)

* `mmb_carrier_gerbers.zip`: Gerbers and Excellon drill file
* `mmb_carrier_bom.csv`: BOM (plus 2 × 1×20 female 2.54 mm headers if you socket the Pico)
* `mmb_carrier_pos.csv`: pick-and-place file for the SMD parts
* `../mmb_carrier_schematic.pdf`: schematic

## Regenerating

The board is generated from `tools/design.py`, which holds the parts, pins and nets. To rebuild:

```bash
tools/build.sh
```

The script writes the schematic, runs ERC, places parts, routes the board with the bundled grid router (`tools/gen_pcb.py`), pours GND, runs DRC with schematic parity, and exports the fab outputs. If you edit the board by hand in KiCad, stop using the script for that board, because the next run overwrites it.

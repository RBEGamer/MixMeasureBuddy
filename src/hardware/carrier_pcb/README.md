# MixMeasureBuddy carrier PCB (Raspberry Pi Pico 2 W)

A 2-layer, 83 × 70 mm board that replaces the breadboard and jumper-wire nest. The top 83 × 55 mm is the breadboard-sized area; the bottom 15 mm band holds the optional LiPo section.

* **Raspberry Pi Pico 2 W**: socketed on 2 × 20 pin headers (or soldered directly), with USB at the board edge
* **HX711** load-cell ADC (v1.1): a ready-made HX711 module plugs into the J4 socket (the bare chip circuit of v1.0 was removed)
* **2 navigation buttons** (LEFT / RIGHT): 6 × 6 mm THT tactile switches on the board
* Headers for the **OLED**, **encoder**, **WS2812 ring**, **load cell**, optional **SD card** and optional **5 V battery shield**
* **Optional LiPo section**: charger, step-up converter, power switch header and battery-voltage sense
* **Stepper driver socket** (v1.1): a StepStick / Pololu-footprint socket (A4988, DRV8825, TMC2208/2209 modules) with a 4-pin motor header
* **USB-C PD motor supply** (v1.1): a second USB-C port with a CH224K PD trigger that asks the charger for **12 V** for the motor only

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
| HX711 module SCK / DT | GP4 (6) / GP5 (7) | J4 socket: 1 GND, 2 DT, 3 SCK, 4 VCC (3V3) |
| Load cell | n/a | soldered to the HX711 module: E+ red, E- black, A- white, A+ green |
| SD card (SPI1, optional) | GP8 MISO, GP9 CS, GP10 SCK, GP11 MOSI | J5: 1 GND, 2 3V3, 3 MISO, 4 MOSI, 5 SCK, 6 CS |
| 5 V in (battery shield, optional) | VBUS (40) | J6: 1 +5V, 2 GND |
| LiPo cell (optional) | n/a | J7 JST-PH 2.0: 1 = **+**, 2 = − |
| Power switch (optional) | n/a | J8: external on/off switch, or a jumper for always-on |
| Battery voltage (optional) | GP26 / ADC0 (31) = VBAT / 2 | n/a |
| Stepper STEP / DIR | GP6 (9) / GP7 (10) | A1 StepStick socket |
| Stepper EN (active low) | GP1 (2), 10k pull-up R13 = driver off at boot | A1 StepStick socket |
| Stepper motor | n/a | J10: 1 = 1B, 2 = 1A (coil 1), 3 = 2A, 4 = 2B (coil 2); silk shows 2B 2A 1A 1B from left to right |
| Motor supply 12 V | n/a | J9 USB-C (power only), PD charger required |

## Optional LiPo section (bottom band)

Leave every part in the band unpopulated if you don't need a battery; the rest of the board works the same without it.

* **Charger, U3 (MCP73831-2-OT):** charges a single 3.7 V LiPo from USB at 500 mA (R4 = 2 kΩ; use 4.7 kΩ for about 200 mA with small cells). The red CHG LED is on while the cell is charging.
* **Load sharing (Q2 AO3401A + D1):** with USB plugged in, the step-up runs from USB and the battery only charges. Without USB, Q2 connects the battery.
* **Power switch, J8:** sits in series with the step-up input. Wire a slide switch from the enclosure to it, or fit a jumper. The battery still charges while the switch is off.
* **Step-up, U4 (MT3608):** makes 5.1 V with a 10 µH inductor and R7/R8 = 75k/10k. D3 feeds that into VSYS, the Pico's recommended way to add a second power source. The WS2812 header now runs from VSYS, so the ring works on battery too. The MT3608 handles roughly 0.8–1 A out of a LiPo, which is plenty for the 26 LEDs at the firmware's brightness limit.
* **Battery level:** R9/R10 (220k/220k) put VBAT/2 on GP26. The current firmware doesn't read it yet; in MicroPython, `machine.ADC(26).read_u16() * 3.3 / 65535 * 2` gives the battery voltage.
* **⚠ Check polarity:** JST-PH LiPo leads are not standardized. Before plugging in a cell, make sure its red wire lands on pin 1 (marked **+**).

## Stepper driver and 12 V USB-C PD supply (v1.1)

* **Driver socket, A1:** two 1 × 8 female 2.54 mm headers, 12.7 mm (0.5") apart, for any StepStick-pinout module. The silkscreen inside the socket marks **GND / DIR** at the top (Pico side) and **VMOT / EN** at the bottom. The square pad is GND. Check the orientation before plugging in a module: a reversed driver is destroyed as soon as power is applied.
* **Logic:** VDD = 3V3, so STEP / DIR / EN use 3.3 V logic. EN has a 10k pull-up (R13), so the motor stays de-energised until the firmware drives GP1 low. RESET and SLEEP are tied together and pulled high (R14).
* **Microstepping:** JP1 / JP2 / JP3 (labelled MS1 / MS2 / MS3) are open solder jumpers. Open = low, bridged = 3V3. The resulting mode depends on the module (A4988 / DRV8825: all open = full step; TMC2209: MS1 = MS2 = low = 1/8 step). On some TMC220x modules the MS3 / RESET positions carry PDN/UART instead, so check the module's pinout.
* **Motor supply, J9 + U5 (CH224K):** a USB-C power-only receptacle feeds **VMOT only**; the Pico, LEDs and HX711 keep running from the Pico's own USB (or the LiPo section). CH224K negotiates 12 V with R12 = 24k (6.8k = 9 V, 56k = 15 V). It is PD only: DP/DM are shorted on the chip side and not wired to the receptacle. VDD is fed from VBUS through R11 (1k) with C12 (1 µF).
* **Bulk capacitance:** C14 100 µF / 25 V low-ESR electrolytic plus C13 100 nF, next to the VMOT pin. If you change R12 to 15 V, keep the 25 V cap. For 20 V (R12 not fitted) use a 35 V part.
* **Charger requirement:** the charger must offer a 12 V PD profile (check its label). Some chargers only offer 5/9/15/20 V, and with those VMOT stays at 5 V. A4988 / DRV8825 drivers stay in under-voltage lockout at 5 V, while TMC2209 modules run (weakly) from 5 V.
* **Layout:** the whole motor power loop (USB-C, bulk cap, driver, motor header) sits in the left half of the board, far from the HX711 module socket J4 on the right edge. VMOT is routed at 0.8 mm and the motor phases at 0.6 mm, both without vias.
* **Moved for v1.1:** SW1 / SW2 (LEFT / RIGHT) moved to the right of the driver socket, and the SD header J5 moved 2.54 mm to the right. Nets and pin mapping are unchanged.
* **Firmware:** not changed yet; the pins above (GP6 STEP, GP7 DIR, GP1 EN) are free in `config.py`.

## HX711 module (v1.1)

* **J4** is a 1 × 4 female 2.54 mm socket on the right board edge. A ready-made HX711 module (the common green or red board) plugs in with its 4-pin header. The pin order is **GND, DT, SCK, VCC**, as printed on most modules and next to J4 on the silkscreen. If your module uses a different order, wire it to the labels instead of plugging it in directly.
* The module is powered from **3V3**, so DT and SCK use 3.3 V logic and are safe for the RP2350. The area next to J4 (where the v1.0 HX711 chip sat) is free of parts, so the module can lie flat there on right-angle pins, or stand upright in the socket.
* Solder the load cell to the module's E+ / E- / A- / A+ pads (red, black, white, green on most cells).
* GP4 (SCK) and GP5 (DT) are the same pins as before, so the firmware works unchanged. The bare-chip circuit (U2, Q1, R1, R2, C1-C6) and the old load-cell header are gone.
* Many cheap modules need the accuracy fix described in the main README's HX711 note (the linked beelogger guide). Apply it on the module itself.
* After swapping the excitation source (module instead of the v1.0 on-board circuit), run the calibration menu once.

## Layout notes

* The Pico W/2 W antenna keepout from the footprint is respected: no copper or tracks under the antenna end.
* Both layers have a GND pour with stitching vias on a 5 mm grid.
* Four M3 mounting holes sit at 4 mm from each corner.
* Reference designators in the LiPo band and in the USB-C PD / stepper area (except A1 and J10) are on the fab layer only (no space for silkscreen); see the schematic or the pick-and-place file.
* Signal tracks are 0.25 mm, supply tracks 0.4–0.5 mm, VMOT 0.8 mm and motor phases 0.6 mm, with 0.2 mm clearance and 0.6/0.3 mm vias. Any standard 2-layer fab can make this.

## Fabrication files (`mmb_carrier/fab/`)

* `mmb_carrier_gerbers.zip`: Gerbers and Excellon drill file
* `mmb_carrier_bom.csv`: BOM with an `LCSC` column (plus 2 × 1×20 female 2.54 mm headers if you socket the Pico, and 2 × 1×8 female 2.54 mm headers for the A1 stepper socket)
* `mmb_carrier_pos.csv`: pick-and-place file for the SMD parts (KiCad format)
* `mmb_carrier_jlcpcb_bom.csv` + `mmb_carrier_jlcpcb_cpl.csv`: BOM (`Comment, Designator, Footprint, LCSC`) and placement file (`Designator, Mid X, Mid Y, Layer, Rotation`) for JLCPCB SMT assembly of the 30 SMD parts

### LCSC part numbers

Every orderable part carries an `LCSC` field in the schematic and on the PCB footprint. The numbers were checked against the LCSC / JLCPCB part pages (November 2026); check stock before ordering.

| Part | LCSC | Notes |
|---|---|---|
| 0805 resistors 330 / 1k / 2k / 10k / 24k / 75k / 100k / 220k | C17630 / C17513 / C17604 / C17414 / C17575 / C17819 / C149504 / C17556 | UNI-ROYAL 0805W8F series, 1 %; 75k is an extended part |
| 100 nF 0805 / 1 µF 0805 / 4.7 µF 0805 / 22 µF 1206 | C49678 / C28323 / C1779 / C12891 | X7R 50 V, X7R 50 V, X5R 25 V, X5R 25 V |
| C14 100 µF 25 V, 6.3 × 5.8 mm | C178540 | Panasonic EEE-FK1E101SP |
| SS14 / red 0805 LED / AO3401A | C2480 / C84256 / C15127 | |
| MCP73831T-2ACI/OT / MT3608 / CH224K | C424093 / C84817 / C970725 | extended parts |
| L1 Bourns SRN6045TA-100M | C2046332 | second source on the same footprint: SXN SMNR6045-100MT, C135304 |
| J9 GCT USB4125-GF-A (USB-C, power only) | C3151650 | exact part for the footprint |
| J4 1×4 female header / A1 1×8 female header (2 pcs) | C2718488 / C27438 | 8.5 mm high |
| J7 JST S2B-PH-K-S / SW1, SW2 6 × 6 × 5 mm tact switch | C173752 / C393938 | |
| Male pin headers J1-J3, J5, J6, J8, J10 | C2337 | 1×40 breakable, cut to length (no field on the symbols) |

The JLCPCB files cover the SMD parts only; the through-hole parts (headers, switches, JST, Pico) are hand-soldered. Rotations in the CPL are KiCad's: check the part orientation in JLCPCB's placement preview before confirming, especially for the SOT-23 parts, the diodes, the electrolytic C14, U5 and J9.
* `../mmb_carrier_schematic.pdf`: schematic

## Regenerating

The board is generated from `tools/design.py`, which holds the parts, pins and nets. To rebuild:

```bash
tools/build.sh
```

The script writes the schematic, runs ERC, places parts, routes the board with the bundled grid router (`tools/gen_pcb.py`), pours GND, runs DRC with schematic parity, and exports the fab outputs. If you edit the board by hand in KiCad, stop using the script for that board, because the next run overwrites it.

**Note for v1.1:** the stepper / USB-C PD rework was added directly to the KiCad files, not to `tools/design.py`. Running the old generator would remove it.

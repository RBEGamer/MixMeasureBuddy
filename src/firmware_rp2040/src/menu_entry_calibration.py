from abc import abstractmethod
import menu_entry
import system_command
from ui import ui
from ledring import ledring
from Scales import ScaleInterface
import time
import config
import static_modules.menu_manager as menu_manager
import settings


class menu_entry_calibration(menu_entry.menu_entry):

    MENU_STATE_CLEAR_PLATE_INIT = 0
    MENU_STATE_CLEAR_PLATE_TARING = 1

    MENU_STATE_FULL_PLATE_INIT = 2
    MENU_STATE_FULL_PLATE_PLACE = 3
    MENU_STATE_FULL_PLATE_TARING = 4

    MEASUREMENT_AVERAGING_POINTS: int = 10
    CALIBRATION_WEIGHT_USER_STEPS: float = 5.0
    MIN_CALIBRATION_WEIGHT: float = 50.0
    menu_state: int = 0

    calibration_value_empty: float = 0.0
    calibration_value_full: float = 0.0
    calibration_value_invert: float = 1.0
    calibration_weight_weight: float = max(config.CFG_CALIBRATION_WEIGHT_WEIGHT, MIN_CALIBRATION_WEIGHT)

    def __init__(self):
        super().__init__("CALIBRATION", "Calibrate system scale")

    def preview(self):
        print("preview {}".format(self.name))
        ui().show_recipe_information(self.name, self.description)


    def activate(self):
        print("activate {}".format(self.name))
        
        ScaleInterface().reset_calibration()
        ledring().set_neopixel_full(10, 10, 10)

        ui().show_msg("Please clear scale plate and press ok")
        self.menu_state = self.MENU_STATE_CLEAR_PLATE_INIT

        # RESET MEASURED VALUES
        self.calibration_value_empty = 0.0
        self.calibration_value_full = 0.0
        self.calibration_value_invert = 1.0
        self.calibration_weight_weight = max(config.CFG_CALIBRATION_WEIGHT_WEIGHT, self.MIN_CALIBRATION_WEIGHT)


    def teardown(self):
        print("teardown {}".format(self.name))


    def update(self, _system_command: system_command.system_command):
        if _system_command.type == system_command.system_command.COMMAND_TYPE_NAVIGATION:
            
            if self.menu_state == self.MENU_STATE_CLEAR_PLATE_INIT and _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                self.menu_state = self.MENU_STATE_CLEAR_PLATE_TARING
                ledring().set_neopixel_full(50, 0, 0)
                ui().show_recipe_information("PLEASE WAIT", "TARING")
                time.sleep(2)
                
                for i in range(self.MEASUREMENT_AVERAGING_POINTS):
                    ledring().set_neopixel_percentage(i/(self.MEASUREMENT_AVERAGING_POINTS*1.0))
                    self.calibration_value_empty += ScaleInterface().get_current_weight()
                    ui().show_recipe_information("PLEASE WAIT", "MEASURING: {}/{}".format(i, self.MEASUREMENT_AVERAGING_POINTS))
                    time.sleep(0.5)

                self.calibration_value_empty = self.calibration_value_empty /self.MEASUREMENT_AVERAGING_POINTS
                ui().show_recipe_information("FIRST RUN DONE", "RAW_VALUE:{}".format(self.calibration_value_empty))
                time.sleep(1)
                self.menu_state = self.MENU_STATE_FULL_PLATE_INIT
                ui().clear()
                ui().show_recipe_information("SET REFERENCE WEIGHT", "\n\n {}g".format(self.calibration_weight_weight))

                ledring().set_neopixel_full(0, 0, 10)


            elif self.menu_state == self.MENU_STATE_FULL_PLATE_INIT:
                

                if _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                    if self.calibration_weight_weight >= self.MIN_CALIBRATION_WEIGHT:
                        ui().show_msg("Please place calibration weight on the plate and press ok")
                        self.menu_state =  self.MENU_STATE_FULL_PLATE_PLACE
                        return
                    else:
                        ui().show_msg("Calibration weight must be at least {}g".format(self.MIN_CALIBRATION_WEIGHT))
                        time.sleep(2)

                elif _system_command.action == system_command.system_command.NAVIGATION_RIGHT:
                    self.calibration_weight_weight = self.calibration_weight_weight + self.CALIBRATION_WEIGHT_USER_STEPS
                elif _system_command.action == system_command.system_command.NAVIGATION_LEFT:
                    if self.calibration_weight_weight >= (self.MIN_CALIBRATION_WEIGHT + self.CALIBRATION_WEIGHT_USER_STEPS):
                        self.calibration_weight_weight = self.calibration_weight_weight - self.CALIBRATION_WEIGHT_USER_STEPS

                # UPDATE VALUE ON DISPLAY
                ui().clear()
                ui().show_recipe_information("SET REF WEIGHT", "\n\n {}g".format(self.calibration_weight_weight))


            elif self.menu_state == self.MENU_STATE_FULL_PLATE_PLACE:
                if _system_command.action == system_command.system_command.NAVIGATION_ENTER:
                    ledring().set_neopixel_full(50, 0, 0)
                    ui().show_recipe_information("PLEASE WAIT", "TARING")
                    time.sleep(2)
                    self.menu_state = self.MENU_STATE_CLEAR_PLATE_TARING

                    for i in range(self.MEASUREMENT_AVERAGING_POINTS):
                        ledring().set_neopixel_percentage(i/(self.MEASUREMENT_AVERAGING_POINTS*1.0))
                        self.calibration_value_full += ScaleInterface().get_untared_weight()
                        ui().show_recipe_information("PLEASE WAIT", "MEASURING: {}/{}".format(i, self.MEASUREMENT_AVERAGING_POINTS))
                        time.sleep(0.5)

                    self.calibration_value_full = self.calibration_value_full /self.MEASUREMENT_AVERAGING_POINTS
                    ui().show_recipe_information("SECOND RUN", "RAW_VALUE:{}/{}".format(self.calibration_value_empty, self.calibration_value_full))
                    time.sleep(2)
                    self.menu_state = self.MENU_STATE_FULL_PLATE_INIT
                    # DETERM THE LOADCELL ORIENTATION
                    
                    self.calibration_value_invert = 1.0
                    settings.settings().save_scale_calibration_values(self.calibration_value_empty, self.calibration_value_full, self.calibration_weight_weight, self.calibration_value_invert)
                    ScaleInterface().reload_calibration()
                    calibrated_measurement: float = 0.0
                    # FIRST READ x DUMMY READS THEN USE THE LEFT OVER TO CALCULATE FINAL ADDITIONAL OFFSET
                    for i in range(self.MEASUREMENT_AVERAGING_POINTS):
                        ledring().set_neopixel_percentage(i/(self.MEASUREMENT_AVERAGING_POINTS))
                        ScaleInterface().get_untared_weight()

                    ledring().set_neopixel_full(50, 0, 0)
                    time.sleep(1.0)
                    cw: float = 0.0
                    for i in range(self.MEASUREMENT_AVERAGING_POINTS):
                        ledring().set_neopixel_percentage(i/(self.MEASUREMENT_AVERAGING_POINTS*1.0))        
                        cw = ScaleInterface().get_untared_weight()
                        ui().show_recipe_information("THRID RUN", "CURRENT WEIGHT: {} {}".format(cw, calibrated_measurement))     
                        calibrated_measurement += cw 


                    calibrated_measurement = (calibrated_measurement / self.MEASUREMENT_AVERAGING_POINTS)
                    if calibrated_measurement <= 0.0:
                        self.calibration_value_invert = -1.0
                    else:
                        self.calibration_value_invert = 1.0
                    #self.calibration_value_invert = self.calibration_weight_weight / calibrated_measurement
                    ui().show_recipe_information("THRID RUN", "INVERT_FACTOR: {} - {}".format(self.calibration_value_invert, calibrated_measurement))
                    time.sleep(2)
                    ui().show_msg("SAVE CALIBRATION")
                    ledring().set_neopixel_full(0, 0, 10)

                    # SAVE CALIBRATION TO FILE
                    #if self.calibration_value_empty > self.calibration_value_full:
                    #   t: float = self.calibration_value_empty
                    #   self.calibration_value_empty = self.calibration_value_full
                    #   self.calibration_value_full = t

                    settings.settings().save_scale_calibration_values(self.calibration_value_empty, self.calibration_value_full, self.calibration_weight_weight, self.calibration_value_invert)
                    #LOAD NEW CALIBRAION FACTOR IN
                    ScaleInterface().reload_calibration()
                    # LEAVE MENU
                    menu_manager.menu_manager().exit_current_menu()


                    


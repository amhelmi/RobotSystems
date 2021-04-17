#!/usr/bin/env python3
import time
import logging
import atexit
from sensors import Sensors
from interpreter import Interpreter
from picarx_new import PiCarX

# this is necessary to fix the car when it powers down and restarts
try:
    from ezblock import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions")
    from sim_ezblock import *

logging_format = "%asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")

class Controller:
    def __init__(self, scaling=41):
        self.sensors = Sensors()
        self.interpreter = Interpreter()
        self.picar = PiCarX()
        self.scaling = scaling

    def line_follow(self):
        pass

    def test(self):
        for i in range(3):
            sensor_values = self.sensors.sensor_read()
            robot_direction = self.interpreter.interpret(sensor_values)
            picar.forward_angle(robot_direction*self.scaling)


        



if __name__ == "__main__":
    controller = Controller()
    controller.test()
    

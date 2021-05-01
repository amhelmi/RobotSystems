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
    def __init__(self, scaling=20):
        # initialize everything
        self.sensors = Sensors()
        self.interpreter = Interpreter(polarity='lighter')
        self.picar = PiCarX()
        self.scaling = scaling

    def line_follow(self, robot_direction):
        '''
        for line following more appropriately
        currently unused
        '''
        self.picar.forward_angle(-robot_direction*self.scaling, 30)
        return robot_direction*self.scaling

    def test(self):
        # testing line following
        self.picar.set_dir_servo_angle(69)
        for i in range(10):
            sensor_values = self.sensors.sensor_read()
            print(sensor_values)
            robot_direction = self.interpreter.interpret(sensor_values)
            self.line_follow(robot_direction)



if __name__ == "__main__":
    controller = Controller()
    controller.test()
    

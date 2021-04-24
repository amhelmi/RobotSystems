#!/usr/bin/env python3
import sys
sys.path.append(r'/opt/ezblock')
import time
import logging
import atexit
import numpy as np
from picarx_new import PiCarX
from camera_sensors import CameraSensor

from logdecorator import log_on_start, log_on_end, log_on_error

# this is necessary to fix the car when it powers down and restarts
try:
    from ezblock import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  calls with  substitute  functions")
    from sim_ezblock import *

class CameraController:
    def __init__(self):
        # testing using cmaera in another thread
        picarx = PiCarX()
        picarx.set_camera_servo1_angle(0)
        picarx.set_camera_servo2_angle(0)
        camera_sensor = CameraSensor()
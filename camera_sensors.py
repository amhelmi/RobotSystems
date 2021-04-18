#!/usr/bin/env python3
import time
import logging
import atexit

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

import cv2
from vilib import Vilib

class Camera_Sensor:
    def __init__(self):
        Vilib.camera_start(True)
        self.video_read()

    def video_read(self):
    	for i in range(10):
	        frame = cv2.imread('192.168.50.32:9000/mjpg')
	        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	        cv2.imshow("hsv", hsv)
	        lower_blue = np.array([60, 40, 40])
	        upper_blue = np.array([150, 255, 255])
	        mask = cv2.inRange(hsv, lower_blue, upper_blue)
	        edges = cv2.Canny(mask, 200, 400)
	        cv2.imshow("blue", mask)
	        cv2.waitKey(0)

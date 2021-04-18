#!/usr/bin/env python3
import sys
sys.path.append(r'/opt/ezblock')
import time
import logging
import atexit
import numpy as np

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
        self.cap = cv2.VideoCapture(0)
        self.video_read()
        
    def video_read(self):
        while True:
            ret, frame = self.cap.read()
            #frame = cv2.imread('192.168.50.32:9000/mjpg')
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imshow("hsv", hsv)
            #print(frame)
            #print("hello")
            lower_blue = np.array([60, 40, 40])
            upper_blue = np.array([150, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            edges = cv2.Canny(mask, 200, 400)
            cv2.imshow("blue", mask)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindowS()

if __name__ == "__main__":
    camera_sensor = Camera_Sensor()

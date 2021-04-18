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
            # cv2.imshow("hsv", hsv)
            #print(frame)
            #print("hello")
            lower_blue = np.array([60, 40, 40])
            upper_blue = np.array([150, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            edges = cv2.Canny(mask, 200, 400)
            # cv2.imshow("blue", mask)
            cropped_edges = self.region_of_interest(edges)
            line_segments = self.detect_line_segments(cropped_edges)
            lane_lines_image = display_lines(frame, line_segments)
            cv2.imshow("lane lines", lane_lines_image)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindowS()

    def region_of_interest(edges):
        # pulled from online to cut frame into bottom half of view
        height, width = edges.shape
        mask = np.zeros_like(edges)

        # only focus bottom half of the screen
        polygon = np.array([[
            (0, height * 1 / 2),
            (width, height * 1 / 2),
            (width, height),
            (0, height),
        ]], np.int32)

        cv2.fillPoly(mask, polygon, 255)
        cropped_edges = cv2.bitwise_and(edges, mask)
        return cropped_edges

    def detect_line_segments(cropped_edges):
        # pulled from online to detect line segments
        # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
        rho = 1  # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
        min_threshold = 10  # minimal of votes
        line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, 
                                        np.array([]), minLineLength=8, maxLineGap=4)

        return line_segments

    def display_lines(frame, lines, line_color=(0, 255, 0), line_width=2):
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
        line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        return line_image

if __name__ == "__main__":
    camera_sensor = Camera_Sensor()

#!/usr/bin/python3

from picarx_class import Motor
import time
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib
import math
import atexit
import logging
import cv2
from  logdecorator  import  log_on_start , log_on_end , log_on_error
import numpy as np

try:
    from ezblock import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  calls with  substitute  functions")
    from sim_ezblock import *


class CameraSensor():
    def __init__(self):

        # Got help from the following tutorials:
        # Tutorial 1: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
        # Tutorial 2: https://towardsdatascience.com/deeppicar-part-4-lane-following-via-opencv-737dd9e47c96

        Vilib.camera_start(True)
        
        #Vilib.color_detect_switch(True)
        #Vilib.detect_color_name('blue')

        self.capture = cv2.VideoCapture(0)

        self.interface_with_camera()


    def interface_with_camera(self):
        # Interface with camera to capture video

        while(True):

            print('hello')

            # Capture frame by frame
            ret,frame = self.capture.read()

            print('hello2')

            # Detect edges of line(s)
            edges = self.detect_edges(frame)

            print('hello3')

            # Crop top half to reduce noise in image
            cropped_edges = self.region_of_interest(edges)

            print('hello4')

            # Get line(s)
            lines = self.detect_line_segments(cropped_edges)

            print('hello5')

            # Display line(s)
            lines_image = self.display_lines(frame, lines)
            cv2.imshow("lines", lines_image)

            print('hello6')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.capture.release()
        cv2.destroyAllWindowS()


    def detect_edges(self, frame):
        # See tutorial 2
        # filter for blue lane lines

        # Render tape same color
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #show_image("hsv", hsv)

        # Create mask
        lower_blue = np.array([60, 40, 40])
        upper_blue = np.array([150, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        #show_image("blue mask", mask)

        # Detect edges
        edges = cv2.Canny(mask, 200, 400)

        return edges

    def region_of_interest(self, edges):
        # See tutorial 2
        # Only consider bottom half of frame, where the lines are

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

    def detect_line_segments(self, cropped_edges):
        # See tutorial 2
        # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
        rho = 1  # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
        min_threshold = 10  # minimal of votes
        line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, 
                                        np.array([]), minLineLength=8, maxLineGap=4)

        return line_segments

    def display_lines(self, frame, lines, line_color=(0, 255, 0), line_width=2):
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
        line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        return line_image


# interpreter class i.e. which way to go

# controller class i.e. go there


if __name__ == '__main__':
    sensor = CameraSensor()
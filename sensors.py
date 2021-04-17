#!/usr/bin/env python3
import time
import logging
import atexit

# this is necessary to fix the car when it powers down and restarts
try:
    from ezblock import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  calls with  substitute  functions")
    from sim_ezblock import *

logging_format = "%asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")

class Sensors:
	def __init__(self):
		self.S0 = ADC('A0')
		self.S1 = ADC('A1')
		self.S2 = ADC('A2')

	def sensor_read(self):
		'''
		read ADC sensor values and return output as a list
		:return: adc outputs in list
		'''
		s0 = self.S0.read()
		s1 = self.S1.read()
		s2 = self.S2.read()
		# return as list
		return [s0, s1, s2]
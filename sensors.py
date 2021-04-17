#!/usr/bin/env python3
import time
import logging
import atexit
from logdecorator import log_on_start, log_on_end, log_on_error
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

class Sensors:
	def __init__(self):
		self.PERIOD = 4095
		self.PRESCALER = 10
		self.TIMEOUT = 0.02

		self.dir_servo_pin = Servo(PWM('P2'))
		self.camera_servo_pin1 = Servo(PWM('P0'))
		self.camera_servo_pin2 = Servo(PWM('P1'))
		self.left_rear_pwn_pin = PWM("P13")
		self.right_rear_pwn_pin = PWM("P12")
		self.left_rear_dir_pin = Pin("D4")
		self.right_rear_dir_pin = Pin("D5")

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
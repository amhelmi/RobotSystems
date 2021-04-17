#!/usr/bin/env python3
import time
import logging
import atexit
from sensors import Sensors

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

class Interpreter:
	def __init__(self, sensitivity=500, polarity='darker'):
		sensors = Sensors()
		self.sensor_values = sensors.read()
		self.sensitivity = sensitivity
		self.polarity = polarity
		self.interpret(self.sensor_values)

	def interpret(self, sensor_values):
		'''
		'''
		self.old_values = sensor_values
		self.sensor_values = sensors.read()
		RIGHT = 0
		MID = 0
		LEFT = 0
		
		if polarity == 'darker':
			# target is darker
			# check first sensor. Is the change in value bigger than our sensitivity?
			if abs(self.sensor_values[0] - self.old_values[0]) > self.sensitivity:
				# ok which direction? if sign is negative, that means we need to turn. Otherwise, continue on
				if self.sensor_values[0] - self.old_values[0] < 0:
					# turn right
					RIGHT = 1
				else:
					RIGHT = 0
			# if this one is higher than sensitivity, we are way off
			elif abs(self.sensor_values[1] - self.old_values[1]) > self.sensitivity:
				if self.sensor_values[1] - self.old_values[1] < 0:
					# go forward
					MID = 1
				else:
					MID = 0
			elif abs(self.sensor_values[2] - self.old_values[2]) > self.sensitivity:
				if self.sensor_values[2] - self.old_values[2] < 0:
					# turn left
					LEFT = 1
				else:
					LEFT = 0

		else:
			# target is lighter
			# check first sensor. Is the change in value bigger than our sensitivity?
			if abs(self.sensor_values[0] - self.old_values[0]) > self.sensitivity:
				# ok which direction? if sign is positive, that means we need to turn. Otherwise, continue on
				if self.sensor_values[0] - self.old_values[0] > 0:
					# turn right
					RIGHT = 1
				else:
					RIGHT = 0
			# if this one is higher than sensitivity, we are way off
			elif abs(self.sensor_values[1] - self.old_values[1])  > self.sensitivity:
				if self.sensor_values[1] - self.old_values[1] > 0:
					# go forward
					MID = 1
				else:
					MID = 0
			elif abs(self.sensor_values[2] - self.old_values[2]) > self.sensitivity:
				if self.sensor_values[2] - self.old_values[2] > 0:
					# turn left
					LEFT = 1
				else:
					LEFT = 0
		directions = [RIGHT, MID, LEFT]

		if MID == 1:
			# did our middle change a lot? if so, likely one of our directions did too
			if RIGHT == 1:
				direction = 'right'
			elif LEFT == 1:
				direction = 'left'
			else:
				# something might be messed up.
				# maybe we reached the end of the line? go forward some more and see if something changes
				direction = 'forward'

		else:
			if RIGHT == 1:
				direction = 'right'
			elif LEFT == 1:
				direction = 'left'
			else:
				# both left and right changed drastically but the middle didn't. that is sus but we are probably fine
				# just keep going
				direction = 'forward'

		if direction == 'forward':
			robot_direction = 0
		elif direction == 'right':
			if MID == 1:
				# turn only slightly 
				robot_direction = -0.5
			else:
				robot_direction = -1
		elif direction == 'left':
			if MID == 1:
				# turn only slightly
				robot_direction = 0.5
			else:
				robot_direction = 1

		return robot_direction



if __name__ == "__main__":
    interpreter = Interpreter()
    
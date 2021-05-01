#!/usr/bin/env python3
import time
import logging
import atexit
from sensors import Sensors
from interpreter import Interpreter
from controller import Controller
import concurrent.futures
from threading import Lock

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

class Bus:
	def __init__(self, message=None):
		self.message = message

	def write(self, message):
		'''
		write a bus message
		:param: message to write
		'''
		self.message = message

	def read(self):
		'''
		send message back
		:return: the current message for that bus
		'''
		return self.message


def sensor_function(sensor_bus, delay):
	'''
	create a sensor class, read the sensor values and write them in a loop
	:param: sensor_bus 
	:param: timer delay
	'''
	sensor = Sensors()
	lock = Lock()
	while True:
		with lock
			sensor_values = sensor.sensor_read()
		sensor_bus.write(sensor_values)
		time.sleep(delay)

def interpreter_function(sensor_bus, interp_bus, delay):
	'''
	get sensor values, interpret them and write the direction the robot should move
	:param: sensor_bus
	:param: interp_bus
	:param: timer delay 
	'''
	interpreter = Interpreter()
	while True:
		sensor_values = sensor_bus.read()
		direction = interpreter.interpret(sensor_values)
		interp_bus.write(direction)
		time.sleep(delay)

def controller_function(interp_bus, controller_bus, delay):
	'''
	get interp value and move the robot using the controller
	:param: interp_bus
	:param: controller_bus 
	:param: timer delay
	'''
	controller = Controller()
	while True:
		direction = interp_bus.read()
		steering_direction = controller.line_follow(direction)
		controller_bus.write(steering_direction)
		time.sleep(delay)


# makes some bus's 
sensor_values_bus = Bus()
interpreter_bus	= Bus()
controller_bus = Bus()
sensor_delay = 1
interpreter_delay = 2
controller_delay = 2

# concurrent setup
with concurrent.futures.ThreadPoolExecutor(max_workers = 2) as executor:
	eSensor = executor.submit(sensor_function ,sensor_values_bus ,sensor_delay)
	eInterpreter = executor.submit(interpreter_function ,sensor_values_bus , interpreter_bus ,interpreter_delay)


#!/usr/bin/env python3
import time
import logging
import atexit
from sensors import Sensors
from interpreter import Interpreter
from controller import Controller
from rossros import Bus, ConsumerProducer, Producer, Consumer, Timer, Printer, runConcurrently

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


sensor = Sensor()
interp = Interpreter()
controller = Controller()

sensor_bus = Bus(name="sensor_bus")
interp_bus = Bus(name="interp_bus")
controller_bus = Bus(name="controller_bus")

#sensing producer or producer Consumer
#interp producer consumer (takes in data and puts it out)
#controller consumer or consumer producer
sens_task = ConsumerProducer(sensor.read, input_busses=sensor_bus, output_busses=sensor_bus, name='sensor', delay = 1)
interp_task = ConsumerProducer(interp.interpret, input_busses=sensor_bus, output_busses=interp_bus, name='interpreter', delay = 1)
control_task = ConsumerProducer(controller.line_follow, input_busses=(sensor_bus, interp_bus), output_busses=controller_bus, name='controller', delay=1)

runConcurrently([sens_task, interp_task,control_task])
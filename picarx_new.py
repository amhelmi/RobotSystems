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


class PiCarX:
    def __init__(self):
        self.PERIOD = 4095
        self.PRESCALER = 10
        self.TIMEOUT = 0.02
        self.zero_angle = 28

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

        self.Servo_dir_flag = 1
        self.dir_cal_value = 0
        self.cam_cal_value_1 = 0
        self.cam_cal_value_2 = 0
        self.motor_direction_pins = [self.left_rear_dir_pin, self.right_rear_dir_pin]
        self.motor_speed_pins = [self.left_rear_pwn_pin, self.right_rear_pwn_pin]
        self.cali_dir_value = [1, -1]
        self.cali_speed_value = [0, 0]

        for pin in self.motor_speed_pins:
            pin.period(self.PERIOD)
            pin.prescaler(self.PRESCALER)

        atexit.register(self.cleanup)

    def set_motor_speed(self, motor, speed):
        motor -= 1
        if speed >= 0:
            direction = 1 * self.self.cali_dir_value[motor]
        elif speed < 0:
            direction = -1 * self.cali_dir_value[motor]
        speed = abs(speed)
        #if speed != 0:
        #    speed = int(speed /2 ) + 50
        speed = speed - self.self.cali_speed_value[motor]
        if direction < 0:
            self.motor_direction_pins[motor].high()
            self.motor_speed_pins[motor].pulse_width_percent(speed)
        else:
            self.motor_direction_pins[motor].low()
            self.motor_speed_pins[motor].pulse_width_percent(speed)

    def motor_speed_calibration(self, value):
        self.cali_speed_value = value
        if value < 0:
            self.cali_speed_value[0] = 0
            self.cali_speed_value[1] = abs(self.cali_speed_value)
        else:
            self.cali_speed_value[0] = abs(self.cali_speed_value)
            self.cali_speed_value[1] = 0

    def motor_direction_calibration(self, motor, value):
        # 0: positive direction
        # 1:negative direction
        motor -= 1
        if value == 1:
            self.cali_dir_value[motor] = -1*self.cali_dir_value[motor]


    def dir_servo_angle_calibration(self, value):
        self.dir_cal_value = value
        self.set_dir_servo_angle(self.dir_cal_value)
        # self.dir_servo_pin.angle(self.dir_cal_value)

    def set_dir_servo_angle(self, value):
        self.dir_servo_pin.angle(value+self.dir_cal_value)

    def camera_servo1_angle_calibration(self, value):
        self.cam_cal_value_1 = value
        set_camera_servo1_angle(self.cam_cal_value_1)
        # self.camera_servo_pin1.angle(cam_cal_value)

    def camera_servo2_angle_calibration(self, value):
        self.cam_cal_value_2 = value
        set_camera_servo2_angle(self.cam_cal_value_2)
        # self.camera_servo_pin2.angle(cam_cal_value)

    def set_camera_servo1_angle(self, value):
        self.camera_servo_pin1.angle(-1 *(value+self.cam_cal_value_1))

    def set_camera_servo2_angle(self, value):
        self.camera_servo_pin2.angle(-1 * (value+self.cam_cal_value_2))

    def get_adc_value(self):
        adc_value_list = []
        adc_value_list.append(S0.read())
        adc_value_list.append(S1.read())
        adc_value_list.append(S2.read())
        return adc_value_list

    def set_power(self, speed):
        # set motor speeds
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed)

    def backward(self, speed):
        # go backwards
        self.set_motor_speed(1, -1*speed)
        self.set_motor_speed(2, speed)

    def forward(self, speed):
        # go forward
        self.set_motor_speed(1, 1*speed)
        self.set_motor_speed(2, -1*speed)

    def stop(self):
        # stop moving
        self.set_motor_speed(1, 0)
        self.set_motor_speed(2, 0)

    def Get_distance(self):
        # get distance
        timeout=0.01
        trig = Pin('D8')
        echo = Pin('D9')

        trig.low()
        time.sleep(0.01)
        trig.high()
        time.sleep(0.000015)
        trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while echo.value()==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > timeout:
                return -1
        while echo.value()==1:
            pulse_end = time.time()
            if pulse_end - timeout_start > timeout:
                return -2
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        #print(cm)
        return cm

    def cleanup(self):
        '''
        set everything back to zero. Motor speeds, camera angles, front wheel angle
        '''
        self.set_motor_speed(1, 0)
        self.set_motor_speed(2, 0)
        self.camera_servo_pin1.angle(0)
        self.camera_servo_pin2.angle(0)
        self.set_dir_servo_angle(self.zero_angle)

    def parallel_parking_right(self):
        '''
        parallel parking when the parking spot is to the right of the car
        '''
        # first move self.backwards
        self.set_dir_servo_angle(69)
        self.backward(50)
        time.sleep(1)
        self.stop()
        # continue self.backwards but flip the wheel
        self.set_dir_servo_angle(0)
        self.backward(50)
        time.sleep(1)
        self.stop()
        # now reset and go self.forward a little
        self.set_dir_servo_angle(self.zero_angle)
        self.forward(35)
        time.sleep(0.1)
        self.stop()

    def parallel_parking_left(self):
        '''
        parallel parking when the parking spot is to the left of the car
        '''
        # first move self.backwards
        self.set_dir_servo_angle(0)
        self.backward(50)
        time.sleep(0.5)
        self.stop()
        # continue self.backwards but flip the wheel
        self.set_dir_servo_angle(69)
        self.backward(50)
        time.sleep(0.5)
        self.stop()
        # now reset and go self.forward a little
        self.set_dir_servo_angle(self.zero_angle)
        self.forward(35)
        time.sleep(1)

    def user_control(self):
        '''
        user control function for letting a user decide what the robot will do. 
        This function loops until Q is pressed (caps is irrelevant)
        '''
        while 1:
            print("---------------------------------")
            print("Available commands, Q to quit:\n")
            print('W or F for self.forward movement, S or B for self.backwards, D for parallel parking right, A for parallel parking left')
            print('J for a left 3 point turn, L for a right 3 point turn')
            command = input("Please choose a command: ")
            if command.upper() == "W" or command.upper() == "F":
                speed = int(input("\nPlease enter a speed to drive at (press enter for default of 50): ") or "50")
                angle = int(input("\nPlease enter an angle to drive at (press enter for default of straight): ") or "0")
                self.forward_angle(angle, speed)
            elif command.upper() == "S" or command.upper() == "B":
                speed = int(input("\nPlease enter a speed to drive at (press enter for default of 50): ") or "50")
                angle = int(input("\nPlease enter an angle to drive at (press enter for straight): " ) or "0")
                self.backward_angle(angle, speed)
            elif command.upper() == "D":
                self.parallel_parking_right()
            elif command.upper() == "A":
                self.parallel_parking_left()
            elif command.upper() == "J":
                self.kturn("left")
            elif command.upper() == "L":
                self.kturn("right")
            elif command.upper() == "Q":
                break
            else:
                print("Input was invalid. Try again")

    def forward_angle(self, angle=0, speed=100):
        '''
        move forward at a given speed and angle
        angle: angle to drive at. 0 is 28 degrees. Default is forward
        speed: speed to drive at. Default is 100
        '''
        self.set_dir_servo_angle(angle+self.zero_angle)
        time.sleep(0.1)
        self.forward(speed)
        time.sleep(1)
        self.stop()

    def backward_angle(self, angle=0, speed=100):
        '''
        move backward at a given speed and angle
        angle: angle to drive at. 0 is 28 degrees. Default is forward
        speed: speed to drive at. Default is 100
        '''
        self.set_dir_servo_angle(angle+self.zero_angle)
        time.sleep(0.1)
        self.backward(speed)
        time.sleep(1)
        self.stop()

    def kturn(self, direction="RIGHT"):
        '''
        make a 3 point turn in a direction. default is starting to turn right
        direction: starting turning left or right
        '''
        if direction.upper() == "LEFT":
            # go left first
            self.set_dir_servo_angle(-20)
            self.forward(50)
            time.sleep(1.25)

            self.set_dir_servo_angle(69)
            self.backward(50)
            time.sleep(1.75)

            self.set_dir_servo_angle(0)
            self.forward(50)
            time.sleep(1)
            self.stop()

            self.set_dir_servo_angle(self.zero_angle)
            self.forward(35)
            time.sleep(0.5)
            self.stop()

        else:
            # go right first
            self.set_dir_servo_angle(69)
            self.forward(50)
            time.sleep(1.25)

            self.set_dir_servo_angle(-20)
            self.backward(50)
            time.sleep(1.75)
            
            self.set_dir_servo_angle(0)
            self.forward(50)
            time.sleep(1)
            self.stop()
            
            self.set_dir_servo_angle(self.zero_angle)
            self.forward(35)
            time.sleep(0.5)
            self.stop()


if __name__ == "__main__":
    picar = PiCarX()
    picar.user_control()
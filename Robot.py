"""
	Robot class
 	Platform = Raspberry Pi 3
	System = Differential Drive Robot
"""
import RPi.GPIO as GPIO
import time
import sys
import os
import math
import random
import numpy as np


class Robot:

    # Constants
    MOTOR_RIGHT_PWM_A = 0
    MOTOR_RIGHT_PWM_B = 1
    MOTOR_LEFT_PWM_A = 2
    MOTOR_LEFT_PWM_B = 3
    ENCODER_RIGHT_A = 4
    ENCODER_RIGHT_B = 5
    ENCODER_LEFT_A = 6
    ENCODER_LEFT_B = 7
    GYRO = 8
    MAX_SPEED = 255

    # Executes the "Drive forward at max speed" command
    def drive_forward_max(self):
        GPIO.output(self.MOTOR_RIGHT_PWM_A, self.MAX_SPEED)
        GPIO.output(self.MOTOR_RIGHT_PWM_B, 0)
        GPIO.output(self.MOTOR_LEFT_PWM_A, self.MAX_SPEED)
        GPIO.output(self.MOTOR_LEFT_PWM_B, 0)

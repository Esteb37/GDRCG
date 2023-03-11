"""
	Command: Drive forward at max speed for 50 cm

	System:

		RaspberryPi. Dual DC motor car with AMT103-V quadrature encoders on each wheel.

	Constants:

		MOTOR_RIGHT_PWM_A
		MOTOR_RIGHT_PWM_B
		MOTOR_LEFT_PWM_A
		MOTOR_LEFT_PWM_B
		ENCODER_RIGHT_A
		ENCODER_RIGHT_B
		ENCODER_LEFT_A
		ENCODER_LEFT_B
		GYRO

"""
import time
import os
import math
from RPI.GPIO import GPIO


class DriveForward50cm:

    MOTOR_RIGHT_PWM_A = os.getenv("MOTOR_RIGHT_PWM_A")
    MOTOR_RIGHT_PWM_B = os.getenv("MOTOR_RIGHT_PWM_B")
    MOTOR_LEFT_PWM_A = os.getenv("MOTOR_LEFT_PWM_A")
    MOTOR_LEFT_PWM_B = os.getenv("MOTOR_LEFT_PWM_B")
    ENCODER_RIGHT_A = os.getenv("ENCODER_RIGHT_A")
    ENCODER_RIGHT_B = os.getenv("ENCODER_RIGHT_B")
    ENCODER_LEFT_A = os.getenv("ENCODER_LEFT_A")
    ENCODER_LEFT_B = os.getenv("ENCODER_LEFT_B")
    # TODO: Add MAX_SPEED to .env
    MAX_SPEED = os.getenv("MAX_SPEED")
    # TODO: Add GEAR_RATIO to .env
    GEAR_RATIO = os.getenv("GEAR_RATIO")
    # TODO: Add WHEEL_DIAMETER to .env
    WHEEL_DIAMETER = os.getenv("WHEEL_DIAMETER")

    right_counter = 0
    right_state = None

    left_counter = 0
    left_state = None

    def right_encoder_callback(self, channel):
        state = self.right_state
        a = GPIO.input(self.ENCODER_RIGHT_A)
        b = GPIO.input(self.ENCODER_RIGHT_B)
        if state is None:
            self.right_state = (a, b)
            return
        if channel == self.ENCODER_RIGHT_A:
            if a == state[0] and b != state[1]:
                self.right_counter += 1
            elif a != state[0] and b == state[1]:
                self.right_counter -= 1
        elif channel == self.ENCODER_RIGHT_B:
            if a != state[0] and b == state[1]:
                self.right_counter += 1
            elif a == state[0] and b != state[1]:
                self.right_counter -= 1
        self.right_state = (a, b)

    def left_encoder_callback(self, channel):
        state = self.left_state
        a = GPIO.input(self.ENCODER_LEFT_A)
        b = GPIO.input(self.ENCODER_LEFT_B)
        if state is None:
            self.left_state = (a, b)
            return
        if channel == self.ENCODER_LEFT_A:
            if a == state[0] and b != state[1]:
                self.left_counter += 1
            elif a != state[0] and b == state[1]:
                self.left_counter -= 1
        elif channel == self.ENCODER_LEFT_B:
            if a != state[0] and b == state[1]:
                self.left_counter += 1
            elif a == state[0] and b != state[1]:
                self.left_counter -= 1
        self.left_state = (a, b)

    def execute(self):
        self.setup()
        self.run()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MOTOR_RIGHT_PWM_A, GPIO.OUT)
        GPIO.setup(self.MOTOR_RIGHT_PWM_B, GPIO.OUT)
        GPIO.setup(self.MOTOR_LEFT_PWM_A, GPIO.OUT)
        GPIO.setup(self.MOTOR_LEFT_PWM_B, GPIO.OUT)
        GPIO.setup(self.ENCODER_RIGHT_A, GPIO.IN)
        GPIO.setup(self.ENCODER_RIGHT_B, GPIO.IN)
        GPIO.setup(self.ENCODER_LEFT_A, GPIO.IN)
        GPIO.setup(self.ENCODER_LEFT_B, GPIO.IN)
        GPIO.add_event_detect(self.ENCODER_RIGHT_A, GPIO.BOTH,
                              callback=self.right_encoder_callback)
        GPIO.add_event_detect(self.ENCODER_RIGHT_B, GPIO.BOTH,
                              callback=self.right_encoder_callback)
        GPIO.add_event_detect(self.ENCODER_LEFT_A, GPIO.BOTH,
                              callback=self.left_encoder_callback)
        GPIO.add_event_detect(self.ENCODER_LEFT_B, GPIO.BOTH,
                              callback=self.left_encoder_callback)

    def run(self):
        GPIO.output(self.MOTOR_RIGHT_PWM_A, self.MAX_SPEED)
        GPIO.output(self.MOTOR_RIGHT_PWM_B, 0)
        GPIO.output(self.MOTOR_LEFT_PWM_A, self.MAX_SPEED)
        GPIO.output(self.MOTOR_LEFT_PWM_B, 0)

        right_distance = 0
        left_distance = 0

        while (right_distance+left_distance)/2 < 50:
            right_distance = self.right_counter * \
                self.WHEEL_DIAMETER * math.pi / self.GEAR_RATIO
            left_distance = self.left_counter * \
                self.WHEEL_DIAMETER * math.pi / self.GEAR_RATIO

        GPIO.output(self.MOTOR_RIGHT_PWM_A, 0)
        GPIO.output(self.MOTOR_RIGHT_PWM_B, 0)
        GPIO.output(self.MOTOR_LEFT_PWM_A, 0)
        GPIO.output(self.MOTOR_LEFT_PWM_B, 0)

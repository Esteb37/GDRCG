"""
	Command: Drive forward at max speed for 50 cm using PID

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
		MAX_SPEED
		GEAR_RATIO
		WHEEL_DIAMETER
        DRIVE_PID_KP
        DRIVE_PID_KI
        DRIVE_PID_KD
        

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
    MAX_SPEED = os.getenv("MAX_SPEED")
    GEAR_RATIO = os.getenv("GEAR_RATIO")
    WHEEL_DIAMETER = os.getenv("WHEEL_DIAMETER")
    DRIVE_PID_KP = os.getenv("DRIVE_PID_KP")
    DRIVE_PID_KI = os.getenv("DRIVE_PID_KI")
    DRIVE_PID_KD = os.getenv("DRIVE_PID_KD")

    right_counter = 0
    right_state = None

    left_counter = 0
    left_state = None

    drive_pid_error = [0, 0, 0]
    drive_pid_output = [0, 0]

    def drive_pid(self, target, current):
        kp = self.DRIVE_PID_KP
        ki = self.DRIVE_PID_KI
        kd = self.DRIVE_PID_KD
        Ts = 0.1
        K1 = kp + ki * Ts / 2 + kd / Ts
        K2 = -kp - 2 * kd / Ts
        K3 = kd / Ts
        self.drive_pid_error[2] = self.drive_pid_error[1]
        self.drive_pid_error[1] = self.drive_pid_error[0]
        self.drive_pid_error[0] = target - current
        self.drive_pid_output[1] = self.drive_pid_output[0]
        self.drive_pid_output[0] = (K1 * self.drive_pid_error[0] +
                                    K2 * self.drive_pid_error[1] +
                                    K3 * self.drive_pid_error[2] +
                                    self.drive_pid_output[1])
        return self.drive_pid_output[0]

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
        target = 50
        right_speed = 0
        left_speed = 0
        while True:
            right_speed = self.drive_pid(target, self.right_counter)
            left_speed = self.drive_pid(target, self.left_counter)
            if right_speed > self.MAX_SPEED:
                right_speed = self.MAX_SPEED
            if left_speed > self.MAX_SPEED:
                left_speed = self.MAX_SPEED
            if right_speed < -self.MAX_SPEED:
                right_speed = -self.MAX_SPEED
            if left_speed < -self.MAX_SPEED:
                left_speed = -self.MAX_SPEED
            if right_speed > 0:
                GPIO.output(self.MOTOR_RIGHT_PWM_A, GPIO.HIGH)
                GPIO.output(self.MOTOR_RIGHT_PWM_B, GPIO.LOW)
            else:
                GPIO.output(self.MOTOR_RIGHT_PWM_A, GPIO.LOW)
                GPIO.output(self.MOTOR_RIGHT_PWM_B, GPIO.HIGH)
            if left_speed > 0:
                GPIO.output(self.MOTOR_LEFT_PWM_A, GPIO.HIGH)
                GPIO.output(self.MOTOR_LEFT_PWM_B, GPIO.LOW)
            else:
                GPIO.output(self.MOTOR_LEFT_PWM_A, GPIO.LOW)
                GPIO.output(self.MOTOR_LEFT_PWM_B, GPIO.HIGH)
            time.sleep(0.1)

"""
	Command: Drive forward at 50% speed for 5 seconds. Left side is inverted

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
 
"""
import time
import os
from RPI.GPIO import GPIO


class DriveForward5Seconds:

    MOTOR_RIGHT_PWM_A = os.getenv("MOTOR_RIGHT_PWM_A")
    MOTOR_RIGHT_PWM_B = os.getenv("MOTOR_RIGHT_PWM_B")
    MOTOR_LEFT_PWM_A = os.getenv("MOTOR_LEFT_PWM_A")
    MOTOR_LEFT_PWM_B = os.getenv("MOTOR_LEFT_PWM_B")
    MAX_SPEED = os.getenv("MAX_SPEED")

    def execute(self):
        self.setup()
        self.run()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MOTOR_RIGHT_PWM_A, GPIO.OUT)
        GPIO.setup(self.MOTOR_RIGHT_PWM_B, GPIO.OUT)
        GPIO.setup(self.MOTOR_LEFT_PWM_A, GPIO.OUT)
        GPIO.setup(self.MOTOR_LEFT_PWM_B, GPIO.OUT)

    def run(self):

        GPIO.output(self.MOTOR_RIGHT_PWM_A, self.MAX_SPEED*0.5)
        GPIO.output(self.MOTOR_RIGHT_PWM_B, 0)
        GPIO.output(self.MOTOR_LEFT_PWM_A, 0)
        GPIO.output(self.MOTOR_LEFT_PWM_B, self.MAX_SPEED*0.5)

        time.sleep(5)

        GPIO.output(self.MOTOR_RIGHT_PWM_A, 0)
        GPIO.output(self.MOTOR_RIGHT_PWM_B, 0)
        GPIO.output(self.MOTOR_LEFT_PWM_A, 0)
        GPIO.output(self.MOTOR_LEFT_PWM_B, 0)

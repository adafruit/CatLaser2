# Raspberry Pi Cat Laser Driver Servo Contoller
# This code implements the logic to control the laser servos using the
# PCA9685 module.  By putting this code in its own class it's easy for the model
# to be tested in isolation with a test servo class implementation.
# Author: Tony DiCola
import Adafruit_PCA9685

class Servos(object):
    def __init__(self, i2cAddress, xAxisChannel, yAxisChannel, pwmFreqHz):
        self.pwm = Adafruit_PCA9685.PCA9685(address=i2cAddress)
        self.pwm.set_pwm_freq(pwmFreqHz)
        self.xaxis = xAxisChannel
        self.yaxis = yAxisChannel

    def setXAxis(self, value):
        self.pwm.set_pwm(self.xaxis, 0, value)

    def setYAxis(self, value):
        self.pwm.set_pwm(self.yaxis, 0, value)

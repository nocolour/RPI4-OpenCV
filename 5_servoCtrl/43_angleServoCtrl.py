#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
* @par Copyright (C): 2010-2020, hunan CLB Tech
* @file         43_angleServoCtrl.py
* @version      V2.0
* @details
* @par History

@author: zhulin
"""

import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print(('{0}us per period'.format(pulse_length)))
    pulse_length //= 4096     # 12 bits of resolution
    print(('{0}us per bit'.format(pulse_length)))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def set_servo_angle(channel,angle):
    angle=4096*((angle*11)+500)/20000
    pwm.set_pwm(channel,0,int(angle))

# Set frequency to 50hz, good for servos.
pwm.set_pwm_freq(50)

print('Moving servo on channel 0, press Ctrl-C to quit...')

set_servo_angle(4,90)
time.sleep(1)
set_servo_angle(5,90)
time.sleep(1)

# pwm.set_pwm(4, 0, 300)
# time.sleep(1)
# pwm.set_pwm(5, 0, 300)
# time.sleep(1)
#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
#import os

FAN_PIN = 18
WAIT_TIME = 1
PWM_FREQ = int(sys.argv[1])

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)

fan=GPIO.PWM(FAN_PIN,PWM_FREQ)
fan.start(50);

try:
    while 1:
        fanSpeed=float(input("Fan Speed: "))
        fan.ChangeDutyCycle(fanSpeed)
        # GPIO.cleanup()
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
        # fan=GPIO.PWM(FAN_PIN,fanSpeed)
        # fan.start(50);


except(KeyboardInterrupt):
    print("Fan ctrl interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()
    

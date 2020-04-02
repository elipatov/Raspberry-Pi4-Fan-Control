#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import signal
import sys
import os

# Configuration
FAN_PIN = 18            # BCM pin used to drive PWM fan. Hardware PWM available on GPIO12, GPIO13, GPIO18, GPIO19
WAIT_TIME = 1           # [s] Time to wait between each refresh
PWM_FREQ = 14           # [Hz] PWM frequency. Adjust it modify PWM noise

# Configurable temperature and fan speed
CUTOFF_TEMP = 59
MIN_TEMP = 65
MAX_TEMP = 75
FAN_LOW = 50
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100
step = (FAN_HIGH - FAN_LOW)/(MAX_TEMP - MIN_TEMP)  

def getCpuTemperature():
    cpuTempFile = open("/sys/class/thermal/thermal_zone0/temp", "r")
    cpuTemp = float(cpuTempFile.read()) / 1000
    cpuTempFile.close()
    #print("CPU temp is {0}".format(cpuTemp)) # Uncomment for testing
    return cpuTemp

def calculateFanSpeed(cpuTemp):
    deltaTemp = cpuTemp - MIN_TEMP
    return (FAN_LOW + (round(deltaTemp) * step ))

def setFanSpeed(speed):
    fan.start(speed)
    return()

def handleFanSpeed():
    cpuTemp = float(getCpuTemperature())
    # Turn off the fan if temperature is below MIN_TEMP
    if cpuTemp < MIN_TEMP:
        setFanSpeed(FAN_OFF)
        #print("Fan OFF") # Uncomment for testing
    # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
    elif cpuTemp > MAX_TEMP:
        setFanSpeed(FAN_MAX)
        #print("Fan MAX") # Uncomment for testing
    # Caculate dynamic fan speed
    else:
        fanSpeed = calculateFanSpeed(cpuTemp)
        setFanSpeed(fanSpeed)
        #print(FAN_LOW + ( round(deltaTemp) * step )) # Uncomment for testing
    return ()

fanOn = False
def handleFanSpeed2():
    cpuTemp = float(getCpuTemperature())

    if cpuTemp < CUTOFF_TEMP:
        setFanSpeed(0)
        fanOn = False
    elif cpuTemp >= MAX_TEMP:
        setFanSpeed(FAN_MAX)
        fanOn = True
    # If temperature is between MIN_TEMP and MAX_TEMP, fan speed is calculated by linear interpolation
    # If temperature is between CUTOFF_TEMP and MIN_TEMP, keap current fan speed
    elif cpuTemp > MIN_TEMP:
            fanSpeed = calculateFanSpeed(cpuTemp)
            setFanSpeed(fanSpeed)
            fanOn = True
    return ()

try:
    # Setup GPIO pin
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN,PWM_FREQ)
    setFanSpeed(FAN_OFF)
    # Handle fan speed every WAIT_TIME sec
    while True:
        handleFanSpeed2()
        time.sleep(WAIT_TIME)
except KeyboardInterrupt:
    print("Fan ctrl interrupted by CTRL+C")
    GPIO.cleanup()
    sys.exit()

#!/usr/bin/env python
# NiteLite - a python daemon process started at system boot, and stopped on shutdown
#          - the default LED pattern is twinkling but if motion is detected, one of 4
#            different patterns are chosen and these are used for 10s after motion detection
#
# Please see our GitHub repository for more information: https://github.com/pistuffing/nitelite/piglow
#
# Once running you'll need to press ctrl-C to cancel stop the script or run
# sudo /etc/init.d/nitelited.sh stop

import signal
import time
import RPi.GPIO as GPIO
import os
from datetime import datetime
import subprocess

#------------------------------------------------------------
# Set up the shutdown handler
#------------------------------------------------------------
def ShutdownHandler(signal, frame):
	global keep_looping
	keep_looping = False

#------------------------------------------------------------
# Set up the PIR movement detection
#------------------------------------------------------------
GPIO_PIR = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_PIR, GPIO.IN, GPIO.PUD_DOWN)

#------------------------------------------------------------
# Final steps of setup
#------------------------------------------------------------
signal.signal(signal.SIGINT, ShutdownHandler)
keep_looping = True

def Daemonize():
	os.setpgrp()

#------------------------------------------------------------
# Once booted, give the user a couple of minutes to place the camera
#------------------------------------------------------------
time.sleep(2 * 60.0)

while keep_looping:
        #----------------------------------------------------
        # Block waiting for motion detection
        #----------------------------------------------------
        GPIO.wait_for_edge(GPIO_PIR, GPIO.RISING)

        #----------------------------------------------------
        # Take a snap
        #----------------------------------------------------
	now = datetime.now()
	now_string = now.strftime("%y%m%d-%H:%M:%S")
	camera = subprocess.Popen(["raspistill", "-rot", "180", "-o", "/home/pi/Photos/img_" + now_string + ".jpg", "-n", "-ISO", "400", "-ex", "night", "-ifx", "none"], preexec_fn =  Daemonize)

        #----------------------------------------------------
        # Wait for a minute
        #----------------------------------------------------
        time.sleep(60.0)

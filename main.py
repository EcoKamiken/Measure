#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
"""

import os
import datetime

from configparser import ConfigParser

import RPi.GPIO as GPIO

import powermeter as pm

# $MEASURE_ROOT
measure_root = os.environ['MEASURE_ROOT']

# Read 'config.ini'
current_dir = os.path.dirname(__file__)
config = ConfigParser()
config.read(measure_root  + '/config.ini', 'UTF-8')

# Init GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()


# Temperature(dummy)
temperature = 0
humidity = 0

# Get values using 'powermeter.py'
phase = config.getint('pcs', 'phase')
line = config.getint('pcs', 'line')

voltage = round(pm.get_voltage(), 2)
ampere = round(pm.get_ampere(voltage), 2)
wattage = round(pm.get_wattage(ampere, phase, line), 2)

# Save CSV to /dev/shm (ramdisk)
site_id = config.getint('info', 'id')
device_id = config.getint('info', 'device_id')
created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

with open(measure_root + '/log.csv', 'a') as log:
    log.write("{},{},{},{},{},{}\n".format(site_id, device_id, temperature,
                                           humidity, wattage, created_at))

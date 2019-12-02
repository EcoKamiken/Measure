#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
"""

import os
import datetime

from configparser import ConfigParser

import DHT11_Python.dht11 as dht11
import RPi.GPIO as GPIO

import powermeter as pm
import thermometer as tm

# Read 'config.ini'
current_dir = os.path.dirname(__file__)
config = ConfigParser()
config.read(current_dir + '/' + 'config.ini', 'UTF-8')

# Init GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# $MEASURE_ROOT
measure_root = os.environ['MEASURE_ROOT']

# Get temperature and humidity using 'thermometer.py'
instance = dht11.DHT11(pin=14)
temperature, humidity = tm.get_data(instance)

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

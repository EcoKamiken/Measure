#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11
import datetime
from configparser import ConfigParser

import thermometer as tm
import powermeter as pm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# thermometer
instance = dht11.DHT11(pin=14)
temperature, humidity = tm.get_data(instance)

# powermeter
voltage = round(pm.get_voltage(), 2)
ampere = round(pm.get_ampere(voltage), 2)
wattage = round(pm.get_wattage(ampere), 2)

# write to csv
current_dir = os.path.dirname(__file__)
config = ConfigParser()
config.read(current_dir + '/' + 'config.ini', 'UTF-8')

site_id = config.getint('info', 'id')
device_id = config.getint('info', 'device_id')
created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

logfile = current_dir + '/' + 'log.csv'
with open(logfile, 'a') as log:
    log.write("{},{},{},{},{},{}\n"
              .format(site_id, device_id,
                      temperature, humidity, wattage, created_at))

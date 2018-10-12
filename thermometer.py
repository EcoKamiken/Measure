#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11

from configparser import ConfigParser

def get_data(instance):
    while True:
        result = instance.read()
        if result.is_valid():
            temperature = result.temperature
            humidity = result.humidity
            return temperature, humidity

def dump_log(t, h):
    config = ConfigParser()
    script_dir = os.path.dirname(__file__)
    config.read(script_dir + '/' + 'config.ini', 'UTF-8')

    d = datetime.datetime.now()
    d = d.strftime("%Y-%m-%d %H:%M")
    p = config.get('web', 'place')
    device_no = config.get('web', 'device_no')

    if os.path.exists(os.path.dirname(__file__)):
        with open(os.path.dirname(__file__) + '/' + 'thermometer.csv', 'a') as log:
            log.write("{},{},{},{},{}\n".format(p, d, t, h, device_no))
    else:
        with open(os.path.dirname(__file__) + '/' + 'thermometer.csv', 'w') as log:
            log.write("{},{},{},{},{}\n".format(p, d, t, h, device_no))

if __name__ == '__main__':
    # Initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    instance_1 = dht11.DHT11(pin=14)
    t, h = get_data(instance_1)
    dump_log(t, h)

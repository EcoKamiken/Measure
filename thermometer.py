#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import sys

import mysql.connector
import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11

def get_data(instance):
    while True:
        result = instance.read()
        if result.is_valid():
            temperature = result.temperature
            humidity = result.humidity
    return temperature, humidity

def dump_log(t, h):
    d = datetime.datetime.now()
    if os.path.exists(os.path.dirname(__file__)):
        with open(os.path.dirname(__file__) + '/' + 'thermometer.csv', 'a') as log:
            log.write("{},{},{}\n".format(d, t, h))
    else:
        with open(os.path.dirname(__file__) + '/' + 'thermometer.csv', 'w') as log:
            log.write("{},{},{}\n".format(d, t, h))

if __name__ == '__main__':
    # Initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    instance_1 = dht11.DHT11(pin=14)
    t, h = get_data(instance_1)

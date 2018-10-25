#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11

def get_data(instance):
    while True:
        result = instance.read()
        if result.is_valid():
            temperature = result.temperature
            humidity = result.humidity
            return temperature, humidity
    return 0, 0

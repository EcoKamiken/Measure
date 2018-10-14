#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11

import thermometer as tm
import wattage as wt

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=14)
temperature, humidity = tm.get_data(instance)
print(temperature, humidity)

v = round(wt.get_voltage(), 2)
a = round(wt.get_ampere(v), 2)
w = round(wt.get_wattage(a), 2)
print(v,a,w)

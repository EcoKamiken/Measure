#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11


def get_data(instance):
    for i in range(1000):
        result = instance.read()
        if result.is_valid():
            with open('thermometer_retry.log', 'a') as f:
                f.write(str(i) + '\n')
            temperature = result.temperature
            humidity = result.humidity
            return temperature, humidity
    return 0, 0


if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    # thermometer
    instance = dht11.DHT11(pin=14)
    while True:
        print(get_data(instance))

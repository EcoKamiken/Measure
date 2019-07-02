#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
温湿度センサ DHT11からデータの読み出しを行う
"""

import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11


# 温度取得のリトライ回数
MAX_RETRY = 300


def get_data(instance):
    """温度、湿度を取得して返す

    Args:
        instance (object): DHT11_Python.dht11()で生成されたオブジェクト

    Returns:
        temperature, humidity (int, int): 温度、湿度
    """
    for i in range(MAX_RETRY):
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
    print(get_data(instance))

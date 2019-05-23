#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
エントリーポイント
thermometer.py, powermeter.pyを呼び出して、
各種センサから取得した値をCSVに記録する。
"""

import os
import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11
import datetime
from configparser import ConfigParser

import thermometer as tm
import powermeter as pm

# Configファイルの読み込み
current_dir = os.path.dirname(__file__)
config = ConfigParser()
config.read(current_dir + '/' + 'config.ini', 'UTF-8')

# GPIO初期化
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# thermometer.pyから値取得
instance = dht11.DHT11(pin=14)
temperature, humidity = tm.get_data(instance)

# powermeter.pyから値取得
phase = config.getint('pcs', 'phase')
line = config.getint('pcs', 'line')

voltage = round(pm.get_voltage(), 2)
ampere = round(pm.get_ampere(voltage), 2)
wattage = round(pm.get_wattage(ampere, phase, line), 2)

# CSVに記録
site_id = config.getint('info', 'id')
device_id = config.getint('info', 'device_id')
created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

logfile = current_dir + '/' + 'log.csv'
with open(logfile, 'a') as log:
    log.write("{},{},{},{},{},{}\n"
              .format(site_id, device_id,
                      temperature, humidity, wattage, created_at))

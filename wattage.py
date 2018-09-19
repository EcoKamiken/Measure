#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
INA260 + I2C 電流/電圧測定
電圧: 0x02
上記のアドレスをi2cgetで読むと、4byteの16進数が返ってくる。
バイトオーダーはリトルエンディアン

Ex.
    ----------------------------------------
    電圧: 0xb50f

    |MSB| 0f b5 |LSB|
    0000 1111 1011 0101
    -> 4021

    出てきた値に1.25をかけたものが電圧になる
    4021 * 1.25 = 5026.25[mV]

    単位をVに揃える
    5.02625[V]

    ----------------------------------------
"""

import datetime
import os
import math
import subprocess
import time

from configparser import ConfigParser

I2C_BUS = 1
I2C_ADDR = 0x4a
I2C_VOLT = 0x02

def get_voltage():
    """
    return:
        Voltage[V]
    """
    volt = subprocess.getoutput("/usr/sbin/i2cget -y {bus} {addr} {volt} w".format(bus=I2C_BUS, addr=I2C_ADDR, volt=I2C_VOLT))
    return (int(volt[4:6], 16) * 256 + int(volt[2:4], 16)) * 1.25 / 1000

def get_ampere(vin):
    """
    vin:
        Voltage input[V]

    return:
        Ampere[A]
    """
    return vin / 5 * 250

def get_wattage(amp):
    """
    amp:
        Ampere[A]

    return:
        Wattage[kW]
    """
    return math.sqrt(3) * 210 * amp * 0.9 / 1000

def dump_log(v,a,w):
    config = ConfigParser()
    script_dir = os.path.dirname(__file__)
    config.read(script_dir + '/' + 'config.ini', 'UTF-8')

    d = datetime.datetime.now()
    d = d.strftime("%Y-%m-%d %H:%M:%S")
    p = config.get('web', 'place')

    if os.path.exists(os.path.dirname(__file__)):
        with open(os.path.dirname(__file__) + '/' + 'wattage.csv', 'a') as log:
            log.write("{},{},{},{},{}\n".format(p, d, v, a, w))
    else:
        with open(os.path.dirname(__file__) + '/' + 'wattage.csv', 'w') as log:
            log.write("{},{},{},{},{}\n".format(p, d, v, a, w))

if __name__ == '__main__':
    v = round(get_voltage(), 2)
    a = round(get_ampere(v), 2)
    w = round(get_wattage(a), 2)
    dump_log(v,a,w)
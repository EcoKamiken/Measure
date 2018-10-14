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

import math
import subprocess

I2C_BUS = 1
I2C_ADDR = 0x4a
I2C_VOLT = 0x02

def get_voltage():
    volt = subprocess.getoutput("/usr/sbin/i2cget -y {bus} {addr} {volt} w".format(bus=I2C_BUS, addr=I2C_ADDR, volt=I2C_VOLT))
    if volt[:5] == 'Error':
        return 0.0
    else:
        return (int(volt[4:6], 16) * 256 + int(volt[2:4], 16)) * 1.25 / 1000

def get_ampere(vin):
    return vin / 5 * 250

def get_wattage(amp):
    return math.sqrt(3) * 210 * amp * 0.9 / 1000

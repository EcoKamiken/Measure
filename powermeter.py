#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
INA260 I2C 電流・電力モニタ

レジスタのアドレス
Bus Voltage Register: 0x02

上記のアドレスをi2cgetで読むと、4byteの16進数が返ってくる。

Ex. Bus Voltage Registerの読み方
----------------------------------------
電圧(Contents): 0xb50f -> b5 0f

|MSB| 0f b5 |LSB|

0000 1111 1011 0101 -> 4021

出てきた値に1.25をかけたものが電圧になる
4021 * 1.25 = 5026.25[mV]

単位をVに揃える
5.02625[V]
----------------------------------------
"""

import math
import subprocess

from search import get_i2c_address

I2C_BUS = 1
I2C_ADDR = get_i2c_address()
I2C_BUS_VOLT = 0x02


def get_voltage():
    volt = subprocess.getoutput("/usr/sbin/i2cget -y {bus} {addr} {volt} w"
                                .format(bus=I2C_BUS, addr=I2C_ADDR,
                                        volt=I2C_BUS_VOLT))
    if volt[:5] == 'Error':
        return 0.0
    else:
        return (int(volt[4:6], 16) * 256 + int(volt[2:4], 16)) * 1.25 / 1000


def get_ampere(v):
    return v / 5 * 250


def get_wattage(i):
    return math.sqrt(3) * 210 * i * 0.9 / 1000


if __name__ == '__main__':
    v = get_voltage()
    i = get_ampere(v)
    w = get_wattage(i)
    print('v => ',  v)
    print('i => ',  i)
    print('w => ',  w)

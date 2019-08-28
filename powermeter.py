#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INA260 I2C 電流・電力モニタ
クランプセンサ CTT-24-CLS-CV-250

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
import sys

from search import get_i2c_address

I2C_BUS = 1
I2C_ADDR = get_i2c_address()
I2C_BUS_VOLT = 0x02


def get_voltage():
    """バス電圧値を取得して返す

    Returns:
        float: バス電圧 単位[V]
    """
    volt = subprocess.getoutput("/usr/sbin/i2cget -y {bus} {addr} {volt} w"
                                .format(bus=I2C_BUS, addr=I2C_ADDR,
                                        volt=I2C_BUS_VOLT))
    if volt[:5] == 'Error':
        return 0.0
    else:
        return (int(volt[4:6], 16) * 256 + int(volt[2:4], 16)) * 1.25 / 1000


def get_ampere(v):
    """バス電圧から計算した電流値を返す

    Returns:
        float: 電流 単位[A]
    """
    return v / 5 * 250


def get_wattage(ampere, phase, line):
    """電流から計算した発電量を返す

    三相三線式と単相三線式に対応

    Args:
        ampere (float): 電流 単位[A]
        phase (int):
            単相 = 1
            三相 = 3
        line (int):
            三線 = 3

    Returns:
        float: 発電量 単位[kW]
    """
    phase_voltage = 210
    power_factor = 0.9

    if phase == 3 and line == 3:
        return math.sqrt(3) * phase_voltage * ampere * power_factor / 1000
    elif phase == 1 and line == 3:
        return phase_voltage * ampere * power_factor / 1000
    else:
        print('ParameterError: please check config.ini', file=sys.stderr)
        return -1


if __name__ == '__main__':
    v = get_voltage()
    i = get_ampere(v)
    w = get_wattage(i, 0, 3)
    #print('I2C_ADDR => ', I2C_ADDR, '[{}]'.format(hex(I2C_ADDR)))
    print('v => ',  v, type(v))
    print('i => ',  i, type(i))
    print('w => ',  w, type(w))

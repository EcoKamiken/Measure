#!/usr/bin/python3

import subprocess


def get_devicelist():
    """
    接続されているi2cデバイスのリストを取得して返す

    Returns:
        rest (list[str]): 接続されているi2cデバイスのアドレスをstrのリストで返す
    """
    rest = []

    devices = subprocess.getoutput("/usr/sbin/i2cdetect -y 1").split(" ")
    for device in devices:
        if len(device) == 2 and device != '--':
            rest.append('0x' + device)
    return rest


def get_i2c_address():
    """
    接続されているi2cデバイスを取得して返す
        Note: 一番番号が若いデバイスのアドレスのみを返す

    Returns:
        (int): i2cアドレス
    """
    devices = subprocess.getoutput("/usr/sbin/i2cdetect -y 1").split(" ")
    for device in devices:
        if len(device) == 2 and device != '--':
            return int(device, 16)


if __name__ == '__main__':
    print(get_devicelist())
    print(get_i2c_address())

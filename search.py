#!/usr/bin/python3

import subprocess

def get_devicelist():
    devices = subprocess.getoutput("/usr/sbin/i2cdetect -y 1").split(" ")
    l = []
    for device in devices:
        if len(device) == 2 and device != '--':
            l.append('0x' + device)
    return l

if __name__ == '__main__':
    print(get_devicelist())

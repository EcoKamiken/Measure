#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import paramiko
import shutil
import time
import datetime

from configparser import ConfigParser

def upload_log():
    d = datetime.datetime.now()
    config = ConfigParser()
    script_dir = os.path.dirname(__file__)

    config.read(script_dir + '/' + 'config.ini', 'UTF-8')
    host = config.get('ssh', 'host')
    port = config.getint('ssh', 'port')
    user = config.get('ssh', 'user')
    passwd = config.get('ssh', 'passwd')

    place = config.get('web', 'place')
    data_dir = config.get('web', 'data_dir')

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=user, password=passwd)
        sftp_connection = client.open_sftp()

        filenames = ['thermometer', 'wattage']
        for fname in filenames:
            sftp_connection.put(script_dir + '/' + fname + '.csv', data_dir + '/' + fname + '/' + place + '/' + '{}{}.csv'.format(fname, d.strftime("%Y%m%d_%H%M%S")))
            shutil.move(script_dir + '/' + fname + '.csv', script_dir + '/' + 'logs/{0}/{0}{1}.csv'.format(fname, d.strftime("%Y%m%d_%H%M%S")))
    except:
        raise
    finally:
        if client:
            client.close()

if __name__ == '__main__':
    upload_log()
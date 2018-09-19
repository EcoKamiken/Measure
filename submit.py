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
            csv_filename = fname + d.strftime("%Y%m%d_%H") + '.csv'
            original = script_dir + '/' + fname + '.csv'
            destination = data_dir + '/' + fname
            backup_dir = script_dir + '/' + 'logs' + '/' + fname

            sftp_connection.put(original, destination + '/' + place + '/' + csv_filename)
            shutil.move(original, backup_dir + '/' + csv_filename)
    except:
        raise
    finally:
        if client:
            client.close()

if __name__ == '__main__':
    upload_log()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import paramiko
import shutil
import time
import datetime

from configparser import ConfigParser

now = datetime.datetime.now().strftime("%Y%m%d_%H")
here = os.path.dirname(__file__)

config = ConfigParser()
config.read(here + '/' + 'config.ini', 'UTF-8')
host = config.get('ssh', 'host')
port = config.getint('ssh', 'port')
user = config.get('ssh', 'user')
passwd = config.get('ssh', 'passwd')

site_id = config.getint('info', 'id')
device_id = config.getint('info', 'device_id')
post_to = config.get('info', 'post_to')

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=user, password=passwd)
    sftp_connection = client.open_sftp()

    filename = 'log.csv'
    filename_bk = 'log_' + now + '.csv'

    logfile = here + '/' + filename
    logfile_bk = here + '/logs/' + filename_bk
    shutil.move(logfile, logfile_bk)

    sftp_connection.put(logfile_bk, post_to + '/' + str(site_id) + '/' +
            str(device_id) +
            '/' + filename_bk)
except:
    raise
finally:
    if client:
        client.close()

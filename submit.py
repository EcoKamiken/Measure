#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import paramiko
import scp
import shutil
import time
import subprocess
import sys

from configparser import ConfigParser

measure_root = os.environ['MEASURE_ROOT']
current_time = datetime.datetime.now().strftime("%Y%m%d_%H")

# Sync /dev/shm/log.csv $MEASURE_ROOT/log.csv
cmd = ['rsync', '-av', '--chmod=F644,D755', '/dev/shm/', measure_root]
try:
    subprocess.check_call(cmd)
except:
    print('Error: rsync failed.', file=sys.stderr)
    sys.exit(1)

# コンフィグファイルを読み込み
config = ConfigParser()
config.read(measure_root + '/' + 'config.ini', 'UTF-8')

# ファイル転送プロトコル(SFTP or SCP)
transfer_protocol = config.get('protocol', 'transfer_protocol')

# SSH接続情報
host = config.get('ssh', 'host')
port = config.getint('ssh', 'port')
user = config.get('ssh', 'user')
passwd = config.get('ssh', 'passwd')

# 発電所情報
site_id = config.getint('info', 'id')
device_id = config.getint('info', 'device_id')
post_to = config.get('info', 'post_to')

if __name__ == '__main__':
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=user, password=passwd)

        filename = 'log.csv'
        backup = filename.split('.')[0] + '_' + current_time + '.csv'

        original_file_path = measure_root + '/' + filename
        backup_file_path = measure_root + '/logs/' + backup
        shutil.move(original_file_path, backup_file_path)

        if transfer_protocol == 'SFTP':
            with ssh.open_sftp() as sftp:
                print(backup_file_path, post_to + '/' + str(site_id) + '/' +
                      str(device_id) + '/' + backup)
                res = sftp.put(backup_file_path, post_to + '/' + str(site_id) +
                               '/' + str(device_id) + '/' + backup)
                print(res)
        elif transfer_protocol == 'SCP':
            with scp.SCPClient(ssh.get_transport()) as scp:
                print(backup_file_path, post_to + '/' + str(site_id) + '/' +
                      str(device_id) + '/' + backup)
                scp.put(backup_file_path, post_to + '/' + str(site_id) + '/' +
                        str(device_id) + '/' + backup)

        os.remove('/dev/shm/log.csv')


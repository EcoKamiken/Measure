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
site_name = config.get('info', 'site_name')
site_id = config.getint('info', 'id')
device_id = config.getint('info', 'device_id')
post_to = config.get('info', 'post_to')

def debug(exc):
    print('--- ERROR ---')
    print('TYPE: ' + str(type(e)))
    print('ARGS: ' + str(e.args))
    print('EXCEPTION: ' + str(e))

if __name__ == '__main__':
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(str(host), port=port, username=user, password=passwd)

        filename = 'log.csv'
        backup = filename.split('.')[0] + '_' + current_time + '.csv'


        try:
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
                with scp.SCPClient(ssh.get_transport()) as s:
                    print(backup_file_path, post_to + '/' + site_name + '/' + backup)
                    s.put(backup_file_path, post_to + '/' + site_name + '/' + backup)
        except FileNotFoundError as e:
            print('missing log.csv')
        except scp.SCPException as e:
            shutil.move(backup_file_path, original_file_path)

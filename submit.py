#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import paramiko
import scp
import shutil
import time

from configparser import ConfigParser

current_time = datetime.datetime.now().strftime("%Y%m%d_%H")
current_dir = os.path.dirname(__file__)

# コンフィグファイルを読み込み
config = ConfigParser()
config.read(current_dir + '/' + 'config.ini', 'UTF-8')

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
        ssh.exec_command('mkdir -p ' + post_to + '/' + str(site_id) + '/' + str(device_id))

        filename = 'log.csv'
        backup = filename.split('.')[0] + '_' + current_time + '.csv'

        original_file_path = current_dir + '/' + filename
        backup_file_path = current_dir + '/logs/' + backup
        shutil.move(original_file_path, backup_file_path)

        if transfer_protocol == 'SFTP':
            with ssh.open_sftp() as sftp:
                sftp.put(backup_file_path, post_to + '/' + str(site_id) + '/' +
                         str(device_id) + '/' + backup)
        elif transfer_protocol == 'SCP':
            with scp.SCPClient(ssh.get_transport()) as scp:
                scp.put(backup_file_path, post_to + '/' + str(site_id) + '/' +
                        str(device_id) + '/' + backup)


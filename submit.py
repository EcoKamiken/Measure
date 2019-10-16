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

from logzero import logger, loglevel, logfile
from configparser import ConfigParser

measure_root = os.environ['MEASURE_ROOT']
current_time = datetime.datetime.now().strftime("%Y%m%d_%H")

# logzero
logfile("%s/syslog/submit.log" % measure_root, maxBytes=65536, backupCount=3, loglevel=10)

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


def print_debug(exc):
    logger.debug('--- DEBUG ---')
    logger.debug('TYPE: ' + str(type(exc)))
    logger.debug('ARGS: ' + str(exc.args))
    logger.debug('EXCEPTION: ' + str(exc))


def check_ssh(host, port, user, passwd, interval=3, retries=3):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for x in range(retries):
        try:
            ssh.connect(str(host), port=port, username=user, password=passwd)
            return ssh
        except OSError as e:
            print_debug(e)
            logger.info('retry: ' + str(x+1))
            time.sleep(interval)
    return False


if __name__ == '__main__':
    ssh = check_ssh(host=str(host), port=port, user=user, passwd=passwd)
    if ssh is False:
        logger.error("exit")
        sys.exit()

    filename = 'log.csv'
    backup = filename.split('.')[0] + '_' + current_time + '.csv'

    original_file_path = measure_root + '/' + filename
    backup_file_path = measure_root + '/logs/' + backup

    try:
        shutil.move(original_file_path, backup_file_path)
        logger.info('Backup: log.csv ' + original_file_path + ' -> ' + backup_file_path)
    except FileNotFoundError as e:
        logger.error('missing log.csv')
        sys.exit()

    
    logger.info('Protocol: ' + transfer_protocol)
    if transfer_protocol == 'SFTP':
        # TODO: Error handling
        with ssh.open_sftp() as sftp:
            dist = post_to + '/' + str(site_id) + '/' + str(device_id) + '/' + backup
            logger.info('Submit: remote server ' + backup_file_path, dist)
            sftp.put(backup_file_path, dist)

    elif transfer_protocol == 'SCP':
        try:
            with scp.SCPClient(ssh.get_transport()) as s:
                dist = post_to + '/' + site_name + '/' + backup
                logger.info('Submit: remote server')
                logger.info(backup_file_path + ' -> ' + dist)
                s.put(backup_file_path, dist)
        except scp.SCPException as e:
            print_debug(e)
            logger.error('submit failed.')
            logger.info(backup_file_path + ' -> ' + original_file_path)
            shutil.move(backup_file_path, original_file_path)

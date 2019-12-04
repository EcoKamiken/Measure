#!/usr/bin/env python3
"""mail_notification.py"""

import csv
import os
import datetime
import glob
import sys

from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from configparser import ConfigParser

# $MEASURE_ROOT
measure_root = os.environ['MEASURE_ROOT']

# Read 'config.ini'
config = ConfigParser()
config.read(os.path.join(measure_root, 'config.ini'), 'UTF-8')

class Email():
    def __init__(self):
        self.dt = datetime.datetime.now()
        self.site_name = config.get('info', 'site_name')
        self.smtp_host = config.get('email', 'host')
        self.smtp_port = config.get('email', 'port')
        self.smtp_user = config.get('email', 'user')
        self.smtp_pass = config.get('email', 'passwd')
        self.from_addr = config.get('email', 'from_addr')
        self.to_addr = config.get('email', 'to_addr')
        self.subject = self.dt.strftime('[{}] %Y-%m-%d 発電量情報'.format(self.site_name))
        self.body = ''

        self.set_body()
        self.create_mime()


    def set_body(self):
        __date_str = self.dt.strftime('%Y%m%d')
        __daily_csv_path = os.path.join(measure_root, 'logs', 'daily_{}.csv'.format(__date_str))
        self.body += '本日の発電量は以下の通りです。\n\n'
        self.body += '日時    発電量 [kWh]\n'
        self.body += '-----------------------------\n'
        with open(__daily_csv_path, 'r') as fp:
            lines = fp.read().splitlines()
            for line in lines:
                self.body += line + '\n'


    def create_mime(self):
        self.msg = MIMEText(self.body, "plain", "utf-8")
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.from_addr
        self.msg['To'] = self.to_addr

    def send(self):
        with SMTP_SSL(self.smtp_host, self.smtp_port) as smtps:
            smtps.login(self.smtp_user, self.smtp_pass)
            smtps.send_message(self.msg)


if __name__ == '__main__':
    em = Email()
    em.send()


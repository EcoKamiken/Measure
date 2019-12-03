#!/usr/bin/env python3
"""mail_notification.py"""

import csv
import os
import datetime
import glob

from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from configparser import ConfigParser

# $MEASURE_ROOT
measure_root = os.environ['MEASURE_ROOT']

# Read 'config.ini'
current_dir = os.path.dirname(__file__)
config = ConfigParser()
config.read(current_dir + '/' + 'config.ini', 'UTF-8')

class Email():
    def __init__(self):
        self.smtp_host = config.get('email', 'host')
        self.smtp_port = config.get('email', 'port')
        self.smtp_user = config.get('email', 'user')
        self.smtp_pass = os.environ.get('SMTP_PASS')

    def create_mime(self, subject, body):
        self.charset = 'utf-8'
        self.body = body
        self.msg = MIMEText(body, "plain", self.charset)
        self.msg['Subject'] = subject
        self.msg['From'] = 'solar@kamiken.info'
        self.msg['To'] = config.get('email', 'to_addr')

    def send(self):
        dt = datetime.datetime.now()
        with SMTP_SSL(self.smtp_host, self.smtp_port) as smtps:
            smtps.login(self.smtp_user, self.smtp_pass)
            smtps.send_message(self.msg)
        if dt.strftime('%H') == '20':
            with SMTP_SSL(self.smtp_host, self.smtp_port) as smtps:
                smtps.login(self.smtp_user, self.smtp_pass)
                smtps.send_message(self.msg)


if __name__ == '__main__':
    em = Email()
    dt = datetime.datetime.now()

    date_str = dt.strftime("%Y%m%d")
    with open(measure_root + "/logs/daily_{}.csv".format(date_str), 'r') as fp:
        lines = fp.read().splitlines()
        s = '本日の発電量は以下の通りです。\n\n日時\t発電量[kWh]\n-----------------------------------------\n'
        for i in lines:
            s += i + '[kWh]\n'
        subject = dt.strftime("%Y-%m-%d 発電量情報")
        body = s
        em.create_mime(subject, body)
        em.send()


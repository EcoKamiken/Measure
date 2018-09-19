#!/bin/bash

cp example_config.ini config.ini

git clone https://github.com/szazo/DHT11_Python.git
apt-get install -y python3-paramiko python3-scp python3-rpi.gpio postfix

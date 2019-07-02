#!/bin/bash

# コンフィグファイルをコピー
cp example_config.ini config.ini

# 必要なライブラリをインストール
git clone https://github.com/szazo/DHT11_Python.git
apt-get install -y python3-paramiko python3-scp python3-rpi.gpio postfix i2c-tools

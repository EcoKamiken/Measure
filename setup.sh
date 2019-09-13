#!/bin/bash

# コンフィグファイルをコピー
cp example_config.ini config.ini

# 必要なライブラリをインストール
git clone https://github.com/szazo/DHT11_Python.git
pip3.7 install --user -r requirements.txt


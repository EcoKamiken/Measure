#!/bin/bash

# 必要なライブラリをインストール
if [[ ! -e DHT11_Python ]]; then
  git clone https://github.com/szazo/DHT11_Python.git
fi

pip3.7 install --user -r requirements.txt

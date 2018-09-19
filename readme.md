# k

## 使い方

## raspi-configでi2cを有効にする

## 以下のコマンドを実行して設定を行う

```
$ adduser kamiken
$ passwd kamiken
$ su kamiken
$ cd
$ git clone https://github.com/ecokamiken/k
$ cd k
$ sudo ./setup.sh
$ sudo crontab -u root crontab_settings
```

## 動かない場合

```
# アドレスを確認
$ sudo i2cdetect -y 1
$ vim wattage.py
I2C_ADDRの値を変更
```

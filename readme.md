# Measure

## 使い方

## raspi-configでi2cを有効にする

## 以下のコマンドを実行して設定を行う

```
$ git clone https://github.com/EcoKamiken/Measure
$ cd Measure
$ sudo ./setup.sh
$ sudo crontab -u root cron.conf
```

## 動かない場合

```
# アドレスを確認
$ sudo i2cdetect -y 1
$ vim wattage.py
I2C_ADDRの値を変更
```

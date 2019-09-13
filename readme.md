# Measure

## Setup

```
$ sudo raspi-config
Advanced Options -> I2C -> Yes -> Reboot

$ sudo usermod -aG i2c $USER
```

## Getting started

```
$ git clone https://github.com/ecokamiken/measure ~/measure
$ cd ~/measure
$ echo "export MEASURE_ROOT=\"$HOME/measure\" >> ~/.bashrc
$ ./setup.sh
$ crontab cron.conf
```

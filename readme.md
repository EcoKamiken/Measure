# Measure

## Setup

```
$ sudo raspi-config
Advanced Options -> I2C -> Yes -> Reboot

$ sudo usermod -aG i2c $USER
```

## Getting started

### Install

```
$ git clone https://github.com/ecokamiken/measure ~/measure
$ cd ~/measure
$ echo "export MEASURE_ROOT=\"$HOME/measure\" >> ~/.bashrc
$ ./setup.sh
```

## Environments

```
$MEASURE_ROOT="/path/to/measure"
$SMTP_PASS="Password"
```

## Cron

```
$ vim cron.conf
MEASURE_ROOT="/path/to/measure"
$ crontab cron.conf
```

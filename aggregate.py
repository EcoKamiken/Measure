#!/usr/bin/env python3

import os 
import csv
import datetime
import shutil

# $MEASURE_ROOT
measure_root = os.environ['MEASURE_ROOT']
dt = datetime.datetime.now()
daily_filename = dt.strftime("daily_%Y%m%d.csv")
hourly_filename = dt.strftime("hourly_%Y%m%d_%H.csv")
dt = dt.strftime("%H:00")

def aggregate():
    count = 0
    total = 0
    with open(measure_root + '/log.csv', 'r') as fp:
        reader = csv.reader(fp)
        for row in reader:
            total += float(row[4])
            count += 1
    with open(measure_root + '/logs/{}'.format(daily_filename), 'a') as fp:
        fp.write(dt + ': ' + str(round(total/count, 2)) + ' [kWh]\n')

if __name__ == "__main__":
    aggregate()
    shutil.move(measure_root + '/log.csv', measure_root + '/logs/{}'.format(hourly_filename))

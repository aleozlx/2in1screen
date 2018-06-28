#!/usr/bin/env python
# ref: https://gist.githubusercontent.com/ei-grad/4d9d23b1463a99d24a8d/raw/rotate.py
from time import sleep
from os import path as op
import sys
from subprocess import check_call, check_output
from glob import glob

def bdopen(fname):
    return open(op.join(basedir, fname))

def read(fname):
    return bdopen(fname).read()

basedir = glob('/sys/bus/iio/devices/iio:device*/in_accel*')
if len(basedir):
	basedir = op.dirname(basedir[0])
else:
    sys.stderr.write("Can't find an accellerator device!\n")
    sys.exit(1)

scale = float(read('in_accel_scale'))
g = 7.0  # (m^2 / s) sensibility, gravity trigger

STATES = [
    {'rot': 'normal', 'coord': '1 0 0 0 1 0 0 0 1', 'touchpad': 'enable', 'check': lambda x, y: y <= -g},
    {'rot': 'inverted', 'coord': '-1 0 1 0 -1 1 0 0 1', 'touchpad': 'disable', 'check': lambda x, y: y >= g},
    # {'rot': 'left', 'coord': '0 -1 1 1 0 0 0 0 1', 'touchpad': 'disable', 'check': lambda x, y: x >= g},
    # {'rot': 'right', 'coord': '0 1 0 -1 0 1 0 0 1', 'touchpad': 'disable', 'check': lambda x, y: x <= -g},
]

def rotate(state):
    s = STATES[state]
    check_call(['xrandr', '-o', s['rot']])
    for dev in ['Wacom HID 4846 Finger']:
        check_call([
            'xinput', 'set-prop', dev,
            'Coordinate Transformation Matrix',
        ] + s['coord'].split())

def read_accel(fp):
    fp.seek(0)
    return float(fp.read()) * scale

if __name__ == '__main__':
    accel_x = open(op.join(basedir, 'in_accel_x_raw'))
    accel_y = open(op.join(basedir, 'in_accel_y_raw'))
    current_state = None
    while True:
        x = read_accel(accel_x)
        y = read_accel(accel_y)
        # print(x, y)
        for i in range(len(STATES)):
            if i == current_state:
                continue
            if STATES[i]['check'](x, y):
                current_state = i
                rotate(i)
                break
        sleep(2)

import pyfirmata
from pyfirmata import Arduino, util

import platform
import os
import re
import tkinter as tk
import time
import csv

system = platform.system()

################# Sample rate per second #################
sample_rate = 100
##########################################################

def append_to_csv(file_path, value):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([value])

def boardSetup():
    global board, sensor
    ######################## Arduino Setup ########################
    lines = []

    if system == "Darwin":
        print("Mac OS Detected, finding ports")
        output = os.popen('ls /dev/tty.*').read()
    elif system == "Windows":
        print("Windows Detected, finding ports")
        output = os.popen('wmic path Win32_SerialPort').read()
    else:
        print("Unknown operating system")

    output = os.popen('ls /dev/tty.*').read()

    for substr in output.split('\n'):
        substr2 = re.sub('\x1b\[[0-9;]*m', '', substr)
        lines.append(substr2)
        print(substr2)
    lines.pop()

    def_index = 0
    for i, line in enumerate(lines):
        if "usb" in line:
            def_index = i
            break

    default_port_name = lines[def_index]
    print("Default Port: " + default_port_name)

    try:
        board = pyfirmata.Arduino(default_port_name)
        it = pyfirmata.util.Iterator(board)
        it.start()
        sensor = board.get_pin('a:2:i')
    except:
        tk.messagebox.showerror('Arduino Selection error', 'Arduino not found')

    ######################## Arduino Setup ########################

board = None
sensor = None
file_path = 'collected_sensor_data.csv'

boardSetup()

it = util.Iterator(board)
it.start()

while True:
    sensor_value = sensor.read()
    if sensor_value is not None:
        print(sensor_value)
        append_to_csv(file_path, sensor_value)

    else:
        print("Not working, either pyfirmata firmware not uploaded or sensor not connected properly")
        append_to_csv(file_path, "Null")



    time.sleep(1/sample_rate)

'''
qwertyToDorak.py ~code adapted~ http://forum.arduino.cc/index.php?topic=319151.0
Derivitive work ~ Copyright 2015 ~ Paul Beaudet ~ GPLv2 see licence for details

This code converts USB input(qwerty) to Dvorak via an attach Arduino
that outputs the convertion result with the Arduino keyboard library

note that currently /dev/input/event1 should be passed as an argument when
calling this program ~ example
" python qwertyToDorak '/dev/input/event1' "
'''

import sys
import globalData as GD  # There should be a better way of managing this
import arduinoComms as Arduino
import evdev as listener
import QtoDConverter as Convert
from array import *

GD.arduinoBoard = "Yun" # "Other" or "Leonardo" or "Yun"

GD.serialPort = "/dev/ttyATH0" # for the Yun
# GD.serialPort = "/dev/ttyACM0"

#=============================  SET_UP
    # open Serial Connection
print "Setup Serial Connection"
try:
    Arduino.setupSerial(GD.serialPort, 115200)
    print "Serial Port Open"

except Exception as Ex:
    print "failed to open serial port"
    print type(Ex)
    sys.exit();

events = listener.EventGenerator() # instantiate event generating object

#============================ MAIN LOOP

while True:
    events.refresh()
    press = events.pressEvent()
    release = events.releaseEvent()
    if press:
        convertion = Convert.toDvorak(press)
        if convertion is "er":
            print press
        else:
            Arduino.sendTo(convertion + "1")
    if release:
        convertion = Convert.toDvorak(release)
        if convertion is "er":
            print release
        else:
            Arduino.sendTo(convertion + "0")
        # print release + " released"

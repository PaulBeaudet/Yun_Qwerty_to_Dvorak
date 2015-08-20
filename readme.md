# USB Qwerty to "your layout" converter

This is a project specifically designed for the Arduino Yun board. A USB keyboard is plugged into the Yun and the micro USB on the Yun into a computer. The code included with this project converts specifically the standard Qwerty keyboard layout to Dvorak for the author's convenience but it can be adapted to other layouts.

The code base has been adapted from two separate pieces of code developed by Micah Dowty (evdev.py) and a Serial protocol code example provided by Robin2 on the Arduino forums - http://forum.arduino.cc/index.php?topic=319151.0

The later of which has been helpful to start but will likely completely be re-adapted to work asynchronously, (although I'm not sure how much I care if there is no concern of blocking or speed)

This code is licensed GPL v2 in respect of derived work, see licence for details

## Using
In order to use this converter the usbConverter folder will need to be scp(ed) to your Yun

This is done issuing a command like this from a local unix computer,

    scp -r "path to /usbConverter/" root@192.168."yun address":/"path on yun"

Of course that is hardly helpful to copy and paste, but its hard to tell where on might have there stuff or might want to put it. Or what address a router gave the Yun.

Once files are on the Yun and the sketch is uploaded to Yun's 32u4

NOTE: this does not autorun yet (though planning on it)

To start, SSH into the Yun

    ssh root@"yunIPaddress"

Enter Yun's password then execute the python program from there

    python qwertyToDorak.py '/dev/input/event1'

Of course this probably will not work because I messed with the packages so much I'm not sure what the exact dependencies are. Or how much of this would just "work" for any given Yun firmware.

Trying to install the following will probably do it, but I'm interested to know what is actually needed and what is not depending on Yun firmware.

    opkg update
    opkg install kmod-input-core
    opkg install kmod-input-evdev
    opkg install kmod-usb-hid

  There were some helpful post here as to getting keyboards to work with yun.
  http://forum.arduino.cc/index.php?topic=207069.15

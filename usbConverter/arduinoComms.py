import serial
import time
import sys
import glob
import globalData as GD

# global variables for module
GD.startMarker = 60
GD.endMarker = 62
GD.ser = "x"
GD.inputBuff = ''
GD.readInProgress = False

#========================

def listSerialPorts():
	# http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#========================

def setupSerial(serPort, baudRate):


	if GD.arduinoBoard == 'Leonardo':
		print "Resetting Leonardo"
		GD.ser = "x"
		GD.ser = serial.Serial(serPort, 1200)
		GD.ser.rtscts = True
		time.sleep(0.5);
		GD.ser.close();
		print "Waiting 12 secs for Leonardo reset process to complete"
		time.sleep(12);


	if GD.arduinoBoard == 'Yun':
		print "Resetting 32u4 on Yun"
		fData = []
		fData.append(["18",   "/sys/class/gpio/export"])             # make GPIO18 available
		fData.append(["high", "/sys/class/gpio/gpio18/direction"])   # set pin 18 as output
		fData.append(["1",    "/sys/class/gpio/gpio18/value"])       # Set pin 18 high
		fData.append(["0",    "/sys/class/gpio/gpio18/value"])       # Set pin 18 low
		fData.append(["18",   "/sys/class/gpio/unexport"])           # close out GPIO18

		try:
			for fd in fData:
				with open(fd[1], "w") as f:
					f.write(fd[0])
		except Exception as Ex:
			print "Exception "
			print type(Ex)
			sys.exit()
		print "Waiting 2 secs for Yun reset process to complete"
		time.sleep(2)


	print "Trying to Open Serial Port"
	GD.ser = "x"
	GD.ser = serial.Serial(serPort, baudRate)
	if GD.arduinoBoard != 'Yun':
		GD.ser.rtscts = True	# seems essential to guarantee a clean start
	if GD.arduinoBoard == 'Other':
		print "Waiting 10 secs for Uno reset process to complete"
		time.sleep(10);
	print "Serial port " + serPort + " opened  Baudrate " + str(baudRate)

	waitForArduinoB()

#========================

def closeSerial():

	if GD.ser != "x":
		GD.ser.close()
		print "Serial Port Closed"
	else:
		print "Serial Port Not Opened"

#========================

def sendTo(sendStr):

	GD.ser.write(chr(GD.startMarker))
	GD.ser.write(sendStr)
	GD.ser.write(chr(GD.endMarker))


#===========================


def recvFromArduino(timeOut): # timeout in seconds eg 1.5

	#~ print "Called with T-O %s" %(timeOut)

	dataBuf = ""
	x = "z" # any value that is not an end- or startMarker
	startTime = time.time()

	# wait for the start marker
	while  ord(x) != GD.startMarker:
		if time.time() - startTime >= timeOut:
			return('<<')
		if GD.ser.inWaiting() > 0: # because ser.read() blocks
			x = GD.ser.read()

	# save data until the end marker is found
	while ord(x) != GD.endMarker:
		if time.time() - startTime >= timeOut:
			return('>>')

		if ord(x) != GD.startMarker:
			dataBuf = dataBuf + x

		if GD.ser.inWaiting() > 0:
			x = GD.ser.read()
		else:
			x = chr(GD.startMarker) # crude way to prevent repeat characters
								 #   when no data is received

	return(dataBuf)


#============================

def recvFromArduinoNoTimeout():

	waitingForData = True
	readInProgress = False
	inputBuff = ''

	while (waitingForData == True):
		x = GD.ser.read()	# don't care that it blocks

		if readInProgress == True:
			if ord(x) == GD.endMarker:
				waitingForData = False
			else:
				inputBuff += x

			# this is here to prevent the startMarker going into inputBuff
		if ord(x) == GD.startMarker:
			readInProgress = True
			inputBuff = ''

	return inputBuff

#============================

def waitForArduinoB():

	# this version assumes the reset period is already complete
	# first send "Python Ready" so the Arduino knows it is safe to talk
	#	required by the Yun
	# then listen for Arduino to send 'Arduino Ready'
	# it also ensures that any bytes left over from a previous message are discarded

	msg = ""
	while msg.find("Arduino is ready") == -1:
			# send start message
		print "Sending start message"
		sendTo("Python ready")
			# listen for response
		msg = recvFromArduino(10)

		print msg
		print

#============================


def waitForArduino():

   # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
   # it also ensures that any bytes left over from a previous message are discarded

	print "Waiting for Arduino to reset"

	msg = ""
	while msg.find("Arduino is ready") == -1:

		msg = recvFromArduino(10)

		print msg
		print

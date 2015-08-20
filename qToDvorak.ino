// a simple program to illustrate communication on a Yun between a Python
//     program on Linux side and a program on the Arduino
//
// this program only makes sense as a companion to the program SimpleDemo.py
// it just causes the on-board LED to switch on or off when "ON" or "OFF" is
//   typed at the request of the Python program
//
// it is NOT intended to be a "useful" program on a Yun as it just uses an SSH
//   terminal for input
//
// if Serial1 is used it will work on a Yun
// if you change it to Serial it will work between a PC and an Uno, Mega or Leonardo
//
// note that, for testing this Arduino code with the Serial Monitor on an Uno
//   Mega or Leonardo
//       you will have to enter <Python ready> in the Serial Monitor to get the
//       the program to move out of setup()
//          This is to prevent the Arduino from interfering with the Linux boot
//          process on the Yun which takes longer than the Arduino startup
//
//       it expects to receive either <0> or <1> to make the
//       LED switch ON and OFF
//
//
// this code is very similar to the code in 3rd example in serial input basics
//       http://forum.arduino.cc/index.php?topic=288234.0
//

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

byte ledPin = 13;

//======================

void setup() {
	Serial1.begin(115200);
	Serial.begin(115200);

		// wait for python to send <Python ready>
	boolean startReceived = false;
	while (startReceived == false) {
		newData = false;
		recvWithStartEndMarkers();
		if (newData == true) {
			if (strcmp(receivedChars, "Python ready") == 0) {
				startReceived = true;
			}
		}
	}
		// send acknowledgment
	Serial1.println("<Arduino is ready>");

	pinMode(ledPin, OUTPUT);
}

//======================

void loop() {
	recvWithStartEndMarkers();
	updateSerial();
  //updateLED();
}

//=======================

void updateSerial(){
	if(newData == true){
		//Serial.print("L:");
		Serial.print(receivedChars[4]);
		newData = false;
	}
}

void updateLED() {
	if (newData == true) {
		if (receivedChars[0] == '0') {
			digitalWrite(ledPin, LOW);
		}
		if (receivedChars[0] == '1') {
			digitalWrite(ledPin, HIGH);
		}
		newData = false;
	}
}

//========================

void recvWithStartEndMarkers() {
	static boolean recvInProgress = false;
	static byte index = 0;
	char startMarker = '<';
	char endMarker = '>';

	while (Serial1.available() > 0 && newData == false) {
		char readChar = Serial1.read();
		if(recvInProgress) {
			if(readChar != endMarker) {
				receivedChars[index] = readChar;
				index++;
				if(index >= numChars) {index = numChars - 1;} // prevent overflow
			} else {
				receivedChars[index] = '\0'; // terminate the string
				recvInProgress = false;
				index = 0;
				newData = true;
			}
		}
		else if(readChar == startMarker){recvInProgress = true;}
	}
}

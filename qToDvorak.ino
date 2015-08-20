// qToDvorak.ino ~
// See licence for details
const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

//======================

void setup() {
	Serial1.begin(115200);
	Serial.begin(115200);
	Keyboard.begin();

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
}

//======================

void loop() {
	recvWithStartEndMarkers();
	// updateSerial();
	printKeys();
}

//=======================

void updateSerial(){
	if(newData == true){
		Serial.print(receivedChars[0]);
		newData = false;
	}
}

void printKeys(){
	if(newData == true){
		if(receivedChars[1] == '1'){Keyboard.press(receivedChars[0]);}
		else                       {Keyboard.release(receivedChars[0]);}
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

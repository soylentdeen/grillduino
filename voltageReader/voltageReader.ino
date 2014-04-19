/*
  Grillduino
  Reads three analog voltages on pins 0, 1, and 2, prints the result to the serial monitor.

  This code was adapted from analogReadSerial code from the Arduino
  website. 
 */

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int R1Value = analogRead(A0);
  int R2Value = analogRead(A1);
  int R3Value = analogRead(A2);
  float V1 = R1Value * (5.0 / 1023.0);
  float V2 = R2Value * (5.0 / 1023.0);
  float V3 = R3Value * (5.0 / 1023.0);
  // print out the value you read:
  Serial.print(V1);
  Serial.print(" ");
  Serial.print(V2);
  Serial.print(" ");
  Serial.println(V3);
  delay(10000);        // delay 30 sec in between reads
}

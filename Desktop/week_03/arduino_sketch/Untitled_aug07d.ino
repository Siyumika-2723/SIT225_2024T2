#include "arduino_secrets.h"
#include "thingProperties.h"



#define TRIG_PIN 2
#define ECHO_PIN 3

void setup() {
  Serial.begin(9600);
  delay(1500);
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  ArduinoCloud.update();
  long duration;
  float distance;

  // Send pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read echo
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;

  distance_cm = distance;  // Update Cloud variable
  Serial.print("Distance: ");
  Serial.print(distance_cm);
  Serial.println(" cm");

  delay(2000);  // Adjust delay if needed
}

/*
  Since DistanceCm is READ_WRITE variable, onDistanceCmChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onDistanceCmChange()  {
  // Add your code here to act upon DistanceCm change
}
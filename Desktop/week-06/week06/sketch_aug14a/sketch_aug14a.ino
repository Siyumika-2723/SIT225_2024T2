#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(115200);
  while (!Serial); 
  if (!IMU.begin()) {
    Serial.println("IMU init failed");
    while (1);
  }
  Serial.println("timestamp_ms,gx,gy,gz");
}

void loop() {
  float gx, gy, gz;
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz); 
    unsigned long t = millis();
    Serial.print(t); Serial.print(",");
    Serial.print(gx); Serial.print(",");
    Serial.print(gy); Serial.print(",");
    Serial.println(gz);
  }
  delay(10); 
}

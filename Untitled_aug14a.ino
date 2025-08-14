#include "arduino_secrets.h"
#include "thingProperties.h"
#include <DHT.h>
#include <Adafruit_Sensor.h>
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

#define DHTPIN 2
#define DHTTYPE DHT22


const float TEMP_HIGH_C   = 36.0;  // High temperature
const float HUM_LOW_PCT   = 20.0;  // Low humidity
const int   CONFIRM_READS = 3;     // Consecutive readings to trigger alarm
const unsigned long SAMPLE_MS = 1000;

DHT dht(DHTPIN, DHTTYPE);
unsigned long lastSample = 0;
int highTempCount = 0;
int lowHumCount  = 0;

void setup() {
  Serial.begin(9600);
  delay(1500);

  dht.begin();

  
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();

 
  unsigned long now = millis();
  if (now - lastSample < SAMPLE_MS) return;
  lastSample = now;

  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (isnan(t) || isnan(h)) {
    Serial.println("DHT read failed");
    return;
  }

  // Update cloud variables
  temperature = t;
  humidity = h;

  // Count consecutive abnormal readings
  highTempCount = (t >= TEMP_HIGH_C) ? highTempCount + 1 : 0;
  lowHumCount   = (h <= HUM_LOW_PCT) ? lowHumCount + 1 : 0;

  // Trigger alarm when confirmed
  if (!alarmTrigger && (highTempCount >= CONFIRM_READS || lowHumCount >= CONFIRM_READS)) {
    alarmTrigger = true;

    if (highTempCount >= CONFIRM_READS && lowHumCount >= CONFIRM_READS) {
      alarmMessage = "High temperature & low humidity";
    } else if (highTempCount >= CONFIRM_READS) {
      alarmMessage = "High temperature";
    } else {
      alarmMessage = "Low humidity";
    }
  }

  // Print for debugging
  Serial.print("T=");
  Serial.print(temperature);
  Serial.print("C  H=");
  Serial.print(humidity);
  Serial.print("%  Alarm=");
  Serial.print(alarmTrigger ? "ON" : "OFF");
  Serial.print("  Message=");
  Serial.println(alarmMessage);
}

// Reset alarm from dashboard switch
void onAlarmTriggerChange() {
  if (!alarmTrigger) {
    highTempCount = 0;
    lowHumCount = 0;
    alarmMessage = "Alarm reset from dashboard";
  }
}

// Required callbacks (empty)
void onTemperatureChange() {}
void onHumidityChange() {}
void onAlarmMessageChange() {}

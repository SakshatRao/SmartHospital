/*

This program Print temperature on terminal

Hardware Connections (Breakoutboard to Arduino):
Vin  - 5V (3.3V is allowed)
GND - GND
SDA - A4 (or SDA)
SCL - A5 (or SCL)

*/

#include <Wire.h>
#include "Protocentral_MAX30205.h"
MAX30205 tempSensor;

void setup() {

  Serial.begin(9600);
  Wire.begin();

  //scan for temperature in every 30 sec untill a sensor is found. Scan for both addresses 0x48 and 0x49
  while(!tempSensor.scanAvailableSensors()){
    Serial.println("Couldn't find the temperature sensor, please connect the sensor." );
    delay(30000);
  }

  tempSensor.begin();   // set continuos mode, active mode
}

void loop() {

  float temp = tempSensor.getTemperature(); // read temperature for every 100ms
  Serial.println(temp ,2);
  delay(100);
}

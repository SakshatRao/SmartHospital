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

#include<SoftwareSerial.h>
SoftwareSerial sw(2, 3);

void setup()
{
  Wire.begin();
  sw.begin(115200);
  // Serial.begin(9600);

  //scan for temperature until a sensor is found. Scan for both addresses 0x48 and 0x49
  while(!tempSensor.scanAvailableSensors()){
    delay(5000);
  }

  tempSensor.begin();   // set continuos mode, active mode
}

void loop()
{
  float temp = tempSensor.getTemperature(); // read temperature for every 100ms
  sw.print(temp, 2);
  // Serial.println(temp, 2);
  delay(5000);
}

#include "MAX30100_PulseOximeter.h"
#include <Wire.h>
#include<stdio.h>

#include<SoftwareSerial.h>
SoftwareSerial sw(2, 3);

uint32_t lastReportTime = 0;

PulseOximeter pox;

void setup()
{
  //Wire.begin();
  //sw.begin(115200);
  Serial.begin(9600);
  
  while(!pox.begin());
  pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
}

void loop()
{
  pox.update();
  uint32_t currentTime = millis();
  if(currentTime - lastReportTime > 100)
  {
    float bpm = pox.getHeartRate();
    char measurements[20];
    sprintf(measurements, "%d", (uint16_t)(bpm * 10));
    Serial.println(measurements);
    //sw.print(bpm, 2);
    lastReportTime = currentTime;
  }
}

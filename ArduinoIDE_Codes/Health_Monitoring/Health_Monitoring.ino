/*

TEMPERATURE connections:
  Vin  - 5V (3.3V is allowed)
  GND - GND
  SDA - A4 (or SDA)
  SCL - A5 (or SCL)

SPO2 connections:
  Vin - 3.3V
  GND - GND
  SDA - A4
  SCL - A5

*/

#include <Wire.h>

#include "Protocentral_MAX30205.h"
#include "MAX30100_PulseOximeter.h"

MAX30205 tempSensor;
PulseOximeter pox;

int MEASURE_PERIOD = 100;                   // Time between measurements (in ms)
int REPORT_PERIOD = 5000;                   // Time between sending the values to the NodeMCU

// For average value of SpO2 and BPM
uint8_t spO2_cnt = 0;
uint8_t bpm_cnt = 0;
float spO2 = 0;
float bpm = 0;
float temp = 0;

// For tracking last measurement and last report
uint32_t lastReportTime = 0;
uint32_t lastMeasureTime = 0;

#include<SoftwareSerial.h>
SoftwareSerial sw(2, 3);

void setup()
{ 
  Wire.begin();
  sw.begin(115200);
  //Serial.begin(9600);
  
  while(!tempSensor.scanAvailableSensors())
    delay(MEASURE_PERIOD);
  tempSensor.begin();

  while(!pox.begin())
    delay(MEASURE_PERIOD);
  pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
}

void loop()
{
  uint32_t currentTime = millis();
  pox.update();
  
  // Checking whether to measure
  if(currentTime - lastMeasureTime > MEASURE_PERIOD)
  {
    float spO2_val = (float)pox.getSpO2();
    if(spO2_val > 0)
    {
      spO2 += spO2_val;
      spO2_cnt += 1;
    }
    float bpm_val = (float)pox.getHeartRate();
    if(bpm_val > 0)
    {
      bpm += bpm_val;
      bpm_cnt += 1;
    }
    
    lastMeasureTime = currentTime;
  }
  
  // Checking whether to report values to the NodeMCU
  if(currentTime - lastReportTime > REPORT_PERIOD)
  {
    temp = tempSensor.getTemperature(); // read temperature for every 100ms
    
    if(spO2_cnt == 0)
      spO2 = 0;
    else
      spO2 /= spO2_cnt;
    
    if(bpm_cnt == 0)
      bpm = 0;
    else
      bpm /= bpm_cnt;
    
    char measurements[20];
    sprintf(measurements, "%d_%d_%d", (uint16_t)(temp * 10), (uint16_t)(spO2 * 10), (uint16_t)(bpm * 10));
    sw.println(measurements);
    //Serial.println(measurements);
    
    lastReportTime = currentTime;
    spO2 = 0;
    spO2_cnt = 0;
    bpm = 0;
    bpm_cnt = 0;
  }
}

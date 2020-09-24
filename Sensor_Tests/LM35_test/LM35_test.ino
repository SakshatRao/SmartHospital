const int sensor=A0;
float tempc;
float vout;

const int m=60;
float temperatures[m];

void setup()
{
  pinMode(sensor,INPUT);
  Serial.begin(9600);
  for(int i=0; i<m; i++)
    temperatures[i] = 0.0;
}

void loop() 
{
  vout=analogRead(sensor);
  vout=(vout*500)/1024;
  tempc=vout;

  float temperature_avg = 0;
  for(int i=1; i<m-1; i++)
  {
    temperatures[i] = temperatures[i+1];
    temperature_avg += (temperatures[i] / m);
  }
  temperatures[m-1] = tempc;
  temperature_avg += (tempc / m);
  Serial.println(temperature_avg);
  delay(1000);
}

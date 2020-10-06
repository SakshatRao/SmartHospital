int IR_recv_pin = A0;

// Exponential Smoothing Setup
float a = 0.05;
float s = 0;
int settle_sec = 8;
int calibrate_sec = 2;
int settle_time_cnt = settle_sec * 1000 / 75;
int calibrate_time_cnt = calibrate_sec * 1000 / 75;
float thresh_wt = 0.5;
float thresh;

float s_avg = 0;
float s_std = 0;

void calibrate() {
  for(int i = 0; i < settle_time_cnt; i++)
  {
    int ir_val = analogRead(IR_recv_pin);
    s = a * ir_val + (1 - a) * s;
    delay(75);
  }

  float s_avg = 0;
  for(int i = 0; i < calibrate_time_cnt; i++)
  {
    int ir_val = analogRead(IR_recv_pin);
    s = a * ir_val + (1 - a) * s;
    s_avg += (s / calibrate_time_cnt);
    delay(75);
  }

  thresh = thresh_wt * s_avg;
}

void setup() {
  pinMode(IR_recv_pin, INPUT);
  Serial.begin(9600);
  calibrate();
}

void loop() {
  int ir_val = analogRead(IR_recv_pin);
  Serial.print(ir_val);

  // Exponential Smoothing
  s = a * ir_val + (1 - a) * s;
  Serial.print("\t");
  Serial.print(s);

  Serial.print("\t");
  Serial.println(thresh);
  
  delay(75);
}

// Sensor Pins
int IR_recv_pin = A0;
int led_buzzer_pin = 7;
int pushbutton_pin = 6;

// Global Variables
int loop_delay = 75;

int detected;
bool alerted;
int alert_sec = 5;
int alert_time_cnt = alert_sec * 1000 / loop_delay;

float a = 0.5;
float s = 0;
int settle_sec = 5;
int calibrate_sec = 1;
int settle_time_cnt = settle_sec * 1000 / loop_delay;
int calibrate_time_cnt = calibrate_sec * 1000 / loop_delay;
float extr1, extr2;
float thresh;

void calibrate() {
  float s_avg = 0;

  s = 0;
  for(int i = 0; i < settle_time_cnt; i++)
  {
    int ir_val = analogRead(IR_recv_pin);
    s = a * ir_val + (1 - a) * s;
    delay(loop_delay);
  }

  for(int i = 0; i < calibrate_time_cnt; i++)
  {
    int ir_val = analogRead(IR_recv_pin);
    s = a * ir_val + (1 - a) * s;
    s_avg += (s / calibrate_time_cnt);
    delay(loop_delay);
  }
  extr1 = s_avg;

  digitalWrite(led_buzzer_pin, HIGH);
  delay(100);
  digitalWrite(led_buzzer_pin, LOW);
  delay(10000);

  s = 0;
  for(int i = 0; i < settle_time_cnt; i++)
  {
    int ir_val = analogRead(IR_recv_pin);
    s = a * ir_val + (1 - a) * s;
    delay(loop_delay);
  }

  s_avg = 0;
  for(int i = 0; i < calibrate_time_cnt; i++)
  {
    int ir_val = analogRead(IR_recv_pin);
    s = a * ir_val + (1 - a) * s;
    s_avg += (s / calibrate_time_cnt);
    delay(loop_delay);
  }
  extr2 = s_avg;

  digitalWrite(led_buzzer_pin, HIGH);
  delay(100);
  digitalWrite(led_buzzer_pin, LOW);
  delay(10000);
  thresh = (extr1 + extr2) / 2.0;

  delay(5000);
}

void setup() {
  pinMode(pushbutton_pin, INPUT);
  pinMode(IR_recv_pin, INPUT);
  pinMode(led_buzzer_pin, OUTPUT);

  detected = 0;
  alerted = false;
  
  calibrate();
}

void loop() {
  int ir_val = analogRead(IR_recv_pin);
  s = a * ir_val + (1 - a) * s;
  
  if(detected == 0)
  {
    if(s > thresh)
    {
      if(alerted == false)
      {
        detected = 1;
      }
    }
    else
    {
      if(alerted == true)
      {
        alerted = false;
      }
    }
  }
  else
  {
    if(detected == alert_time_cnt)
    {
      digitalWrite(led_buzzer_pin, LOW);
      detected = 0;
      alerted = true;
    }
    else
    {
      int button = digitalRead(pushbutton_pin);
      if(button == 1)
      {
        digitalWrite(led_buzzer_pin, LOW);
        detected = 0;
        alerted = true;
      }
      else
      {
        detected = detected + 1;
        if(detected % 8 < 2)
        {
          digitalWrite(led_buzzer_pin, HIGH);
        }
        else
        {
          digitalWrite(led_buzzer_pin, LOW);
        }
      }
    }
  }
  delay(loop_delay);
}

// Sensor Pins
int IR_recv_pin = A0;
int led_buzzer_pin = 7;
int pushbutton_pin = 6;

// Global Variables
int loop_delay = 75;                                                        // Refresh period (in ms)
int detected;                                                               // To check whether door motion has been detected
bool alerted;                                                               // To check whether incomer has been alerted
int alert_sec = 5;                                                          // Alert time (in s)
int alert_time_cnt = alert_sec * 1000 / loop_delay;                         // Number of ticks for alert

// For exponential smoothing
float a = 0.5;
float s = 0;

// For calibration
int settle_sec = 5;
int calibrate_sec = 1;
int settle_time_cnt = settle_sec * 1000 / loop_delay;
int calibrate_time_cnt = calibrate_sec * 1000 / loop_delay;
float extr1, extr2;
float thresh;

/*
  Calibration Steps:
    1. Settle time
    2. Measuring one extreme value
    3. Light blink
    4. Settle time
    5. Measuring second extreme value
    6. Light blink
    7. Final light blink
*/
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

  // Indicating first calibration
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

  // Indicating second calibration
  digitalWrite(led_buzzer_pin, HIGH);
  delay(100);
  digitalWrite(led_buzzer_pin, LOW);
  delay(10000);
  thresh = (extr1 + extr2) / 2.0;

  // Indicating device is ready
  digitalWrite(led_buzzer_pin, HIGH);
  delay(100);
  digitalWrite(led_buzzer_pin, LOW);
}

// Setting up GPIOs, initializing flags & performing calibration
void setup() {
  pinMode(pushbutton_pin, INPUT);
  pinMode(IR_recv_pin, INPUT);
  pinMode(led_buzzer_pin, OUTPUT);

  detected = 0;
  alerted = false;
  
  calibrate();
}

void loop() {
  // Measuring analog value
  int ir_val = analogRead(IR_recv_pin);
  s = a * ir_val + (1 - a) * s;
  
  /*
    Alerting Algorithm:
    1. If door motion is detected, start alerting; else do nothing
    2. Keep alerting till either pushbutton is pressed or time-out occurs
  */
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

unsigned int ir_input_pin = 2;
unsigned int led_output_pin = LED_BUILTIN;
unsigned int button_input_pin = 3;

int ir_values[] = {0, 0, 0, 0, 0};

void ir_update(int ir_value) {
  int i;
  int detected = 1;
  for(i=0; i<4; i++)
    ir_values[i] = ir_values[i+1];
  ir_values[i] = ir_value;
}

int ir_detect() {
  for(int i=0; i<5; i++)
    if(ir_values[i] == 1)
      return 1;
  return 0;
}

void setup() {
  pinMode(ir_input_pin, INPUT);
  pinMode(button_input_pin, INPUT);
  pinMode(led_output_pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  unsigned int ir_value = 1 - digitalRead(ir_input_pin);
  ir_update(ir_value);
  int detected = ir_detect();
  if(detected == 1)
  {
    digitalWrite(led_output_pin, HIGH);
    for(int i=0; i<200; i++)
    {
      unsigned int button_value = digitalRead(button_input_pin);
      if(button_value == 1)
        break;
      delay(50);
      ir_value = 1 - digitalRead(ir_input_pin);
      ir_update(ir_value);
    }
    digitalWrite(led_output_pin, LOW);
  }
  delay(50);
}

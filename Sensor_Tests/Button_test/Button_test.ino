int button_pin = 5;

void setup() {
  pinMode(button_pin, INPUT);
  Serial.begin(9600);
}

void loop() {
  int button_pressed = digitalRead(button_pin);
  Serial.println(button_pressed);
  delay(100);
}

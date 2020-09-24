int IR_recv_pin = A0;

void setup() {
  pinMode(IR_recv_pin, INPUT);
  Serial.begin(9600);
}

void loop() {
  int ir_val = analogRead(IR_recv_pin);
  Serial.println(ir_val);
  delay(1000);
}

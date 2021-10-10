int channel[4];
void setup() {
  // put your setup code here, to run once:
pinMode(2, INPUT);
pinMode(3, INPUT);
pinMode(4, INPUT);
pinMode(5, INPUT);
Serial.begin(19200);
}

void loop() {
  // put your main code here, to run repeatedly:
channel[0] = pulseIn(2, HIGH);
channel[1] = pulseIn(3, HIGH);
channel[2] = pulseIn(4, HIGH);
channel[3] = pulseIn(5, HIGH);
Serial.print(channel[0]);
Serial.print(' ');
Serial.print(channel[1]);
Serial.print(' ');
Serial.print(channel[2]);
Serial.print(' ');
Serial.print(channel[3]);
Serial.print('\n');
}

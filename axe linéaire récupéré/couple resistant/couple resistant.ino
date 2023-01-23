#define Y1 10
#define Y2 9

void setup() {
  // put your setup code here, to run once:
pinMode(Y1,OUTPUT);

pinMode(Y2,OUTPUT);
digitalWrite(Y2,0);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
for (int i =0; i<256;i++) {
  analogWrite(Y1,i);
  Serial.println(i);
  delay(250);

}
}

#define Y1 3
#define Y2 4 


void setup() {
  // put your setup code here, to run once:
pinMode(Y1,OUTPUT);
pinMode(Y2,OUTPUT);
pinMode(LED_BUILTIN,OUTPUT);
for (int i =0;i<3;i++) {
digitalWrite(LED_BUILTIN,HIGH);
delay(100);
digitalWrite(LED_BUILTIN,LOW);
delay(100);
}


digitalWrite(Y1,HIGH);
digitalWrite(Y2,LOW);
delay(500);
digitalWrite(Y1,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
 digitalWrite(Y1, HIGH);
 digitalWrite(Y2, LOW);
 delay(10000);
 digitalWrite(Y1,LOW);
 digitalWrite(Y2,HIGH);
 delay(10000);
}

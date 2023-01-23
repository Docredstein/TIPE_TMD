#define Y1 10
#define Y2 9
#define ArrayLength 255

#include "sine.h"
const auto f = 2;
char offset = 40;
double T = (1/(f*2*ArrayLength))*1000000; //dt entre chaque valeur de l'array en us
void setup() {
  Serial.begin(115200);
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
Serial.println(T);
/*
digitalWrite(Y1,HIGH);
digitalWrite(Y2,LOW);
delay(500);
digitalWrite(Y1,LOW);*/
}
unsigned long lastMicros =micros();
int lastI=0;
int i =0;
void loop() {
  // put your main code here, to run repeatedly:
 /*digitalWrite(Y1, HIGH);
 digitalWrite(Y2, LOW);
 delay(1000);
 digitalWrite(Y1,LOW);
 digitalWrite(Y2,HIGH);
 delay(1000);*/ 
 if ((micros()-lastMicros)>T) {
   i++;
   
   lastMicros = micros();
   if (i>=2*ArrayLength) {
     i=0;
   }
 }
 if (lastI != i ) {
 unsigned char si = min(sinus[i%ArrayLength],255);//max(sinus[i%ArrayLength],offset); //min(sinus[i%ArrayLength]+offset,255);
 //Serial.println(si);
si = map(si, 0,255, 0,255-offset) + offset;
 if (i<ArrayLength) {
   analogWrite(Y1, si);
   digitalWrite(Y2,0);
   //Serial.println(si);
 }
 else {
   analogWrite(Y2,si);
   digitalWrite(Y1,0);
   //Serial.println(-si);
 }
 Serial.println(i);
 lastI= i;
 }
 delayMicroseconds(1);
  
 


}

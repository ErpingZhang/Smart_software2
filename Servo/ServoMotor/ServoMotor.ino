#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int waittime;
int ang_per_step;
int origin_ang = 90;
void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  pinMode(13,OUTPUT);
  Serial.begin(9600);
}

void xincrease(){
  int current_ang = myservo.read();
  if (current_ang > 180 - ang_per_step){
    myservo.write(180);
    delay(waittime);
  }else{
     myservo.write(current_ang + ang_per_step);
     delay(waittime);
  }
}

void xdecrease(){
  int current_ang = myservo.read();
  if (current_ang < 0 + ang_per_step){
    myservo.write(0);
    delay(waittime);
  }else{
     myservo.write(current_ang - ang_per_step);
     delay(waittime);
  }
}

void move_origin(){
  myservo.write(origin_ang);
  delay(3000);
}

void loop() {
  if(Serial.available()>0){
    char data = Serial.read();
  if (data == 'i'){ // increase servo angle
    digitalWrite(13,1);
    delay(100);
    digitalWrite(13,0);
    xincrease();
    Serial.end();
    Serial.begin(9600);
  }
  if (data == 'd'){ //decrease servo angle
    digitalWrite(13,1);
    delay(50);
    digitalWrite(13,0);
    delay(50);
    digitalWrite(13,1);
    delay(50);
    digitalWrite(13,0);
    xdecrease();
    Serial.end();
    Serial.begin(9600);
  }
  if (data == 'o'){ //back to origin angle
    digitalWrite(13,1);
    move_origin();
    digitalWrite(13,0);
    Serial.end();
    Serial.begin(9600);
  }
  if (data == '2'){
    digitalWrite(13,1);
    delay(500);
    digitalWrite(13,0);
    Serial.end();
    Serial.begin(9600);
  }
}
}

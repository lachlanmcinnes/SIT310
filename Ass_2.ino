#include <Wire.h>
#include <Zumo32U4.h>

Zumo32U4ProximitySensors proxSensors;
Zumo32U4Motors motors;
Zumo32U4ButtonA buttonA;

bool proxLeftActive;
bool proxRightActive;
bool proxFrontActive;

void setup() {
  // put your setup code here, to run once:
  buttonA.waitForButton();
  delay(1000);

  proxSensors.initThreeSensors();

}

void printReadingsToSerial() {
  static char buffer[80];
  sprintf(buffer, "%d %d %d %d\n",
  proxSensors.countsLeftWithLeftLeds(),
  proxSensors.countsFrontWithLeftLeds(),
  proxSensors.countsFrontWithRightLeds(),
  proxSensors.countsRightWithRightLeds()
  );
  Serial.print(buffer);
}

void forward(int t) {
  motors.setLeftSpeed(100);
  motors.setRightSpeed(100);
  delay(t);
}

void backward(int t) {
  motors.setLeftSpeed(-100);
  motors.setRightSpeed(-100);
  delay(t);
}

void left(int t) {
  motors.setLeftSpeed(-100);
  motors.setRightSpeed(100);
  delay(t);
}

void right(int t) {
  motors.setLeftSpeed(100);
  motors.setRightSpeed(-100);
  delay(t);
}

void stop() {
  motors.setLeftSpeed(0);
  motors.setRightSpeed(0);
}

void fortyfivedeg(int t) {
  motors.setLeftSpeed(-100);
  motors.setRightSpeed(100);
  delay(t);
}

void loop() {
  // put your main code here, to run repeatedly:

  proxSensors.read();

  proxLeftActive = proxSensors.readBasicLeft();
  proxFrontActive = proxSensors.readBasicFront();
  proxRightActive = proxSensors.readBasicRight();
  
  printReadingsToSerial();

  movement();

  delay(100);
}


void movement() {

  if(proxSensors.countsLeftWithLeftLeds() <=3){
    right(500);
  }else if(proxSensors.countsRightWithRightLeds() <=3){
    left(500);
  } else if(proxSensors.countsFrontWithLeftLeds() <=3 || proxSensors.countsFrontWithRightLeds() <=3){
    backward(500);
    fortyfivedeg(1000);
  }else{
    forward(100);
  }
}

#define USE_USBCON

#include <Wire.h>
#include <Zumo32U4.h>

#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int8.h>
#include <std_msgs/Int16.h>
#include <std_msgs/String.h>

const uint16_t maxSpeed = 100;

Zumo32U4Buzzer buzzer;
Zumo32U4LineSensors lineSensors;
Zumo32U4Motors motors;
Zumo32U4ButtonA buttonA;
Zumo32U4LCD lcd;

int stopSend = 0;

ros::NodeHandle nh;
std_msgs::Int8 prox_msg;
std_msgs::Int16 l_msg;
std_msgs::Int16 r_msg;
std_msgs::String str_msg;

ros::Publisher pub_lerror("/zumo/lerror", &l_msg);
ros::Publisher pub_left("/zumo/leftsensor", &l_msg);
ros::Publisher pub_right("/zumo/rightsensor", &l_msg);
ros::Publisher pub_output("/zumo/rule", &str_msg);

void intersection(const geometry_msgs::Twist& cmd_msg){
  float y = cmd_msg.linear.y;
  float x = cmd_msg.linear.x;
  float xa = cmd_msg.angular.x;
  
  if(x==1.0){
    int16_t error = tan(xa)*2000;
    int16_t speedDiff = error/4;
    int16_t leftSpeed = (int16_t)maxSpeed + speedDiff;
    int16_t rightSpeed = (int16_t)maxSpeed - speedDiff;
    leftSpeed = constrain(leftSpeed, 0, (int16_t)maxSpeed);
    rightSpeed = constrain(rightSpeed, 0, (int16_t)maxSpeed);
    motors.setSpeeds(leftSpeed, rightSpeed);
    delay(1);
  }
  if(y==1.0){
    //straight(500);
    right(2000);
    straight(500);
  }
  if(y==-1.0){
    //straight(500);
    left(1500);
    straight(500);
  }

}

ros::Subscriber<geometry_msgs::Twist>lt_sub("/zumo/t",intersection);

int16_t lastError = 0;

#define NUM_SENSORS 5
unsigned int lineSensorValues[NUM_SENSORS];

void loadCustomCharacters()
{
  static const char levels[] PROGMEM = {
    0, 0, 0, 0, 0, 0, 0, 63, 63, 63, 63, 63, 63, 63
  };
  lcd.loadCustomCharacter(levels + 0, 0);  // 1 bar
  lcd.loadCustomCharacter(levels + 1, 1);  // 2 bars
  lcd.loadCustomCharacter(levels + 2, 2);  // 3 bars
  lcd.loadCustomCharacter(levels + 3, 3);  // 4 bars
  lcd.loadCustomCharacter(levels + 4, 4);  // 5 bars
  lcd.loadCustomCharacter(levels + 5, 5);  // 6 bars
  lcd.loadCustomCharacter(levels + 6, 6);  // 7 bars
}

void printBar(uint8_t height)
{
  if (height > 8) { height = 8; }
  const char barChars[] = {' ', 0, 1, 2, 3, 4, 5, 6, 255};
  lcd.print(barChars[height]);
}

void calibrateSensors()
{
  lcd.clear();

  // Wait 1 second and then begin automatic sensor calibration
  // by rotating in place to sweep the sensors over the line
  delay(1000);
  for(uint16_t i = 0; i < 120; i++)
  {
    if (i > 30 && i <= 90)
    {
      motors.setSpeeds(-200, 200);
    }
    else
    {
      motors.setSpeeds(200, -200);
    }

    lineSensors.calibrate();
  }
  motors.setSpeeds(0, 0);
}

void showReadings()
{
  lcd.clear();

  while(!buttonA.getSingleDebouncedPress())
  {
    lineSensors.readCalibrated(lineSensorValues);

    lcd.gotoXY(0, 0);
    for (uint8_t i = 0; i < NUM_SENSORS; i++)
    {
      uint8_t barHeight = map(lineSensorValues[i], 0, 1000, 0, 8);
      printBar(barHeight);
    }
  }
}

void left(int t){
  motors.setLeftSpeed(-100);
  motors.setRightSpeed(100);
  delay(t);
}

void right(int t){
  motors.setLeftSpeed(100);
  motors.setRightSpeed(-100);
  delay(t);
}

void straight(int t){
  motors.setLeftSpeed(100);
  motors.setRightSpeed(100);
  delay(t);
}

void setup()
{

  Wire.begin();

  nh.initNode();
  nh.subscribe(lt_sub);

  nh.advertise(pub_lerror);
  nh.advertise(pub_left);
  nh.advertise(pub_right);
  nh.advertise(pub_output);

  lineSensors.initFiveSensors();

  loadCustomCharacters();

  // Play a little welcome song
  buzzer.play(">g32>>c32");

  // Wait for button A to be pressed and released.
  lcd.clear();
  lcd.print(F("Press A"));
  lcd.gotoXY(0, 1);
  lcd.print(F("to calib"));
  buttonA.waitForButton();    //Serial.println(position);

  calibrateSensors();

  showReadings();

  // Play music and wait for it to finish before we start driving.
  lcd.clear();
  lcd.print(F("Go!"));
  buzzer.play("L16 cdegreg4");
  while(buzzer.isPlaying());
}


void loop()
{
  static uint16_t lastSampleTime = 0;  

  if ((uint16_t)(millis()-lastSampleTime)>=100){
    lastSampleTime=millis();
    int16_t position = lineSensors.readLine(lineSensorValues);
    Serial.println(position);
    l_msg.data = position;
    pub_lerror.publish(&l_msg);
    if (lineSensorValues[0]>=800){
      l_msg.data = lineSensorValues[0];
      pub_left.publish(&l_msg);
    }
    if(lineSensorValues[4]>=800){
      r_msg.data = lineSensorValues[4];
      pub_right.publish(&r_msg);
    }
    
  }

  nh.spinOnce();
  delay(1);
}

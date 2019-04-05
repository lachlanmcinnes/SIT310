#define USE_USBCON

#include <Wire.h>
#include <Zumo32U4.h>

#include <ros.h>
#include <std_msgs/UInt16.h>
#include <geometry_msgs/Twist.h>

ros::NodeHandle nh;

void ros_handler(const geometry_msgs::Twist& cmd_msg) {
  float x = cmd_msg.linear.x;
  float z = cmd_msg.angular.z;
  if(x == -2.0)backward(100);
  if(x == 2.0) forward(100);
  if(z == 2.0)left(100);
  if(z ==-2.0)right(100);
  stop();
}

ros::Subscriber<geometry_msgs::Twist>sub("/turtle1/cmd_vel",ros_handler);

Zumo32U4Motors motors;

void setup() {
  // put your setup code here, to run once:

  nh.initNode();
  nh.subscribe(sub);

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

void loop() {
  // put your main code here, to run repeatedly:

  nh.spinOnce();
  delay(1);

}

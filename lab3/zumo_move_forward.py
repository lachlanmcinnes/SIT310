#!/usr/bin/env python

import rospy
import sys
from time import sleep
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist

rospy.init_node('zumo_move_forward', anonymous=True)
pub = rospy.Publisher('/zumo/1/cmd_vel',Twist, queue_size=10)

def move_forward(msg):
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    vel_msg.linear.x = 1
    pub.publish(vel_msg)
    sleep(0.1)

rospy.Subscriber('/zumo/prox_frontleft',Int8,move_forward)
rospy.spin()
    

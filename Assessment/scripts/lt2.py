#!/usr/bin/env python

import rospy
import math
import sys
import tf

from time import sleep
from std_msgs.msg import Int8
from std_msgs.msg import Int16
from std_msgs.msg import String
from geometry_msgs.msg import Twist

line_left, line_right=0,0
sensorThreshold = 800
lastError = 0
signDirection = ""

pub_linetrace=rospy.Publisher('/zumo/1/t', Twist, queue_size=10)

def handle_error(err_msg):

    t=err_msg.data
    ang = math.atan((t-2000)/2000)
    
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    vel_msg.linear.x = 1
    vel_msg.angular.x=ang
    pub_linetrace.publish(vel_msg)
    sleep(0.1)


if __name__=='__main__':
    rospy.init_node('t1', anonymous=True)
    
    rospy.Subscriber('/zumo/lerror', Int16, handle_error)
    
    rospy.spin()

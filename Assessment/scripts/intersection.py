#!/usr/bin/env python

import rospy
import math
import sys
import tf
import os

from datetime import datetime
import time
from time import sleep
from std_msgs.msg import Int8
from std_msgs.msg import Int16
from std_msgs.msg import String
from geometry_msgs.msg import Twist

rospy.init_node('t2', anonymous=True)
pub_intersection = rospy.Publisher('/zumo/2/t',Twist, queue_size=10)

line_left, line_right=0,0
sensorThreshold = 950
signDirection = "LEFT"

current_topic=0
new_topic=1
l=0
r=0
startR=time.time()
finishR=time.time()
startL=time.time()
finishL=time.time()

def calc():

    l_msg=Twist()

    if signDirection=="LEFT":
        l_msg.linear.x = 0
        l_msg.linear.y = 0
        l_msg.linear.z = 0
        l_msg.angular.x = 0
        l_msg.angular.y = 0
        l_msg.angular.z = 0
        l_msg.linear.y = -1
    else:
        l_msg.linear.x = 0
        l_msg.linear.y = 0
        l_msg.linear.z = 0
        l_msg.angular.x = 0
        l_msg.angular.y = 0
        l_msg.angular.z = 0
        l_msg.linear.y = 1

    pub_intersection.publish(l_msg)

    sleep(0.5)
    os.system("rosrun topic_tools mux_select mux_t /zumo/1/t")

def handle_left(line_msg):
    global l
    global startL
    global finishL
    
    if l==0:
        os.system("rosrun topic_tools mux_select mux_t /zumo/2/t")
        calc()
        l=1
        startL=time.time()
    else:
        finishL=time.time()
        if(finishL-startL>5):
            startL=time.time()
            os.system("rosrun topic_tools mux_select mux_t /zumo/2/t")
            calc()

def handle_right(line_msg):
    global r
    global startR
    global finishR
    
    if r==0:
        calc()
        r=1
        startR=time.time()
    else:
        finishR=time.time()
        if(finishR-startR>5):
            startR=time.time()
            os.system("rosrun topic_tools mux_select mux_t /zumo/2/t")
            calc()

        
def handle_sign(sign_msg):
    global signDirection
    signDirection = sign_msg.data

rospy.Subscriber('/zumo/leftsensor', Int16, handle_left)

rospy.Subscriber('/zumo/signdirection', String, handle_sign)

os.system("rosrun topic_tools mux_select mux_t /zumo/1/t")
current_topic=1
    
rospy.spin()

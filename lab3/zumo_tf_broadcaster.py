#!/usr/bin/env python
import rospy
import tf_conversions
import tf2_ros
import geometry_msgs.msg
from geometry_msgs.msg import Twist
import math
from math import sin, cos, pi

x=0
y=0
th=0.0

def handle_zumo_pose(vel_msg):
    global x
    global y
    global th
    br=tf2_ros.TransformBroadcaster()
    t=geometry_msgs.msg.TransformStamped()
    print("x: "+str(x))
    print("y: "+str(y))
    print("th: "+str(th))

    if(vel_msg.linear.y==1.0): th+=0.0872665
    elif(vel_msg.linear.y==-1.0): th-=0.0872665
    elif(vel_msg.linear.x==1.0):
        vx=0.1
        delta_x=vx*cos(th)
        delta_y=vx*sin(th)
        delta_th=0
        x-=delta_x
        y-=delta_y
        th-=delta_th

    t.header.stamp=rospy.Time.now()
    t.header.frame_id="world"
    t.child_frame_id="zumo"

    t.transform.translation.x=x
    t.transform.translation.y=y
    t.transform.translation.z=0.0

    q=tf_conversions.transformations.quaternion_from_euler(0,0,th)
    t.transform.rotation.x=q[0]
    t.transform.rotation.y=q[1]
    t.transform.rotation.z=q[2]
    t.transform.rotation.w=q[3]

    br.sendTransform(t)

if __name__=='__main__':
    rospy.init_node('zumo_tf_broadcaster')
    rospy.Subscriber('/zumo/cmd_vel',
        Twist,
        handle_zumo_pose)
    rospy.spin()



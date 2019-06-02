#!/usr/bin/env python

import rospy

from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

import imutils
from imutils.video import VideoStream
import numpy as np
import cv2

import Tkinter as tk

import Image, ImageTk

pub = rospy.Publisher('/zumo/location', String, queue_size=10)

window = tk.Tk()
window.wm_title("Hello There")
window.config(background="#FFFFFF")

imageFrame=tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)

def tester(img_msg):

    np_arr = np.fromstring(img_msg.data, np.uint8)
    
    frame = cv2.imdecode(np_arr, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk=imgtk
    lmain.configure(image=imgtk)

def sendMessageA():
    pub.publish("A")
    location.set("Heading to A")

def sendMessageB():
    pub.publish("B")
    location.set("Heading to B")

def sendMessageC():
    pub.publish("C")
    location.set("Heading to C")

def handle_inter(cmd_msg):
    intersection.set(cmd_msg.data)

A = tk.Button(window, text="Go to A", command = sendMessageA)
A.grid(row=600, column=0, padx=10, pady=2)

B = tk.Button(window, text="Go to B", command = sendMessageB)
B.grid(row=700, column=0, padx=10, pady=2)

C = tk.Button(window, text="Go to C", command = sendMessageC)
C.grid(row=800, column=0, padx=10, pady=2)

location = tk.StringVar()
location.set("Please Choose a Location")

locMessage = tk.Label(window, textvariable=location, width=50)
locMessage.grid(row=900, column = 0, padx=10, pady=2)

intersection = tk.StringVar()
intersection.set("No Intersection")

intMessage = tk.Label(window, textvariable=intersection, width=50)
intMessage.grid(row=1000, column = 0, padx=10, pady=2)

if __name__=='__main__':
    rospy.init_node('gui_v3', anonymous=True)
    rospy.Subscriber('/output/image/compressed', CompressedImage, tester)
    rospy.Subscriber('/zumo/signdirection', String, handle_inter)
    window.mainloop()
    rospy.spin()

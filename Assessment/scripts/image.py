#!/usr/bin/env python

import rospy

from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2
import numpy as np

import json

loc=""

def location(loc_msg):
    global loc

    loc=loc_msg.data

def main():
    
    

    print("[INFO] starting video stream...")

    img_pub=rospy.Publisher('/output/image/compressed', CompressedImage, queue_size=10)
    json_pub=rospy.Publisher('/zumo/signdirection',String, queue_size=10)

    
    
    vs = VideoStream(src=0).start()
        
    while True:

        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:

            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            dir_dict = json.loads(barcodeData)
            for d in dir_dict:
                if d['L']== loc:
                    json_pub.publish(d['D'])

                        # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        img_send=CompressedImage()
        img_send.header.stamp=rospy.Time.now()
        img_send.format="jpeg"
        img_send.data=np.array(cv2.imencode('.jpg', frame)[1]).tostring()
        img_pub.publish(img_send)
            

        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF
                # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # close the output CSV file do a bit of cleanup
    print("[INFO] cleaning up...")
    cv2.destroyAllWindows()
    vs.stop()
    rospy.spin()

if __name__=='__main__':
    rospy.init_node('lachlan', anonymous=True)
    rospy.Subscriber('/zumo/location',String, location)
    main()

#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32, ColorRGBA
from roboy_communication_cognition.srv import RecognizeSpeech


def sam_service_client():
    rospy.wait_for_service("SAM_service")
    sam_service = rospy.ServiceProxy("SAM_service", RecognizeSpeech)
    resp = sam_service()
    return resp.text



def main():
    statement =  sam_service_client()
    ledmodesimple_pub = rospy.Publisher("/roboy/control/matrix/leds/mode/simple", Int32, queue_size=3)
    ledcolor_pub = rospy.Publisher("/roboy/control/matrix/leds/color", ColorRGBA)
    ledface_pub = rospy.Publisher("/roboy/control/matrix/leds/face", Int32)
    rospy.init_node("e2bc", anonymous=True)
    print "user said: ", statement
    if "sad" in statement:
        print "sad"
        msg = Int32()
        msg.data = 5
        ledmodesimple_pub.publish(msg)
        msg = ColorRGBA()
        msg.r = 50
        msg.g = 0
        msg.b = 0
        msg.a = 0
        ledcolor_pub.publish(msg)
        msg = Int32()
        msg.data = 1
        ledface_pub.publish(msg)
    if "happy" in statement:
        print "happy"
        msg = Int32()
        msg.data = 5
        ledmodesimple_pub.publish(msg)
        msg = ColorRGBA()
        msg.r = 0
        msg.g = 50
        msg.b = 0
        msg.a = 0
        ledcolor_pub.publish(msg)
        msg = Int32()
        msg.data = 0
        ledface_pub.publish(msg)



if __name__=="__main__":
    main()
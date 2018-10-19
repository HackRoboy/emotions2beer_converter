#!/usr/bin/env python
# kevins ros changes
import rospy
from std_msgs.msg import String
from roboy_communication_cognition.srv import RecognizeSpeech
from roboy_communication_control.msg import ControlLeds
from std_msgs.msg import Empty as msg_Empty


def start_tail():
    ledmode_pub = rospy.Publisher("/roboy/control/matrix/leds/mode", ControlLeds, queue_size=3)
    ledoff_pub = rospy.Publisher('/roboy/control/matrix/leds/off', msg_Empty, queue_size=10)
    ledfreeze_pub = rospy.Publisher("/roboy/control/matrix/leds/freeze", msg_Empty, queue_size=1)

    rospy.init_node("e2bc_led", anonymous=True)

    msg = ControlLeds()
    msg.mode = 2
    msg.duration = 0
    ledmode_pub.publish(msg)
    rospy.spin()


if __name__=="__main__":
    start_tail()
#!/usr/bin/env python

import rospy
import std_msgs
from roboy_communication_cognition.srv import RecognizeSpeech


def sam_service_client():
    rospy.wait_for_service("SAM_service")
    sam_service = rospy.ServiceProxy("SAM_service", RecognizeSpeech)
    resp = sam_service()
    return resp.string


def main():
    print sam_service_client()


if __name__=="__main__":
    main()
#!/usr/bin/env python
import rospy
from ar_track_alvar_msgs.msg import AlvarMarkers

import threading
import copy
import numpy
import ipdb



writable = threading.Event()
writable.clear()
shared_msg = None

def cb(msg):
    global writable, shared_msg
    if writable.is_set():
        shared_msg = msg


if __name__ == '__main__':
    rospy.init_node("marker_pose_sub_py")
    
    rospy.Subscriber("ar_pose_marker", AlvarMarkers, cb)

    writable.set()
    marker = [None,None,None]
    while not rospy.is_shutdown():
        writable.clear()
        msg = copy.deepcopy(shared_msg)
        writable.set()

        if msg is not None: 
            marker[0] = msg.markers[0].pose.pose.position.x
            marker[1] = msg.markers[0].pose.pose.position.y
            marker[2] = msg.markers[0].pose.pose.position.z
            numpy.savetxt('markerpose.txt', marker, delimiter=',') 
            if marker is not None:
                print "save marker pose successfully,please press Ctrl+c"


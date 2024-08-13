#!/usr/bin/env python

import rospy
from geometry_msgs.msg import TwistStamped
import math

rospy.init_node('shape_mover', anonymous=True)
rate = rospy.Rate(10)  # 10 Hz

cmd_vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
forward_cmd = TwistStamped() #message type

def forward(dist, speed):
    time = dist/speed
    time = int(time)
    for i in range(time):
        # Move forward
        #forward_cmd = TwistStamped()
        forward_cmd.twist.linear.x = speed
        forward_cmd.twist.linear.y = 0.0
        forward_cmd.twist.linear.z = 0.0  # Adjust the linear speed as needed
        cmd_vel_pub.publish(forward_cmd)
        rospy.sleep(1)  # Move forward for 1 second

def turn_left(angle, time): #Rotate about the z axis
    r_angle = math.radians(angle)
    turn_rate = r_angle/time
    for j in range(time):
        forward_cmd.twist.angular.x = 0.0
        forward_cmd.twist.angular.y = 0.0
        forward_cmd.twist.angular.z = turn_rate + 0.35 #Compensating the error by adding a constant
        cmd_vel_pub.publish(forward_cmd)
        rospy.sleep(1)

def stop(): #Stop the boat completely
    forward_cmd.twist.linear.x = 0.0
    forward_cmd.twist.linear.y = 0.0
    forward_cmd.twist.linear.z = 0.0
    forward_cmd.twist.angular.x = 0.0
    forward_cmd.twist.angular.y = 0.0
    forward_cmd.twist.angular.z = 0.0
    cmd_vel_pub.publish(forward_cmd)
    rospy.sleep(2)  

def move_in_shape():
    #Function for pattern navigation
    forward(30,2) #parameters: distance to move forward in meters, speed in meters/sec
    stop()
    turn_left(90,3) #parameters: turn angle in degrees, time required to turn in sec
    print("First turn")
    stop()
    forward(30,2)
    stop()
    turn_left(90, 3)
    print("Second turn")
    stop()
    forward(30,2)
    stop()
    turn_left(90, 3)
    print("Third turn")
    stop()
    forward(30, 2)
    stop()

if __name__ == '__main__':
    try:
        move_in_shape()
    except rospy.ROSInterruptException:
        pass

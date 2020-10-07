#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Sugerimos rodar com:
# roslaunch turtlebot3_gazebo  turtlebot3_empty_world.launch 


from __future__ import print_function, division
import rospy
import numpy as np
import cv2
from geometry_msgs.msg import Twist, Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Vector3
import math
import time
from tf import transformations


x = None
y = None
alpha = 0


contador = 0
pula = 50
dist = 50


def recebe_odometria(data):
    global x
    global y
    global alpha
    global contador

    x = data.pose.pose.position.x
    y = data.pose.pose.position.y

    quat = data.pose.pose.orientation
    lista = [quat.x, quat.y, quat.z, quat.w]
    angulos = np.degrees(transformations.euler_from_quaternion(lista))    
    alpha = math.radians(angulos[2])

    if contador % pula == 0:
        print("Posicao (x,y)  ({:.2f} , {:.2f}) + angulo {:.2f}".format(x, y,angulos[2]))
    contador = contador + 1


def go_to(x1, y1, pub):
    global alpha 
    global x
    global y
    global dist
    global zero

    x0 = x
    y0 = y
    deltay = y1-y0
    deltax = x1-x0

    dist = ((deltax)**2 + (deltay)**2)**(1/2)

    while dist > 0.3:

        teta = math.atan2(deltay, deltax)

        v = 0.3
        w = 0.3

        angulo = teta - alpha
        tempo = abs(angulo)/w

        if angulo > 0:
            velocidade = Twist(Vector3(0, 0, 0), Vector3(0, 0, w))
        
        else:
            velocidade = Twist(Vector3(0, 0, 0), Vector3(0, 0, -w))


        pub.publish(velocidade)
        rospy.sleep(tempo)
        pub.publish(zero)
        rospy.sleep(0.1)

        # Translação
        tempo = dist/v
        velocidade = Twist(Vector3(v, 0, 0), Vector3(0, 0, 0))
        pub.publish(velocidade)
        rospy.sleep(tempo)

        pub.publish(zero)
        rospy.sleep(0.1)

        x0 = x
        y0 = y
        deltay = y1-y0
        deltax = x1-x0
        dist = ((deltax)**2 + (deltay)**2)**(1/2)
        print(dist)


if __name__=="__main__":

    rospy.init_node("q3")

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )

    ref_odometria = rospy.Subscriber("/odom", Odometry, recebe_odometria)

    rospy.sleep(1.0) # contorna bugs de timing    

    pontos = [(3,3), (6, 0), (0, 0)]

    zero = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))

    while not rospy.is_shutdown():
        rospy.sleep(0.5)
        for p in pontos:
            print(p)
            go_to(p[0],p[1], pub)
            rospy.sleep(1.0) 
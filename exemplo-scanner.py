#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
O código para este exercício está em: `sub202/scripts/Q2.py`

Para rodar, recomendamos que faça:

    roslaunch turtlebot3_gazebo turtlebot3_stage_1.launch

Depois:

    rosrun sim202 Q2.py
"""


from __future__ import division, print_function
import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from math import radians

v = 0.5  # Velocidade linear
w = 0.5  # Velocidade angular

nao_bateu = True

ang=radians(90)
dis=1

def scaneou(dado):
    global nao_bateu
    if dado.ranges[0]<= dis:
		nao_bateu = False
    else:
        nao_bateu = True

if __name__=="__main__":
	rospy.init_node("Q2")
	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
	recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)
    

	vel = Twist(Vector3(v, 0, 0), Vector3(0, 0, 0))
	vel_ang = Twist(Vector3(0, 0, 0), Vector3(0, 0, w))
	vel_para = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))

	sleep = 0.01 
	sleep_ang = abs(ang/w)


	while not rospy.is_shutdown():
		if nao_bateu:
			velocidade_saida.publish(vel)
			rospy.sleep(sleep)

		else:
			velocidade_saida.publish(vel_ang)
			rospy.sleep(sleep_ang)
			
			ang -= radians(5)
			dis -= 0.05
		
		while ang <= radians(40):
			velocidade_saida.publish(vel_para)
			rospy.sleep(sleep)

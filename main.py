#!/usr/bin/env python3


import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion



class skillcheck():

	def __init__(self):

		self.fl = [] 
		self.fr = []
		self.mid = []
		self.value =0
		self.theta = 0
		self.move = Twist()
		self.scan = LaserScan()
		self.position=Odometry()
		self.sub1=rospy.Subscriber('scan',LaserScan,self.callback)
		self.pub = rospy.Publisher('cmd_vel',Twist,queue_size=1)
		self.sub2=rospy.Subscriber('odom',Odometry,self.my_callback)
		
	def callback(self,scan):
		
		self.fl = scan.ranges[0:35]                        #stores front left laser readings
		self.fr = scan.ranges[324:359]                     #stores front right laser readings
		self.mid = scan.ranges	                            #stores complete laser reading list
		return scan
	
	def my_callback(self,position):
		
		self.x = position.pose.pose.position.x
		self.y = position.pose.pose.position.y
		self.quaternion_orient = position.pose.pose.orientation
		[self.roll , self.pitch , self.theta]= euler_from_quaternion([self.quaternion_orient.x, self.quaternion_orient.y, self.quaternion_orient.z, self.quaternion_orient.w])
		return position
			

	def main(self):
	
		while not rospy.is_shutdown():
			self.rate = rospy.Rate(1)
			if (self.fl == [] and self.fr == []) or (self.theta == 0 and self.mid == []):
				continue
			print(self.fl,self.fr)
			
			# To check max no.of 'inf' in fl and fr readings
			
			for i, value in enumerate([self.fl.count(float('inf')),self.fr.count(float('inf'))]):
				if value == max(self.fl.count(float('inf')),self.fr.count(float('inf'))) :
					self.a = i
					print(f"max no.of inf are {max(self.fl.count(float('inf')),self.fr.count(float('inf')))}\n")
					
			i = 0
			
			# Rotate left if fl has max no.of 'inf' 
			
			if self.a == 0:
				print('max no.of inf are in fl\nrotating left') 
				while i <= 0.4:
					self.move.angular.z = 0.1
					self.pub.publish(self.move)
					i += 0.1
					self.rate.sleep()
			
			# Rotate right if fr has max no.of 'inf' 
						
			
			else:
				i = 0
				print('max no.of inf are in fr\nrotating right') 
				while i <= 5.5:
					self.move.angular.z = 0.1
					self.pub.publish(self.move)
					i += 0.1
					self.rate.sleep()
			self.move.angular.z = 0
			self.pub.publish(self.move)
			
			i = 0
			
			#To move the bot forward till it is 0.5 unit distance away from the wall
			
			while min(self.fl) >= 0.5 or min(self.fr) >= 0.5:
				print(f"minimum values are {min(self.fl)},{min(self.fr)}")
				print('moving towards wall')
				self.move.linear.x = 0.2
				self.pub.publish(self.move)
				self.rate.sleep()
				
			else:
				self.move.linear.x = 0
				self.pub.publish(self.move)
				
			#To rotate the bot parallel to the wall to the left side	
				
			while (1.57 - self.theta) >= 0.01:
				print('rotating to the left')
				self.move.angular.z = 0.1
				self.pub.publish(self.move)
				self.rate.sleep()
				
			self.move.angular.z = 0
			self.pub.publish(self.move)
				
			#To move along the wall, till it passes the wall
			
			while min(self.mid[235:305]) != float('inf') : # move the bot until the laser readings are inf on the wall side
				print('moving along the wall')
				self.move.linear.x = 0.2
				self.pub.publish(self.move)
				self.rate.sleep()
			else:
				self.move.linear.x =0
				self.pub.publish(self.move)
				
			
			#To rotate the bot to the right and move forward into infinity	
				
			while self.theta <= 3.15 and abs(self.theta) > 0.1:
				print('rotating')
				self.move.angular.z = 0.1
				self.pub.publish(self.move)
				
			else:
				while True:
					print('moving into infinity')
					self.move.angular.z = 0
					self.move.linear.x = 0.1
					self.pub.publish(self.move)
					



if __name__=='__main__':
    rospy.init_node('trial2')
    me = skillcheck()
    try:
        me.main()
    except rospy.ROSInterruptException:
        pass
				
	
	
	
			
		
		
			
		
		


from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math

X = []
Y = []
Z = []

def distance(p1, p2):
	return math.sqrt(abs(p1[0]-p2[0])**2+abs(p1[1]-p2[1])**2)

class rt(object):

	def __init__(self, polygon):
		super(rt, self).__init__()
		self.spine2other = polygon.spine2other
		self.points = polygon.points
		self.totalSpine = polygon.totalSpine


	def SpineUp(self):
		#print (self.totalSpine)
		spineup = []
		for i in self.totalSpine:
			for j in i:
				key = str(j)
				neibor = self.spine2other[key]
				count = len(neibor) 
				dis = 0
				for k in neibor:	
					dis += distance(j, self.points[k])
				dis = dis / count
				list_for_append = []
				l = str(j)
				list_for_append.append(l)
				list_for_append.append(dis)
				spineup.append(list_for_append)
		self.spineup = spineup
		'''
		print ("")
		print (self.spineup)
		print ("")
		'''

	def MakeOval(self):
		oval = {}
		for i in self.totalSpine:
			for j in i:
				key = str(j)
				neibor = self.spine2other[key]
				#print (neibor)
				for k in neibor:
					position = self.points[k]
					key_ = str(j) + str(position)
					if key_ in oval:
						continue
					else:
						init = []
						oval[key_] = init
						theta = math.pi / 18
						while theta <= math.pi / 2:
							for l in self.spineup:
								if l[0] == key:
									m = l[1]
									break
							# n = distance(j, position)
							'''
							m = str(m)
							n = str(n)
							k = str(k)
							print ("for j = " + key + " neibor = " + k + ",m = " + m + " n = " + n)
							'''
							z = m * math.sin(theta)
							x = j[0] + (position[0] - j[0]) * math.cos(theta)
							y = j[1] + (position[1] - j[1]) * math.cos(theta)
							X.append(x)
							Y.append(y)
							Z.append(z)
							list_to_append = [x, y, z]
							oval[key_].append(list_to_append)
							theta += math.pi / 18
					#print("")
					#print(key_)
					#print(oval[key_])
		#print("")
		self.oval = oval

	def Plot(self):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(X, Y, Z, c = 'r', marker = 'o')
		ax.set_xlabel('x axis')
		ax.set_ylabel('y axis')
		ax.set_zlabel('z axis')
		plt.show()

	def run(self):
		self.length = len(self.points)
		#print (self.length)
		self.SpineUp()
		self.MakeOval()
		#self.MakeTri()
		self.Plot()

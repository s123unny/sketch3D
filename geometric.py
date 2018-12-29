from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import math

def distance(p1, p2):
	return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def midpoint(p1, p2):
    return [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2]

def almostEqual(p1, p2, EPSILON=15):
	return (abs(p1[0]-p2[0])+abs(p1[1]-p2[1])) < EPSILON

class geometric(object):
	"""docstring for geometric"""
	def __init__(self, points):
		super(geometric, self).__init__()
		self.points = np.asarray(points)

	def cleanpoints(self):
		for i in range(len(self.points)-1):
			if distance(self.points[i], self.points[i+1]) > 40:
				add = self.points[[i,i+1]].mean(axis=0)
				self.points = np.insert(self.points, i+1, add, axis=0)
		Len = len(self.points)-1
		idx = 0
		while idx < Len:
			if almostEqual(self.points[idx], self.points[idx+1]):
				self.points = np.delete(self.points, idx+1, axis=0)
				Len -= 1
			else:
				idx += 1

	def po2tri(self):
		self.cleanpoints()
		Len = len(self.points)
		L, R = np.zeros(Len), np.zeros(Len) 
		for i in range(Len):
			L[i], R[i] = i-1, i+1
		L[0], R[Len-1] = Len-1, 0

		self.orig = self.points
		tri = Delaunay(self.points)
		for j, s in enumerate(tri.simplices):
			s = np.sort(s)
			if s[0] == L[s[1]] and s[2] == R[s[1]]:
				add = self.points[s[[0,2]]].mean(axis=0)
				self.points = np.concatenate((self.points, add.reshape(1,-1)), axis=0)
			else:
				add = self.points[s].mean(axis=0)
				self.points = np.concatenate((self.points, add.reshape(1,-1)), axis=0)
		self.tri = Delaunay(self.points)



	def plot_show(self):
		plt.triplot(self.points[:,0], self.points[:,1], self.tri.simplices)
		plt.plot(self.points[:,0], self.points[:,1], 'o')
		for j, p in enumerate(self.orig):
			plt.text(p[0]-0.03, p[1]+0.03, j, ha='right') # label the points
		plt.show()


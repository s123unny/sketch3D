from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import math

def distance(p1, p2):
	return math.sqrt(abs(p1[0]-p2[0])**2+abs(p1[1]-p2[1])**2)

def almostEqual(p1, p2, EPSILON=20):
	return math.sqrt(abs(p1[0]-p2[0])**2+abs(p1[1]-p2[1])**2) < EPSILON

class geometric(object):
	"""docstring for geometric"""
	def __init__(self, points):
		super(geometric, self).__init__()
		self.points = np.asarray(points)

	def isConvex(self):
		_vertices = self.points
		if len(_vertices) < 4:
			return true

		sign = False
		n = len(_vertices)

		for i in  range(n):
			dx1 = _vertices[(i + 2) % n][0] - _vertices[(i + 1) % n][0]
			dy1 = _vertices[(i + 2) % n][1] - _vertices[(i + 1) % n][1]
			dx2 = _vertices[i][0] - _vertices[(i + 1) % n][0]
			dy2 = _vertices[i][1] - _vertices[(i + 1) % n][1]
			zcrossproduct = dx1 * dy2 - dy1 * dx2

			if i == 0:
				sign = zcrossproduct > 0
			elif sign != (zcrossproduct > 0):
				return False

		return True

	def cleanpoints(self):
		for i in range(len(self.points)-1):
			if distance(self.points[i], self.points[i+1]) > 50.0:
				add = self.points[[i,i+1]].mean(axis=0)
				self.points = np.insert(self.points, i+1, add, axis=0)
		cut = distance(self.points[-1], self.points[0])
		if cut > 30.0:
			add = self.points[[0,-1]].mean(axis=0)
			self.points = np.insert(self.points, 0, add, axis=0)
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
		if self.isConvex() == False:
			print ("not convex")
			return False
		# self.points = np.asarray([[439,368],[400,357],[382,341],[372,323],[365,300],[364,277],[364,254],[374,227],[388,205],[406,186],[422,173],[442,164],[467,159],[490,158],[512,161],[537,175],[556,193],[573,215],[588,237],[599,260],[605,285],[605,307],[604,328],[592,346],[570,362],[548,372],[523,378],[502,380],[481,381]])
		# b = np.array([440, 367])
		# self.points = self.points - b
		print (self.points)
		
		Len = len(self.points)
		LR = []
		for i in range(Len):
			LR.append([i-1, i+1])
		LR[0] = [Len-1,1]
		LR[Len-1] = [Len-2, 0]

		tri = Delaunay(self.points)

		# plt.triplot(self.points[:,0], self.points[:,1], tri.simplices)
		# plt.plot(self.points[:,0], self.points[:,1])#, 'o')
		# for j, p in enumerate(self.points):
		# 	plt.text(p[0]-0.03, p[1]+0.03, j, ha='right')
		# for j, s in enumerate(tri.simplices):
		# 	p = self.points[s].mean(axis=0)
		# 	plt.text(p[0], p[1], '#%d' % j, ha='center') # label triangles
		# plt.show()
		# print (tri.simplices)
		# print (tri.neighbors)

		TLen = len(tri.simplices)
		Tri = np.zeros(TLen)
		# print ("TLen",TLen)
		add = []
		inner = []
		totalSpine = []
		Other = []
		spine2other = {}
		
		for j, s in enumerate(tri.simplices):
			spine = []
			needcheck = s
			if all(x in LR[s[2]] for x in [s[0], s[1]]) or all(x in LR[s[1]] for x in [s[0], s[2]]) or all(x in LR[s[0]] for x in [s[2], s[1]]):
				Tri[j] = 1
				current = j
				keepgoing = True;
				track = False
				prev = -1
				# print ("=====",j,"======")
				while keepgoing:
					for idx, tri_num in enumerate(tri.neighbors[current]):
						if tri_num != -1 and tri_num != prev and Tri[tri_num] != 1:
							point_num = tri.simplices[tri_num]

							if all(x in LR[point_num[2]] for x in [point_num[0], point_num[1]]) or all(x in LR[point_num[1]] for x in [point_num[0], point_num[2]]) or all(x in LR[point_num[0]] for x in [point_num[2], point_num[1]]):
								keepgoing = False
								break
							
							# print ("current", current, "tri_num",tri_num)
							# newone, oldone
							if point_num[0] in LR[point_num[1]]:
								if point_num[0] not in needcheck:
									needcheck = np.append(needcheck, point_num[0])
									newone = point_num[0]
								else:
									needcheck = np.append(needcheck, point_num[1])
									newone = point_num[1]
								oldone = point_num[2]
							elif point_num[0] in LR[point_num[2]]:
								if point_num[0] not in needcheck:
									needcheck = np.append(needcheck, point_num[0])
									newone = point_num[0]
								else:
									needcheck = np.append(needcheck, point_num[2])
									newone = point_num[2]
								oldone = point_num[1]
							elif point_num[1] in LR[point_num[2]]:
								if point_num[1] not in needcheck:
									needcheck = np.append(needcheck, point_num[1])
									newone = point_num[1]
								else:
									needcheck = np.append(needcheck, point_num[2])
									newone = point_num[2]
								oldone = point_num[0]
							else:
								for i in point_num:
									if i not in needcheck:
										needcheck = np.append(needcheck, i)

							#check inner triangle
							# print ("point_num", point_num)
							if point_num[0] not in LR[point_num[1]] and point_num[2] not in LR[point_num[1]] and point_num[2] not in LR[point_num[0]]:
								keepgoing = False
								add.append(self.points[point_num].mean(axis=0))
								if [tri_num, True] not in inner:
									inner.append([tri_num, True])
								# print ("inner", self.points[point_num].mean(axis=0))

								# 扇形
								key = str(add[len(add)-1])
								if key in spine2other:
									init = spine2other[key]
								else:
									init = []
								# print (needcheck)
								init += list(needcheck)
								spine2other[key] = init
								break

							radius = distance(self.points[oldone], self.points[newone]) / 2
							center = self.points[[oldone, newone]].mean(axis=0)
							#check circle
							for p in needcheck:
								if distance(self.points[p], center) > radius:
									spine.append(center)
									add.append(center)
									inner.append([tri_num, False])

									#扇形
									key = str(center)
									if key in spine2other:
										init = spine2other[key]
									else:
										init = []
									init += list(needcheck)
									spine2other[key] = init
									# print ("circle", center)
									keepgoing = False
									break
							
							prev = current
							current = tri_num
							Tri[tri_num] = 1
							break
						elif tri_num != -1 and tri_num != prev:
							keepgoing = False
							break
				if len(spine) > 1:
					totalSpine.append(spine)
					spine = np.asarray(spine)
					# plt.plot(spine[:,0], spine[:,1], "o")
		self.add = np.asarray(add)
		self.tri = tri

		for element in inner:
			for tri_num in tri.neighbors[element[0]]:
				Tri[element[0]] = 1
				first = True
				# print ("=====", element, "======")
				spine = []
				if element[1]:
					spine.append(self.points[tri.simplices[element[0]]].mean(axis=0))
				prev = element[0]
				current = tri_num
				while Tri[current] == 0:
					point_num = tri.simplices[current]
					if point_num[0] in LR[point_num[1]]:
						if point_num[0] not in tri.simplices[prev]:
							newone = point_num[0]
							otherone = point_num[1]
						else:
							newone = point_num[1]
							otherone = point_num[0]
						oldone = point_num[2]
					elif point_num[0] in LR[point_num[2]]:
						if point_num[0] not in tri.simplices[prev]:
							newone = point_num[0]
							otherone = point_num[2]
						else:
							newone = point_num[2]
							otherone = point_num[0]
						oldone = point_num[1]
					elif point_num[1] in LR[point_num[2]]:
						if point_num[1] not in tri.simplices[prev]:
							newone = point_num[1]
							otherone = point_num[2]
						else:
							newone = point_num[2]
							otherone = point_num[1]
						oldone = point_num[0]
					else:
						tmp = self.points[tri.simplices[current]].mean(axis=0)
						key = str(tmp)
						if key in spine2other:
							init = spine2other[key]
						else:
							init = []
						init += list(tri.simplices[current])
						spine2other[key] = init
						spine.append( self.points[tri.simplices[current]].mean(axis=0) )
						break
					if first == True:
						first = False
						tmp = self.points[[oldone, otherone]].mean(axis=0)
						spine.append( tmp )
						key = str(tmp)
						if key in spine2other:
							init = spine2other[key]
						else:
							init = []
						init.append(oldone)
						init.append(otherone)
						spine2other[key] = init
					tmp = self.points[[oldone, newone]].mean(axis=0)
					spine.append( tmp )
					key = str(tmp)
					if key in spine2other:
						init = spine2other[key]
					else:
						init = []
					init += list(tri.simplices[current])
					spine2other[key] = init
					nei = tri.neighbors[current]
					Tri[current] = 1
					for i in nei:
						if i != -1 and i != prev:
							prev = current
							current = i
							break
				if len(spine) > 1:
					totalSpine.append(spine)
					spine = np.asarray(spine)
					# print (spine)
					# plt.plot(spine[:,0], spine[:,1])
		# print (Tri)
		# print (totalSpine)
		self.totalSpine = totalSpine
		self.spine2other = spine2other
		return True

	def plot_show(self):
		# plt.triplot(self.points[:,0], self.points[:,1], self.tri.simplices)
		# plt.plot(self.points[:,0], self.points[:,1])#, 'o')
		# plt.plot(self.add[:,0], self.add[:,1], 'o')
		# for j, p in enumerate(self.points):
		# 	plt.text(p[0]-0.03, p[1]+0.03, j, ha='right') # label the points
		# for j, s in enumerate(self.tri.simplices):
		# 	p = self.points[s].mean(axis=0)
		# 	plt.text(p[0], p[1], '#%d' % j, ha='center') # label triangles
		# print ("=======")
		Len = len(self.points)
		for i in self.totalSpine:
			# print (i)
			# plt.plot(np.asarray(i)[:,0], np.asarray(i)[:,1], color='skyblue')
			for element in i:
				key = str(element)
				if key in self.spine2other:
					init = self.spine2other[key]
					init = list(sorted(set(init)))
					if 0 in init and Len-1 in init:
						current = Len-1
						while current in init:
							current -= 1
						front, last = [], []
						for x in init:
							(last, front)[x < current].append(x)
						init = last + front
					self.spine2other[key] = init
					# for j in self.spine2other[key]:
					# 	plt.plot([self.points[j,0],element[0]], [self.points[j,1],element[1]], color='#FFDD44')
		# print (self.totalSpine)
		# print (self.spine2other)
		# plt.show()


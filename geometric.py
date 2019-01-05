from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import math

def distance(p1, p2):
	return math.sqrt(abs(p1[0]-p2[0])**2+abs(p1[1]-p2[1])**2)

def midpoint(p1, p2):
    return [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2]

def almostEqual(p1, p2, EPSILON=20):
	return (abs(p1[0]-p2[0])+abs(p1[1]-p2[1])) < EPSILON

class geometric(object):
	"""docstring for geometric"""
	def __init__(self, points):
		super(geometric, self).__init__()
		self.points = np.asarray(points)

	def cleanpoints(self):
		for i in range(len(self.points)-1):
			if distance(self.points[i], self.points[i+1]) > 50:
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
		
		# self.tri = Delaunay(self.points)
		
		self.points = np.asarray([[716,488],[710,488],[702,487],[693,482],[679,476],[666,467],[656,457],[645,445],[635,429],[628,412],[622,391],[620,375],[620,348],[620,340],[632,309],[647,290],[683,261],[712,244],[738,233],[762,227],[778,224],[805,223],[824,223],[846,226],[859,233],[871,241],[879,250],[886,260],[893,276],[895,288],[896,303],[897,317],[897,338],[891,365],[887,380],[881,395],[875,408],[871,417],[867,424],[862,431],[858,437],[854,441],[849,446],[845,450],[840,454],[838,455],[836,456],[835,456],[834,457],[833,458],[831,458],[829,459],[826,460],[823,460],[821,461],[820,461],[819,461]])
		self.cleanpoints()
		Len = len(self.points)
		LR = []
		for i in range(Len):
			LR.append([i-1, i+1])
		LR[0] = [Len-1,1]
		LR[Len-1] = [Len-2, 0]

		# print ("LR", LR)

		
		tri = Delaunay(self.points)
		# print (tri.simplices)
		# print (tri.neighbors)

		TLen = len(tri.simplices)
		Tri = np.zeros(TLen)
		print ("TLen",TLen)
		add = []
		inner = []
		totalSpine = []
		Other = []
		
		for j, s in enumerate(tri.simplices):
			# s = np.sort(s)
			spine = []
			needcheck = s
			if all(x in LR[s[2]] for x in [s[0], s[1]]) or all(x in LR[s[1]] for x in [s[0], s[2]]) or all(x in LR[s[0]] for x in [s[2], s[1]]):
				# if all(x in LR[s[2]] for x in [s[0], s[1]]):
				# 	spine.append(self.points[s[2]])
				# 	spine.append(self.points[[s[0],s[1]]].mean(axis=0))
				# elif all(x in LR[s[1]] for x in [s[0], s[2]]):
				# 	spine.append(self.points[s[1]])
				# 	spine.append(self.points[[s[0],s[2]]].mean(axis=0))
				# else:
				# 	spine.append(self.points[s[0]])
				# 	spine.append(self.points[[s[2],s[1]]].mean(axis=0))
				Tri[j] = 1
				current = j
				keepgoing = True;
				track = False
				prev = -1
				while keepgoing:
					# print ("current",current)
					for idx, tri_num in enumerate(tri.neighbors[current]):
						# print (tri_num)
						if tri_num != -1 and tri_num != prev and Tri[tri_num] != 1:
							# print ("found",tri_num)
							point_num = tri.simplices[tri_num]
							
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
							else:
								if point_num[1] not in needcheck:
									needcheck = np.append(needcheck, point_num[1])
									newone = point_num[1]
								else:
									needcheck = np.append(needcheck, point_num[2])
									newone = point_num[2]
								oldone = point_num[0]
							radius = distance(self.points[oldone], self.points[newone]) / 2
							center = self.points[[oldone, newone]].mean(axis=0)

							#check inner triangle
							# print ("point_num", point_num)
							if point_num[0] not in LR[point_num[1]] and point_num[2] not in LR[point_num[1]] and point_num[2] not in LR[point_num[0]]:
								keepgoing = False
								add.append(self.points[point_num].mean(axis=0))
								inner.append(tri_num)
								print ("inner", self.points[point_num].mean(axis=0))

								for element in needcheck:
									plt.plot([self.points[element,0], add[len(add)-1][0]],[self.points[element,1], add[len(add)-1][1]])
									Other.append([self.points[element], add[len(add)-1]])
								break

							if track == True:
								spine.append(center)
							#check circle
							for p in needcheck:
								if distance(self.points[p], center) > radius:
									# keepgoing = False
									track = True
									add.append(center)
									print ("circle", center)
									# break
							
							prev = current
							current = tri_num
							Tri[tri_num] = 1
							break
						elif tri_num != -1 and tri_num != prev:
							# print ("quit", tri_num, current)
							keepgoing = False
							break
				if len(spine) != 0:
					totalSpine.append(spine)
					spine = np.asarray(spine)
					plt.plot(spine[:,0], spine[:,1])
		self.add = np.asarray(add)
		# self.points = np.concatenate((self.points, add), axis=0)			
		self.tri = tri

		for element in inner:
			for tri_num in tri.neighbors[element]:
				spine = []
				spine.append(self.points[tri.simplices[element]].mean(axis=0))
				prev = element
				current = tri_num
				while Tri[current] == 0:
					print (current)
					point_num = tri.simplices[current]
					if point_num[0] in LR[point_num[1]]:
						if point_num[0] not in tri.simplices[current]:
							newone = point_num[0]
						else:
							newone = point_num[1]
						oldone = point_num[2]
					elif point_num[0] in LR[point_num[2]]:
						if point_num[0] not in tri.simplices[current]:
							newone = point_num[0]
						else:
							newone = point_num[2]
						oldone = point_num[1]
					elif point_num[1] in LR[point_num[2]]:
						if point_num[1] not in tri.simplices[current]:
							newone = point_num[1]
						else:
							newone = point_num[2]
						oldone = point_num[0]
					else:
						spine.append( self.points[tri.simplices[current]].mean(axis=0) )
						break
					tmp = self.points[[oldone, newone]].mean(axis=0)
					spine.append( tmp )
					for i in tri.simplices[current]:
						plt.plot([self.points[i,0], tmp[0]],[self.points[i,1], tmp[1]])
					nei = tri.neighbors[current]
					Tri[current] = 1
					for i in nei:
						if i != -1 and i != prev:
							prev = current
							current = i
							break
				if len(spine) != 0:
					totalSpine.append(spine)
					spine = np.asarray(spine)
					print (spine)
					plt.plot(spine[:,0], spine[:,1])
		print (Tri)

	def plot_show(self):
		# plt.triplot(self.points[:,0], self.points[:,1], self.tri.simplices)
		plt.plot(self.points[:,0], self.points[:,1])#, 'o')
		plt.plot(self.add[:,0], self.add[:,1], 'o')
		# for j, p in enumerate(self.points):
		# 	plt.text(p[0]-0.03, p[1]+0.03, j, ha='right') # label the points
		# for j, s in enumerate(self.tri.simplices):
		# 	p = self.points[s].mean(axis=0)
		# 	plt.text(p[0], p[1], '#%d' % j, ha='center') # label triangles
		plt.show()


from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
import numpy as np
import math

X = []
Y = []
Z = []

def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    lens = np.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
    for i in range(len(lens)):
    	if lens[i] == 0:
    		continue
    	arr[i,0] /= lens[i]
    	arr[i,1] /= lens[i]
    	arr[i,2] /= lens[i]
    return arr

def distance(p1, p2):
	return math.sqrt(abs(p1[0]-p2[0])**2+abs(p1[1]-p2[1])**2)

def translate(value):
	if value % 2 == 0:
		return value // 2 + 1
	else:
		print ("error!!!!!!" + str(value))
		return -(value + 1) // 2

def reverse(value, TLen):
	if value >= TLen:
		return value
	if value > 0:
		return (value-1)*2
	else:
		return value*(-2) - 1

class rt(object):

	def __init__(self, polygon):
		super(rt, self).__init__()
		self.spine2other = polygon.spine2other
		self.points = polygon.points
		self.totalSpine = polygon.totalSpine


	def SpineUp(self):
		#print (self.totalSpine)
		spineup = []
		disl = [[] for i in range(len(self.totalSpine))]
		for idx, i in enumerate(self.totalSpine):
			for j in i:
				key = str(j)
				neibor = self.spine2other[key]
				count = len(neibor) 
				dis = 0
				for k in neibor:	
					dis += distance(j, self.points[k])
				dis = dis / count
				disl[idx].append(dis)
		print("disl = ", disl)
				# list_for_append = []
				# l = str(j)
				# list_for_append.append(l)
				# list_for_append.append(dis)
				# spineup.append(list_for_append)
		for idx, i in enumerate(disl):
			for jdx, j in enumerate(i):
				#print(type(idx), type(j))
				if jdx == 0:
					if jdx == len(i) - 1:
						continue
					modify = (2 * j + disl[idx][jdx + 1]) / 3
				elif jdx == len(i) - 1:
					modify = (2 * j + disl[idx][jdx - 1]) / 3
				else:
					modify = (2 * j + disl[idx][jdx - 1] + disl[idx][jdx + 1]) / 4
				l = str(self.totalSpine[idx][jdx])
				list_for_append = []
				list_for_append.append(l)
				list_for_append.append(modify)
				spineup.append(list_for_append)
		print("spine = ", spineup)
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
							z = m * math.sin(theta)
							x = j[0] + (position[0] - j[0]) * math.cos(theta)
							y = j[1] + (position[1] - j[1]) * math.cos(theta)
							test = np.argwhere(np.asarray(list(self.vertex.values())) == [x, y, z])
							flag = 0
							for k in test:
								if flag == 2:
									if k[1] == 2:
										flag = 3
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							if flag != 3:
								#self.vertex = np.insert(self.vertex, len(self.vertex), [[x,y,z]], axis=0)
								tlen = len(self.vertex) // 2 + 1
								self.vertex[tlen] = [x,y,z]
								self.vertex[-tlen] = [x,y,-z]
								X.append(x)
								Y.append(y)
								Z.append(z)
							list_to_append = [x, y, z]
							oval[key_].append(list_to_append)
							theta += math.pi / 18
		self.oval = oval

	def MakeTri(self):
		'''
		for i in self.totalSpine:
			for j in i:
				key = str(j)
				neibor = self.spine2other[key]
				min = 100000
				for k in neibor:
					if k < min:
						min = k

		key = str(j)
		neibor = self.spine2other[key]
		count = len(neibor) 
		dis = 0
		for k in neibor:
		'''
		#print(vertex)
		'''
		index = 0
		i = 0
		j = 0
		leng = len(self.totalSpine)
		while i < leng:
			length = len(self.totalSpine[i])
			#print(i, j)
			spine = self.totalSpine[i][j]
			key = str(spine)
			neibor = self.spine2other[key]
			if index in neibor:
				break
			if j < length - 1:
				j += 1
			else:
				i += 1
				j = 0
		'''
		leng = len(self.totalSpine)
		for i in range(leng):
			#print("i = " + str(i))
			length = len(self.totalSpine[i])
			#print(self.spine2other[str(self.totalSpine[i][0])])
			neibor_check = np.zeros(len(self.spine2other[str(self.totalSpine[i][0])]))
			#print(neibor_check)
			flag_for_repeat = 0
			time = 0
			while time < 2:
				j = 0
				flag_for_last = 0
				key = str(self.totalSpine[i][j])
				neibor = self.spine2other[key]
				if flag_for_repeat == 0:
					index = neibor[0]
				else:
					index = index
				flag1 = 0
				flag2 = 0
				while j < length:
					#print("j = " + str(j) + ", length = " + str(length) + ", index = " + str(index))
					#print("flag1 and flag 2 = " + str(flag1) + ", " + str(flag2))
					#if j < length - 1:
						#print(self.spine2other[str(self.totalSpine[i][j+1])])
					if flag_for_last == 1:
						time += 1
						break
					key = str(self.totalSpine[i][j])
					neibor = self.spine2other[key]
					while True:
						if time == 0:
							way = 1
						else:
							way = -1
						if index == 0 and way == -1:
							way = self.length - 1
							#print("zero to end")
						if index == self.length - 1 and way == 1:
							way = 1 - self.length
							#print("end to zero")
						if index+way not in neibor:
							flag1 = 1
							if (flag1 == 1 and flag2 == 1) or (j == length - 1):
								flag_for_last = 1
								if np.sum(neibor_check) != len(self.spine2other[str(self.totalSpine[i][0])]) and time == 1:
									#print("otherside")
									time = -1
									flag_for_repeat = 1
									for loop in range(len(self.spine2other[str(self.totalSpine[i][0])])):
										if neibor_check[int(loop)] == 0:
											index = int(self.spine2other[str(self.totalSpine[i][0])][int(loop)])
											#print("new index = " + str(index))
											break
							break
						else:
							#print("judge1, index = " + str(index) + " and " + str(index + way) + ", spine = " + str(j))
							#print(j, neibor)
							#print(index, index+way)
							#print(flag1, flag2)
							temp = index
							if temp in self.spine2other[str(self.totalSpine[i][0])]:
								#print(temp)
								#print(self.spine2other[str(self.totalSpine[i][0])].index(temp))
								neibor_check[self.spine2other[str(self.totalSpine[i][0])].index(temp)] = 1
								#print(self.spine2other[str(self.totalSpine[i][0])])
								#print(neibor_check)
							if temp+way in self.spine2other[str(self.totalSpine[i][0])]:
								#print(temp+way)
								#print(self.spine2other[str(self.totalSpine[i][0])].index(temp+way))
								neibor_check[self.spine2other[str(self.totalSpine[i][0])].index(temp+way)] = 1
								#print(self.spine2other[str(self.totalSpine[i][0])])
								#print(neibor_check)
							x_ = [self.points[index][0], self.points[index][1], 0]
							# print(x_)
							tlen = len(self.vertex)
							# print (list(self.vertex.values()))
							x__ = np.argwhere(np.asarray(list(self.vertex.values())) == x_)
							# print(x__)
							flag = 0
							for k in x__:
								if flag == 2:
									if k[1] == 2:
										x = k[0]
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							y_ = [self.points[index + way][0], self.points[index + way][1],  0]
							# print(y_)
							y__ = np.argwhere(np.asarray(list(self.vertex.values())) == y_)
							# print(y__)
							flag = 0
							for k in y__:
								if flag == 2:
									if k[1] == 2:
										y = k[0]
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							#print(str(self.totalSpine[i][j]), str(self.points[index]))
							#print("278", j, index)
							z_ = self.oval[str(self.totalSpine[i][j])+str(self.points[index])][0]
							# print(z_)
							z__ = np.argwhere(np.asarray(list(self.vertex.values())) == z_)
							#print(z__)
							flag = 0
							for k in z__:
								if flag == 2:
									if k[1] == 2:
										z = translate(k[0])	
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							# print(x, y, z)
							#print([x,y,z])
							self.face = np.insert(self.face, len(self.face), [[x,y,z]], axis=0)
							self.face = np.insert(self.face, len(self.face), [[x, y, -z]], axis = 0)
							x = y
							y = z
							z_ = self.oval[str(self.totalSpine[i][j])+str(self.points[index+way])][0]
							# print(z_)
							z__ = np.argwhere(np.asarray(list(self.vertex.values())) == z_)
							# print(z__)
							flag = 0
							for k in z__:
								if flag == 2:
									if k[1] == 2:
										z = translate(k[0])
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							# print(x, y, z)
							self.face = np.insert(self.face, len(self.face), [[x,y,z]], axis=0)
							self.face = np.insert(self.face, len(self.face), [[x, -y, -z]], axis = 0)
							count = 0
							while count < 7:
								#print([y+count,z+count,y+1+count])
								self.face = np.insert(self.face, len(self.face), [[y+count,z+count,y+1+count]], axis=0)
								self.face = np.insert(self.face, len(self.face), [[-y-count, -z-count, -y-1-count]], axis = 0)
								#print([z+count,y+1+count,z+1+count])
								self.face = np.insert(self.face, len(self.face), [[z+count,y+1+count,z+1+count]], axis=0)
								self.face = np.insert(self.face, len(self.face), [[-z-count, -y-1-count, -z-1-count]], axis = 0)
								count += 1
							x_ = self.oval[str(self.totalSpine[i][j])+str(self.points[index])][8]
							# print(x_)
							x__ = np.argwhere(np.asarray(list(self.vertex.values())) == x_)
							# print(x__)
							flag = 0
							for k in x__:
								if flag == 2:
									if k[1] == 2:
										x = translate(k[0])
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							#print([y+7,z+7,x])
							self.face = np.insert(self.face, len(self.face), [[y+7,z+7,x]], axis=0)
							self.face = np.insert(self.face, len(self.face), [[-y-7, -z-7, -x]], axis = 0)
							index += way
							continue	

					if j < length - 1:
						judge2 = self.spine2other[str(self.totalSpine[i][j+1])]
						if index in judge2:
							#print("judge2, index = " + str(index) + ", spine = ", str(j) + " and " + str(j + 1))
							#print(j, neibor, judge2)
							#print(index)
							if index in self.spine2other[str(self.totalSpine[i][0])]:
								neibor_check[self.spine2other[str(self.totalSpine[i][0])].index(index)] = 1
							x_ = [self.points[index][0], self.points[index][1], 0]
							# print(x_)
							x__ = np.argwhere(np.asarray(list(self.vertex.values())) == x_)
							# print(x__)
							flag = 0
							for k in x__:
								if flag == 2:
									if k[1] == 2:
										x = k[0]
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							#print("387", j, index)
							y_ = self.oval[str(self.totalSpine[i][j])+str(self.points[index])][0]
							# print(y_)
							y__ = np.argwhere(np.asarray(list(self.vertex.values())) == y_)
							# print(y__)
							flag = 0
							for k in y__:
								if flag == 2:
									if k[1] == 2:
										y = translate(k[0])
										if k[0] == 1039:
											#print(z_)
											#print(z__)
											break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							z_ = self.oval[str(self.totalSpine[i][j+1])+str(self.points[index])][0]
							# print(z_)
							z__ = np.argwhere(np.asarray(list(self.vertex.values())) == z_)
							# print(z__)
							flag = 0
							for k in z__:
								if flag == 2:
									if k[1] == 2:
										z = translate(k[0])
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							# print(x, y, z)
							#print([x,y,z])
							self.face = np.insert(self.face, len(self.face), [[x,y,z]], axis=0)
							self.face = np.insert(self.face, len(self.face), [[x, -y, -z]], axis = 0)
							count = 0
							while count < 7:
								#print([y+count,z+count,y+1+count])
								self.face = np.insert(self.face, len(self.face), [[y+count,z+count,y+1+count]], axis=0)
								self.face = np.insert(self.face, len(self.face), [[-y-count,-z-count,-y-1-count]], axis=0)
								#print([z+count,y+1+count,z+1+count])
								self.face = np.insert(self.face, len(self.face), [[z+count,y+1+count,z+1+count]], axis=0)
								self.face = np.insert(self.face, len(self.face), [[-z-count,-y-1-count,-z-1-count]], axis=0)
								count += 1
							x_ = self.oval[str(self.totalSpine[i][j])+str(self.points[index])][8]
							# print(x_)
							x__ = np.argwhere(np.asarray(list(self.vertex.values())) == x_)
							# print(x__)
							flag = 0
							for k in x__:
								if flag == 2:
									if k[1] == 2:
										x = translate(k[0])
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							#print([y+7,z+7,x])
							self.face = np.insert(self.face, len(self.face), [[y+7,z+7,x]], axis=0)
							self.face = np.insert(self.face, len(self.face), [[-y-7,-z-7,-x]], axis=0)
							y_ = self.oval[str(self.totalSpine[i][j+1])+str(self.points[index])][8]
							# print(y_)
							y__ = np.argwhere(np.asarray(list(self.vertex.values())) == y_)
							# print(y__)
							flag = 0
							for k in y__:
								if flag == 2:
									if k[1] == 2:
										y = translate(k[0])
										break
									else:
										flag = 0
								if flag == 1:
									if k[1] == 1:
										flag = 2
									else:
										flag = 0
								if k[1] == 0:
									flag = 1
							#print([[z+7,x,y]])
							self.face = np.insert(self.face, len(self.face), [[z+7,x,y]], axis=0)
							self.face = np.insert(self.face, len(self.face), [[-z-7,-x,-y]], axis=0)
							j += 1
						else:
							flag2 = 1


	def Plot(self):
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		'''
		ax.scatter(X, Y, Z, c = 'r', marker = 'o')
		ax.set_xlabel('x axis')
		ax.set_ylabel('y axis')
		ax.set_zlabel('z axis')
		'''
		# print(len(self.vertex), len(self.face))
		# print (self.vertex)
		

		# poly3d = [[self.vertex[int(vert_id)] for vert_id in face] for face in self.face]
		poly3d = [[self.vertex[face[0]], self.vertex[face[1]], self.vertex[face[2]], self.vertex[face[0]]] for face in self.face]
		
		x, y, z = zip(*self.vertex)
		for i in self.totalSpine:
			for j in i:
				X.append(j[0])
				Y.append(j[1])
				Z.append(0)
		ax.scatter(x, y, z)
		# ax.scatter(X, Y, Z, c = 'b')
		
		ax.add_collection3d(Poly3DCollection(poly3d, facecolors='w', linewidths=0.5, alpha=0.5))
		ax.add_collection3d(Line3DCollection(poly3d, colors='k', linewidths=0.1, linestyles="solid"))

		#LEN = len(self.vertex)
		#normal = []
		#for i in range(LEN):
			#normal.append(self.vertex[i] + 50*self.norm[i])
		#plotnorm = [[self.vertex[i], normal[i] ] for i in range(LEN)]
		#ax.add_collection3d(Line3DCollection(plotnorm, colors='k', linewidths=0.1, linestyles="solid"))
		tmp = [[[x[0], x[1], 0] for x in s] for s in self.totalSpine]
		# ax.add_collection3d(Line3DCollection(tmp, colors='b', linewidths=0.5, linestyles="solid"))
		#print(len(self.totalSpine))
		plt.show()

	def Normal(self):
		norm = np.zeros( self.vertex.shape, dtype=self.vertex.dtype )
		tris = self.vertex[self.face]
		n = np.cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )
		normalize_v3(n)
		norm[ self.face[:,0] ] += n
		norm[ self.face[:,1] ] += n
		norm[ self.face[:,2] ] += n
		normalize_v3(norm)
		self.norm = norm

	def run(self):
		#print(self.totalSpine)
		self.length = len(self.points)
		self.vertex = {}
		#print(self.vertex)
		self.face = np.zeros((0, 3))
		print (self.vertex)
		#print("")
		self.SpineUp()
		self.MakeOval()
		self.TLen = len(self.vertex)
		for i in range(self.length):
			self.vertex[len(self.vertex)] = [self.points[i][0], self.points[i][1], 0]
		#print(self.vertex)
		self.MakeTri()
		self.vertex = np.asarray(list(self.vertex.values()))
		b = np.array([440, 367, 16])
		self.vertex = self.vertex - b
		self.face = np.asarray([[ int(reverse(x, self.TLen)) for x in face] for face in self.face])
		#print(self.face)
		self.Normal()
		# self.Plot()
		

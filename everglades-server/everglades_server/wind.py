# Michael Fielder
# Wind Library for Everglades Games

import sys
from noise import pnoise2, snoise2, snoise3, pnoise3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import random as r
from everglades_server import generate_map
import os

# Calculates dot product between two vectors
def dot(v1, v2):
	(x1,y1) = v1
	(x2,y2) = v2
	return x1 * x2 + y1 * y2

# Generates hash map of each connection's direction
def genConnMags(xsize, ysize, map, conn, wind):

	neighbors = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
	diagonals = [(1,1), (-1, 1), (-1,-1), (1,-1)]

	# Iterate through map
	for y in range(ysize):
		for x in range(xsize):
			# Check neighboring nodes for connections
			if map[y][x] != -1:
				for n in neighbors:
					(i, j) = n

					# Bounds check
					xCheck = x + i >= 0 and x + i < xsize
					yCheck = y + j >= 0 and y + j < ysize

					if xCheck and yCheck and map[y + j][x + i] != -1:

						node1 = map[y][x]
						node2 = map[y + j][x + i]

						node1_wind = wind[y][x]
						node2_wind = wind[y + j][x + i]

						# Add node as connection after performing scalar multiplier
						if not ((node1, node2) in conn.keys()):
							if n in diagonals:
								node1_mag = dot(node1_wind, (i * 0.7071, j * 0.7071))
								node2_mag = dot(node2_wind, (i * 0.7071, j * 0.7071))
							else:
								node1_mag = dot(node1_wind, n)
								node2_mag = dot(node2_wind, n)

							conn[(node1, node2)] = [round(node1_mag * .2,3), round(node2_mag * .2,3)]
						# Add node going in other direction
						if not ((node2,node1) in conn.keys()):
							if n in diagonals:
								node1_mag = dot(node1_wind, (-i * 0.7071, -j * 0.7071))
								node2_mag = dot(node2_wind, (-i * 0.7071, -j * 0.7071))
							else:
								node1_mag = dot(node1_wind, (-i,-j))
								node2_mag = dot(node2_wind, (-i,-j))

							conn[(node2, node1)] = [round(node2_mag * .2,3), round(node1_mag * .2,3)]

	return

# Creates a vector array for the wind
def createWindArray(xsize, ysize, octaves=1, offset=0, mirrored=True):
	wind = []

	freq  = 16 * octaves

	# Mirrors the wind vector field
	if mirrored:
		xsize_half = int(xsize / 2)

		for y in range(ysize):
			row = []
			# Creates vectors using Perlin noise as angle for vector in radians
			for x in range(xsize):
				noise = snoise2((x + offset)/freq, (y+offset)/freq, octaves)
				angle = noise * 2 * math.pi
				print("Noise: ", noise)
				#print("Angle: ", angle)
				x_dir = math.cos(angle)
				y_dir = math.sin(angle)
				print("X: ", x_dir, "Y: ", y_dir)

				if x < xsize_half:
					row.append((round(x_dir,3),round(y_dir,3)))
				# Makes middle row have no vectors to ensure fairness
				elif x == xsize_half:
					row.append((0,0))

				else:
					(x,y) = row[xsize - 1 - x]
					row.append((-x,y))

			wind.append(row)

	else:
		for y in range(ysize):
			row = []
			for x in range(xsize):
				noise = snoise2((x + offset)/freq, (y+offset)/freq, octaves)
				angle = noise * 2 * math.pi
				x_dir = math.cos(angle)
				y_dir = math.sin(angle)

				row.append((round(x_dir,3),round(y_dir,3)))

			wind.append(row)

	return wind

def create3DWindArray(xsize, ysize, zsize, octaves=2, offset=0, mirrored=True):
	wind = [[[(0, 0, 0) for x in range(xsize)] for y in range(ysize)] for z in range(zsize)]
	magnitude = 2
	freq  = 16 * octaves
	print("Postoffset", offset)
	print("Freq", freq)
	# Mirrors the wind vector field
	if mirrored:
		zlength = int(zsize/2)
	else:
		zlength = zsize
	print("half:", int(zsize/2))
	for z in range(zlength):
		page = []
		for y in range(ysize):
			row = []
			for x in range(xsize):
				noise = snoise3((x + offset)/freq, (y+offset)/freq, (z+offset)/freq, octaves=1, persistence=1)
				print(noise)
				theta = (noise * 2 * math.pi)# + math.pi/4
				phi = noise * math.pi
				x_dir = magnitude * math.sin(phi) * math.cos(theta)
				y_dir = magnitude * math.sin(phi) * math.sin(theta)
				z_dir = magnitude * math.cos(phi)
				wind[z][y][x] = (round(x_dir, 4), round(y_dir, 4), round(z_dir, 4))
				print("z:", z, "y:", y, "x:", x)
				if mirrored:
					(x_mirror, y_mirror, z_mirror) = wind[z][y][x]
					wind[(zsize - 1) - z][y][x] = (x_mirror, y_mirror, -z_mirror)

	return wind

# def export(filename, map, conn,w):
#
# 	f = open(filename, "w")
#
# 	for x in map:
# 		for y in x:
# 			f.write(str(y) + "\t")
# 		f.write("\n")
#
# 	for y in w:
# 		f.write(str(y) + "\n")
#
# 	for x in conn:
# 		f.write(str(x) + "->" + str(conn[x]) + "\n")
#
# 	f.close()

# Generates an interpretation of wind vector map using MatPlotLib

# def genVecMap(w):
#
# 	fig, ax = plt.subplots(figsize=(9,7))
#
# 	for y in range(7):
# 		for x in range(9):
# 			(x_dir, y_dir) = w[y][x]
# 			ax.quiver(x,y,x_dir,y_dir)
#
# 	plt.show()

def gen3DVecMap(w, count):

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d', azim = -45)

	for z in range(5):
		for y in range(5):
			for x in range(5):
				(x_dir, y_dir, z_dir) = w[z][y][x]
				ax.quiver(x,y,z,x_dir,y_dir,z_dir, length = .3, normalize=True)

	filename = "model{}.pdf".format(count)
	winddir = os.path.abspath('windmodels')
	output = os.path.join(winddir, filename)
	ax.set_xlabel("X Axis")
	ax.set_ylabel("Y Axis")
	ax.set_zlabel("Z Axis")
	#plt.xticks(rotation=45)
	#plt.savefig(output)
	plt.show()
	plt.close()

# Main function that creates vector field
def exec(map, xsize, ysize, seed=0):
	r.seed(seed)
	offset = int(r.random() * 10000)
	#file = open("wind.txt", "w")
	conn = {}
	m = map
	w = createWindArray(xsize,ysize,5,offset,True)
	genConnMags(xsize, ysize, m, conn, w)
	#export("wind.txt", map, conn, w)
	#genVecMap(w)

	return conn;

# for i in range(20):
# 	r.seed(i * 23)
# 	offset = int(r.random() * 10000)
# 	print(offset)
# 	gen3DVecMap(create3DWindArray(5,5,5,offset,mirrored=False), i)

#r.seed(121)
offset = int(r.random() * 10000)
print("Preoffset", offset)
nice = 5
gen3DVecMap(create3DWindArray(nice,nice,nice,5,offset,mirrored=True), 0)
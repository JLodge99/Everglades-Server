# Michael Fielder
# Wind Library for Everglades Games

import sys
from noise import pnoise2, snoise2
#import matplotlib.pyplot as plt
import numpy as np
import math
import random as r

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

	return;

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
				x_dir = math.cos(angle)
				y_dir = math.sin(angle)

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

# -*- coding: iso-8859-1 -*-
# Caelan Garrett, Edge Detection
from random import *
import math
from copy import *
global G_HIGH
global G_LOW
G_HIGH = 40
G_LOW = 20
initial = open('epic-fail-access-sign-fail.ppm').read().replace('\n','')
image=initial.split(' ')[:-1]
header = image[:4]
image = image[4:]

f1 = open('copy1.pgm', 'w')
header[0] = 'P2'
f1.write(header[0]+' \n')
f1.write(header[1]+' '+header[2]+' \n')
f1.write(header[3]+' \n')

newimage = [] #Grayscale list
for i in xrange(0, len(image), 3):
	temp = int((.3)*int(image[i])+(.59)*int(image[i+1])+(.11)*int(image[i+2]))
	newimage.append(temp)
	#f1.write(str(temp)+' \n')

l = int(header[2])
w = int(header[1])
matrix = []#Grayscale matrix
for i in xrange(l):
	matrix.append(newimage[i*w:(i+1)*w])
matrix2 = []#Smoothed matrix
for r in xrange(l):
	temp = []
	for c in xrange(w):
		if r == 0 or c == 0 or r == l-1 or c == w-1:
			temp.append(matrix[r][c])
		else:
			value = (matrix[r][c]*4+matrix[r+1][c]*2+matrix[r-1][c]*2+matrix[r][c+1]*2+matrix[r][c-1]*2+matrix[r+1][c+1]+matrix[r+1][c-1]+matrix[r-1][c+1]+matrix[r-1][c-1])/16
			temp.append(value)
	matrix2.append(temp)

f2 = open('copy2.pgm', 'w')
f2.write(header[0]+' \n')
f2.write(header[1]+' '+header[2]+' \n')
f2.write(header[3]+' \n')
for r in xrange(l):
	for c in xrange(w):
		f2.write(str(matrix2[r][c])+' \n')

#Canny Edge Detection
gvalue = []#G Values
highlist = []#List of high values
matrix3 = deepcopy(matrix2)#Edge Detection Matrix
polar = [[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]]
for r in xrange(1,l-1):
	temp = []
	for c in xrange(1,w-1):
		gy = (matrix2[r+1][c]*2-matrix2[r-1][c]*2+matrix2[r+1][c+1]+matrix2[r+1][c-1]-matrix2[r-1][c+1]-matrix2[r-1][c-1])/8
		gx = (matrix2[r][c+1]*2-matrix2[r][c-1]*2+matrix2[r+1][c+1]-matrix2[r+1][c-1]+matrix2[r-1][c+1]-matrix2[r-1][c-1])/8
		value = abs(gx)+abs(gy)
		if value>= G_HIGH:
			highlist.append([r,c])
		temp.append([gx,gy])
	if len(temp) > 0:
		gvalue.append(temp)

def recur(r,c):
	gx,gy = gvalue[r-1][c-1]
	value = abs(gx)+abs(gy)
	if value<G_LOW or matrix3[r][c]<0:
		return
	angle = (180.0/math.pi)*math.atan2(1.0*gy, 1.0*gx)
	if angle<0:
		angle = 360+angle
	if ((angle >= 0 and angle < 5.0) or (angle <=360 and angle > 355.0)) or (angle > 85.0 and angle < 95.0) or (angle > 175.0 and angle < 185.0) or (angle > 265.0 and angle < 275.0):
		index = int((angle)/45.0)
	else:
		index = int((angle-22.5)/45.0)
	#Pencil Code
	if index >= 8:
		index-=8
	index1 = index
	index2 = index
	if index2>= 4:
		index2-=4
	else:
		index2+=4
	tr,tc = (r-1)+polar[index1][0], (c-1)+polar[index1][1]
	if (not (tr < -1 or tc < -1 or  tr > l-2 or tc > w-2)) and matrix3[tr+1][tc+1] < 0:
		return
	if not (tr < 0 or tc < 0 or  tr > l-3 or tc > w-3):
		tempx, tempy = gvalue[tr][tc]
		if value<(abs(tempx)+abs(tempy)):
			return
	tr,tc = (r-1)+polar[index2][0], (c-1)+polar[index2][1]
	if (not (tr < -1 or tc < -1 or  tr > l-2 or tc > w-2)) and matrix3[tr+1][tc+1] < 0:
		return
	if not (tr < 0 or tc < 0 or  tr > l-3 or tc > w-3):
		tempx, tempy = gvalue[tr][tc]
		if value<(abs(tempx)+abs(tempy)):
			return
	matrix3[r][c] = -255
	
	#Recur Code
	index2 = index-2
	index1 = index+2
	if index1 >= 8:
		index1-=8
	if index2<0:
		index2+=8
	tr,tc = (r)+polar[index1][0], (c)+polar[index1][1]
	if not (tr < 1 or tc < 1 or  tr > l-2 or tc > w-2):
		recur(tr,tc)
	tr,tc = (r)+polar[index2][0], (c)+polar[index2][1]
	if not (tr < 1 or tc < 1 or  tr > l-2 or tc > w-2):
		recur(tr,tc)

for point in highlist:
	recur(point[0],point[1])

f3 = open('copy3.ppm', 'w')
header[0] = 'P3'
f3.write(header[0]+' \n')
f3.write(header[1]+' '+header[2]+' \n')
f3.write(header[3]+' \n')
for r in xrange(l):
	for c in xrange(w):
		if matrix3[r][c] < 0:
			f3.write(str(255)+' ')
			f3.write(str(0)+' ')
			f3.write(str(0)+' \n')
		else:
			f3.write(str(matrix3[r][c])+' ')
			f3.write(str(matrix3[r][c])+' ')
			f3.write(str(matrix3[r][c])+' \n')
#convert -compress None yourfile.jpg yourfile.ppm

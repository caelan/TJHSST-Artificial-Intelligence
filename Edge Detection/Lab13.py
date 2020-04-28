# -*- coding: iso-8859-1 -*-
# Caelan Garrett, Edge Detection
from random import *
import math
from copy import *
global G_HIGH
global G_LOW
G_HIGH = 50
G_LOW = 25
"""initial = open('shapes.pgm').read().replace('\n',' ')
image=initial.split(' ')[:-1]
header = image[:4]
image = image[4:]"""

"""l = int(header[2])
w = int(header[1])
matrix2 = []
count = 0
for i in xrange(l):
	temp = []
	for i in range(w):
		temp.append(int(image[count]))
		count+=1
	matrix2.append(temp)"""

initial = open('google.ppm').read().replace('\n','')
image=initial.split(' ')[:-1]
header = image[:4]
image = image[4:]

newimage = []
for i in xrange(0, len(image), 3):
	temp = int((.3)*int(image[i])+(.59)*int(image[i+1])+(.11)*int(image[i+2]))
	newimage.append(temp)

l = int(header[2])
w = int(header[1])
matrix = []
for i in xrange(l):
	matrix.append(newimage[i*w:(i+1)*w])
matrix2 = []
for r in xrange(l):
	temp = []
	for c in xrange(w):
		if r == 0 or c == 0 or r == l-1 or c == w-1:
			temp.append(matrix[r][c])
		else:
			value = (matrix[r][c]*4+matrix[r+1][c]*2+matrix[r-1][c]*2+matrix[r][c+1]*2+matrix[r][c-1]*2+matrix[r+1][c+1]+matrix[r+1][c-1]+matrix[r-1][c+1]+matrix[r-1][c-1])/16
			temp.append(value)
	matrix2.append(temp)

#Canny Edge Detection
gvalue = []
highlist = []
markedpoints = []
matrix3 = deepcopy(matrix2)
polar = [[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]]
done = []

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
	if value<G_LOW or matrix3[r][c]<0 or [r,c] in done:
		return
	done.append([r,c])
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
	markedpoints.append([r,c])

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

binsize = 5
bins = [] 
for x in range(int(l/binsize)):
	temp  = []
	for y in range(int(w/binsize)):
		temp.append([])
	bins.append(temp)

maxr, maxc, maxvalue = 0,0,0
centerpoints = []
for point in markedpoints:
	r,c = point
	gx,gy = gvalue[r-1][c-1]
	angle = (180.0/math.pi)*math.atan2(1.0*gy, 1.0*gx)
	if angle<0:
		angle = 360+angle
	if ((angle >= 0 and angle < 5.0) or (angle <=360 and angle > 355.0)) or (angle > 85.0 and angle < 95.0) or (angle > 175.0 and angle < 185.0) or (angle > 265.0 and angle < 275.0):
		index = int((angle)/45.0)
	else:
		index = int((angle-22.5)/45.0)
	dx = int((binsize/1.0)*math.cos(angle*(math.pi/180.0)))
	dy = int((binsize/1.0)*math.sin(angle*(math.pi/180.0)))
	tr = r
	tc = c
	itr = 0;
	while tr>=0 and tr<l and tc>=0 and tc<w:
		bins[int(tr/binsize)][int(tc/binsize)].append((binsize/1.0)*itr)
		if len(bins[int(tr/binsize)][int(tc/binsize)])>maxvalue:
			maxvalue = len(bins[int(tr/binsize)][int(tc/binsize)])
			maxr = int(tr/binsize)
			maxc = int(tc/binsize)
		"""if len(bins[int(tr/binsize)][int(tc/binsize)])>100:
			centerpoints.append([int(tr/binsize),int(tc/binsize)])"""
		tr+= dy
		tc+= dx
		itr+=1
	itr = 0;
	tr = r
	tc = c
	while tr>=0 and tr<l and tc>=0 and tc<w:
		bins[int(tr/binsize)][int(tc/binsize)].append((binsize/1.0)*itr)
		if len(bins[int(tr/binsize)][int(tc/binsize)])>maxvalue:
			maxvalue = len(bins[int(tr/binsize)][int(tc/binsize)])
			maxr = int(tr/binsize)
			maxc = int(tc/binsize)
		"""if len(bins[int(tr/binsize)][int(tc/binsize)])>100:
			centerpoints.append([int(tr/binsize),int(tc/binsize)])"""
		tr-= dy
		tc-= dx
		itr+=1

#for pos in centerpoints:
centerbin = bins[maxr][maxc][:]####
avgdist = 0
for dist in centerbin:
	avgdist+=dist
avgdist = int(avgdist/len(centerbin))

standiv = 0
for dist in centerbin:
	standiv+= pow(avgdist-dist,2)
standiv = int(math.sqrt(standiv/len(centerbin)))

for i in range(len(centerbin)-1, -1,-1):
	if abs(centerbin[i]-avgdist)>standiv:
		centerbin.pop(i)

avgdist = 0
for dist in centerbin:
	avgdist+=dist
avgdist = int(avgdist/len(centerbin))

centerc = maxc*binsize+(binsize/2.0)####
centerr = maxr*binsize+(binsize/2.0)####
for r in xrange(int(centerr-avgdist)-2, int(centerr+avgdist+3)):
	for c in xrange(int(centerc-avgdist)-2, int(centerc+avgdist+3)):
		temp = math.sqrt(pow(r-centerr, 2)+pow(c-centerc,2))
		if temp >= avgdist-1 and temp<=avgdist+1:
			matrix3[r][c] = -100

f3 = open('circle.ppm', 'w')
header[0] = 'P3'
f3.write(header[0]+' \n')
f3.write(header[1]+' '+header[2]+' \n')
f3.write(header[3]+' \n')
for r in xrange(l):
	for c in xrange(w):
		if matrix3[r][c] == -255:
			f3.write(str(255)+' ')
			f3.write(str(0)+' ')
			f3.write(str(0)+' \n')
		elif matrix3[r][c] == -100:
			f3.write(str(0)+' ')
			f3.write(str(255)+' ')
			f3.write(str(0)+' \n')
		else:
			f3.write(str(matrix3[r][c])+' ')
			f3.write(str(matrix3[r][c])+' ')
			f3.write(str(matrix3[r][c])+' \n')

f4 = open('bins.pgm', 'w')
f4.write('P2 \n')
f4.write(header[1]+' '+header[2]+' \n')
f4.write(header[3]+' \n')
for r in xrange(len(bins)):
	for q in xrange(binsize):
		for c in xrange(len(bins[r])):
			for w in xrange(binsize):
				f4.write(str(255-int(((len(bins[r][c]))/(1.0*maxvalue))*255))+' \n')

#convert -compress None yourfile.jpg yourfile.ppm

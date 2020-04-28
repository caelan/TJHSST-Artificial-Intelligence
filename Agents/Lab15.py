# -*- coding: iso-8859-1 -*-
# Agents, Caelan Garrett

from Tkinter import *
from sys import exit
from random import *
from math import *

w,h=800,800
d = 50
moveable = True
rect = []
matrix = []

def click(evnt):
	global moveable
	if not moveable:
		return
	moveable = False
	steps = -1
	while 1:
		steps+=1
		b2 = True
		for r in range(0, h/d):
			for c in range(0, w/d):
				if matrix[r][c] == -1:
					continue
				n,t = neigh(r,c,matrix[r][c])
				if (t<=2 and n >= 1) or (t>=3 and t<=5 and n>= 2) or (t>=6 and n>=3):
					continue
				b2 = False
				ex,ey = -1,-1
				ylist = range(0, h/d)
				shuffle(ylist)
				for y in ylist:
					boo = False
					xlist = range(0, w/d)
					shuffle(xlist)
					for x in xlist:
						if matrix[y][x] == -1:
							ex, ey = x,y
							ntemp,ttemp = neigh(y,x,matrix[r][c])
							if (ttemp<=2 and ntemp >= 1) or (ttemp>=3 and ttemp<=5 and ntemp>= 2) or (ttemp>=6 and ntemp>=3):
								boo = True
								break
					if boo:
						break
				if not (ex == -1 and ey == -1):
					matrix[ey][ex] = matrix[r][c]
					matrix[r][c] = -1
		if b2:
			break
	print (w/d),(h/d)
	print (w/d)*(h/d)
	print steps
	
	for r in range(h/d):
		for c in range(w/d):
			if matrix[r][c] == -1:
				canvas.itemconfigure(rect[r][c],fill='white')
				canvas.itemconfigure(rect[r][c], outline='white')
				continue
			canvas.itemconfigure(rect[r][c], outline='black')
			if matrix[r][c] == 0:
				canvas.itemconfigure(rect[r][c], fill='blue')
			else:
				canvas.itemconfigure(rect[r][c], fill='red')

	total = 0
	seg = 0
	for r in range(h/d):
		for c in range(w/d):
			if matrix[r][c] == -1:
				continue
			total+=1
			a,b = neigh(r,c,matrix[r][c])
			if a == b:
				seg+=1
			elif matrix[r][c] == 0:
				canvas.itemconfigure(rect[r][c], fill='purple')
			else:
				canvas.itemconfigure(rect[r][c], fill='orange')
	print seg
	print (100.0*seg)/total

def neigh(r,c, color):
	count = 0
	total = 0
	for y in range(r-1,r+2):
		for x in range(c-1,c+2):
			if y<0 or y>(h/d)-1 or x<0 or x>(w/d)-1:
				continue
			if y == r and x == c:
				continue
			if matrix[y][x] != -1:
				total+=1
			if matrix[y][x] == color:
				count+=1
	return count, total

def quit(evnt):
	exit(0)

#
# Initialize.
#
root=Tk()
canvas=Canvas(root,width=w,height=h,bg='white')
canvas.pack()
#
# Graphics objects. 
#
count = 0;
for y in range(0, h/d):
	temp1 = []
	for x in range(0,w/d):
		temp1.append(count%2)
		count+=1
	count+=1
	matrix.append(temp1)

matrix[0][0] = -1
matrix[h/d-1][0] = -1
matrix[0][w/d-1] = -1
matrix[h/d-1][w/d-1] = -1

remove = int((5*(h/d)*(w/d))/16)
while remove > 0: 
	r = randint(0,h/d-1)
	c = randint(0,w/d-1)
	if matrix[r][c] != -1:
		matrix[r][c] = -1
		remove-=1
add = int(((h/d)*(w/d))/13)
while add > 0: 
	r = randint(0,h/d-1)
	c = randint(0,w/d-1)
	if matrix[r][c] == -1:
		matrix[r][c] = randint(0,1)
		add-=1

for y in range(0, h/d):
	temp1 = []
	for x in range(0,w/d):
		if matrix[y][x] == 0:
			temp1.append(canvas.create_oval(x*d+d/10,y*d+d/10,x*d+(9*d)/10,y*d+(9*d)/10,fill='blue',outline='black'))
		elif matrix[y][x] == 1:
			temp1.append(canvas.create_oval(x*d+d/10,y*d+d/10,x*d+(9*d)/10,y*d+(9*d)/10,fill='red',outline='black'))
		else:
			temp1.append(canvas.create_oval(x*d+d/10,y*d+d/10,x*d+(9*d)/10,y*d+(9*d)/10,fill='white',outline='white'))
	rect.append(temp1)

root.bind('<Button-1>',click)
root.bind('<q>',quit)
root.mainloop()

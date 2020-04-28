# -*- coding: iso-8859-1 -*-
# Agents, Caelan Garrett

from Tkinter import *
from sys import exit
from random import *
from math import *

N = []
N.append(0)
w,h=800,800
data=open('scape.txt').read().split('\n')[:-1]
scape = []
for row in data:
	temp = []
	for number in row:
		temp.append(int(number))
	scape.append(temp)

r = len(scape)
c = len(scape[0])

class agent:
	def __init__(self,a,b,c):
		self.sugar = a
		self.met = b
		self.vision = c
	def move(self,y,x):
		my,mx = -1,-1
		value = -1
		for i in range(1,matrix[y][x].vision+1):
			array = []
			array.append([y,x+i])
			array.append([y+i,x])
			array.append([y,x-i])
			array.append([y-i,x])
			shuffle(array)
			for coor in array:
				ty = coor[0]
				tx = coor[1]
				if ty<0 or ty>= r or tx<0 or tx>=c:
					continue
				if not isinstance(matrix[ty][tx], int):
					continue
				if matrix[ty][tx] > value:
					my,mx = ty,tx
					value = matrix[ty][tx]
		return my,mx

matrix = []
for y in range(r):
	temp = []
	for x in range(c):
		temp.append(None)
	matrix.append(temp)

vm = []
for a in range(4):
	temp = []
	for b in range(6):
		temp.append(0)
	vm.append(temp)

for i in range(400):
	y = randint(0,r-1)
	x = randint(0,c-1)
	while matrix[y][x] != None:
		y = randint(0,r-1)
		x = randint(0,c-1)
	matrix[y][x] = agent(randint(5,25)+scape[y][x],randint(1,4),randint(1,6))

for y in range(r):
	for x in range(c):
		if matrix[y][x] == None:
			matrix[y][x] = scape[y][x]

def quit(evnt):
	exit(0)

def tick():
	queue = []
	arrayy = range(r)
	shuffle(arrayy)
	arrayx = range(c)
	shuffle(arrayx)
	for y in arrayy:
		for x in arrayx:
			if isinstance(matrix[y][x], int):
				continue
			queue.append([y,x])

	if N[0] == 100:
		f = open('weamet.txt','w')
		f2 = open('vmdeath.txt','w')
		array = [0,0,0,0]
		left = [0,0,0,0]
		for a in queue:
			array[matrix[a[0]][a[1]].met-1]+=matrix[a[0]][a[1]].sugar
			left[matrix[a[0]][a[1]].met-1]+=1
		for a in range(0,4):
			if left[a] == 0:
			      f.write(str(a+1)+' 0\n')
			else:
			      f.write(str(a+1)+' '+str((array[a]*1.0)/left[a])+'\n')
		for y in range(len(vm)):
			for x in range(len(vm[y])):
				f2.write(str(y+1)+' '+str(x+1)+' '+str(vm[y][x])+'\n')
		exit();

	for coor in queue:
		y,x = coor[0], coor[1]
		ny,nx = matrix[y][x].move(y,x)
		matrix[y][x].sugar+= (matrix[ny][nx]-matrix[y][x].met)
		matrix[ny][nx] = matrix[y][x]
		matrix[y][x] = 0
		if matrix[ny][nx].sugar<=0:
			vm[matrix[ny][nx].met-1][matrix[ny][nx].vision-1]+=1
			matrix[ny][nx] = 0
		else:
			canvas.itemconfigure(rect[ny][nx],fill='orange')
			canvas.itemconfigure(rect[ny][nx], outline='orange')
			canvas.coords(rect[ny][nx],nx*dx+dx/10,ny*dy+dy/10,nx*dx+(9*dx)/10,ny*dy+(9*dy)/10)

	for y in range(r):
		for x in range(c):
			if not isinstance(matrix[y][x], int):
				continue
			if scape[y][x]>matrix[y][x]:
				matrix[y][x]+=1
			if matrix[y][x] == 0:
				canvas.itemconfigure(rect[y][x],fill='white')
				canvas.itemconfigure(rect[y][x], outline='white')
			else:
				canvas.itemconfigure(rect[y][x],fill='green')
				canvas.itemconfigure(rect[y][x], outline='green')
				canvas.coords(rect[y][x],x*dx+dx/10+2*(4-matrix[y][x]),y*dy+dy/10+2*(4-matrix[y][x]),x*dx+(9*dx)/10-2*(4-matrix[y][x]),y*dy+(9*dy)/10-2*(4-matrix[y][x]))
	N[0]+=1
	canvas.after(10,tick)
#
# Initialize.
#
root=Tk()
canvas=Canvas(root,width=w,height=h,bg='white')
canvas.pack()
#
# Graphics objects. 
#
rect = []
dx = h/r
dy = w/c

for y in range(r):
	temp1 = []
	for x in range(c):
		if isinstance(matrix[y][x], int):
			if matrix[y][x] == 0:
				temp1.append(canvas.create_oval(x*dx+dx/10+2*(4-matrix[y][x]),y*dy+dy/10+2*(4-matrix[y][x]),x*dx+(9*dx)/10-2*(4-matrix[y][x]),y*dy+(9*dy)/10-2*(4-matrix[y][x]),fill='white',outline='white'))
			else:
				temp1.append(canvas.create_oval(x*dx+dx/10+2*(4-matrix[y][x]),y*dy+dy/10+2*(4-matrix[y][x]),x*dx+(9*dx)/10-2*(4-matrix[y][x]),y*dy+(9*dy)/10-2*(4-matrix[y][x]),fill='green',outline='green'))
		else:
			temp1.append(canvas.create_oval(x*dx+dx/10,y*dy+dy/10,x*dx+(9*dx)/10,y*dy+(9*dy)/10,fill='orange',outline='orange'))
	rect.append(temp1)

canvas.after(10,tick)
root.bind('<q>',quit)
root.mainloop()

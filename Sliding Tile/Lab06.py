# -*- coding: iso-8859-1 -*-
# Sliding Tile Problem, Caelan Garrett, 11/5/09

from Tkinter import *
from sys import exit
from random import *
from math import *

w,h=800,600
data=open('input.in').read().split('\n')[:3]
dx,dy= (w-200)/int(data[0]),h/int(data[1])
store = range(1, int(data[0])*int(data[1])+1)
store[-1] = -1

def shu(times):
	r,c = int(data[0])-1, int(data[1])-1
	last1, last2 = -1,-1
	for s in range(0, times):
		choices = []
		if c+1<= int(data[1])-1 and (r != last1 or c+1 != last2): 
			choices.append(r*int(data[0])+c+1)
		if c-1>= 0 and (r != last1 or c-1 != last2):
			choices.append(r*int(data[0])+c-1)
		if r+1<= int(data[0])-1 and (r+1 != last1 or c != last2): 
			choices.append((r+1)*int(data[0])+c)
		if r-1>=0 and (r-1 != last1 or c != last2): 
			choices.append((r-1)*int(data[0])+c)
		shuffle(choices)
		store[r*int(data[0])+c] = store[choices[0]]
		store[choices[0]] = -1
		last1, last2 = r,c
		r, c = choices[0]/int(data[0]), choices[0]%int(data[0])

shu(int(data[2]))
rect = []
objt = []

def click(evnt):
	x,y=evnt.x,evnt.y
	if x>=0 and x<=w-200 and y>=0 and y<=h:
		r, c = y/dy, x/dx
		index = r*int(data[0])+c
		ntb = nextToBlank(r,c)
		if store[index] != -1 and ntb != -1:
			store[ntb] = store[index]
			store[index] = -1
			canvas.itemconfigure(rect[ntb],fill='grey')
			canvas.itemconfigure(rect[index], fill='white')
			canvas.itemconfigure(objt[index],text='')
			canvas.itemconfigure(objt[ntb],text=store[ntb])
			canvas.itemconfigure(label[0],text=h1())
			canvas.itemconfigure(label[1],text=h2())
			canvas.itemconfigure(label[2],text=h3())


def quit(evnt):
	exit(0)

def nextToBlank(r, c):
	if c+1<= int(data[1])-1 and store[r*int(data[0])+c+1] == -1: 
		return r*int(data[0])+c+1
	if c-1>= 0 and store[r*int(data[0])+c-1] == -1: 
		return r*int(data[0])+c-1
	if r+1<= int(data[0])-1 and store[(r+1)*int(data[0])+c] == -1: 
		return (r+1)*int(data[0])+c
	if r-1>=0 and store[(r-1)*int(data[0])+c] == -1: 
		return (r-1)*int(data[0])+c
	return -1

def h1():
	count = 0
	for a in range(0, len(store)-1):
		if store[a] != a+1:
			count+=1
	return  count

def h2():
	count = 0
	for a in range(0, len(store)):
		if store[a] != -1:
			r,c = (store[a]-1)/int(data[0]), (store[a]-1)%int(data[0])
			r2, c2 = (a)/int(data[0]), (a)%int(data[0])
			count += int(fabs(r2-r)+fabs(c2-c))
	return count

def h3():
	count = 0
	for a in range(0, len(store)):
		if store[a] != -1:
			r,c = (store[a]-1)/int(data[0]), (store[a]-1)%int(data[0])
			r2, c2 = (a)/int(data[0]), (a)%int(data[0])
			count += int(fabs(r2-r)+fabs(c2-c))
			if (r2-r) == 0:
				for e in range(0, int(data[1])):
					index = r*int(data[0])+e
					if store[index] != -1 and store[index] != store[a]:
						if(store[index]-1)/int(data[0]) == r:
							if(c<=e and c2>=e) or (c>=e and c2<=e):	
								count+=1
	return count
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
for y in range(0, int(data[1])):
	for x in range(0,int(data[0])): 
		if store[y*int(data[0])+x] == -1:
			rect.append(canvas.create_rectangle(x*dx,y*dy,x*dx+dx,y*dy+dy,fill='white',outline='black'))
			objt.append(canvas.create_text(x*dy+dx/2,y*dy+dy/2,text='',fill='white'))
			count+= 1
		else:
			rect.append(canvas.create_rectangle(x*dx,y*dy,x*dx+dx,y*dy+dy,fill='grey',outline='black'))
			objt.append(canvas.create_text(x*dy+dx/2,y*dy+dy/2,text=store[count],fill='white'))
			count+= 1
label =[]
label.append(canvas.create_text(w-150,h/2,text=h1(),fill='grey'))
label.append(canvas.create_text(w-100,h/2,text=h2(),fill='grey'))
label.append(canvas.create_text(w-50,h/2,text=h3(),fill='grey'))
#
# Callbacks.
#
root.bind('<Button-1>',click)
root.bind('<q>',quit)
#
# Here we go.
#
root.mainloop()

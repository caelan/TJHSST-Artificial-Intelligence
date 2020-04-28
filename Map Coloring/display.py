# -*- coding: iso-8859-1 -*-

from Tkinter import *
from sys import exit
from random import *
from math import *

w = 1200
h = 600

root=Tk()
canvas=Canvas(root,width=w,height=h,bg='white')
canvas.pack()


poly = open('states_48_poly.txt').read().split('\n')[:-1]
color = open('solution.txt').read().split('\n')[:-1]

ht = {}
for x in color:
	temp = x.split()
	ht[temp[0]] = temp[1]

current = []
state = ''
for item in poly:
	if item in ht:
		state = item
	elif item == 'stop':
		canvas.create_polygon(current, fill = ht[state], outline = 'black')
		current = []
	elif item == 'next':
		state = ''
	else:
		temp = item.split()
		current.append(w*(float(temp[0])+125)/60)
		current.append(h-h*(float(temp[1])-25)/25)

def quit(evnt):
	exit(0)

root.bind('<q>',quit)
root.mainloop()

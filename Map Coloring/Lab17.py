# -*- coding: iso-8859-1 -*-
#Caelan Garrett

from Tkinter import *
from sys import exit
from random import *
from math import *

data=open('states_48.txt').read().split('\n')[:-1]
hm = {}
hc = {}
#c = {'green':None,'blue':None,'purple':None,'red':None}
c = {'green':None,'blue':None,'red':None}

for item in data:
	temp = item.split()
	if not temp[0] in hm:
		hm[temp[0]] = {}
		hc[temp[0]] = c
	hm[temp[0]][temp[1]]= None

	if not temp[1] in hm:
		hm[temp[1]] = {}
		hc[temp[1]] = c
	hm[temp[1]][temp[0]]= None


def H():
	color = 9999999
	neigh = 0
	place = ''
	re = True
	for item in hc.keys():
		if len(hc[item].keys()) > 1: #Like Mr. Torbert Said, if it only has one color by elimination it may be wrong
			re = False
			if len(hc[item].keys()) < color or (len(hc[item].keys()) == color and len(hm[item].keys()) > neigh):
				place = item
				color = len(hc[item].keys())
				neigh = len(hm[item].keys())
	return place,re

def move():
	a,b = H()
	if b:
		return b
	
	mn = len(c)
	mncol = ''
	for col in hc[a].keys():
		temp = 0
		for item in hm[a].keys():
			if col in hc[item].keys():
				temp+=1
		if temp < mn:
			mn = temp
			mncol = col

	if mn == len(c): #Sometimes causes it to fail but is more diverse!
		l = hc[a].keys()
		shuffle(l)
		mncol = l[0]
		
	hc[a] = {}
	hc[a][mncol] = None

	for item in hm[a].keys():
		if mncol in hc[item].keys():
			thing = hc[item].keys()
			hc[item] = {}
			for i in thing:
				if i != mncol:
					hc[item][i] = None
	return b

while True:
	if move():
		break

f = open('solution.txt', 'w')
for item in hc.keys():
	temp = hc[item].keys()
	if len(temp) == 0:
		f.write(item+' yellow\n')
	else:
		f.write(item+' '+temp[0]+'\n')


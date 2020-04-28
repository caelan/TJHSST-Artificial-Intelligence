# -*- coding: iso-8859-1 -*-
from Tkinter import *
from sys import exit
from random import *
from math import *
from copy import *

data=open('states_48.txt').read().split('\n')[:-1]
hm = {}
colormap = {}
c = {'green':None,'blue':None,'purple':None,'red':None}
count = 0

for item in data:
	temp = item.split()
	if not temp[0] in hm:
		hm[temp[0]] = {}
		colormap[temp[0]] = c
	hm[temp[0]][temp[1]]= None

	if not temp[1] in hm:
		hm[temp[1]] = {}
		colormap[temp[1]] = c
	hm[temp[1]][temp[0]]= None


def H(hc, tried):
	color = 9999999
	neigh = 0
	place = ''
	for item in hc.keys():
		if len(hc[item].keys()) > 1 and item not in tried:
			if len(hc[item].keys()) < color or (len(hc[item].keys()) == color and len(hm[item].keys()) > neigh):
				place = item
				color = len(hc[item].keys())
				neigh = len(hm[item].keys())
	return place

def recur(hc):
	tried = []
	global count
	count+=1
	i = 0
	for x in hc.keys():
		if len(hc[x].keys()) < 1:
			i = -1
			break
		if len(hc[x].keys()) > 1:
			i = 1
			break
	if i == 0:
		f = open('solution.txt', 'w')
		for item in hc.keys():
			f.write(item+' '+hc[item].keys()[0]+'\n')
		exit(0)
	if i > 0:
		a = H(hc, tried)
		if a == '':
			return
		tried.append(a)
		temp = hc[a].keys()
		shuffle(temp)
		for mncol in temp:
			newmap = deepcopy(hc)
			newmap[a] = {}
			newmap[a][mncol] = None
			for item in hm[a].keys():
				if mncol in newmap[item].keys():
					thing = newmap[item].keys()
					newmap[item] = {}
					for i in thing:
						if i != mncol:
							newmap[item][i] = None
			recur(newmap)

recur(colormap)


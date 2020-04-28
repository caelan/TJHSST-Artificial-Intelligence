# -*- coding: iso-8859-1 -*-
from Tkinter import *
from sys import exit
from random import *
from math import *
from copy import *

data=open('states_48.txt').read().split('\n')[:-1]
hm = {}
colormap = {}
c = ['green','blue','purple','red']
count = 0

for item in data:
	temp = item.split()
	if not temp[0] in hm:
		hm[temp[0]] = []
		colormap[temp[0]] = c[:]
	hm[temp[0]].append(temp[1])

	if not temp[1] in hm:
		hm[temp[1]] = []
		colormap[temp[1]] = c[:]
	hm[temp[1]].append(temp[0])


def H(hc, done):
	color = 9999999
	neigh = 0
	place = ''
	for item in hc.keys():
		if item not in done:
			if len(hc[item]) < color or (len(hc[item]) == color and len(hm[item]) > neigh):
				place = item
				color = len(hc[item])
				neigh = len(hm[item])
	return place

def recur(hc, done):
	global count
	count+=1
	i = 0
	for x in hc.keys():
		if len(hc[x]) < 1:
			i = -1
			break
		if len(hc[x]) > 1:
			i = 1
			break
	if i == 0:
		f = open('solution.txt', 'w')
		for item in hc.keys():
			f.write(item+' '+hc[item][0]+'\n')
		exit(0)
	if i > 0:
		a = H(hc, done) #Finds the next node
		if a == '':
			return
		
		hashtemp = {} #Finds the least affected order
		for col in hc[a]:
			temp = 0
			for item in hm[a]:
				if col in hc[item]:
					temp+=1
			if temp not in hashtemp.keys():
				hashtemp[temp] = []
			hashtemp[temp].append(col)
		keyset = hashtemp.keys()
		keyset.sort()
		temp = []
		for x in keyset:
			shuffle(hashtemp[x])
			for y in hashtemp[x]:
				temp.append(y)

		for mncol in temp: #Actually recurs for each color
			newmap = deepcopy(hc)
			newmap[a] = []
			newmap[a].append(mncol)
			for item in hm[a]:
				if mncol in newmap[item]:
					thing = newmap[item]
					newmap[item] = []
					for i in thing:
						if i != mncol:
							newmap[item].append(i)
			recur(newmap, done+[a])

recur(colormap, []) #Main


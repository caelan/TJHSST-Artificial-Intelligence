# -*- coding: iso-8859-1 -*-
from Tkinter import *
from sys import exit
from random import *
from math import *
from copy import *

poss = ['1','2','3','4','5','6','7','8','9']
count = 0

data=open('top95.txt').read().split('\n')[:-1]
i = randint(0, len(data)-1)
puz = data[i]
print i

hm = {}
numbermap = {}

def pr(puzzle):
	count = 0
	for x in range(0, 3):
		for y in range(3*x, 3*(x+1)):
			for z in range(0, 3):
				for a in range(3*z, 3*(z+1)):
					print puzzle[count]+' ',
					count+=1
				if z != 2:
					print '|',
			print
		print

def neighboors(pos, puzzle):
	ls = []
	r = pos/10
	c = pos%10
	for x in range(9):
		temp = r*10+x
		if temp != pos and temp not in ls:
			ls.append(temp)
	for x in range(9):
		temp = x*10+c
		if temp != pos and temp not in ls:
			ls.append(temp)

	rs = r/3
	cs = c/3
	for x in range(rs*3, (rs+1)*3):
		for y in range(cs*3, (cs+1)*3):
			temp = x*10+y
			if temp != pos and temp not in ls:
				ls.append(temp)
	return ls

def H(hn, done):
	number = 9999999
	neigh = 0
	place = ''
	for item in hn.keys():
		if item not in done:
			if len(hn[item]) < number or (len(hn[item]) == number and len(hm[item]) > neigh):
				place = item
				number = len(hn[item])
				neigh = len(hm[item])
	return place

def recur(hn, done):
	global count
	count+=1
	i = 0
	for x in hn.keys():
		if len(hn[x]) < 1:
			i = -1
			break
		if len(hn[x]) > 1:
			i = 1
			break
	if i == 0:
		r = 0
		c = 0
		nw = ''
		for x in xrange(len(puz)):
			if c == 9:
				c = 0
				r+=1
			if r == 9:
				r = 0
			nw+=str(hn[r*10+c][0])
			c+=1
		pr(nw)
		exit(0)
	if i > 0:
		a = H(hn, done) #Finds the next node
		if a == '':
			return
		
		hashtemp = {} #Finds the least affected order
		for num in hn[a]:
			temp = 0
			for item in hm[a]:
				if num in hn[item]:
					temp+=1
			if temp not in hashtemp.keys():
				hashtemp[temp] = []
			hashtemp[temp].append(num)
		keyset = hashtemp.keys()
		keyset.sort()
		temp = []
		for x in keyset:
			shuffle(hashtemp[x])
			for y in hashtemp[x]:
				temp.append(y)

		for mnnum in temp: #Actually recurs for each number
			newmap = deepcopy(hn)
			newmap[a] = []
			newmap[a].append(mnnum)
			for item in hm[a]:
				if mnnum in newmap[item]:
					thing = newmap[item]
					newmap[item] = []
					for i in thing:
						if i != mnnum:
							newmap[item].append(i)
			recur(newmap, done+[a])

pr(puz)
print '\n'
r = 0
c = 0
for x in xrange(len(puz)):
	item = puz[x]
	if c == 9:
		c = 0
		r+=1
	if r == 9:
		r = 0
	pos = r*10 + c
	if item == '.':
		numbermap[pos] = poss[:]
	else:
		numbermap[pos] = [item]
	hm[pos] = neighboors(pos, puz)
	c+=1

recur(numbermap, []) #Main


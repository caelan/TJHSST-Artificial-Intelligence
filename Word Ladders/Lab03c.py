# -*- coding: iso-8859-1 -*-
#Caelan Garrett, 9/17/09, Search (DFSID)
#

from random import *
import string
from time import time
wlist=open('words.txt').read().split('\n')[:-1]

def neighboors(ustr): #Finds neighboors
	neigh = []
	x = 0;
	while x<len(ustr):
		for letter in string.ascii_lowercase:
			  temp = ustr[:x]+ letter+ ustr[x+1:]
			  if temp in wlist and temp != ustr:
				  neigh[len(neigh):] = [temp]
		x+=1
	return neigh
def sim(a,b):#Returns amount of simular letters
	count = 0;
	index = 0
	for letter in a:
		if b[index]== letter:
			count+=1
		index+=1;
	return count

def sort(a, targ ): #Sorts list acording to the function sim(a,b)
	array = a[:]
	length = len(array)
	if length <= 1:
		return array
	for x in range(0, length):
		index = 0
		for y in range(1, length-x):
			if sim(array[y], targ) < sim(array[index], targ):
				index = y
		temp = array[length-x-1]
		array[length-x-1] = array[index]
		array[index] = temp
	return array

badpath = {}
def recur(c, t, path, lim, level): #Finds path, DFSID style
	 if c == t:
		 return True,path
	 if 0 == lim:
		 return False, path
	 temp = neighboors(c)
	 temp = sort(temp, t)
	 for node in temp:
		if node not in badpath or badpath[node] >= level:
			path[len(path):] = [node]
			badpath[node] = level
			find,seq = recur(node, t, path, lim-1, level+1)
			if find:
				return find,seq
			else:
				path.pop(len(path)-1)
	 return False, path
	 
start =raw_input('Start: ')
while start not in wlist:
	start = raw_input('Not a valid word, try again: ')
target = raw_input('Target: ')
while target not in wlist:
	target = raw_input('Not a valid word, try again: ')

limit = 0
time1 = time()
done, store = recur(start, target, [start], limit, 1)
while done == 0 and limit != 50: #Uses limit to find path
	limit+=1
	done, store = recur(start, target, [start], limit, 1)
time2 = time()

print start#Output
print target
print '\n'
for key in store:
	print key
print len(store)
print time2-time1

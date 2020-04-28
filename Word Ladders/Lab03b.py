# -*- coding: iso-8859-1 -*-
#Caelan Garrett, 9/17/09, Search (BFS)
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

start =raw_input('Start: ')
while start not in wlist:
	start = raw_input('Not a valid word, try again: ')
target = raw_input('Target: ')
while target not in wlist:
	target = raw_input('Not a valid word, try again: ')

paths = [[start]]
finalpath = []
done = {}
done[start] = False
time1= time()
while len(paths) != 0: #Finds path, BFS style
	current = paths.pop(0)
	last = current[len(current)-1]
	if last == target:
		finalpath = current
		break
	neigh = neighboors(last)
	neigh = sort(neigh, target)
	for n in neigh:
		if n not in done:
			done[n] = False
			temp = current[:]
			temp.append(n)
			paths.append(temp)
time2 = time()

print '\n'
print start#Output
print target
print '\n'
for key in finalpath:
	print key
print len(finalpath)
print time2-time1
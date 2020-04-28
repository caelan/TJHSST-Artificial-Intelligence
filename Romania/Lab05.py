# -*- coding: iso-8859-1 -*-
#Caelan Garrett, Uniform Cost Search
from random import *
import string
from time import time
from math import hypot
from heapq import heappush, heappop
wlist=open('xy.txt').read().split('\n')[:-1]
elist = open('edge_list.txt').read().split('\n')[:-1]
ht = {} #Store city with neighboors and distances to neighboors
loc = {} #Stores city with location
def read(): #Read in text files
	for string in wlist:
	  temp = string.split(',')
	  loc[temp[0]] = temp[1:]
	for string in elist:
	  temp = string.split(',')
	  dist = calculate(temp[0], temp[1])
	  if temp[0] in ht:
	    ht[temp[0]][temp[1]] = dist
	  else:
	    ht[temp[0]] = {}
	    ht[temp[0]][temp[1]]= dist
	  if temp[1] in ht:
	    ht[temp[1]][temp[0]] = dist
	  else:
	    ht[temp[1]] = {}
	    ht[temp[1]][temp[0]]= dist

def calculate(curr, prev): #Distance formula!!!
	return hypot((float(loc[curr][0])-float(loc[prev][0])), (float(loc[curr][1])-float(loc[prev][1])))

def sortC(a, targ): #Sorts list acording to the function calculate
	array = a[:]
	length = len(array)
	if length <= 1:
		return array
	for x in range(0, length):
		index = 0
		for y in range(1, length-x):
			if calculate(array[y], targ) > calculate(array[index], targ):
				index = y
		temp = array[length-x-1]
		array[length-x-1] = array[index]
		array[index] = temp
	return array
badpath = {}
def dfs(c, t, path): #Finds path, DFS
	 if c == t:
		 return True,path
	 temp = ht[c].keys()
	 temp = sortC(temp, t)
	 for node in temp:
		if node not in badpath:
			badpath[node] = False
			path[len(path):] = [node]
			find,seq = dfs(node, t, path)
			if find:
				return find,seq
			else:
				path.pop(len(path)-1)
	 return False, path

def bfs(start, target):#Finds path, BFS
	paths = [[start]]
	done = {}
	done[start] = False
	while len(paths) != 0:
		current = paths.pop(0)
		last = current[len(current)-1]
		if last == target:
			return current
		neigh = ht[last].keys()
		neigh = sortC(neigh, target)
		for n in neigh:
			if n not in done:
				done[n] = False
				temp = current[:]
				temp.append(n)
				paths.append(temp)
	return []
def ucs(start, target): #Finds path, Uniform Cost Search 
	paths = [[0,start]]
	done = {}
	done[start] = 0
	while len(paths) != 0:
		current = heappop(paths)
		last = current[len(current)-1]
		if last == target:
			return current[1:]
		neigh = ht[last].keys()
		for n in neigh:
			if n not in done or done[n]>(current[0]+ht[last][n]):
				temp = current[:]
				temp.append(n)
				temp[0] = temp[0]+ht[last][n]
				done[n] = temp[0]
				heappush(paths,temp)
		print sum([(len(p)-1) for p in paths])
	return []

def astar(start, target): #Finds path, A-Star 
	paths = [[calculate(start, target),0,start]]
	done = {}
	done[start] = 0
	while len(paths) != 0:
		print paths
		current = heappop(paths)
		last = current[len(current)-1]
		print last
		if last == target:
			return current[2:]
		neigh = ht[last].keys()
		for n in neigh:
			if n not in done or done[n]>(current[1]+ht[last][n]):
				temp = current[:]
				temp.append(n)
				temp[1] = temp[1]+ht[last][n]
				done[n] = temp[1]
				temp[0] = temp[1]+calculate(n, target)
				heappush(paths,temp) 
		#print sum([(len(p)-2) for p in paths])
	return []
	
read()
start =raw_input('Start: ')
while start not in ht:
	start = raw_input('Not a valid start, try again: ')
end = raw_input('End: ')
while end not in ht:
	end = raw_input('Not a valid end, try again: ')
sort = raw_input('Sort: ')
final = []
while True:
	if sort == 'astar':
		final = astar(start, end)
		break
	elif sort == 'dfs':
		badpath[start] = False
		stuff, final = dfs(start, end, [start])
		break
	elif sort == 'bfs':
		final = bfs(start, end)
		break
	elif sort == 'ucs':
		final = ucs(start, end)
		break
	sort = raw_input('Not a valid sort, try again: ')

print '\n'
if len(final)>1:
	total = 0
	prev = final[0]
	print prev
	for i in range(1, len(final)):
		print final[i]
		total+=ht[prev][final[i]]
		prev = final[i]
	print len(final)
	print total
else:
	print 'No Path'

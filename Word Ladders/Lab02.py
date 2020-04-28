# -*- coding: iso-8859-1 -*-
#Caelan Garrett, 9/11/09, Random Ladders
#

from random import *
wlist=open('words.txt').read().split('\n')[:-1]

def neighboors(ustr): #Finds neighboors
	ls = []
	neigh = 0
	for word in wlist:
		nonmatches = 0
		index = 0
		for letter in word:
			if ustr[index]!= letter:
				nonmatches+= 1
			if nonmatches>1:
				break
			index+= 1
		if nonmatches==1:
			ls[len(ls):] = [word]
			neigh+=1
	return ls

def different(word1, word2): #Checks to see if words are different for every character
	index = 0
	for letter in word2:
		if word1[index]== letter:
			return 0
		else:
			 index+=1;
	return 1

start = 'acorns'#Initial string
current = start
store = [current]
words = {}
badwords = []
count = 0
while different(start, current) == 0:
	 words[current] = neighboors(current)
	 temp = words[current]
	 length = len(temp)
	 allused = 1
	 if length > 0:
		  shuffle(temp)
		  for path in temp:#randomly finds a neighboor to use on the path
			if path in store or path in badwords:
			   	 pass
			else:
	                	current = path
				store[len(store):] = [current]
			        allused = 0
 			        break
         if allused == 1:
		store = store[:len(store)-1]
		badwords[len(badwords):] = [current]
		current = store[len(store)-1]
         count+=1
         if count==100: #So the program doesn't crash
		break

print start#Output
print current
print '\n'
for key in store:
	print key

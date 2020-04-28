# -*- coding: iso-8859-1 -*-
# Caelan Garrett, N-Queens
from random import *
import string
from time import time
from Tkinter import *
from sys import exit
from math import *
n = 0
def create():
	temp = []
	for x in range(0,n):
		temp.append(randint(0, n-1))
	return temp
def h(temp):
	count = 0
	for elem in range(0, len(temp)):
		for other in range(elem+1, len(temp)):
			if temp[elem] == temp[other]:
				count+=1
			elif fabs(temp[elem]-temp[other]) == fabs(elem-other):
				count+=1
	return count

def minlocal(a,b):
	new = a
	hmin = b
	for col in range(0, len(a)):
		curr = a[col]
		for row in range(0,len(a)):
			if row != curr:
				temp = a[:]
				temp[col] = row
				y = h(temp)
				if y< hmin:
					new = temp
					hmin = y
	return new, hmin
def minfirst(a,b):
	clist = range(0, len(a))
	shuffle(clist)
	for col in clist:
		curr = a[col]
		rlist = range(0, len(a))
		shuffle(rlist)
		for row in rlist:
			if row != curr:
				temp = a[:]
				temp[col] = row
				y = h(temp)
				if y< b:
					return temp, y
	return a,b
def minweight(a,b):
	thing = []
	for col in range(0, len(a)):
		curr = a[col]
		for row in range(0, len(a)):
			if row != curr:
				temp = a[:]
				temp[col] = row
				y = h(temp)
				if y<b:
					thing.append([y,temp])
	thing.sort()
	if len(thing) == 0:
		return a,b
	guess = []                                                                                                  
	for x in range(0,len(thing)):
		guess[len(guess):] = range(0, len(thing)-x)
	shuffle(guess)
	return thing[guess[0]][1], thing[guess[0]][0]
def localsearch():
	a = create()
	b = h(a)
	while b != 0: 
		ta,tb = minlocal(a,b)
		if ta == a:
			a = create()
			b = h(a)
		else:
			a = ta
			b = tb
	return a
def bogosort():
	a = []
	col = range(0, n)
	shuffle(col)
	for x in range(0,n):
		a.append(col[x])
	b = h(a)
	while b != 0:
		a = []
		shuffle(col)
		for x in range(0,n):
			a.append(col[x])
		b = h(a)
	return a
def stochfirst():
	a = create()
	b = h(a)
	while b != 0: 
		ta,tb = minfirst(a,b)
		if ta == a:
			a = create()
			b = h(a)
		else:
			a = ta
			b = tb
	return a
def stochweight():
	a = create()
	b = h(a)
	while b != 0: 
		ta,tb = minweight(a,b)
		if ta == a:
			a = create()
			b = h(a)
		else:
			a = ta
			b = tb
	return a
def splice(a, b):
	r = randint(1, len(a)-1)
	c = b[:r]+a[r:]
	d = a[:r]+b[r:]
	return c,d

def randomize(a):
	c = randint(0, len(a)-1)
	r = randint(0, len(a)-1)
	while r == a[c]:
		r = randint(0, len(a)-1)
	b = a[:]
	b[c] = r
	return b
def genetic():
	size = 2*n
	die = int(n/2)
	pop = []
	count = 1
	for x in range(0, size):
		temp = create()
		htemp = h(temp)
		if htemp == 0:
			return temp
		else:
			pop[len(pop):] = [[htemp, temp]]
	pop.sort()
	while 1:
		print len(pop)
		if count > 100: # Reset population
			pop = []
			count = 1
			for x in range(0, size):
				temp = create()
				htemp = h(temp)
				if htemp == 0:
					return temp
				else:
					pop[len(pop):] = [[htemp, temp]]
			pop.sort()
			continue

		pop = pop[:len(pop)-die]
		guess = []                                                                                                  
		for y in range(0, n):
			guess[len(guess):] = range(0, n-y)
		shuffle(guess)
		for x in range(0, int(die/2)):
			temp1,temp2 = splice(pop[guess.pop()][1], pop[guess.pop()][1])
			htemp1, htemp2 = h(temp1),h(temp2)
			if htemp1 == 0:
				return temp1
			if htemp2 == 0:
				return temp2
			for x in range(0, int(die/2)):
				temp1, temp2 = randomize(temp1),randomize(temp2)
				htemp1, htemp2 = h(temp1),h(temp2)
				if htemp1 == 0:
					return temp1
				if htemp2 == 0:
					return temp2
			pop[len(pop):] = [[htemp1, temp1]]
			pop[len(pop):] = [[htemp2, temp2]]
			pop.sort()
		count+=1
def printboard(yay):
	for x in range(0, len(yay)):
		for y in range(0, len(yay)):
			if yay[y] == x:
				print ' X ',
			else:
				print ' - ', 
		print '\n'
#Code for evaluation
#count = 0
#t1 = time()
#n = 8
#for i in range(0, 100):
#	a,b = genetic()
#	count+=b
#print count/100
#print time()-t1

while True: #Code for runs
	s = raw_input('The Sort: ')
	if s == 'quit':
		break
	n = int(raw_input('The size of the board: '))
	if s == 'local':
		printboard(localsearch())
	elif s == 'bogo':
		printboard(bogosort())
	elif s == 'first':
		printboard(stochfirst())
	elif s == 'weight':
		printboard(stochweight())
	elif s == 'genetic':
		printboard(genetic())
	else:
		print 'Fail, try again'
	print '\n'

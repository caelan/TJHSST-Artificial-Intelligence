# -*- coding: iso-8859-1 -*-
# Caelan Garrett, N-Queens
from random import *
import string
from time import time
from Tkinter import *
from sys import exit
from math import *
data=open('data.txt').read().split('\n')[:-1]
mp = {}
for entry in data:
	raw = string.split(entry)
	temp = []
	for i in range(0,3):
		temp.append(int(raw[i]))
	mp[temp] = float(raw[3])
print mp
	
print data
n = 0
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
		if count > 100:
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

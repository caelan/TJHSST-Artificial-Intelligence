# -*- coding: iso-8859-1 -*-
# Caelan Garrett, N-Queens
from random import *
import string
from time import time
from Tkinter import *
from sys import exit
import math

class neuralnet:
	def __init__(self, array):
		self.layers = []
		self.w_layers = []
		self.layerlen = array
		for y in range(len(self.layerlen)):
			temp = [1.0]*self.layerlen[y]
			if y != len(self.layerlen) -1:
				temp.append(1.0)
			self.layers.append(temp)
		
		for y in range(len(self.layerlen)-1):
			matrix = []
			for x in range(len(self.layers[y])):
				temp = []
				for z in range(self.layerlen[y+1]):
					temp.append(random())
				matrix.append(temp)
			self.w_layers.append(matrix)
				
	def calculate(self, data):
		if len(data) != len(self.layers[0])-1:
			print "Input length not expected"
			exit(0)
		for x in range(len(self.layers[0])-1): # Set input layer, bias node on end of layer
			self.layers[0][x] = data[x] 
		for x in range(len(self.w_layers)):
			for y in range(self.layerlen[x+1]):
				total = 0.0
				for z in range(len(self.layers[x])):
					total+=self.layers[x][z]*self.w_layers[x][z][y]
				self.layers[x+1][y] = 1.0/(1.0+math.exp(-total))
		return self.layers[-1]

	def backPropagation(self, target, learn_rate):
		if len(target) != len(self.layers[-1]):
			print "Target length not expected"
			exit(0)
		
		deltas = []
		for x in range(len(self.layers[-1])):
			deltas.append(self.layers[-1][x]*(target[x]-self.layers[-1][x])*(1-self.layers[-1][x]))
		
		itr = range(len(self.w_layers)-1)
		itr.reverse()
		for x in itr:
			temp = []
			for y in range(len(self.layers[x+1])):
				total = 0.0
				for z in range(self.layerlen[x+2]):
					total+=deltas[z]*self.w_layers[x+1][y][z]
					self.w_layers[x+1][y][z]+=learn_rate*deltas[z]*self.layers[x+1][y]
				temp.append(total*self.layers[x+1][y]*(1-self.layers[x+1][y]))
			deltas = temp

		for x in range(len(self.layers[0])):
			for y in range(self.layerlen[1]):
				self.w_layers[0][x][y]+=learn_rate*deltas[y]*self.layers[0][x]		

	def learnBackUntil(self,master, maxerror):
		learn_rate = .8
		t1 = time()
		currentError = self.error(master)
		x = 0
		while currentError>maxerror:
			for data in master:
				self.calculate(data[0])
				self.backPropagation(data[1], learn_rate)
			currentError = self.error(master)
			x+=1
			if time()-t1 > 3:
				return 3
		return time()-t1

	def save(self, s):
		f = open(s, 'w')
		for x in range(len(self.w_layers)):
			for y in range(len(self.w_layers[x])):
				for z in range(len(self.w_layers[x][y])):
					f.write(str(self.w_layers[x][y][z])+'\n')

	def load(self, s):
		stuff=open(s).read().split('\n')[:-1]
		i = 0
		for x in range(len(self.w_layers)):
			for y in range(len(self.w_layers[x])):
				for z in range(len(self.w_layers[x][y])):
					self.w_layers[x][y][z] = float(stuff[i])
					i+=1
	
	def error(self,dataset):
		error = 0
		for item in dataset:
			result = self.calculate(item[0])
			for x in range(len(result)):
				error+= .5*(pow(result[x]-item[1][x], 2))
		return error

	def test(self,dataset):
		for item in dataset:
			print 'Input: ', item[0], ' Output: ',self.calculate(item[0]), ' Expected: ',item[1]

def create():
	temp = []
	for i in range(randint(1,3)):
		temp.append(randint(1,4))
	return temp

def h(temp):
	dataset = [[[0,0],[0]],[[1,0],[1]],[[0,1],[1]],[[1,1],[0]]]
	passing = [2]
	temp.append(1)
	passing.extend(temp)
	nn = neuralnet(passing)
	return nn.learnBackUntil(dataset, .001)

def splice(a, b):
	r = randint(1, len(a)-1)
	c = b[:r]+a[r:]
	d = a[:r]+b[r:]
	return c,d

def randomize(a):
			print i
		print len(pop)c = randint(1, 4)
	b = a[:]
	b[randint(0,len(b)-1)] = c
	return b

def genetic(n):
	print 'Start'
	size = 2*n
	die = int(n/2)
	pop = []
	count = 1
	for x in range(0, size):
		temp = create()
		htemp = h(temp)
		pop[len(pop):] = [[htemp, temp]]
	
	pop.sort()
	for i in range(10):
		print i
		pop = pop[:len(pop)-die]
		guess = []                                                                                                  
		for y in range(0, n):
			guess[len(guess):] = range(0, n-y)
		shuffle(guess)
		for x in range(0, int(die/2)):
			temp1,temp2 = splice(pop[guess.pop()][1], pop[guess.pop()][1])
			htemp1, htemp2 = h(temp1),h(temp2)
			for x in range(0, int(die/2)):
				temp1, temp2 = randomize(temp1),randomize(temp2)
				htemp1, htemp2 = h(temp1),h(temp2)
			pop[len(pop):] = [[htemp1, temp1]]
			pop[len(pop):] = [[htemp2, temp2]]
			pop.sort()

	print pop
	print 'End'

genetic(4)
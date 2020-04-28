# -*- coding: iso-8859-1 -*-
# Caelan Garrett
# Neural Network code for implementing a neural network with any amount of layers
# Every layer has a bias node except the output layer

from random import *
import pdb
import math
from time import time
from copy import *

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

	def learnBackItr(self, master, itr):
		learn_rate = .8
		t1 = time()
		print 'Backpropagation Learning Start: ',itr,' Iterations'
		for x in range(itr): 
			for data in master:
				self.calculate(data[0])
				self.backPropagation(data[1], learn_rate)
			if x%100 == 0:
				print 'Epoch: ',x,' = ',self.error(master)
		print 'Done: ',time()-t1, ' Seconds'

	def learnBackUntil(self,master, maxerror):
		learn_rate = .8
		t1 = time()
		print 'Backpropagation Learning Start: Until ', maxerror,' error'
		currentError = self.error(master)
		x = 0
		while currentError>maxerror:
			for data in master:
				self.calculate(data[0])
				self.backPropagation(data[1], learn_rate)
			currentError = self.error(master)
			if x%100 == 0:
				print 'Epoch: ',x,' = ',currentError
			x+=1
		print 'Done: ',time()-t1, ' Seconds, ', x-1, ' Iterations'


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

def main():	
	dataset = [[[0,0],[0]],[[1,0],[1]],[[0,1],[1]],[[1,1],[0]]]
	nn = neuralnet([2,3,3,1])
	nn.learnBackUntil(dataset, .0001)
	nn.save('weightsMulti.txt')
	nn.test(dataset)

main()

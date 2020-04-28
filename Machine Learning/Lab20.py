# -*- coding: iso-8859-1 -*-
#Caelan Garrett

from random import *
import pdb
import math
from time import time
from copy import *

class neuralnet:
	def __init__(self, i, h, o):
		self.inp = []
		self.hid = []
		self.out = []
		self.w_in = []
		self.w_out = []
		for x in range(i+1): #Plus Bias node
			self.inp.append(1.0)
			temp = []
			for y in range(h):
				temp.append(random()) #Random number settings
			self.w_in.append(temp)
		for x in range(h+1):
			self.hid.append(1.0) #Plus Bias node
			temp = []
			for y in range(o):
				temp.append(random()) #Random number settings
			self.w_out.append(temp)
		for x in range(o):
			self.out.append(1.0)

	def calculate(self, data):
		if len(data) != len(self.inp)-1:
			print "Input length not expected"
			exit(0)
		for x in range(len(self.inp)-1):
			self.inp[x] = data[x] # Set input layer, bias node on end of layer
		for x in range(len(self.hid)-1):
			total = 0.0
			for y in range(len(self.inp)):
				total+= self.inp[y]*self.w_in[y][x]
			self.hid[x] = 1.0/(1.0+math.exp(-total)) # Set hidden layer
		for x in range(len(self.out)):
			total = 0.0
			for y in range(len(self.hid)):
				total+= self.hid[y]*self.w_out[y][x]
			self.out[x] = 1.0/(1.0+math.exp(-total)) #Set output layer
		return self.out

	def backPropagation(self, target, learn_rate):
		if len(target) != len(self.out):
			print "Target length not expected"
			exit(0)
		d_out = []
		for x in range(len(self.out)):
			d_out.append(self.out[x]*(target[x]-self.out[x])*(1-self.out[x])) # Local output node error
		d_hid = []
		for x in range(len(self.hid)):
			total = 0.0
			for y in range(len(self.out)):
				total+= d_out[y]*self.w_out[x][y]
			d_hid.append(total*self.hid[x]*(1-self.hid[x])) # Local hidden node error
		for x in range(len(self.hid)):
			for y in range(len(self.out)):
				delta = d_out[y]*self.hid[x]
				self.w_out[x][y]+=learn_rate*delta # Adjust output weights
		for x in range(len(self.inp)):
			for y in range(len(self.hid)-1):
				delta = d_hid[y]*self.inp[x]
				self.w_in[x][y]+=learn_rate*delta # Adjust input weights
		
		error = 0.0 # Calculate total error for evaluation
		for x in range(len(target)):
			delta = target[x]-self.out[x]
			error+=(delta*delta)*(.5)

		return error

	def finiteDifferenes(self, master, learn_rate, step_size, initialError):

		newout = deepcopy(self.w_out) #Output Weight Configure
		for a in range(len(self.hid)):
			for b in range(len(self.out)):
				error = 0
				for thing in master:
					data = thing[0]
					target = thing[1]
					for x in range(len(self.inp)-1):
						self.inp[x] = data[x] # Set input layer, bias node on end of layer
					for x in range(len(self.hid)-1):
						total = 0.0
						for y in range(len(self.inp)):
							total+= self.inp[y]*self.w_in[y][x] 
						self.hid[x] = 1.0/(1.0+math.exp(-total)) # Set hidden layer
					for x in range(len(self.out)):
						total = 0.0
						for y in range(len(self.hid)):
							if b == x and a == y:
								total+= self.hid[y]*(self.w_out[y][x]+step_size)
							else:
								total+= self.hid[y]*self.w_out[y][x]
						self.out[x] = 1.0/(1.0+math.exp(-total)) #Set output layer

					for x in range(len(target)):
						delta = target[x]-self.out[x]
						error+=(delta*delta)*(.5)
				
				newout[a][b]-=learn_rate*(error-initialError)/step_size
				
		newin = deepcopy(self.w_in) #Input Weight Configure
		for a in range(len(self.inp)):
			for b in range(len(self.hid)-1):
				error = 0
				for thing in master:
					data = thing[0]
					target = thing[1]
					for x in range(len(self.inp)-1):
						self.inp[x] = data[x] # Set input layer, bias node on end of layer
					for x in range(len(self.hid)-1):
						total = 0.0
						for y in range(len(self.inp)):
							if b == x and a == y:
								total+= self.inp[y]*(self.w_in[y][x]+step_size)
							else:
								total+= self.inp[y]*self.w_in[y][x] 
						self.hid[x] = 1.0/(1.0+math.exp(-total)) # Set hidden layer
					for x in range(len(self.out)):
						total = 0.0
						for y in range(len(self.hid)):
							total+= self.hid[y]*self.w_out[y][x]
						self.out[x] = 1.0/(1.0+math.exp(-total)) #Set output layer

					for x in range(len(target)):
						delta = target[x]-self.out[x]
						error+=(delta*delta)*(.5)
				newin[a][b]-=learn_rate*(error-initialError)/step_size
		
		self.w_in = newin
		self.w_out= newout
		
		newerror = 0
		for data in master:
			self.calculate(data[0])
			for x in range(len(self.out)):
				delta = data[1][x]-self.out[x]
				newerror+=(delta*delta)*(.5)

		return newerror

	def learnBack(self, master, itr):
		learn_rate = .8
		t1 = time()
		print 'Backpropagation Learning Start: ',itr,' Iterations'
		for x in range(itr): #Can also change to make it a while loop that ends at a specifc error
			error = 0
			for data in master:
				self.calculate(data[0])
				error+=self.backPropagation(data[1], learn_rate)
			if x%100 == 0:
				print 'Epoch: ',x,' = ',error
		print 'Done: ',time()-t1, ' Seconds'

	def learnFinite(self, master, itr):
		learn_rate = .8
		step = .1
		t1 = time()
		print 'Finite Differences Learning Start: ',itr,' Iterations'
		inputs = []
		outputs = []
		initialError = 0
		for data in master:
			self.calculate(data[0])
			for x in range(len(self.out)):
				delta = data[1][x]-self.out[x]
				initialError+=(delta*delta)*(.5)
		for x in range(itr): #Can also change to make it a while loop that ends at a specifc error
			initialError = self.finiteDifferenes(master, learn_rate, step, initialError)
			if x%100 == 0:
				print 'Epoch: ',x,' = ',initialError
		print 'Done: ',time()-t1, ' Seconds'

	def save(self, s):
		f = open(s, 'w')
		for x in range(len(self.w_in)):
			for y in range(len(self.w_in[x])):
				f.write(str(self.w_in[x][y])+'\n')
		for x in range(len(self.w_out)):
			for y in range(len(self.w_out[x])):
				f.write(str(self.w_out[x][y])+'\n')

	def load(self, s):
		stuff=open(s).read().split('\n')[:-1]
		i = 0
		for x in range(len(self.w_in)):
			for y in range(len(self.w_in[x])):
				self.w_in[x][y] = float(stuff[i])
				i+=1
		for x in range(len(self.w_out)):
			for y in range(len(self.w_out[x])):
				self.w_out[x][y] = float(stuff[i])
				i+=1
	
	def test(self,dataset):
		for item in dataset:
			print 'Input: ', item[0], ' Output: ',self.calculate(item[0]), ' Expected: ',item[1]

def main():	
	stuff=open('iris.txt').read().split('\n')[:-1]
	dataset = []
	for thing in stuff:
		temp1 = thing.split(' ')[:]
		inp = [] 
		for x in xrange(len(temp1)-1):
			inp.append(float(temp1[x]))
		out = [0]*3;
		out[int(temp1[-1])-1] = 1;
		dataset.append([inp,out])

	nn = neuralnet(4,5,3)
	nn.learnBack(dataset, 3000)
	nn.save('weightIris.txt')
	nn.test(dataset)

main()

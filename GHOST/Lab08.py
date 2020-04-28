# -*- coding: iso-8859-1 -*-
# Caelan Garrett, GHOST
from random import *
import string
from time import time
from math import *
players = 0
class letter:
	def __init__(self, a, b, c):
		self.value = a
		self.level = c
		self.word = b
		self.next = []
	def add(self,a):
		self.next.append(a)
	def get(self, a):
		for elem in self.next:
			if elem.value == a:
				return elem
		return None
	def __str__(self):
		return self.value

def addtree(node, word, nword, index):
	if len(word) == index:
		if index<=len(nword) and word[:index] == nword[:index]:
			return node,index
		else:
			return letter('', False, -1), -1
	lt = word[index]
	qw = node.get(lt)
	n = None
	if qw == None:	
		if len(word)-1 == index:
			n = letter(lt, True, index+1)
		else:
			n = letter(lt, False, index+1)
		node.add(n)
	else:
		n = qw
	a,b = addtree(n, word, nword, index+1)
	if b != -1:
		return a,b
	elif index<=len(nword) and word[:index] == nword[:index]:
		return node,index
	else:
		return a,b

def playerpick(p,wd):
	print 'Player ',p+1
	return raw_input('Input: ')

def recur(p,t,wd,nd):
	if nd == None or len(nd.next) == 0 or (nd.word and len(wd)>3):
		q = t-1
		if q <0:
			q = players-1
		if p == q:
			return None, -1
		else:
			return None, 1
	store1, store2 = None, None
	gh = nd.next
	shuffle(gh)
	for stuff in gh:
		q = t+1
		if q == players:
			q = 0
		pick,good = recur(p,q,wd+(stuff.value), stuff)
		if (p == t and good == 1) or (p != t and good == -1):
			return stuff.value, good
		else:
			store1, store2 = stuff.value, good
	return store1,store2

def computerpick(p,t,wd,nd):
	print 'Player ', p+1
	if nd == None or len(nd.next) == 0 or (nd.word and len(wd)>3):
		print 'Input: challenge'
		return 'challenge'
	else:
		choice,good = recur(p,t,wd,nd)
		if good == -1:
			print 'Aw, I lost'
		print 'Input: ',choice
		return choice
			
t = time()
print 'Loading...'
infile=open('dictionary.txt')
root = letter('', False, 0)
st = root
current = infile.readline()[:-1]
next = None
i = 0
while current != '':
	next = infile.readline()[:-1]
	st, i = addtree(st, current, next, i)
	if i == -1:
		st = root
		i = 0
	current = next
infile.close()
print time()-t


humans = int(raw_input('Welcome to GHOST! How many Humans?: '))
computers = int(raw_input('How many Computers?: '))
players = humans+computers
if players <2:
	players = 2
	computers = 1
	humans = 1
while True:
	play = []
	for i in range(0, humans):
		play.append(False)
	for i in range(0, computers):
		play.append(True)
	turn = 0
	w = ''
	itr = root
	print '\n'
	print 'New Game'
	while True:
		
		if play[turn]:
			new = computerpick(turn,turn, w,itr)
		else:
			new = playerpick(turn,w)
		if new == 'challenge':
			if itr == None or len(itr.next) == 0 or (itr.word and len(w)>3):
				if len(play) > 2:
					if turn == 0:
						print 'Player ',players,' lost!'
					else:
						print 'Player ',turn,' lost!'
				else:
					print 'Player ',turn+1,' won!'
				if raw_input('Play Again (y/n): ') == 'y':
					break
				else:
					exit(0)
			else:
				if len(play) > 2:
					print 'Player ',turn+1,' lost!'
				else:
					if turn+1 == players:
						print 'Player ',1,' won!'
					else:
						print 'Player ',turn+2,' won!'
				if raw_input('Play Again (y/n): ') == 'y':
					break
				else:
					exit(0)
		else:
			new = new[0]
			if itr != None:
				tmp = itr.get(new)
			w = w+new
			print w
			itr = tmp
			turn+=1
			if turn == players:
				turn = 0


# -*- coding: iso-8859-1 -*-
#Caelan Garrett, 9/10/09, Neighboors
#
import string

wlist=open('words.txt').read().split('\n')[:-1] # emoticon is like chomp
while 1:
	ustr=raw_input('String (quit): ')
	if ustr == 'quit':
		break
	while ustr not in wlist:
		ustr=raw_input('String (quit): ')
	neigh = []
	x = 0;
	while x<len(ustr):
		for letter in string.ascii_lowercase:
			  temp = ustr[:x]+ letter+ ustr[x+1:]
			  if temp in wlist and temp != ustr:
				  neigh[len(neigh):] = [temp]
				  print temp
		x+=1
	if len(neigh) == 0:
		print 'No matches'
print 'Done!'

# -*- coding: iso-8859-1 -*-
#
# Torbert, 4.20.2010
#

from random import choice

regions='WA SA NT Q NSW V'.split()
colors ='red green blue'.split()

nbrs={}
nbrs['WA']='NT SA'.split()
nbrs['SA']='NT WA Q NSW V'.split()
nbrs['NT']='WA SA Q'.split()
nbrs['Q']='NT SA NSW'.split()
nbrs['NSW']='SA Q V'.split()
nbrs['V']='SA NSW'.split()

def recur(assignments,variables,values,constraints):

	done=True
	#
	# heuristic: choose the state w/ the fewest colors remaining
	#
	# tiebreaker --> who has the most neighbors
	#
	for var in variables:
		if var not in assignments:
			done=False
			break

	if done:
#		solution=True
#		for r in regions:
#			for n in nbrs[r]:
#				if ht[r]==ht[n]:
#					solution=False
#		if solution:
			for r in regions:
				print '%3s %5s'%(r,ht[r]),
			print
			from sys import exit
			exit(0)
	else:
		for val in values[var]:
			assignments[var]=val
			#
			# loop over nbrs and "take away" color val
			#
			recur(assignments,variables,values,constraints)
			#
			# loop over nbrs and "give back" color val *tricky careful only if you took it out
			#

		del assignments[var] # backtracking !!!

ht={}
recur(ht,regions,colors,nbrs)

# solution=True
# for r in regions:
# 	print r,ht[r]
# 	for n in nbrs[r]:
# 		print '\t',n,ht[n]
# 		if ht[r]==ht[n]:
# 			solution=False
# print
# print 'solution:',solution

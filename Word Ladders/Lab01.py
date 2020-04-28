#Caelan Garrett, 9/10/09, Neighboors
#

wlist=open('words.txt').read().split('\n')[:-1] # emoticon is like chomp
while 1:
	ustr=raw_input('String (quit): ')
	if ustr == 'quit':
		break
	neigh = 0
	if ustr in wlist:
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
				print word
				neigh = 1
	elif neigh == 0:
		print 'No matches'
	else:
		print 'No, %s is not a word.' % (ustr)
print 'Done!'

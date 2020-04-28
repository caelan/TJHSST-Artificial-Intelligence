# -*- coding: iso-8859-1 -*-
black, white, empty, outer = 1, 2, 0, 3
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
from heapq import heappush, heappop

def bracket(board, player, square):
	opp = opponent_color(player)
	for d in directions:
		k = square + d
		if board[k] is not opp:
			continue
		while board[k] is opp:
			k = k + d
		if board[k] is player:
			k = k - d
			while k != square:
				board[k] = player
				k = k - d

def would_bracket(board, player, square):
	opp = opponent_color(player)
	for d in directions:
		k = square + d
		if board[k] is not opp:
			continue
		while board[k] is opp:
			k = k + d
		if board[k] is player:
			return True
	return False

def get_legal_moves(board, player):
	possible = []
	for row in range(10, 90, 10):
		for col in range(1, 9):
			square = row + col
			if board[square] is not empty:
				continue
			if would_bracket(board, player, square):
				possible.append(square)
	return possible

def opponent_color(player):
	if player is black: 
		return white
	return black




#def pick(board,player):
#	Pointboard=makePointBoard()
#bracket changes the board
#would bracket tells which one is white and which one is block
#	poss=get_legal_moves(board,player)
#	if len(poss)==0:
#		return None

#	return poss[0]
   # *  Total piece differential.
    #* Weighted piece differential.
    #* Potential, stability, and mobility. 
import pdb
def opponent_color(player):
	if player is black: 
		return white
	return black
def makePointBoard():
	pointboard=[]
	for x in xrange(0,100,1):
		pointboard.append(0)
	pointboard[0]=5
	pointboard[9]=5
	pointboard[99]=5
	pointboard[90]=5
	return pointboard
	#evaluates the corners
def boardHeur(board,directions,player):
	return board[square]
def totalheur(board,player,square):#calculates the total number of boards
	bracket(board,player,square)
	count=0
	oppcount=0	
	opp=opponent_color(player)
	if(square==11 or square==18 or square==81 or square==88):
		return 9999
	for x in board:
		if(x==player):
			count+=1
	return player

	 


def changem(value):
	if(value==1):
		return -1
	else:
		return 1

def minimaxtotal(board,player,curscore,level,square):#starts with max
	if(square<0):
		return [totalheur(board,player,square),square]

	if(level==5):
		#print '*****************************'
		#bracket(board,player,square)
		return [totalheur(board,player,square),square]
	elif(would_bracket(board,player,square)):
		bracket(board,player,square)
	elif(would_bracket(board,player,square)==False):
		return [totalheur(board,player,square),square]
	
	leafarray=[]
	nsquare=square
	for d in directions:
		nsquare=nsquare+d
		curvalue=minimaxtotal(board,opponent_color(player),curscore, level+1,nsquare)
		leafarray.append([curvalue,square])
	returnvalue=0 #current lowest/or bigger value
	for x in leafarray:
		if(returnvalue>x[0]):
			if(player==-1):
				returnvalue=x
			if(player==1):
				continue
	return returnvalue

def pick(board, player):
	
	poss=get_legal_moves(board,player)
	if len(poss)==0:
	  return None
	pointboard=makePointBoard()
	totalarray=[]
	for k in poss:
    		moppy=minimaxtotal(board,player,0,0,k)
		print moppy
		heappush(totalarray,k)
	#passing illegally is when you return none
	return totalarray[-1]

#def minimaxboard(board, curplayer, curscore):


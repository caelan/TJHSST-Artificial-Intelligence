# -*- coding: iso-8859-1 -*-
from random import *
black, white, empty, outer = 1, 2, 0, 3
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
corners = [11,18,81,88]
bad = [12, 21, 22, 17, 28, 27, 77, 78,87,71, 82, 72]
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

def evaluate(board,player):
	mycount = 0
	oppcount = 0
	for row in range(10, 90, 10):
		for col in range(1, 9):
			square = row + col
			if board[square] == empty:
				continue
			if board[square] == player:
				if square in corners:
					mycount+=65
				elif square in bad:
					mycount-=40
				elif row == 10 or row == 80 or col == 1 or col == 8:
					mycount+=2
				else:
					mycount+=1
			else:
				if square in corners:
					oppcount+=65
				elif square in bad:
					oppcount-=40
				elif row == 10 or row == 80 or col == 1 or col == 8:
					oppcount+=2
				else:
					oppcount+=1
	if oppcount == 0:
		return 1000
	elif mycount == 0:
		return -1000
	return mycount-oppcount

def recur(board,player,turn,depth,constant,alpha,beta): # Alpha-beta my algorithm
	if depth < 0:
		return -1, evaluate(board, player)
	poss = get_legal_moves(board,player)
	if depth == constant: #Get the corners!!!
		cmoves = []
		for m in poss:
			if m in corners:
				cmoves.append(m)
		if len(cmoves) >0:
			poss = cmoves[:]
			print poss
	returnmove = None
	shuffle(poss)
	for move in poss:
		temp = board[:]
		temp[move] = turn
		bracket(temp, turn, move)
		pos, value = recur(temp, player, opponent_color(turn), depth-1,constant, alpha, beta)
		if turn == player:
			if value > alpha:
				returnmove, alpha = move, value
		else:
			if value < beta:
				returnmove, beta = move, value
		if alpha >= beta:
			break
	if len(poss) == 0:
		temp = board[:]
		pos, value = recur(temp, player, opponent_color(turn), depth-1,constant, alpha, beta)
		if turn == player:
			value-=20
			if value > alpha:
				returnmove, alpha = None, value
		else:
			value+=20
			if value < beta:
				returnmove, beta = None, value
	if turn == player:
		return returnmove, alpha
	else:
		return returnmove, beta

def pick(board,player):
	move,value = recur(board,player,player, 5, 5, -9999, 9999) #Only odd ply!
	return move


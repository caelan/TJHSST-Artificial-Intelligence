# -*- coding: iso-8859-1 -*-
from random import *
black, white, empty, outer = 1, 2, 0, 3
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
corners = [11,18,81,88]
bad = [[12, 21, 22],[17, 28, 27],[71, 82, 72], [77, 78,87]]
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
	cornersleft = 4
	for i in range(0,4):
		if board[corners[i]] == player:
			mycount+=65
			cornersleft-=1
		elif board[corners[i]] == opponent_color(player):
			oppcount+=65
			cornersleft-=1
		else:
			for s in range(0,3):
				if board[bad[i][s]] == player:
					oppcount+=40
				elif board[bad[i][s]] == opponent_color(player):
					mycount+=40
	if mycount == 0 or cornersleft == 0:	
		for row in range(10, 90, 10):
			for col in range(1, 9):
				square = row + col
				if board[square] == empty:
					continue
				if board[square] == player:
					if row == 10 or row == 80 or col == 1 or col == 8:
						mycount+=2
					else:
						mycount+=1
				else:
					if row == 10 or row == 80 or col == 1 or col == 8:
						oppcount+=2
					else:
						oppcount+=1
		if oppcount == 0:
			return 1000
		if mycount == 0:
			return -1000
	return mycount-oppcount

def recur(board,player,turn,depth,constant,number,alpha,beta): # Alpha-beta my algorithm
	if depth < 0 or number == 64:
		return -1, evaluate(board, player)
	poss = get_legal_moves(board,player)
	if depth == constant: #Get the corners FOOL!!!
		cmoves = []
		for m in poss:
			if m in corners:
				cmoves.append(m)
		if len(cmoves) >0:
			poss = cmoves[:]
	returnmove = None
	shuffle(poss)
	for move in poss:
		temp = board[:]
		temp[move] = turn
		bracket(temp, turn, move)
		pos, value = recur(temp, player, opponent_color(turn), depth-1,constant,number+1, alpha, beta)
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
		pos, value = recur(temp, player, opponent_color(turn), depth-1,constant,number+1, alpha, beta)
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
	number = 0
	cornersleft = 4
	for i in range(0,4):
		if board[corners[i]] != empty:
			cornersleft-=1
	for row in range(10, 90, 10):
			for col in range(1, 9):
				square = row + col
				if board[square] != empty:
					number+=1

	move, value = -1, -1
	if cornersleft>=2:
		move,value = recur(board,player,player, 5, 5,number, -9999, 9999) #Only odd ply!
	elif cornersleft == 0:
		move,value = recur(board,player,player, 64-number, 64-number,number, -9999, 9999)
	else:
		move,value = recur(board,player,player, 7, 7,number, -9999, 9999)
	return move


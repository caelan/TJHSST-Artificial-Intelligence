# -*- coding: iso-8859-1 -*-
from random import *
black, white, empty, outer = 1, 2, 0, 3
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
#spaces = [outer, outer, outer, outer, outer, outer, outer,outer,outer, outer, outer,50,-1,5,2,2,5,-1,50,outer,outer,-1,-10,1,1,1,1,-10,-1,outer,outer,5,1,1,1,1,1,1,5,outer,outer,2,1,1,1,1,1,1,2,outer,outer,2,1,1,1,1,1,1,2,outer,outer,5,1,1,1,1,1,1,5,outer,outer,-1,-10,1,1,1,1,-10,-1,outer,outer,50,-1,5,2,2,5,-1,50,outer,outer, outer, outer, outer,outer,outer, outer, outer, outer, outer]
corners = [11,18,81,88]
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
					mycount+=10
				elif row == 10 or row == 80 or col == 1 or col == 8:
					mycount+=2
				else:
					mycount+=1
			else:
				if square in corners:
					oppcount+=10
				elif row == 10 or row == 80 or col == 1 or col == 8:
					oppcount+=2
				else:
					oppcount+=1
	return mycount-oppcount

def recur(board,player,turn,depth,alpha,beta): # Alpha-beta prunning normal algorithm
	if depth < 0:
		return -1, evaluate(board, player)
	poss = get_legal_moves(board,player)
	returnmove = None
	for move in poss:
		temp = board[:]
		temp[move] = turn
		bracket(temp, turn, move)
		pos, value = recur(temp, player, opponent_color(turn), depth-1, -1*beta, -1*alpha)
		value*=-1
		if value > alpha:
			alpha = value
			returnmove = move
		if beta <= alpha:
			break
	if len(poss) == 0:
		temp = board[:]
		pos, value = recur(temp, player, opponent_color(turn), depth-1, beta*-1, alpha*-1)
		value*=-1
		if value > alpha:
			alpha = value
			returnmove = None
	return returnmove, alpha

def pick(board,player):
	move,value = recur(board,player,player, 5, -9999, 9999) #Only odd ply!
	return move


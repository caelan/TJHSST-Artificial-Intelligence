# -*- coding: iso-8859-1 -*-
from random import *
from time import time
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

def recur(board,player,limit): # Iterative
	depth = 0
	turn = player
	paths = [[board[:],None]]
	time1 = time()
	gameturn = 0
	for row in range(10, 90, 10):
		for col in range(1, 9):
			square = row + col
			if board[square] != empty:
				gameturn+=1
	while gameturn+depth<64:
		if time()-time1>=limit:
			break
		length = len(paths)
		for i in range(0, length):
			current = paths.pop(0)
			cboard = current[0]
			moves = get_legal_moves(cboard,player)
			for n in moves:
				temp = cboard[:]
				temp[n] = turn
				bracket(temp, turn, n)
				package = [temp,current[1]]
				if depth == 0:
					package[1] = n
				paths.append(package)
		turn = opponent_color(player)
		depth+=1
	print depth
	best = [-9999, None]
	length = len(paths)
	for i in range(0, length):
		current = paths.pop(0)
		number = evaluate(current[0], player)
		if number>best[0]:
			best[0] = number
			best[1] = current[1]
	return best[1], best[0]


def pick(board,player):
	move,value = recur(board,player,.15)
	return move


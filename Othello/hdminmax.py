# -*- coding: utf-8 -*-
black, white, empty, outer = 1, 2, 0, 3
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
maxlvl = 5
maxval = beta = 1000
minval = alpha = -1000
curpos = None

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

def pick(board,player):
	#val = minmax(board,player)
	val = alpha_beta_search(board, player)
	return curpos


def alpha_beta_search(state, player):
	global curpos
	curpos = None
	j = maxvalue(state, 1, player)
	return j

def maxvalue(state, lvl, player):
	global curpos, alpha, beta
	if lvl == maxlvl:
		utl = utility(state, player)
		return utl
	i = minval
	positions = get_legal_moves(state,player)
	if len(positions) == 0:
		utl = utility(state, player)
		return utl
	for pos in positions:
		if lvl%2 == 1:
			temp = player
		else:	
			temp = opponent_color(player)
		state[pos] = temp
		bracket(state, temp, pos)
		j = minvalue(state, lvl+1, player)
		if i < j:
			curpos = pos
			i = j
		if i >= beta:
			return i
		if alpha <= i:
			alpha = i
	return i

def minvalue(state, lvl, player):
	global curpos, alpha, beta
	if lvl == maxlvl:
		utl = utility(state, player)
		return utl
	i = maxval
	positions = get_legal_moves(state,player)
	if len(positions) == 0:   
		utl = utility(state, player)
		return utl
	for pos in positions:
		if lvl%2 == 1:
			temp = player
		else:	
			temp = opponent_color(player)
		state[pos] = temp
		bracket(state, temp, pos)
		j = maxvalue(state, lvl+1, player)
		if i > j:
			curpos = pos
			i = j
		if i <= alpha:
			return i
		if beta >= i:
			beta = i
	return i

def utility(state, player):
	bcnt, wcnt = 0,0
	for i in state:
		if i == black:
			bcnt = bcnt + 1
		elif i == white:
			wcnt = wcnt + 1
	if player == black:
		return bcnt-wcnt
	else:
		return wcnt-bcnt
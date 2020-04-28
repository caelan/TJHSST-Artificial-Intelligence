black, white, empty, outer = 1, 2, 0, 3
directions = [-11, -10, -9, -1, 1, 9, 10, 11]

class TreeNode:
	val = None
	left = None
	right = None
	def __init__(self, val, left, right):
		self.val = val
		self.left = left
		self.right = right
	def setLeft(l):
		self.left = l
	def setRight(r):
		self.right = r
	def setVal(v):
		self.val = v
	def getLeft():
		return left
	def getRight():
		return right
	def getVal():
		return val

def mobility(board,player):
	return len(get_legal_moves(board,opponent_color(player)))

def stableCount(board, player):
	count = 0
	for square in board:
		if isStable(board, player, square):
			count = count + 1
	return count

def isStable(board, player, square):
	opp = opponent_color(player)
	for d in directions:
		k = square + d
		while board[k] != 3:
			if board[k] == 0 or board[k] == opp:
				test = k-d
				while board[test] != 3:
					if board[test] == 0 or board[test] == opp:
						return False
					test = test-d
			k = k + d
	return True

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
	poss = get_legal_moves(board,player)
	maxscore = 0
	from random import choice
	if len(poss) < 1:
		return None
	move = choice(poss)
	for child in poss:
		test = board
		test[child] = player
		bracket(test, player, child)
		h = minimax(test,player,10,stableCount)
		if h > maxscore:
			maxscore = h
			move = child
	if h == 0:
		for child in poss:
			test = board
			test[child] = player
			bracket(test, player, child)
			h = minimax(test,player,10,mobility)
			if h > maxscore:
				maxscore = h
				move = child
	return move

def minimax(board,player,depth,score):
	if depth == 0:
		return score(board,player)
	else:
		h = -9999
		poss = get_legal_moves(board,player)
		for child in poss:
			a = 0
			if child in [12,16,21,22,27,28,71,72,77,78,82,87]:
				a = -1
			test = board
			test[child] = player
			bracket(test, player, child)
			h = max(h+a, -minimax(test,opponent_color(player),depth-1,score))
		return h

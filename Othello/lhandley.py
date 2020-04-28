# Laura's Othello AI- part 2 
#THIS IS THE GOOD ONE
#from time import time

black, white, empty, outer = 1, 2, 0, 3
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
badlist=[12, 21, 22, 17, 27, 28, 71, 72, 82, 77, 78, 87]
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

def pick(board,player):  #picks a move
#	warning=time()
	limit=5 #maximum recursion depth- 5 sort of works, 7 does not
	foo=get_legal_moves(board, player)
	if len(foo)==0:
		return None
	best=0
	thing=-1000
	copy=board[:]
	for x in range(len(foo)):
		if foo[x]==11 or foo[x]==18 or foo[x]==81 or foo[x]==88:
			return foo[x] #corners are always nice :)
		board[foo[x]]=player
		bracket(board, player,foo[x])
		it=search(board, player, 1, limit, player, 1000, -1000)
		if it>thing:
			thing=it
			best=x
		board=copy[:]
	#	if time()-warning>=1:
	#		print 'almost hit time limit'
	#		return foo[best] #just return best so far
	return foo[best]

def search(board, me, depth, limit, minimax, alpha, beta): #returns best possible weight after limit moves
	if depth==limit:
		return weight(board, me) #weight of board
	else:
		copy=board[:]
		poss=get_legal_moves(board, minimax)
		if minimax==me:
			best=-1000
		else:
			best=1000
		if len(poss)==0:
			return None
		for x in poss:
			board[x]=minimax
			bracket(board, minimax, x)
			#ALPHA-BETA PRUNING
			good=search(board, me, depth+1, limit, opponent_color(minimax), -beta, -alpha)
			if alpha>good:
				alpha=good
			if minimax==me:
				if good>best:
					best=good
			elif good<best:
				best=good
			board=copy[:]
			#ALPHA-BETA
			if beta>alpha:
				break
		return best 

def weight(board, player): #bigger is better for me, worse for opponent
	ihave=0
	youhave=0
	for piece in range(len(board)):
		if piece in badlist: #next to a corner
			grams=-50
		elif piece/10==1 or piece%10==1 or piece/10==8 or piece%10==8:
			grams=15
		elif piece/10==2 or piece%10==2 or piece/10==7 or piece%10==7:
			grams=-15
		else:
			grams=1
		if board[piece]==player:
			ihave+=grams
		elif board[piece]==opponent_color(player):
			youhave+=grams
	return ihave-youhave

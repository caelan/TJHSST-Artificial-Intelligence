import random

black, white, empty, outer = 1, 2, 0, 3
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
hvalue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0,90,-8,07,06,06,07,-8,90,00,
          0,-8,-15,-4,-3,-3,-4,-15,-8,00,
          0,07,-4,07,04,04,07,-4,07,00,
          0,06,-3,04,00,00,04,-3,06,00,
          0,06,-3,04,00,00,04,-3,06,00,
          0,07,-4,07,04,04,07,-4,-8,00,
          0,-8,-15,-4,-3,-3,-4,-15,-8,00,
          0,90,-8,07,06,06,07,-8,90,00,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
refuted = []

bboard = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 2, 1, 0, 0, 0, 3, 3, 0, 0, 0, 1, 2, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

def bracket(board, player, square):
        board = board[:]
        board[square] = player
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
        return board

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
        global refuted
        poss=get_legal_moves(board,player)
        if len(poss)==0:
                return None
        alpha,beta = -float('inf'), float('inf')
        index = 0
        refuted = set()
        limit = 8
        for i in range(len(poss)):
                t = recurse(bracket(board,player,poss[i]),opponent_color(player),1,-beta,-alpha,limit)
                index = i if -t > alpha else index
                alpha = -t if -t > alpha else alpha
                if beta <= alpha:
                        break
        return poss[index]

def recurse(board,player,count,alpha,beta,limit):
        global refuted
        poss=get_legal_moves(board,player)
        if len(poss) > 8:
                limit -= 1
        for i in range(len(poss)):
                if poss[i] in refuted:
                        poss.insert(0, poss[i])
                        del poss[i]
        if len(poss) == 0 or count >= limit or count == 10:
                return h(board,player)
        for i in poss:
                t = recurse(bracket(board,player,i),opponent_color(player),count+1,-beta,-alpha,limit)
                alpha = -t if -t > alpha else alpha
                if beta <= alpha:
                        refuted.add(i)
                        break
                try:
                        refuted.remove(i)
                except:
                        pass
                        
        return alpha

def h(board,player):
        op = opponent_color(player)
        val = [0,0,0]
        for i in range(len(board)):
                item = board[i]
                if item in (player,op):
                        val[item] += hvalue[i]*5
                        for d in directions:
                                k = i+d
                                if board[k] == item:
                                        val[item] += hvalue[k]
        return (val[player] - val[op])

        #return (board.count(player) - board.count(opponent_color(player)))

import cProfile

#cProfile.run('pick(bboard,white)')

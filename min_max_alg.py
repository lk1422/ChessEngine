from function import function_class
import chess
import random
from collections import OrderedDict

class min_max_alg():

    def minimax(board, depth, alpha, beta, current_turn, func, cache):

        if depth == 1:
            FEN = board.fen()
            parent_FEN = cache[1].fen()
            if current_turn:
                return -(func.eval(FEN, parent_FEN, current_turn, cache))
            else:
                return (func.eval(FEN, parent_FEN, current_turn, cache))

        if current_turn:
            alpha_pr = [float('-inf'), " "]
            move_list = board.legal_moves
            if depth == cache[0]:
                move_list = min_max_alg.process_parents(board, False, func, cache)
            for move in move_list:
                newboard = board.copy()
                newboard.push(move)
                pr = min_max_alg.minimax(newboard, depth -1, alpha, beta, False, func, cache)
                if not isinstance(pr, float):
                    if pr[0] > alpha_pr[0]:
                        alpha_pr = [pr[0], move]
                    alpha = max(alpha, pr[0])
                else:
                    if pr > alpha_pr[0]:
                        alpha_pr = [pr, move]
                    alpha = max(alpha, pr)
                if beta <= alpha:
                    break
            return alpha_pr

        else:
            beta_pr = [float('inf'), " "]
            move_list = board.legal_moves
            if depth == cache[0]:
                move_list = min_max_alg.process_parents(board, True, func, cache)
            for move in move_list:
                newboard = board.copy()
                newboard.push(move)
                pr = min_max_alg.minimax(newboard, depth -1, alpha, beta, True, func, cache)
                if not isinstance(pr, float):
                    if pr[0] < beta_pr[0]:
                        beta_pr = [pr[0], move]
                    beta = min(beta, pr[0])
                else:
                    if pr < beta_pr[0]:
                        beta_pr = [pr, move]
                    beta = min(beta, pr)
                if beta <= alpha:
                    break
            return beta_pr
            
    def process_parents(board, current_turn, func, cache):
        evaluations = {}
        move_list = board.legal_moves
        for move in move_list:
            newboard = board.copy()
            newboard.push(move)
            FEN, orig_board = newboard.fen(), board.copy()
            parent_FEN = orig_board.fen()
            evaluations[move] = (func.eval(FEN, parent_FEN, current_turn, cache))
        sorted_list = sorted(evaluations.items(), key=lambda item: item[1])
        sorted_list.reverse()
        array = []
        i, limit = 0, (len(sorted_list))/2
        for key in sorted_list:
            if i < limit:
                array.append(key[0])
                i+=1
        return array







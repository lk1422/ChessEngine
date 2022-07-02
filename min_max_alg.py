from function import function_class
import chess


class min_max_alg():

    def minimax(board, depth, alpha, beta, current_turn, func, cache):

        if depth == 1:
            FEN = board.fen()
            if current_turn:
                orig_board = cache[2]
                parent_FEN = orig_board.fen()
                return -(func.eval(FEN, parent_FEN, current_turn))
            else:
                orig_board = cache[1]
                parent_FEN = orig_board.fen()
                return (func.eval(FEN, parent_FEN, current_turn))

        if current_turn:
            if depth == cache[0] or depth == cache[0]-1:
                cache[1] = board
            alpha_pr = [float('-inf'), " "]
            move_list = board.legal_moves
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
            if depth == cache[0] or depth == cache[0]-1:
                cache[2] = board
            beta_pr = [float('inf'), " "]
            move_list = board.legal_moves
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
            

   

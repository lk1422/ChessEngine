from function import function_class
import chess


class min_max_alg():

    def minimax(board, depth, alpha, beta, current_turn, func, cache):

        if depth == 0:
            FEN = board.fen()
            parent_FEN = cache[2].fen()
            if current_turn:
                parent_FEN = cache[1].fen()
            return func.eval(FEN, parent_FEN, current_turn)

        if current_turn:
            if depth == cache[0] or depth == cache[0]-1:
                cache[2] = board
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
                cache[1] = board
            beta_pr = [float('inf'), " "]
            move_list = board.legal_moves
            for move in move_list:
                newboard = board.copy()
                if depth == cache[0]-1:
                    cache[1] = newboard
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
            

if __name__ == '__main__':
    FEN = "rnb1k2r/p4ppp/4p3/2b3P1/4p2N/8/P1P1PP1P/R1BK1B1R b kq - 0 11"
    board = chess.Board(FEN)
    print(min_max_alg.wrapper(board, 3, float('-inf'), float('inf'), True))
   

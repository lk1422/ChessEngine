import move_set

class min_max_alg:
    
    def minimax(FEN, move_list, depth, alpha, beta, current_turn):
        if depth == 0:
            #return computed value from lenny's bad network
            return 0

        alpha_pr = float('inf')
        beta_pr = float('-inf')
        Game = move_set()

        if current_turn:
            for move in move_list:
                new_fen, new_move_list = Game.update_fen(FEN, move)
                pr = min_max_alg.minimax(new_fen, new_move_list, depth-1, alpha, beta, False)
                alpha_pr = max(alpha_pr, pr)
                alpha = max(alpha,pr)
                if beta <= alpha:
                    break
            return alpha_pr
        else:
            for move in move_list:
                new_fen, new_move_list = Game.update_fen(FEN, move)
                pr = min_max_alg.minimax(new_fen, new_move_list, depth-1, alpha, beta, False)
                beta_pr = min(beta_pr, pr)
                beta = min(beta, pr)
            return beta_pr
            






    
from move_set import move_set

class min_max_alg():

    def minimax(FEN, move_list, depth, alpha, beta, current_turn):

        if depth == 0:
            return 0

        Game = move_set()

        if current_turn:
            alpha_pr = [float('-inf'), " "]
            for move in move_list:
                new_fen, new_move_list = Game.update_fen(FEN, move)
                pr = min_max_alg.minimax(new_fen, new_move_list, depth -1, alpha, beta, False)
                if not isinstance(pr, int):
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
            for move in move_list:
                new_fen, new_move_list = Game.update_fen(FEN, move)
                pr = min_max_alg.minimax(new_fen, new_move_list, depth -1, alpha, beta, True)
                if not isinstance(pr, int):
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
    print(min_max_alg.wrapper())


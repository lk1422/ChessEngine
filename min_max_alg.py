from function import function_class

    
from move_set import move_set


class min_max_alg():
    
    def wrapper(FEN, move_list, depth, alpha, beta, current_turn):
        f = function_class('./previous_models/Prototype2.0-Adam-SGD-1C5L0B-4.pth')
        test =min_max_alg.minimax(FEN, move_list, depth, alpha, beta, current_turn, f)
        return test



    def minimax(FEN, move_list, depth, alpha, beta, current_turn, func):

        if depth == 0:
            return func.eval(FEN)

        Game = move_set()

        if current_turn:
            alpha_pr = [float('-inf'), " "]
            for move in move_list:
                new_fen, new_move_list = Game.update_fen(FEN, move)
                pr = min_max_alg.minimax(new_fen, new_move_list, depth -1, alpha, beta, False, func)
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
            for move in move_list:
                new_fen, new_move_list = Game.update_fen(FEN, move)
                pr = min_max_alg.minimax(new_fen, new_move_list, depth -1, alpha, beta, True, func)
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
    FEN = "rnb1k2r/p4ppp/4p3/2b3P1/4p2N/8/P1P1PP1P/R1BqKB1R w - KQkq 0 11"
    game = move_set()
    movelist, count, castle = game.process_move(FEN)
    print(min_max_alg.wrapper(FEN, movelist, 2, float('-inf'), float('inf'), True))


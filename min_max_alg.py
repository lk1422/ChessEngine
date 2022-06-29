from move_set import  move_set
from function import function_class
class min_max_alg():

    def wrapper():
        f = function_class('./previous_models/./Prototype2.0-Adam-SGD-1C5L0B-4.pth')
        fen = 'rnb1k3/pppp1p2/4pn2/8/3NP3/2N4q/PPP2PP1/R1B1KB2 w Qq - 0 13'
        game = move_set()
        mv_list = game.process_move(fen)
        print(minimax(fen,mv_list,2,0,0,True,f))


    
    def minimax(FEN, move_list, depth, alpha, beta, current_turn, fn_class):
        if depth == 0:
            return f.eval(FEN)

        alpha_pr = float('inf')
        beta_pr = float('-inf')
        Game = move_set()

        if current_turn:
            for move in move_list:
                new_fen, new_move_list = Game.update_fen(FEN, move)
                pr = min_max_alg.minimax(new_fen, new_move_list, depth-1, alpha, beta, False, fn_class)
                alpha_pr = max(alpha_pr, pr)
                alpha = max(alpha,pr)
                if beta <= alpha:
                    break
            return alpha_pr,FEN
        else:
            for move in move_list:
                new_fen, new_move_list = Game.update_fen(FEN, move)
                pr = min_max_alg.minimax(new_fen, new_move_list, depth-1, alpha, beta, True, fn_class)
                beta_pr = min(beta_pr, pr)
                beta = min(beta, pr)
            return beta_pr,FEN
            


if __name__ == '__main__':
    print(min_max_alg.wrapper())


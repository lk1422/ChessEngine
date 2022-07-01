from min_max_alg import min_max_alg
import chess
from function import function_class



class Main_Class():

    def __init__(self, model_path):
        self.minimax = min_max_alg.minimax
        self.f = function_class(model_path)
        print("Model Loaded")
        self.board = chess.Board()


    def run(self): #run on command line input next moves
        print("Welcome to ScoreNet, A Deep Learning model for scoring the board\nparied with a implementation of the minimax algorithm")
        print("What Color am i? [W] or [B]")
        color = input()
        move_state =None
        if color == 'W':
            move_state=True
        elif color == "B":
            move_state= False
        else:
            print("Not a valid color, Exiting")
        if move_state:#make first move 
            #minimax(board, depth, alpha, beta, current_turn, func):
            move = self.minimax(self.board, 2, float('-inf'), float('inf'),move_state, self.f, self.board)
            print(f"Confidence {move[0]}, Move: {move[1]}")
            self.board.push(move[1])
            print(self.board)
        while (command:= input("Enter Your move or [Q] to quit ")) != "Q":
                try:
                    mv = self.board.push_san(command)
                    print(self.board)
                    print(f"You moved {mv}")
                    move = self.minimax(self.board, 2, float('-inf'), float('inf'),move_state, self.f,self.board)
                    print(f"Confidence {move[0]}, Move: {move[1]}")
                    self.board.push(move[1])
                    print(self.board)
                except Exception as e:
                    print("Invalid Input")
                    print(e)



if __name__== '__main__':
    m = Main_Class("./previous_models/ScoreNetL3-N2-cpu.pth")
    m.run()




            

            

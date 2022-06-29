import torch
from chess import pgn, Board 
import chess
from typing import List, Tuple




def format_pieces(board: Board) -> List[Tuple]:
        #Paremeters:
        #board is a chess board

        #returns:
        #list of a list for each peice containing the peices color pos/neg and index 0-63
        arr =[]
        pieces = [ chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING]
        for  piece in pieces:
            #get white and black indexes
            white = list(board.pieces(piece, chess.WHITE))
            black = list(board.pieces(piece, chess.BLACK))
            neg_black = [-i for i in black]
            white.extend(neg_black)
            arr.append(white)
        return arr


def convert_data(data, move):
    arr =[]     
    #get rid of new line
    #iterate through all the pieces
    for pieces in data:
        data =[0 for i in range(64)]
        #iterate through all splaces for the piece
        for piece in pieces:
            color =1
            if piece == []:
                break
            piece = int(piece)
            if piece < 0:
                color = -1
                piece *=-1 

            data[piece]= color
        arr.extend(data)
    move = [move for i in range(64)]
    arr+=move
    tensor = torch.tensor(arr)
    tensor = tensor.reshape(7,8,8)
    tensor = tensor.to(torch.float32)
    return tensor

def convert_Fen(fen):
    board = chess.Board(fen)
    if board.turn:
        move=1
    else:
        move=-1
    format_board = format_pieces(board)
    convert_to_in =convert_data(format_board, move)
    return convert_to_in

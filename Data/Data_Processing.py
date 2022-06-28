import torch
from chess import pgn, Board 
import chess
import os
from typing import List, Tuple
import typing
import zipfile
import requests
from bs4 import BeautifulSoup
class Data_Processing():
    
    def Get_Key_Boards(game: pgn.Game) ->List[Tuple]:
 
        #Parameters:
        # Game -> pgn Game which contains all moves for a given PGN

        #Returns:
        # list[Board] a list of all boards which are deemed interesting these boards are formated and paired with whose move it is
        #interestng boards are boards which come 6 moves befroe a material difference or checkmate
        #NOTE IF THE GAME AS NO INTERESTING BOARDS IT RETURNS NONE
        material_buffer=[]
        mate_buffer =[]
        interesting_boards =[]
        board = game.board()
        material_change= True
        max_buffer = 7
        last_score=0
        for i, move in enumerate(game.mainline_moves()):
            board.push(move)
            turn = board.turn
            turn_num=None
            if turn:
                turn_num=1
            else:
                turn_num=-1

            buffer_element = Data_Processing.format_pieces(board)
            material_buffer = [(turn_num,buffer_element)] + material_buffer
            mate_buffer = [(turn_num, buffer_element)] + mate_buffer
            if len(material_buffer) >max_buffer:
                material_buffer = material_buffer[:max_buffer]
            if len(mate_buffer) > max_buffer:
                mate_buffer = mate_buffer[:max_buffer]
            

            score = Data_Processing.Material_Score(board)
            if score > 3 and not material_change:
                interesting_boards.extend(material_buffer)
                material_buffer =[]
            if board.is_checkmate():
                interesting_boards.extend(mate_buffer)
            
            #SO THE METHOD DOESNT ACCIDENTLY THINK EVEN TRADES ARE INTERESTING
            if score != last_score:
                material_change = True
            if score == last_score:
                material_change = False

            last_score = score
        if len(interesting_boards) == 0:
            interesting_boards= None
        return interesting_boards 


                
       
        
    def Material_Score(board: Board) -> int:
         
         #Parameters:
         #Board: a board containing information about all current pieces on the baord
         
         #Returns:
         #a integer representing the material score of the board
        
        
        score =0
        for i in range(64):
            piece = board.piece_type_at(i)
            if piece == None or piece == chess.KING:
                continue
            '''Find Color'''           
            color=None
            color_boolean = board.color_at(i)
            if color_boolean == True:
                color=1
            else:
                color = -1
            '''Calculate the Pieces score'''
            if piece == chess.BISHOP or piece == chess.KNIGHT:
                score += color*3
            
            elif piece == chess.PAWN:
                score += color

            elif piece == chess.QUEEN:
                score += color*9

            elif piece == chess.ROOK:
                score += color * 5

        #NEGATIVES DONT MATTER SO GET ABS HERE
        if score < 0:
            score *=-1
        return score

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
        print(board)
        if board.turn:
            move=1
        else:
            move=-1
        format_board = Data_Processing.format_pieces(board)
        convert_to_in = Data_Processing.convert_data(format_board, move)
        return convert_to_in

                


    def get_pgn_to_test():
        file ='./data_file/Akopian.pgn'
        pgns = open(file)
        first_game = chess.pgn.read_game(pgns)
        first_game = chess.pgn.read_game(pgns)
        print(first_game.headers["Result"])
        vals =Data_Processing.Get_Key_Boards(first_game)
        print(len(vals))
        print(vals)
        print(Data_Processing.Stringify_Key_Boards(vals, 1))

    def Stringify_Key_Boards(keyboards: List[Tuple], label: int) -> List[str]:

        #TAKES IN A LIST OF boards
        #returns a list of strings to write to the datafile

        arr =[]
        current_string =''
        label = str(label)
        for move, boards in keyboards:
            current_string = label + " "+ str(move) +" "
            for piece_arr in boards:
                if len(piece_arr) == 0:
                    current_string+= 'e|'
                    continue
                for index in piece_arr:
                    current_string+=str(index) +','
                current_string+='|'
            current_string+='\n'
            arr.append(current_string)
        return arr



    
    def make_dataset():
        head = './data_file'
        files = os.listdir(head)
        files = files[205:]
        for file in files:
            if file == 'model_data':
                continue
            games = open(os.path.join(head, file))
            while (game_pgn:=chess.pgn.read_game(games)) != None:
                    #get interesting games
                    label = None
                    if game_pgn.headers["Result"] == '1/2-1/2':
                        continue
                    
                    elif game_pgn.headers["Result"] == '1-0':
                        label = 1
                    elif game_pgn.headers["Result"] == '0-1':
                        label = -1
                    else:
                        continue
                    #get interesting boards
                    try: 
                        boards = Data_Processing.Get_Key_Boards(game_pgn)
                    except:
                        print('skipped game')
                        continue
                    if boards == None:
                        continue
                    data = Data_Processing.Stringify_Key_Boards(boards,label)
                    data = ''.join(data)
                    with open('./data_file/model_data/training.csv', 'a+') as f:
                        f.write(data)
            games.close()
            print(f'{file} has been converted')
        print('Completed')

    
    def csv_length():
        with open('./data_file/model_data/training.csv', 'r') as f:
            j =f.readlines()
            print(len(j))
    def print_test_data():
        with open('./data_file/model_data/training.csv', 'r') as f:
            print(f.readline())
            print(f.readline())
            print(f.readline())


    def donwload_all_files():
        test_url = "https://www.pgnmentor.com/files.html"
        page = requests.get(test_url)
        soup = BeautifulSoup(page.content, "html.parser") 
        test_elements = soup.find_all("a", class_="view" )
        for test in test_elements:
            if "pgn" in str(test) or "zip" in str(test):
                string_variable = str(test)[22:]
                end_index = string_variable.index('"')
                end_path = string_variable[:end_index]

        
    def download_element(head_path, tail_path, file_path):
    #'''Get The Name of the Local File path
    #  This will use the specific name given after the / but before the .
    #'''
        start_index= tail_path.index('/') + 1 
        end_index  = tail_path.index('.')

        local_file_name ='data_file/'+ tail_path[start_index:end_index]
    
        internet_path = head_path+tail_path

        response = requests.get(internet_path)
    
        if '.zip' in tail_path:
            local_file_name+='.zip'
        
        elif '.pgn' in tail_path:
            local_file_name+= '.pgn'

    
        with open(local_file_name, 'w+b') as f:
            f.write(response.content)
            print(f"Downloded: {local_file_name} Sucessfully!")



    def unzip_all_files():
        for dirs in os.listdir('./data_file'):
            if 'zip' in dirs:
                with zipfile.ZipFile(os.path.join('./data_file', dirs), 'r') as zip_ref:
                    zip_ref.extractall('./data_file')
                    print(f"Unzipped {dirs} !")


    def delete_zipped_files():
        for dirs in os.listdir('./data_file'):
            if 'zip' in dirs:
                os.remove('./data_file/'+dirs)
                print(f'Deleted {dirs}')


if  __name__ == '__main__':
    #Data_Processing.make_dataset()   EnglishSicRev2g3.pgn has been converted
    #Data_Processing.print_test_data()
    print(Data_Processing.convert_Fen('4r3/k1r1q2p/p2R2p1/2p5/2b1P3/P3Q2P/3K2P1/2R5 w - - 0 1'))
    


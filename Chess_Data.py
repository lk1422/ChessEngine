from torch.utils.data import Dataset
import os
import torch


class ChessData(Dataset):

    def __init__(self, file_path):
        root = './Data/data_file/model_data/'
        f = open(root+file_path, 'r')
        self.data = f.readlines()
        f.close()


    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        info = self.data[index]
        label, value = self.convert_data(info)
        return label, value
        


    def convert_data(self, data):
        non_positional_data = data.split(' ')
        move = int(non_positional_data[1])
        label = int(non_positional_data[0])

        positional_data = non_positional_data[2]
        positional_data = positional_data.split('|')
        #NOTE DATA ORDER : P Q N B Q K
        arr =[]     
        #get rid of new line
        if positional_data[-1] == '\n':
            positional_data = positional_data[:-1]
        #iterate through all the pieces
        for piece in positional_data:
            data =[0 for i in range(64)]
            pieces = piece.split(',')
            #iterate through all splaces for the piece
            for piece in pieces:
                color =1
                if piece == 'e':
                    break
                if piece =='':
                    continue
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
        if label == -1:
            label =0
        return label, tensor

                

    def split_dataset(self, split):
        return None

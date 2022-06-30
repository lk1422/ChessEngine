
from torch.utils.data import Dataset
import os
import torch


class TripletData(Dataset):

    def __init__(self, file_path):
        root = './Data/data_file/model_data/'
        f = open(root+file_path, 'r')
        self.data = f.readlines()
        f.close()


    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        info = self.data[index]
        anchor, pos, neg= self.triplet_convert_data(info)
        return anchor, pos, neg

    def triplet_convert_data(self, data):
        first_split = data.index('-')
        if first_split == 0 :
            first_split=2
        
        move = int(data[:first_split])
        data = data[first_split+1: ].split(' ')
        if data[-1] == '\n':
            data = data[:-1]
        anchor = self.convert_data(data[0], move)
        pos = self.convert_data(data[1], -1*move)
        neg = self.convert_data(data[2], -1 * move)
        return anchor, pos, neg

        


    def convert_data(self, data, move):


        positional_data = data.split('|')
        #NOTE DATA ORDER : P Q N B Q K
        arr =[]     
        #get rid of new line
        #iterate through all the pieces
        for pieces in positional_data:

            if pieces == '':
                continue
            data =[0 for i in range(64)]
            pieces = pieces.split(',')
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
        return tensor

                

    def split_dataset(self, split):
        return None

import torch
from model import *
from Utils import convert_Fen
import torch
import torch.nn.functional as F
import chess
from collections import OrderedDict

class function_class():
    def __init__(self,path):
        self.model = ScoreNetL3("./previous_models/LVec2-Cpu.pth")
        self.model.load_state_dict(torch.load(path))
        self.model.eval()

    def eval(self,pos,anchor, move, cache):
        key = pos.split(" ")[0] + anchor.split(" ")[0]
        if key in cache[2]:
            return cache[2][key]
        else:
            pos = convert_Fen(pos).unsqueeze(0)
            anchor = convert_Fen(anchor).unsqueeze(0)
            out = torch.sigmoid(self.model(anchor, pos))
            out = out.squeeze().item()
            cache[2][key] = out
            return out



#if __name__ == '__main__':
#    f = function_class('./previous_models/Prototype2.0-Adam-SGD-1C5L0B-4.pth')
#    print(f.eval('r5k1/pp2bppp/2n2n2/5bB1/8/6P1/PPP1PPBP/R2R2K1 b - - 1 16'))
#    print(f.eval('rnb1k3/pppp1p2/4p3/8/3Nn3/2N4P/PPP2P2/R1B1KB2 w Qq - 0 14'))

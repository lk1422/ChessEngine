import torch
from model import Test_Model
from Utils import convert_Fen
import torch.nn.functional as F
device= torch.device('cuda') if torch.cuda_is_available() else torch.device('cpu')


class function_class():
    def __init__(self,path):
        self.model = Test_Model().to(device)
        self.model.load_state_dict(torch.load(path))


    def eval(self, fen):
        inputs = convert_Fen(fen).to(device).unsqueeze(0)
        out = F.softmax(self.model(inputs), dim=1).squeeze()[1].item()
        return out



#if __name__ == '__main__':
#    f = function_class('./previous_models/Prototype2.0-Adam-SGD-1C5L0B-4.pth')
#    print(f.eval('r5k1/pp2bppp/2n2n2/5bB1/8/6P1/PPP1PPBP/R2R2K1 b - - 1 16'))
#    print(f.eval('rnb1k3/pppp1p2/4p3/8/3Nn3/2N4P/PPP2P2/R1B1KB2 w Qq - 0 14'))

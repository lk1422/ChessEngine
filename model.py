import torch.nn as nn
import torch
import torch.nn.functional as F


#TO BE IMPLEMENTED
        
#BASIC TESTING MODEL
class Test_Model(nn.Module):
    def __init__(self):
        super(Test_Model,self).__init__()
        self.conv1 = nn.Conv2d(7,128, kernel_size=3,stride=1)
        self.max = nn.MaxPool2d(2,2)
        self.linear = nn.Sequential(nn.Linear(1152, 512), nn.ReLU(), nn.Linear(512,512), nn.ReLU(), nn.Linear(512,128),
                                   nn.ReLU(), nn.Linear(128,64), nn.ReLU(), nn.Linear(64,2))
        

    def init_weights(self):#For hyper parameter testing
        torch.nn.init.normal_(self.conv1.weight,0, 1e-7)
        torch.nn.init.normal_(self.conv2.weight,0, 1e-7)
        torch.nn.init.normal_(self.conv3.weight,0, 1e-7)
        torch.nn.init.normal_(self.conv4.weight,0, 1e-6)
    
    def forward(self,x):
        x = F.relu(self.conv1(x))
        x = self.max(x)
        x = x.reshape(x.shape[0], -1)
        x = self.linear(x)
        
        
        return x


class Encoding_Network(nn.Module):
    
    def __init__(self):
        
        super(Encoding_Network, self).__init__()
        self.conv = nn.Sequential(nn.Conv2d(7, 32, kernel_size=2), nn.ReLU(), nn.Conv2d(32, 64, kernel_size=2), nn.BatchNorm2d(64), nn.ReLU(),
                                 nn.MaxPool2d(2,2))
        self.linear = nn.Linear(576, 256)
        
        
    def forward(self,x):
        x = self.conv(x)
        x = x.reshape(x.shape[0], -1)
        x = F.relu(self.linear(x))
      
        return x


class Longer_Encoding_Network(nn.Module):
    
    def __init__(self):
        
        super(Longer_Encoding_Network, self).__init__()
        self.conv = nn.Sequential(nn.Conv2d(7, 32, kernel_size=2), nn.ReLU(), nn.Conv2d(32, 64, kernel_size=2), nn.BatchNorm2d(64), nn.ReLU(),
                                 nn.MaxPool2d(2,2))

        self.linear = nn.Linear(576, 784)
        
        
    def forward(self,x):
        x = self.conv(x)
        x = x.reshape(x.shape[0], -1)
        x = F.relu(self.linear(x))
      
        return x
     
    
class ScoreNetL2(nn.Module):#
    def __init__(self, Encoder_Path):
        super(ScoreNetL2, self).__init__()
        self.Enc = Longer_Encoding_Network()
        self.Enc.load_state_dict(torch.load(Encoder_Path))
        
        self.linear = nn.Sequential(nn.Linear(1568, 1024), nn.BatchNorm1d(1024), nn.ReLU(), nn.Linear(1024,1))
        
    def forward(self,Anchor, Sample):
        AnchorVec = self.Enc(Anchor)
        SampleVec = self.Enc(Sample)
        x = torch.cat((AnchorVec, SampleVec), 1)
        x = self.linear(x)
        return x




class ScoreNetL3(nn.Module):
    def __init__(self, Encoder_Path):
        super(ScoreNetL3, self).__init__()
        self.Enc = Longer_Encoding_Network()
        self.Enc.load_state_dict(torch.load(Encoder_Path))
        
        self.linear = nn.Sequential(nn.Linear(1568, 2048), nn.BatchNorm1d(2048), nn.ReLU(), nn.Linear(2048,512),
                                    nn.BatchNorm1d(512), nn.ReLU(), nn.Linear(512,1))
        
    def forward(self,Anchor, Sample):
        AnchorVec = self.Enc(Anchor)
        SampleVec = self.Enc(Sample)
        x = torch.cat((AnchorVec, SampleVec), 1)
        x = self.linear(x)
        return x

class ScoreNetL5(nn.Module):#
    def __init__(self, Encoder_Path):
        super(ScoreNetL5, self).__init__()
        self.Enc = Longer_Encoding_Network()
        self.Enc.load_state_dict(torch.load(Encoder_Path))
        
        self.linear = nn.Sequential(nn.Linear(1568, 2048), nn.BatchNorm1d(2048), nn.ReLU(), nn.Linear(2048,2048),
                                    nn.BatchNorm1d(2048), nn.ReLU(), nn.Linear(2048,1024), nn.BatchNorm1d(1024), nn.ReLU(),
                                   nn.Linear(1024,512), nn.BatchNorm1d(512), nn.ReLU(), nn.Linear(512, 1))
        
    def forward(self,Anchor, Sample):
        AnchorVec = self.Enc(Anchor)
        SampleVec = self.Enc(Sample)
        x = torch.cat((AnchorVec, SampleVec), 1)
        x = self.linear(x)
        return x

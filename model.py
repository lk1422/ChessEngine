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
     



import torch
import torch.nn as nn
from torch.autograd import Variable as V
import torch.nn.functional as F


class rerank_Controller(torch.nn.Module):
    
    def __init__(self, input_dim,hidden_dim,output_dim):
        super(rerank_Controller,self).__init__()



        self.proj1=nn.Linear(input_dim,hidden_dim)
        self.proj2=nn.Linear(hidden_dim,output_dim)
        self.proj3=nn.Linear(output_dim,output_dim)

        #nn.init.xavier_normal(self.proj1.weight)
        #nn.init.xavier_normal(self.proj2.weight)

        nn.init.kaiming_normal_(self.proj1.weight, mode='fan_out', nonlinearity='relu')
        nn.init.kaiming_normal_(self.proj2.weight, mode='fan_out', nonlinearity='relu')
        nn.init.kaiming_normal_(self.proj3.weight, mode='fan_out', nonlinearity='relu')

        self.softmax=nn.Softmax()
        #self.softplus=nn.Softplus()

        
    def forward(self,input_dis):


        input=input_dis.view(1,-1)

        input = F.normalize(input)
        #print('input',input)

        output = self.proj1(input)
        output = F.relu(output)
        output = self.proj2(output)
        output = F.relu(output)
        output = self.proj3(output)
        #print('output',output)
        n_weight = self.softmax(output[:,0:output.shape[1]-1])
        new_old_weight = F.sigmoid(output[:,output.shape[1]-1])
        
        return n_weight,new_old_weight
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import data.npz as npz
import core.constants as constants

import math

device = torch.device("cpu")
if torch.cuda.is_available():
    device = torch.device("cuda:0")        

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 1, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(1, 1, 5)
        self.fc1 = nn.Linear(286, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 2)
        self.output_layer = nn.Sigmoid()
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        x = self.output_layer(x)
        return x
    
class NN(nn.Module):
    def __init__(self):
        super().__init__()

class LinearRegression():
    def __init__(self):
        pass

def train_cnn(npzs):
    hop_len = constants.HOP_LEN
    sample_rate = constants.SAMPLE_RATE
    hop_ms = hop_len/sample_rate
    hop_count_base = 8 #how many hops will be in each parititon (mostly for labels)
    hop_count_input = 100 #how many hops will be used for the model input
    splice_ms = hop_count_base * hop_ms * 1000
    
    #   partition song  #
    #each partition gets hop_count_input data
    #active partition gets changed via hop_count_base
    #there will be a lot of overlap
    
    #initialize pytorch
    model = CNN()
    model = model.to(device)
    loss_function = nn.BCELoss()
    
    #hyperparameters
    learning_rate = .1
    momentum = .9
    
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=momentum)
    
    for npz_data in npzs:
        #------ get audio data  ------#        

        #create audio partitions for training
        spectogram = npz_data.spectogram #[freq, hop]
        spectogram_T = spectogram.T #[hop, freq]
        
        partitions = [] #3d array

        hop_count = len(spectogram_T)
        
        for hop_index in range(0, hop_count - (hop_count_input + 1), hop_count_base):
            partition = spectogram_T[hop_index:(hop_index + hop_count_input), :]
            partitions.append(partition)
        partitions = np.array(partitions)
                
        #------ train on each song  ------#
        for song in npz_data.hit_objs:
            #------ get labeled data  ------#
            labels = np.zeros((len(partitions), 2), dtype=np.float32) #one hot
                        
            #for each hit object, mark the partition it is on.
            for hit_obj in song:
                lane = hit_obj[0]
                ms = float(hit_obj[1])
                
                partition_i = math.floor(ms/splice_ms)
                labels[partition_i][1] = 1 #(0, 1) = yes, there is a note here
            
            labels = torch.from_numpy(labels)
            labels = labels.to(device)
            
            #------ get input  ------#
            
            #input = partition (debug)
            
            # for inputs in partitions:
            x = torch.tensor(partitions) #tensor: (batch, width, height)
            x = x.unsqueeze(1) #add channels dimension, tensor: (batch, channels, width, height)
            x = x.to(device)
            
            #-----  train model -----#
            
            epoch_count = 100
            for epoch in range(0, epoch_count):
                optimizer.zero_grad()
                
                outputs = model(x)
                loss = loss_function(outputs, labels)
                loss.backward()
                optimizer.step()
                
                print(loss.item())
                
            print("next song.")
                       
def get_model(model_type):
    npzs = npz.get_npzs()
    
    if model_type == "CNN":
        train_cnn(npzs)
        
        # print(npzs[0].hit_objs[0]) #from the first npz file, print the first song
        # print(len(npzs[0].fft))
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import data.npz as npz

import math

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 1, 5)
        self.pool = nn.MaxPool1d(2, 2)
        self.conv2 = nn.Conv1d(1, 1, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
class NN(nn.Module):
    def __init__(self):
        super().__init__()

class LinearRegression():
    def __init__(self):
        pass

def train_cnn(npzs):
    sample_rate = 44100 #probably wont change
    splice_ms = 25 #partition phyisical time size
    partition_size = sample_rate/splice_ms
    
    model = CNN()
    loss_function = nn.BCELoss()
    
    for npz_data in npzs:
        #------ get audio data  ------#
        i = 0
        
        partitions = [] #2d array [[partition], [partition], ...]
        temp_partition = []
        
        #create audio partitions for training
        for n in npz_data.fft:
            if (i % partition_size == 0):
                partitions.append(temp_partition)
                temp_partition.clear()
            temp_partition.append(n)
            i+=1
        temp_partition.clear()

        #------ train on each song  ------#
        for song in npz_data.hit_objs:
            #------ get labeled data  ------#
            labels = np.zeros(len(partitions))
                        
            #for each hit object, mark the partition it is on.
            for hit_obj in song:
                lane = hit_obj[0]
                ms = float(hit_obj[1])
                
                partition_i = math.floor(ms/splice_ms)
                labels[partition_i] = 1
            
            labels = torch.from_numpy(labels)
            
            #------ get input  ------#
            inputs = []
            for i in range(0, len(partitions)):
                input_data = partitions[i]
                inputs.append(input_data)
            inputs = np.array(inputs, dtype=np.float32)
            inputs = torch.from_numpy(inputs)
            
            outputs = model(inputs)
            loss = loss_function(outputs, labels)
            

def get_model(model_type):
    npzs = npz.get_npzs()
    if model_type == "CNN":
        train_cnn(npzs)
        
        # print(npzs[0].hit_objs[0]) #from the first npz file, print the first song
        # print(len(npzs[0].fft))
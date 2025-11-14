import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

import data.npz as npz
import core.constants as constants

from pathlib import Path

import math

device = torch.device("cpu")
if torch.cuda.is_available():
    device = torch.device("cuda:0")        
# device = torch.device("cpu")
src_dir = Path(__file__).resolve().parent.parent
data_dir = (src_dir.parent.resolve() / "data").resolve()
models_dir = (data_dir / "models").resolve()

class CNN(nn.Module):
    def __init__(self):
        super().__init__()        
        self.conv1 = nn.Conv2d(1, 8, 4)
        self.conv2 = nn.Conv2d(8, 16, 4)
        self.conv3 = nn.Conv2d(16, 32, 4)
        
        self.fc1 = nn.Linear(3808, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 256)
        self.fc4 = nn.Linear(256, 128)
        self.fc5 = nn.Linear(128, 4)
        
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x
    
class NN(nn.Module):
    def __init__(self):
        super().__init__()

class LinearRegression():
    def __init__(self):
        pass

def parse_audio(spectogram_data):
    hop_len = constants.HOP_LEN
    sample_rate = constants.SAMPLE_RATE
    hop_ms = hop_len/sample_rate
    hop_count_base = 1 #how many hops will be in each parititon (mostly for labels)
    hop_count_input = 5 #10 #how many hops will be used for the model input
    splice_ms = hop_count_base * hop_ms * 1000
    
    #create audio partitions for training
    spectogram = spectogram_data #[freq, hop]
    spectogram_T = spectogram.T #[hop, freq]
    
    partitions = [] #3d array

    hop_count = len(spectogram_T)
        
    for hop_index in range(0, hop_count - (hop_count_input + 1), hop_count_base):
        if hop_index - hop_count_input < 0:
            partition = spectogram_T[hop_index:(hop_index + hop_count_input * 2), :] #look ahead only
        else:
            partition = spectogram_T[(hop_index - hop_count_input):(hop_index + hop_count_input), :] #look both ahead and behind
        partitions.append(partition)
    partitions = np.array(partitions)
    
    #standardize
    mean = partitions.mean()
    std = partitions.std() + .000001
    partitions = (partitions - mean) / std
    
    return partitions, splice_ms

def train_cnn(npzs):    
    #initialize pytorch
    model = CNN()
    model = model.to(device)

    #hyperparameters
    learning_rate = .00001
    
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    carnation_skip_debug = False
    for npz_data in npzs:
        if not carnation_skip_debug:
            carnation_skip_debug = True
            continue
        
        #------ get partitions  ------#        

        partitions, splice_ms = parse_audio(npz_data.spectogram)
        
        #------ train on each song/beatmap  ------#
        for song in npz_data.hit_objs:
            #------ get labeled data  ------#
            labels = np.zeros((len(partitions), 4), dtype=np.float32) #4 lanes
                        
            #for each hit object, mark the partition it is on.
            pos_weight = torch.tensor([8, 8, 8, 8], device=device)
            for hit_obj in song:
                lane = math.floor(float(hit_obj[0]) * float(4/512)) #4k
                ms = float(hit_obj[1])
                
                partition_i = math.floor(ms/splice_ms)
                labels[partition_i][lane] = 1
                
                pos_weight[lane] += 1
            
            labels = torch.from_numpy(labels)
            labels = labels.to(device)

            # part_len = len(partitions)
            # for i,v in enumerate(pos_weight):
            #     negatives = part_len - v
            #     ratio = negatives / v
            #     pos_weight[i] = ratio/2
            
            loss_function = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
            
            #------ get input  ------#
            
            #input = partition (debug)
            
            # for inputs in partitions:
            x = torch.tensor(partitions) #tensor: (batch, width, height)
            x = x.unsqueeze(1) #add channels dimension, tensor: (batch, channels, width, height)
            x = x.to(device)
            
            #-----  train model -----#
            
            batch_size = 256
            loader = DataLoader(TensorDataset(x, labels), batch_size, shuffle=True, drop_last=False)

            epoch_count = 8 #100

            for epoch in range(0, epoch_count):
                loss_sum = 0
                model.train()
                for xb, yb in loader:
                    xb = xb.to(device)
                    yb = yb.to(device)
                    
                    optimizer.zero_grad()
                    
                    output = model(xb)  
                    loss = loss_function(output, yb)
                    loss.backward()
                    optimizer.step()

                    loss_sum+=loss.item()
                    
                print(loss.item()/len(loader))
        print("_" * 24)
        break
    
    save_model_name = input("Save model as: ")
    
    if len(save_model_name) == 0:
        return
    
    path = ((models_dir.resolve() / "CNN") / (save_model_name + ".pth"))
    
    if path.exists():
        print("Overwriting previous model.")
        path.unlink()
    
    torch.save(model.state_dict(), path)
                       
def get_model(model_type):
    npzs = npz.get_npzs()
    
    if model_type == "CNN":
        train_cnn(npzs)
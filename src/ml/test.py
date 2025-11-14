import math
import random

import ml.train as train

import numpy as np
import torch

from core.game import Game
from data.npz import Npz
from pathlib import Path

src_dir = Path(__file__).resolve().parent.parent
data_dir = (src_dir.parent.resolve() / "data").resolve()
models_dir = (data_dir / "models").resolve()
predicted_dir = (data_dir / "predicted").resolve()
npz_dir = (data_dir / "npz")

device = torch.device("cpu")
if torch.cuda.is_available():
    device = torch.device("cuda:0")

def get_hit_objects(outputs, splice_ms):
    raw_hit_objects = []
    
    for i, tensor in enumerate(outputs):
        probs = torch.sigmoid(tensor)
        threshold = .75
        for lane, v in enumerate(probs):
            if v > threshold:
                #add hit object
                hit_object_ms = int(i * splice_ms)
                raw_hit_objects.append([lane, hit_object_ms])
        
    #parse hit objects for Game        
    hit_objects = []
    for hit_object in raw_hit_objects:
        # lane = math.floor(float(hit_object[0]) * float(4/512)) #4k for now.
        lane = hit_object[0]
        start_time = int(hit_object[1])
            
        hit_object_data = [lane, start_time]
        hit_objects.append(hit_object_data)
        
    return hit_objects

def test_model(model_type, model_name):
    if model_type == "CNN":
        cnn_path = (models_dir / "cnn")
        model_path = (cnn_path / (model_name + ".pth"))
        
        if not model_path:
            raise RuntimeError("Model does not exist.")
        
        model_path = str(model_path)
        
        model = train.CNN()
        model.load_state_dict(torch.load(model_path, weights_only=True))
        model.eval()
        
        npz_number = input("Enter song number: ")
        
        npz_obj = Npz(str(npz_dir / str(npz_number)))
        
        spectogram = npz_obj.spectogram
        partitions, splice_ms = train.parse_audio(spectogram)
                        
        x = torch.tensor(partitions) 
        x = x.unsqueeze(1)
        x = x.to(device)
        model = model.to(device)
        outputs = model(x)
        
        hit_objects = get_hit_objects(outputs, splice_ms) 
        game = Game(npz_number, "pysu", False, hit_objects)
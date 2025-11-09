import os
from data.generate_files import load_dataset
from core.game import Game
from ml.train import get_model
from ml.test import test_model

#ask render type, ask what to play, ask if 
def main():    
    run_type = input("Enter run type (train, generate, test, pysu, termisu): ")

    if run_type == "generate":
        load_dataset()

    if run_type == "pysu" or run_type == "termisu":
        osz_id = input("Enter osz file id.")
        pred = input("Split screen prediction? (y/n)")
        if pred == "y":
            pred = True
        else:
            pred = False
        
        game = None
        if run_type == "pysu":
            game = Game(osz_id, "pysu", pred)
        else:
            game = Game(osz_id, "termisu", pred)
    elif run_type == "test":
        model_type = input("What model (CNN, NN, or Linear)?")
        model_name = input("Input model name: ")
        
        test_model(model_type, model_name)
    elif run_type == "train":
        model_type = input("What model (CNN, NN, or Linear)?")
        
        model = get_model(model_type)

if __name__ == "__main__":
    main()
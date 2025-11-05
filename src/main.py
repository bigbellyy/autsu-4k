import os
from data.generate_files import load_dataset
from core.game import Game

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
        pass
    elif run_type == "train":
        pass

if __name__ == "__main__":
    main()
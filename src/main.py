import os
from data.generate_files import load_dataset
import data.npz as npz
from core.game import Game

#config
_generate_dataset = False

def main():
    if _generate_dataset:
        load_dataset()

    print("\x1b[H\x1b[2J")
    
    osu_type = int(input("Enter render type: 0, 1 or 2."))

    if osu_type != 0 and osu_type != 1 and osu_type != 2:
        raise RuntimeError("Invalid render type.")

    if osu_type == 1:
        osz_id = input("Enter osz file id. Append -p for the predicted version.")
        
        game = Game(osu_type, 0)

if __name__ == "__main__":
    main()
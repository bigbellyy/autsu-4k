from pathlib import Path
import numpy as np

script_dir = Path(__file__).resolve().parent
data_dir = (script_dir / "../../data").resolve()
npz_dir = (data_dir / "npz").resolve()

def get_npzs():
    npzs = []
    for path in npz_dir.iterdir():
        npz = Npz(path.stem)
        npzs.append(npz)
    return npzs

#Helper class, loads, parses npzs
class Npz:
    def __init__(self, file_name: str):
        file_name += ".npz" #add extension
        file_path = (npz_dir / file_name)
        
        #contains keys: fft, hit_obj
        #hit_obj : hit_obj[0] = 0th song
        #hit_obj[1] = 1st song
        #hit_obj[0][0] 0th song's first hit object
        self.data = np.load(file_path, allow_pickle=True)
        self.hit_objs = self.data["hit_obj"]
        self.fft = self.data["fft"]
        
        pass
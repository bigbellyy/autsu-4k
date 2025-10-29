import os
import shutil
from pathlib import Path

script_dir = Path(__file__).resolve().parent
data_dir = (script_dir / "../../data").resolve()
osr_dir = (data_dir / "osr").resolve()
zip_dir = (data_dir / "zip").resolve()

#Convert .osr's to zips.
def load_osr():
    #Get all zip files
    zip_paths = zip_dir.rglob('*.zip')
    zips = set()
    for path in zip_paths:
        file_name = path.resolve().stem #File name, no extension.
        zips.add(file_name)
    
    #Get all osr files
    osr_paths = osr_dir.rglob('*.osr')
    for path in osr_paths:
        file_name = path.resolve().stem

        #Continue on duplicates
        if file_name in zips:
            continue
        
        #Clone file
        src = path.resolve()
        dst = zip_dir.resolve()
        shutil.copy(src, dst)

def process_zip():
    pass

def load_dataset():
    pass

if __name__ == "__main__":
    load_osr()
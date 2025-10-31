import os
import shutil
import zipfile
from pathlib import Path


script_dir = Path(__file__).resolve().parent
data_dir = (script_dir / "../../data").resolve()
osz_dir = (data_dir / "osz").resolve()
zip_dir = (data_dir / "zip").resolve()
processed_dir = (data_dir / "processed").resolve()
temp_dir = (data_dir / "temp").resolve()

def _sanity_check():
    if not data_dir.is_relative_to(script_dir.parent.parent):
        raise RuntimeError("A directory's location has been modified.")

#Convert .osr's to zips.
def load_osr():
    _sanity_check()
    
    _processed_children = os.listdir(processed_dir)
    file_id = len(_processed_children)
    
    #Get all zip files
    zip_paths = zip_dir.rglob('*.zip')
    zips = set()
    for path in zip_paths:
        file_name = path.resolve().stem #File name, no extension.
        zips.add(file_name)
    
    #Get all osr files
    osz_paths = osz_dir.rglob('*.osz')
    for path in osz_paths:
        file_name = path.resolve().stem
        
        #Continue on duplicates
        if file_name in zips:
            continue

        #Clone file
        src = path.resolve()
        dst = zip_dir.resolve()
        copied_osr = shutil.copy(src, dst)
        
        #change extension to .zip
        new_name = str(zip_dir / file_name) + ".zip"
        os.rename(copied_osr, new_name)
        
        #create directory for osz
        osz_dir_path = (processed_dir / str(file_id)).resolve()
        if os.path.exists(osz_dir_path):
            raise RuntimeError("Processed directory already exists.")
        os.makedirs(osz_dir_path)
        
        #extract zip
        with zipfile.ZipFile(new_name, 'r') as zip_ref:
            zip_ref.extractall(osz_dir_path)
        
        audio_file = (osz_dir_path / "audio.mp3").resolve()
        osu_file = str(osz_dir_path / file_name) + ".osu"     
        
        ####        clean up osz directories        ####
        
        #delete instruments, keep music file
        
        #mp3 pass
        for path in osz_dir_path.iterdir():
            if path.suffix != ".osu" and path.suffix != ".mp3": #audios are mp3
                path.unlink()
            
        #rename pass
        for path in osz_dir_path.iterdir():
            if path.suffix == ".mp3":
                new_name = (path.parent / "audio.mp3") 
                path.rename(new_name)
        
        file_id+=1

def load_dataset():
    pass

def _clean():
    #Clear zip directory
    zip_paths = zip_dir.rglob('*.zip')
    for path in zip_paths:
        file_name = path.resolve()
        os.remove(file_name)
        
    #Clear processed
    for path in processed_dir.iterdir():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


if __name__ == "__main__":
    _sanity_check()
    
    _clean()
    
    load_osr()
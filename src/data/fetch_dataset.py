import os
import shutil
import zipfile
from util.osu_parser import OSUFile
from pathlib import Path


script_dir = Path(__file__).resolve().parent
data_dir = (script_dir / "../../data").resolve()
osr_dir = (data_dir / "osr").resolve()
zip_dir = (data_dir / "zip").resolve()
processed_dir = (data_dir / "processed").resolve()

def _sanity_check():
    if not data_dir.is_relative_to(script_dir.parent.parent):
        raise RuntimeError("A directory's location has been modified.")

#Convert .osr's to zips.
def load_osr():
    _sanity_check()
    
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
        copied_osr = shutil.copy(src, dst)
        
        #change extension to .zip
        new_name = str(zip_dir / file_name) + ".zip"
        os.rename(copied_osr, new_name)
        
        #extract zip
        extraction_directory = (processed_dir / "temp").resolve()
        
        with zipfile.ZipFile(new_name, 'r') as zip_ref:
            zip_ref.extractall(extraction_directory)
            
        audio_file = (extraction_directory / "audio.mp3").resolve()
        osu_file = str(extraction_directory / file_name) + ".osu"     
        
        #rename files and move files
        mp3_dir = (processed_dir / "mp3").resolve()
        osu_dir = (processed_dir / "osu").resolve()
        
        #move to mp3 directory
        new_name = str(mp3_dir / file_name) + ".mp3"
        os.rename(audio_file, new_name)
        
        #move to osu directory
        new_name = str(osu_dir / file_name) + ".osu"
        os.rename(osu_file, new_name)

def load_dataset():
    pass

def _clean():
    #Clear zip directory
    zip_paths = zip_dir.rglob('*.zip')
    for path in zip_paths:
        file_name = path.resolve()
        os.remove(file_name)
    
    mp3_dir = (processed_dir / "mp3")
    osu_dir = (processed_dir / "osu")
    
    #Clear osu directory
    osu_paths = osu_dir.rglob('*.osu')
    for path in osu_paths:
        file_name = path.resolve()
        os.remove(file_name)

    #Clear mp3 directory
    mp3_paths = mp3_dir.rglob('*.mp3')
    for path in mp3_paths:
        file_name = path.resolve()
        os.remove(file_name)


if __name__ == "__main__":
    _sanity_check()
    
    _clean()
    
    load_osr()
    
    print(str((data_dir / "osu") / "AAAA - Hoshizora no Kanransha.osu"))
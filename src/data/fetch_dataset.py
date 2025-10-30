import os
import shutil
import zipfile
from pathlib import Path

script_dir = Path(__file__).resolve().parent
data_dir = (script_dir / "../../data").resolve()
osr_dir = (data_dir / "osr").resolve()
zip_dir = (data_dir / "zip").resolve()
processed_dir = (data_dir / "processed").resolve()

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

if __name__ == "__main__":
    load_osr()
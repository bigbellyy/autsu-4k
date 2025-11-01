import os
import shutil
import zipfile
import librosa
import soundfile as sf
import numpy as np
from scipy.io.wavfile import read
from pathlib import Path

script_dir = Path(__file__).resolve().parent
data_dir = (script_dir / "../../data").resolve()
osz_dir = (data_dir / "osz").resolve()
zip_dir = (data_dir / "zip").resolve()
processed_dir = (data_dir / "processed").resolve()
temp_dir = (data_dir / "temp").resolve()
npz_dir = (data_dir / "npz").resolve()

def _sanity_check():
    if not data_dir.is_relative_to(script_dir.parent.parent):
        raise RuntimeError("A directory's location has been modified.")

#Convert .osr's to zips.
def _load_osz():
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
                
        #.mp3 -> .wav
        audio_path = (osz_dir_path / "audio.mp3").resolve()
        output_path = (osz_dir_path / "audio.wav").resolve()
        y, sample_rate = librosa.load(str(audio_path), sr=44100) #Fix sample rate, to make life easier
        sf.write(str(output_path), y, sample_rate)
        
        #delete the previous audio file
        audio_path.unlink()
        
        file_id+=1

def _parse_osu(path: Path):
    data = []
    
    with open(path) as f: #Hit objects format: column, nil, timing (milli), (1 = normal, 128 = long), nil,endTiming (milli)
        found_hit_objects = False
        for line in f:        
            #Continue until it reaches "[HitObjects]"
            if "[HitObjects]" in line:
                found_hit_objects = True
                continue
            
            if not found_hit_objects:
                continue
            
            line_data = line.split(",")
            column = line_data[0]
            time = line_data[2]
            hit_type = line_data[3]
            end_time = line_data[5]
            
            #parse end_time (its padded with colons)
            end_time_colon_index = end_time.find(":")
            end_time = end_time[0:end_time_colon_index]
            
            hit_data = [column, time, hit_type, end_time]
            
            data.append(hit_data)
        if not found_hit_objects:
            raise RuntimeError("No [HitObjects] tag found." + path.stem)
    
    return data
        
def _parse_audio(path:Path):
    rate, data = read(str(path.resolve()))
    audio_fft = np.fft.fft(data)
    
    return audio_fft

def _generate_npz():
    osz_count = len(os.listdir(processed_dir))
    processed_count = 0
    for osz_dir in processed_dir.iterdir():
        if not osz_dir.is_dir():
            continue
        
        file_id = osz_dir.stem
        
        audio_data = None
        hit_objs = []
        
        for path in osz_dir.iterdir():
            if path.stem == "audio":
                audio_data = _parse_audio(path)
            elif path.suffix == ".osu":
                hit_obj_data = _parse_osu(path)
                hit_objs.append(hit_obj_data)
            
        #Save to file
        file_name = str(npz_dir / file_id) + ".npz"
        with open(file_name, "wb") as f:
            np.savez_compressed(f, fft=audio_data, hit_obj=np.asarray(hit_objs, dtype="object")) #compress it
                
        processed_count+=1
        print(str(processed_count)+"/"+str(osz_count) + " completed.")
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
    
    #Clear npy
    for path in npz_dir.iterdir():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

#Reads the stored json file containing the dataset, then returns it parsed.
def get_dataset():
    pass

def load_dataset():
    _sanity_check()
    _clean()
    _load_osz()
    _generate_npz()
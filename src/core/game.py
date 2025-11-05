import time
import math

from playsound import playsound
import pygame
from data.npz import Npz
from core.pysu import Pysu

from pathlib import Path

#visualizes osz files.
class Game:
    def __init__(self, osu_id, osu_type, pred):
        self.osu_id = osu_id
        if osu_type == "pysu":
            self.npz_data = Npz(osu_id)
            self.cur_ms = 0
            self.starting_ms = int(time.time() * 1000)
            
            self.hit_objects = self.generate_hit_objects()
            self.renderer = Pysu(self.hit_objects, pred)

            self.play_song()

            while True:
                self.update_pysu()

    def play_song(self):
        script_dir = Path(__file__).parent.resolve()
        data_dir = (script_dir / "../../data").resolve()
        processed_dir = (data_dir / "processed").resolve()
        
        song_dir = (processed_dir / self.osu_id).resolve()
        audio = (song_dir / "audio.wav").resolve()
        
        pygame.mixer.init()
        pygame.mixer.music.load(str(audio))
        pygame.mixer.music.play()
    
    def generate_hit_objects(self):
        hit_objects = []
        raw_hit_objects = self.npz_data.hit_objs

        song_index = 0
        songs_count = len(raw_hit_objects)
        if songs_count > 1:
            song_index = input("Which song will be played? (" + str(songs_count) + " songs)")
            song_index = int(song_index) - 1

        if song_index < 0 or song_index > songs_count:
            raise RuntimeError("Song index is out of bounds.")
        
        song = raw_hit_objects[song_index]
        
        for hit_object in song:
            lane = math.floor(float(hit_object[0]) * float(4/512)) #4k for now.
            start_time = int(hit_object[1])
            
            hit_object_data = [lane, start_time]
            hit_objects.append(hit_object_data)
            #todo, end time
        
        return hit_objects
    
    def update_pysu(self):
        self.cur_ms = int(time.time() * 1000) - self.starting_ms
        self.renderer.render()
        self.renderer.update_ms(self.cur_ms)
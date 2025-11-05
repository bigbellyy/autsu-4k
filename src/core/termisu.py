import os
import math

#Terminal renderer for osu
class Termisu:
    def __init__(self, hit_objects, pred):
        self.hit_objects = hit_objects
        self.pred = pred
        self.cur_ms = 0
        
        self.frame_time = 20
        self.last_ms = self.cur_ms
        
        #static size
        self.width = 4
        self.height = 50
        
        #Initialize pixel array
        self.pixels = {}
        for y in range(0, self.height):
            self.pixels[y] = {}
            for x in range(0, self.width):
                self.pixels[y][x] = " "
                        
    def render(self):
        #maximize frame rate
        if (self.cur_ms - self.last_ms < self.frame_time):
            return
        self.last_ms = self.cur_ms
        
        self.clear_pixels()
        
        offset = -44.5
        for hit_obj in self.hit_objects:
            lane = hit_obj[0]
            
            #scale ms to fit on grid
            scale = 20
            ms = hit_obj[1]
            ms = math.floor(ms / scale)
            ms += offset
            
            pixel_x = lane
            pixel_y = math.floor(self.cur_ms/scale - ms)
            
            if (pixel_x >= self.width or pixel_x < 0 or pixel_y < 0 or pixel_y >= self.height):
                continue
            
            self.pixels[pixel_y][pixel_x] = "######"
        
        self.print_pixels()

    def print_pixels(self):
        left_padding = 10
        for y in range(0, self.height):
            line = " " * left_padding
            for x in range(0, self.width):
                hit_size = len(self.pixels[y][x]) * 2
                line += " " * hit_size
                line += self.pixels[y][x]
                line += " " * hit_size
            print(line)
    
    def clear_pixels(self):
        os.system('cls' if os.name == "nt" else 'clear')
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.pixels[y][x] = " "
    
    def update_ms(self, new_ms):
        self.cur_ms = new_ms
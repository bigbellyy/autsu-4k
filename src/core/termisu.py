import os
import numpy

#Terminal renderer for osu
class Termisu:
    def __init__(self, lane_width, height):
        self.lane_width = lane_width
        self.height = height
        self.lane_count = 4
        
    def render(self):
        pass
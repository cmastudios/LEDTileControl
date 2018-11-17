import numpy as np
import cv2
import random
from math import sin, cos, pi

color_choices = (
    (255, 0, 171),  # Magenta
    (20, 248, 255), # Cyan
    (255, 137, 0),  # Bright Orange
    (255, 255, 0),  # Yellow
    (255, 0, 0),    # Red
    (255, 255, 255) # White
)

fireworks = []
background_color = (0, 0, 0)
time = 0
max_fireworks = 10000

def display(board, leds, num_fireworks=5, firework_omega=100, segs=10):
    global fireworks, time, background_color, color_choices
    num_fireworks = int(num_fireworks)
    firework_omega = int(firework_omega)
    segs = int(segs)
    img = np.tile(background_color, board.shape).astype(np.uint8)
    if time % firework_omega == 0 and len(fireworks) < max_fireworks:
        for i in range(num_fireworks):
            segments = []
            start = (random.randint(0, board.shape[0]), random.randint(0, board.shape[1]))
            offset = random.random()
            for s in range(segs):
                segments.append(Segment(
                    start,
                    angle=2*pi*s/segs + offset,
                    color=random.choice(color_choices)
                ))
            fireworks.append(Firework(segments))
    for firework in fireworks:
        for segment in firework.segments:
            cv2.line(img, segment.get_start(), segment.get_end(), segment.color)
        firework.update()
        if firework.times > firework.duration:
            fireworks.remove(firework)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    leds.draw(img)
    time += 1
    

class Firework:
    def __init__(self, segments):
        self.times = 0
        self.duration = segments[0].duration
        self.segments = segments
        
    def update(self):
        for s in self.segments:
            s.update()
        self.times += 1

class Segment:
    def __init__(self, start:tuple, length=5, angle=0, duration=500, speed=0.1, color=(255, 255, 255)):
        """
        :param angle: Angle in radians
        """
        self.start = start
        self.length = length
        self.angle = angle
        self.duration = duration
        self.times = 0
        self.color = color
        self.speed = speed
        self.end = self.get_end()
        
    def get_start(self):
        return (int(self.start[0]), int(self.start[1]))
        
    def update(self):
        self.start = (self.start[0] + self.speed*cos(self.angle), self.start[1] + self.speed*sin(self.angle))
        self.times += 1
        self.color = (int(self.color[0] * 0.99), int(self.color[1] * 0.99), int(self.color[2] * 0.99))
    
    def get_end(self):
        return (int(self.start[0] + self.length*cos(self.angle)),
            int(self.start[1] + self.length*sin(self.angle)))
        

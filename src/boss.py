from random import randint
from boss_items import Items
from bullet import Bullet
import pygame
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

class Boss:
    def __init__(self, boss_rect):
        self.boss_rect = boss_rect
        self.health = 6000
        self.x = boss_rect.x
        self.y = boss_rect.y
        
    def attack(self):
        circles = list()
        for _ in range(0,20):
            radius = 45
            x = random.randint(radius, SCREEN_WIDTH - radius)
            y = random.randint(radius, SCREEN_HEIGHT - radius)
            circles.append({
                "x": x,
                "y": y,
                "radius": radius,
            })
            
        return circles
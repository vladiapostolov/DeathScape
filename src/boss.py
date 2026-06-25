from random import randint
from boss_items import Items
from bullet import Bullet
import pygame

class Boss:
    def __init__(self, boss_rect):
        self.boss_rect = boss_rect
        self.health = 6000
        self.x = boss_rect.x
        self.y = boss_rect.y
        
    def attack(self, items_object):
        for i in range(3):
            number = randint(1, 100)
            if number >=1 or number < 3:
                #draw a shield in front of it
                shield_rect = pygame.Rect(self.x + 200, self.y + 50, 50, 200)
                items_object.add_shields(shield_rect)
            elif number >=3 or number < 6:
                #draw bullets toward the player
                bullet = Bullet(self.x, self.y, 60, 30, 'right')
                items_object.add_bullets(bullet)
            else:
                #use_attack _ 3
                pass
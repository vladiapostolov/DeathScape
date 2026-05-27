import pygame
from pathlib import Path
from enemy import Enemy
from bullet import Bullet

SHEET_DIR = Path('./assets/gangster-pixel-character-sprite-sheets-pack/Gangsters_1')

#128x128 is each frame
def load_sheet(filename, frame_w = 128, frame_h = 128):
    sheet = pygame.image.load(str(SHEET_DIR/filename)).convert_alpha()
    cols = sheet.get_width() // frame_w
    frames = []
    for i in range(cols):
        frame = sheet.subsurface((i*frame_w, 0, frame_w, frame_h))
        frames.append(frame)
    return frames

def hasCollided(bullet, enemies):
    
    bullet_rect = pygame.Rect(
        int(bullet.x), int(bullet.y), 10, 4
    )
    
    for enemy in enemies:
        enemy_rect = pygame.Rect(
            int(enemy.x), int(enemy.y), 18, 18
        )
        if bullet_rect.colliderect(enemy_rect):
            if enemy.is_dead:
                continue
            enemy.health -= bullet.damage
            if enemy.health <= 0:
                enemy.is_dead = True
                bullet.killed_enemy = True
            return True
    return False
        

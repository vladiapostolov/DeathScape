import pygame
import random
from utils import load_sheet, hasCollided
from hero import Hero
from enemy import Enemy
from bullet import Bullet

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
ANIM_FPS = 10
BULLET_SPEED = 700
BULLET_DAMAGE = 34
BULLET_W = 10
BULLET_H = 4
BULLET_COLOR = (255, 220, 120)

clock = pygame.time.Clock()
pygame.display.set_caption('DeathScape')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('./assets/game_background.png')

idle_frames = load_sheet('Idle.png')
walk_frames = load_sheet('Walk.png')
shooting_frames = load_sheet('Shot.png')
jumping_frames = load_sheet('Jump.png')

hud = pygame.image.load('./assets/ui/hud_panel.png').convert_alpha()
avatar_img = pygame.image.load('./assets/ui/hero_avatar.png').convert_alpha()
health_bg_img = pygame.image.load('./assets/ui/health_bar_bg.png').convert_alpha()
health_fill_img = pygame.image.load('./assets/ui/health_bar_fill.png').convert_alpha()
ammo_icon_img = pygame.image.load('./assets/ui/ammo_icon.png').convert_alpha()
health_fill_w, health_fill_h = health_fill_img.get_size()

avatar_smooth = pygame.transform.smoothscale(avatar_img, (80, 80))

player = Hero(screen.get_width() / 2, screen.get_height() / 2)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
facing = 'right'

base_enemies = 5
current_wave = 1
spawn_timer = 0.0
wave_break = 15
has_wave_finished = True
killed_count = 0

next_spawn_in = random.uniform(0.25, 1.25)
enemy_size = (18, 18)
enemy_speed = 80
enemies = list()

dt = 0
anim_timer = 0
fire_interval = 0.15
time_since_last_shot = 0.0
anim_frame = 0
run = True
cur_state = ''
prev_state = 'idle'
jump_iterations = 0
jumping = False

bullets = list()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if jump_iterations == len(jumping_frames):
        jump_iterations = 0
        
    keys = pygame.key.get_pressed()
    moving = False
    shooting = False
    cur_state = 'idle'
    if keys[pygame.K_w]:
        player_pos.y -= 200 * dt
        player.y = player_pos.y
        moving = True
        cur_state = 'w'
    if keys[pygame.K_s]:
        player_pos.y += 200 * dt
        player.y = player_pos.y
        moving = True
        cur_state = 's'
    if keys[pygame.K_a]:
        facing = 'left'
        player_pos.x -= 200 * dt
        player.x = player_pos.x
        moving = True
        cur_state = 'a'
    if keys[pygame.K_d]:
        facing = 'right'
        player_pos.x += 200 * dt
        player.x = player_pos.x
        moving = True
        cur_state = 'd'
    if keys[pygame.K_SPACE]:
        jumping = True
        cur_state = 'space'
    if keys[pygame.K_h] and time_since_last_shot >= fire_interval:
        player.shoot(1)
        shooting = True if player.ammo > 0 else False
            #we throw the bullet from the current position
        time_since_last_shot = 0.0
        if shooting:
            if facing == 'left':
                bullet_x = player.x - 20
                bullet_y = player.y
            elif facing == 'right':
                bullet_x = player.x + 20
                bullet_y = player.y
            bullets.append(Bullet(bullet_x, bullet_y, BULLET_SPEED, BULLET_DAMAGE, facing))
    
    
    if cur_state != prev_state and jumping == False:
        prev_state = cur_state
        anim_frame = 0
        
    anim_timer += dt
    spawn_timer += dt
    
    if spawn_timer >= next_spawn_in:
        spawn_timer = 0.0

    if has_wave_finished:
        for _ in range(base_enemies):
            side = random.choice(("left", "right"))
            enemy_y = random.randint(0, SCREEN_HEIGHT)
            
            if side == "left":
                enemy_x = 0
                enemy = Enemy(enemy_x, enemy_y)
            else:
                enemy_x = SCREEN_WIDTH
                enemy = Enemy(enemy_x, enemy_y)
            
            enemies.append(enemy)
        has_wave_finished = False
        next_spawn_in = random.uniform(0.25, 1.25)
    
        
    
    frame_duration = 1 / ANIM_FPS
    if anim_timer >= frame_duration:
        if jumping:    
            jump_iterations += 1
        anim_timer -= frame_duration
        #anim_frame = (anim_frame + 1) % len(walk_frames if moving else idle_frames)
        if jumping or jump_iterations > 0:
            anim_frame = (anim_frame + 1) % len(jumping_frames)
        elif moving:
            anim_frame = (anim_frame + 1) % len(walk_frames)
        elif shooting:
            anim_frame = (anim_frame + 1) % len(shooting_frames)
        else:
            anim_frame = (anim_frame + 1) % len(idle_frames)
    
    if jump_iterations >= 1:
        frame = jumping_frames[anim_frame % len(jumping_frames)]
        #jump_iterations += 1
        if jump_iterations >= len(jumping_frames):
            jump_iterations = 0  # Reset only after completing all frames
            jumping = False  # Ensure jumping state is reset after animation
    elif moving:
        frame = walk_frames[anim_frame % len(walk_frames)]
    elif shooting:
        frame = shooting_frames[anim_frame % len(shooting_frames)]
    else:
        frame = idle_frames[anim_frame % len(idle_frames)]
    
    if facing == 'left':
        frame = pygame.transform.flip(frame, True, False)
            
    screen.blit(background, (0, 0))
    screen.blit(frame, (player.x - 55, player.y - 90))

    hud_x = 17
    hud_y = 13
    screen.blit(hud, (hud_x, hud_y))
    screen.blit(avatar_smooth, (hud_x + 5, hud_y + 9))

    health_pct = max(0, min(1, player.health / 100))
    screen.blit(health_bg_img, (hud_x + 86, hud_y + 16))
    fill_visible_w = int(health_fill_w * health_pct)
    if fill_visible_w > 0:
        health_fill_cropped = health_fill_img.subsurface((0, 0, fill_visible_w, health_fill_h))
        screen.blit(health_fill_cropped, (hud_x + 89, hud_y + 19))

    screen.blit(ammo_icon_img, (hud_x + 84, hud_y + 44))
    
    
    
    #lets draw the fuckers
    for enemy in enemies:
        if enemy.is_dead:
            continue
        
        pygame.draw.rect(screen, (0,0,0), (enemy.x, enemy.y, enemy_size[0], enemy_size[1])) 
        dx = player.x - enemy.x
        dy = player.y - enemy.y
        distance = (dx * dx + dy * dy) ** 0.5
        if distance > 0:
            enemy.x += (dx / distance) * enemy_speed * dt
            enemy.y += (dy / distance) * enemy_speed * dt
    #if shooting:
    for bullet in bullets:
        bullet.updateBullet(dt)
        if bullet.isOffMap() or bullet.collided:
            continue
        
        if hasCollided(bullet, enemies):
            bullet.collided = True
            if bullet.killed_enemy:
                killed_count += 1
            continue
            
        pygame.draw.rect(
            screen,
            BULLET_COLOR,
            (int(bullet.x), int(bullet.y), BULLET_W, BULLET_H)
        )
        
        
    if killed_count == base_enemies:
        has_wave_finished = True
        base_enemies *= 2
        
    time_since_last_shot += dt
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

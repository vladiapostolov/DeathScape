import pygame
import random
from utils import load_sheet, hasCollided
from hero import Hero
from enemy import Enemy
from bullet import Bullet
from object_factory import object_factory
from health_object import health_obj
from ammo_object import ammo_obj
from grenade_object import grenade_obj
from picked_grenade import ThrowGrenade
from boss_items import Items
from boss import Boss

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
ANIM_FPS = 10
BULLET_SPEED = 700
BULLET_DAMAGE = 34
BULLET_W = 10
BULLET_H = 4
BULLET_COLOR = (255, 220, 120)

ammo_color = (214, 170, 92)
ammo_font = pygame.font.SysFont('ammo', 28)

grenade_color = (214, 170, 92)
grenade_font = pygame.font.SysFont('grenade', 28)

clock = pygame.time.Clock()
pygame.display.set_caption('DeathScape')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('./assets/game_background.png')

idle_frames = load_sheet('Idle.png')
walk_frames = load_sheet('Walk.png')
shooting_frames = load_sheet('Shot.png')
jumping_frames = load_sheet('Jump.png')
death_frames = load_sheet('Dead.png')

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
current_wave = 5
spawn_timer = 0.0
wave_break = 15
has_wave_finished = True
killed_count = 0

next_spawn_in = random.uniform(0.25, 1.25)
enemy_size = (25, 25)
enemy_speed = 60
enemies = list()

time_since_last_grenade = 0.0
grenade_throw_interval = 0.35
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
random_object_spawn_rate = 0
dying = False
dying_frames_passed = 0
enemy_hit_cooldown = 0.6
time_since_last_hit = 0.0
dead = False

healths = list()
ammos = list()
bullets = list()
active_grenades = list()
grenades = list()
restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 62, SCREEN_HEIGHT // 2 + 50, 120, 50)
pygame.draw.rect(screen, (80, 80, 80), restart_button_rect)

boss_items = Items()
boss = None
dt_boss = 0
boss_movement_interval = 1.0
boss_shield_interval = 8.0
dt_shield = 0
spawnBossAfterTime = 0.0
timer = 5.0
hasTimerPassed = False
boss_attack_timer = 4.0
attack_timer_passed = 0.0
boss_circles_render_timer = 1.2
boss_circles_passed_time = 0.0
animated_circles = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button_rect.collidepoint(event.pos):
                current_wave = 1
                #Logic: We restart the game, wave is 1, enemies should disappear and annulate everything that was rendered
                #no idea how to do it tho, lets see
                player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                player.x = player_pos.x
                player.y = player_pos.y
                #we center back the fucker player
                moving = False
                cur_state = 'idle'
                dead = False
                dying = False
                jumping = False
                player.ammo = 50
                player.health = 100
                player.has_grenade = False
                player.grenades_count = 0
                healths = list()
                ammos = list()
                bullets = list()
                active_grenades = list()
                grenades = list()
                dt = 0
                anim_timer = 0
                cur_state = ''
                prev_state = 'idle'
                jump_iterations = 0
                dying_frames_passed = 0
                time_since_last_hit = 0.0
                random_object_spawn_rate = 0
                killed_count = 0
                enemies = list()
                base_enemies = 5
                has_wave_finished = True
                
    if jump_iterations == len(jumping_frames):
        jump_iterations = 0
        
    random_object_spawn_rate = random.uniform(0,22)
    keys = pygame.key.get_pressed()
    moving = False
    shooting = False
    cur_state = 'idle' if not dead else None
    if keys[pygame.K_w] and not dying and not dead:
        player_pos.y -= 200 * dt
        player.y = player_pos.y
        moving = True
        cur_state = 'w'
    if keys[pygame.K_s] and not dying and not dead:
        player_pos.y += 200 * dt
        player.y = player_pos.y
        moving = True
        cur_state = 's'
    if keys[pygame.K_a] and not dying and not dead:
        facing = 'left'
        player_pos.x -= 200 * dt
        player.x = player_pos.x
        moving = True
        cur_state = 'a'
    if keys[pygame.K_d] and not dying and not dead:
        facing = 'right'
        player_pos.x += 200 * dt
        player.x = player_pos.x
        moving = True
        cur_state = 'd'
    if keys[pygame.K_SPACE] and not dying and not dead:
        jumping = True
        cur_state = 'space'
    if keys[pygame.K_h] and time_since_last_shot >= fire_interval and not dying and not dead:
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
    if keys[pygame.K_g] and player.has_grenade() and time_since_last_grenade >= grenade_throw_interval:
        player.grenades_count -= 1
        
        time_since_last_grenade = 0.0
        throw_dir = -1 if facing == 'left' else 1
        target_x = player.x + throw_dir * 240
        target_y = player.y - 20
    
        active_grenades.append(ThrowGrenade(
            start_x=player.x,
            start_y=player.y - 30,
            target_x=target_x,
            target_y=target_y,
            flight_time=0.55,
            damage=100,
            explosion_radius=90,
        ))
                
    if cur_state != prev_state and jumping == False:
        prev_state = cur_state
        anim_frame = 0
        
    anim_timer += dt
    spawn_timer += dt
    
    if spawn_timer >= next_spawn_in:
        spawn_timer = 0.0

    if has_wave_finished:
        if current_wave % 5 == 0 and boss is None:
            #this is boss wave:
            if spawnBossAfterTime >= timer:
                boss_rect = pygame.Rect(0,SCREEN_HEIGHT // 2, 250, 300)
                boss = Boss(boss_rect)
                pygame.draw.rect(screen, (150, 0, 0), boss_rect)
                has_wave_finished = False
                spawnBossAfterTime = 0.0
                hasTimerPassed = True
        else:
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
        elif dying:
            anim_frame = (anim_frame + 1) % len(death_frames)
            dying_frames_passed += 1
        elif not dead:
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
    elif dying:
        frame = death_frames[anim_frame % len(death_frames)]
    elif dead:
        frame = death_frames[4]
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
    player_rect = pygame.Rect(int(player.x - 28), int(player.y - 45), 56, 90)
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
        #lets check if there is colllision between the enemies and the player
        enemy_rect = pygame.Rect(int(enemy.x), int(enemy.y), enemy_size[0], enemy_size[1])
        if player_rect.colliderect(enemy_rect) and time_since_last_hit >= enemy_hit_cooldown:
            player.health -= 25
            time_since_last_hit = 0.0
            if player.health <= 0:
                #animate the death scene entirely, disappear all enemies
                dying = True
                anim_frame = 0                
    #if shooting:
    for bullet in bullets:
        bullet.updateBullet(dt)
        if bullet.isOffMap() or bullet.collided:
            continue
        
        if hasCollided(bullet, enemies):
            bullet.collided = True
            if bullet.killed_enemy:
                killed_count += 1
                #obj = random_object(bullet.x, bullet.y) #we need to get the killed enemy's x and y
                object_to_spawn = object_factory(bullet.x, bullet.y, random_object_spawn_rate)
                
                if isinstance(object_to_spawn, health_obj):
                    healths.append(object_to_spawn)
                    object_to_spawn.is_activated = True
                elif isinstance(object_to_spawn, ammo_obj):
                    ammos.append(object_to_spawn)
                    object_to_spawn.is_activated = True
                elif isinstance(object_to_spawn, grenade_obj):
                    grenades.append(object_to_spawn)
                    object_to_spawn.is_activated = True
            continue
        
        bullet_rect = pygame.Rect(int(bullet.x), int(bullet.y), BULLET_W, BULLET_H)
        if boss is not None and boss_rect.colliderect(bullet_rect):
            boss.health -= bullet.damage
            if boss.health <= 0:
                boss = None
                has_wave_finished = True
                current_wave += 1
        for shield in boss_items.shields:
            if shield.colliderect(bullet_rect):
                boss_items.shields.remove(shield)
                bullet.collided = True
            
        pygame.draw.rect(
            screen,
            BULLET_COLOR,
            (int(bullet.x), int(bullet.y), BULLET_W, BULLET_H)
        )
    #boss_animtaion
    if boss:
        ratio = boss.health / 6000
        pygame.draw.rect(screen, "red", (SCREEN_WIDTH - 320, 20, 300, 40))
        pygame.draw.rect(screen, "green", (SCREEN_WIDTH - 320, 20, 300 * ratio, 40))
        pygame.draw.rect(screen, (150, 0, 0), (boss.x, boss.y, 75, 125))
        #now we animate the different boss items
        if dt_shield >= boss_shield_interval:
            dt_shield = 0.0
            shield_rect = pygame.Rect(boss.x + 150, boss.y, 100, 200)
            boss_items.add_shields(shield_rect)
        direction = -1 if random.choice(('up','down')) == 'down' else 1
        if dt_boss >= boss_movement_interval:
            dt_boss = 0.0
            new_y = boss.y + (50*direction)
            if new_y <=0:
                boss.y = 0
            elif new_y + 125 >= SCREEN_HEIGHT:
                boss.y = SCREEN_HEIGHT - 125
            else:
                boss.y = new_y
            pygame.draw.rect(screen, (150, 0, 0), (boss.x, boss.y, 75, 125))
        for shield in boss_items.shields:
            pygame.draw.rect(screen, "purple", shield)
        if attack_timer_passed >= boss_attack_timer or animated_circles == True:
            attack_timer_passed = 0.0
            if animated_circles == False:
                circles_to_draw = boss.attack()
                animated_circles = True
            else:
                if boss_circles_passed_time >= boss_circles_render_timer:
                    boss_circles_passed_time = 0.0
                    animated_circles = False
            for circle in circles_to_draw:
                pygame.draw.circle(screen, "orange", (circle["x"], circle["y"]), circle["radius"], width=0)
                orange_circle_rect = pygame.Rect(int(circle["x"]), int(circle["y"]), circle["radius"] * 2, circle["radius"] * 2)
                if orange_circle_rect.colliderect(player_rect):
                    player.health -= 30
                    circles_to_draw.remove(circle)
                    if player.health <= 0:
                        dying = True
                        anim_frame = 0
                        boss = None
                        
                
    ammo_text = ammo_font.render(str(player.ammo), True, ammo_color)
    screen.blit(ammo_text, (170, 63))
    grenade_text = grenade_font.render(str(player.grenades_count), True, grenade_color)
    screen.blit(grenade_text, (200, 63))
    if killed_count == base_enemies:
        has_wave_finished = True
        base_enemies *= 2
        killed_count = 0
        current_wave += 1
        
    for health_drop in healths[:]:
        if health_drop.is_activated:
            health_rect = pygame.Rect(int(health_drop.x - 6), int(health_drop.y - 6), 12, 12)
            pygame.draw.circle(screen, (255, 0, 0), (int(health_drop.x), int(health_drop.y)), 8)
            if player_rect.colliderect(health_rect):
                health_drop.apply_to_player(player)
                healths.remove(health_drop)

    for ammo_drop in ammos:
        if ammo_drop.is_activated:
            ammo_rect = pygame.Rect(int(ammo_drop.x - 6), int(ammo_drop.y - 6), 12, 12)
            pygame.draw.circle(screen, (255, 215, 0), (int(ammo_drop.x), int(ammo_drop.y)), 8)
            if player_rect.colliderect(ammo_rect):
                ammo_drop.apply_to_player(player)
                ammos.remove(ammo_drop)

    for grenade_drop in grenades:
        if grenade_drop.is_activated:
            grenade_rect = pygame.Rect(int(grenade_drop.x - 6), int(grenade_drop.y - 6), 12, 12)
            pygame.draw.circle(screen, (0, 255, 0), (int(grenade_drop.x), int(grenade_drop.y)), 8)
            if player_rect.colliderect(grenade_rect):
                grenade_drop.apply_to_player(player)
                grenades.remove(grenade_drop)
    
    for g in active_grenades:
        g.t += dt
        p = min(1.0, g.t / g.flight_time)
        g.x = g.start_x + (g.target_x - g.start_x) * p
        g.y = g.start_y + (g.target_y - g.start_y) * p - 4 * g.arc_height * p * (1 - p)
        if p >= 1.0:
            g.exploded = True
        pygame.draw.circle(screen, (60, 90, 120), (int(g.x), int(g.y)), 6)
        
        if g.exploded:
            for enemy in enemies:
                if enemy.is_dead:
                    continue
                
                enemy_rect = pygame.Rect(int(enemy.x), int(enemy.y), enemy_size[0], enemy_size[1])
                #now we check for the nearest point to the rect. Why? Idk, thats the alghorithm. We trust
                closest_x = max(enemy_rect.left, min(g.x, enemy_rect.right))
                closest_y = max(enemy_rect.top, min(g.y, enemy_rect.bottom))
                closest_point = pygame.math.Vector2(closest_x, closest_y)
                
                distance_vector = (g.x, g.y) - closest_point
                if distance_vector.length_squared() <= g.explosion_radius ** 2:
                    enemy.health -= g.damage
                    if enemy.health <= 0:
                        enemy.is_dead = True
                        killed_count += 1
                        if killed_count == base_enemies:
                            has_wave_finished = True
                            base_enemies *= 2
                            killed_count = 0
                            current_wave += 1
            
            g.explosion_timer += dt
            if g.explosion_timer >= frame_duration:
                active_grenades.pop(active_grenades.index(g))
            else:
                pygame.draw.circle(screen, (255, 130, 0), (int(g.x), int(g.y)), g.explosion_radius)
        
    time_since_last_shot += dt
    time_since_last_grenade += dt
    time_since_last_hit += dt
    if hasTimerPassed:
        dt_boss +=  dt
        dt_shield += dt
        attack_timer_passed += dt
        if animated_circles:
            boss_circles_passed_time += dt
    if current_wave % 5 == 0:
        spawnBossAfterTime += dt
    if dying_frames_passed >= 4:
        text = ammo_font.render("YOU DIED", True, (255, 60, 60))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        restart = ammo_font.render("TRY AGAIN", True, (255, 60, 60))
        screen.blit(restart, (SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2 + 70))
        dead = True
        dying = False
    pygame.display.flip()
    dt = clock.tick(60) / 1000
    
pygame.quit()

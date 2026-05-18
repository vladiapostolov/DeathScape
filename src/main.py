import pygame
from utils import load_sheet
from hero import Hero

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
ANIM_FPS = 10

clock = pygame.time.Clock()
pygame.display.set_caption('DeathScape')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('./assets/game_background.png')

idle_frames = load_sheet('Idle.png')
walk_frames = load_sheet('Walk.png')
shooting_frames = load_sheet('Shot.png')

player = Hero(screen.get_width() / 2, screen.get_height() / 2)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
facing = 'right'

dt = 0
anim_timer = 0
anim_frame = 0
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_w]:
        player_pos.y -= 200 * dt
        player.y = player_pos.y
        moving = True
    if keys[pygame.K_s]:
        player_pos.y += 200 * dt
        player.y = player_pos.y
        moving = True
    if keys[pygame.K_a]:
        facing = 'left'
        player_pos.x -= 200 * dt
        player.x = player_pos.x
        moving = True
    if keys[pygame.K_d]:
        facing = 'right'
        player_pos.x += 200 * dt
        player.x = player_pos.x
        moving = True

    anim_timer += dt
    frame_duration = 1 / ANIM_FPS
    if anim_timer >= frame_duration:
        anim_timer -= frame_duration
        anim_frame = (anim_frame + 1) % len(walk_frames if moving else idle_frames)

    if not moving:
        frame = idle_frames[anim_frame]
    else:
        frame = walk_frames[anim_frame]
    
    if facing == 'left':
        frame = pygame.transform.flip(frame, True, False)
            
    screen.blit(background, (0, 0))
    screen.blit(frame, player_pos)
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

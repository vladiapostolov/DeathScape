import pygame
from pathlib import Path

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

"""
Generate high-quality pixel-art player sprites with detailed soldier design.
Run once to create sprite files.
"""
import pygame as pg
import os
import math

def create_soldier_sprite(state, filename):
    """Create detailed pixel-art soldier sprite from BACK view."""
    size = 300
    surf = pg.Surface((size, size), pg.SRCALPHA)
    
    # Colors
    uniform_dark = (60, 100, 50)     # Dark green uniform
    uniform_light = (90, 150, 70)    # Light green
    skin = (230, 200, 160)           # Skin tone
    hair = (30, 25, 20)              # Dark brown/black hair
    gun_metal = (60, 60, 70)         # Gun metal
    gun_barrel = (100, 100, 110)     # Bright barrel
    boot = (40, 40, 35)              # Boot color
    shoulder = (80, 120, 60)         # Shoulder pad
    
    cx = size // 2
    
    # HEAD
    pg.draw.circle(surf, hair, (cx, size//5 - 5), 24)
    pg.draw.circle(surf, skin, (cx - 8, size//5 + 5), 6)  # Ear
    pg.draw.circle(surf, skin, (cx + 8, size//5 + 5), 6)  # Ear
    
    # NECK
    pg.draw.rect(surf, skin, (cx - 6, size//5 + 15, 12, 10))
    
    # HELMET/HEAD GEAR
    pg.draw.polygon(surf, (70, 70, 80), [(cx - 26, size//5 - 8), 
                                          (cx + 26, size//5 - 8),
                                          (cx + 24, size//5 + 10),
                                          (cx - 24, size//5 + 10)])
    
    # SHOULDERS & ARMOR
    pg.draw.polygon(surf, shoulder, [(cx - 32, size//5 + 25), 
                                      (cx - 50, size//5 + 35),
                                      (cx - 48, size//5 + 50),
                                      (cx - 28, size//5 + 35)])
    pg.draw.polygon(surf, shoulder, [(cx + 32, size//5 + 25), 
                                      (cx + 50, size//5 + 35),
                                      (cx + 48, size//5 + 50),
                                      (cx + 28, size//5 + 35)])
    
    # BODY/CHEST PLATE
    pg.draw.rect(surf, uniform_dark, (cx - 28, size//5 + 25, 56, 65))
    # Chest detail
    pg.draw.rect(surf, uniform_light, (cx - 26, size//5 + 28, 52, 12))
    
    # BACKPACK
    pg.draw.rect(surf, (70, 70, 70), (cx - 32, size//5 + 35, 64, 50))
    pg.draw.line(surf, (100, 100, 100), (cx - 32, size//5 + 50), (cx + 32, size//5 + 50), 2)
    
    # ARMS
    if state == 'idle':
        # Both arms at sides
        pg.draw.polygon(surf, skin, [(cx - 32, size//5 + 35), (cx - 38, size//5 + 40), (cx - 36, size//5 + 80)])
        pg.draw.polygon(surf, skin, [(cx + 32, size//5 + 35), (cx + 38, size//5 + 40), (cx + 36, size//5 + 80)])
    elif state == 'walk':
        # Left arm forward, right back
        pg.draw.polygon(surf, skin, [(cx - 32, size//5 + 35), (cx - 35, size//5 + 25), (cx - 34, size//5 + 75)])
        pg.draw.polygon(surf, skin, [(cx + 32, size//5 + 35), (cx + 42, size//5 + 50), (cx + 40, size//5 + 85)])
    elif state == 'run':
        # Exaggerated running pose
        pg.draw.polygon(surf, skin, [(cx - 32, size//5 + 35), (cx - 38, size//5 + 15), (cx - 36, size//5 + 70)])
        pg.draw.polygon(surf, skin, [(cx + 32, size//5 + 35), (cx + 45, size//5 + 55), (cx + 42, size//5 + 90)])
    elif state == 'shoot':
        # Both arms ready on gun
        pg.draw.polygon(surf, skin, [(cx - 32, size//5 + 35), (cx - 35, size//5 + 30), (cx - 32, size//5 + 70)])
        pg.draw.polygon(surf, skin, [(cx + 32, size//5 + 35), (cx + 35, size//5 + 28), (cx + 34, size//5 + 68)])
    
    # GUN - Prominent rifle
    gun_y = size//5 + 45
    if state in ['idle', 'walk']:
        # Gun at ready
        pg.draw.rect(surf, gun_metal, (cx + 35, gun_y, 50, 10))           # Barrel
        pg.draw.rect(surf, gun_barrel, (cx + 83, gun_y - 2, 6, 14))       # Muzzle
        pg.draw.rect(surf, gun_metal, (cx + 42, gun_y + 10, 30, 14))      # Stock
        pg.draw.rect(surf, gun_metal, (cx + 50, gun_y - 8, 4, 10))        # Sight
    elif state == 'run':
        # Gun raised while running
        pg.draw.rect(surf, gun_metal, (cx + 30, gun_y - 20, 50, 10))
        pg.draw.rect(surf, gun_barrel, (cx + 78, gun_y - 22, 6, 14))
        pg.draw.rect(surf, gun_metal, (cx + 38, gun_y - 10, 30, 14))
        pg.draw.rect(surf, gun_metal, (cx + 45, gun_y - 28, 4, 10))
    elif state == 'shoot':
        # Gun firing - recoil position
        pg.draw.rect(surf, gun_metal, (cx + 32, gun_y - 15, 52, 10))
        pg.draw.rect(surf, gun_barrel, (cx + 82, gun_y - 17, 7, 14))
        pg.draw.rect(surf, gun_metal, (cx + 40, gun_y - 5, 32, 14))
        pg.draw.rect(surf, gun_metal, (cx + 48, gun_y - 25, 4, 12))
        # Muzzle flash
        pg.draw.polygon(surf, (255, 200, 80), [(cx + 88, gun_y - 17),
                                                (cx + 105, gun_y - 19),
                                                (cx + 102, gun_y + 5)])
        pg.draw.polygon(surf, (255, 150, 50), [(cx + 90, gun_y - 15),
                                                (cx + 100, gun_y - 16),
                                                (cx + 98, gun_y - 2)])
    
    # LEGS
    leg_start_y = size//5 + 90
    if state in ['idle', 'shoot']:
        # Legs together
        pg.draw.polygon(surf, uniform_dark, [(cx - 16, leg_start_y), (cx - 18, leg_start_y + 60), (cx - 16, leg_start_y + 62)])
        pg.draw.polygon(surf, uniform_dark, [(cx + 16, leg_start_y), (cx + 18, leg_start_y + 60), (cx + 16, leg_start_y + 62)])
        pg.draw.polygon(surf, boot, [(cx - 18, leg_start_y + 60), (cx - 16, leg_start_y + 75), (cx - 14, leg_start_y + 62)])
        pg.draw.polygon(surf, boot, [(cx + 18, leg_start_y + 60), (cx + 16, leg_start_y + 75), (cx + 14, leg_start_y + 62)])
    elif state == 'walk':
        # Walking stride
        pg.draw.polygon(surf, uniform_dark, [(cx - 16, leg_start_y - 5), (cx - 20, leg_start_y + 55), (cx - 18, leg_start_y + 57)])
        pg.draw.polygon(surf, uniform_dark, [(cx + 16, leg_start_y + 5), (cx + 22, leg_start_y + 60), (cx + 20, leg_start_y + 62)])
        pg.draw.polygon(surf, boot, [(cx - 20, leg_start_y + 55), (cx - 18, leg_start_y + 70), (cx - 16, leg_start_y + 57)])
        pg.draw.polygon(surf, boot, [(cx + 22, leg_start_y + 60), (cx + 20, leg_start_y + 75), (cx + 18, leg_start_y + 62)])
    elif state == 'run':
        # Running stride - legs very extended
        pg.draw.polygon(surf, uniform_dark, [(cx - 16, leg_start_y - 15), (cx - 24, leg_start_y + 50), (cx - 22, leg_start_y + 52)])
        pg.draw.polygon(surf, uniform_dark, [(cx + 16, leg_start_y + 15), (cx + 28, leg_start_y + 70), (cx + 26, leg_start_y + 72)])
        pg.draw.polygon(surf, boot, [(cx - 24, leg_start_y + 50), (cx - 22, leg_start_y + 65), (cx - 20, leg_start_y + 52)])
        pg.draw.polygon(surf, boot, [(cx + 28, leg_start_y + 70), (cx + 26, leg_start_y + 85), (cx + 24, leg_start_y + 72)])
    
    # DETAILS - Buttons, patches
    pg.draw.circle(surf, (150, 150, 150), (cx - 8, size//5 + 50), 3)
    pg.draw.circle(surf, (150, 150, 150), (cx, size//5 + 50), 3)
    pg.draw.circle(surf, (150, 150, 150), (cx + 8, size//5 + 50), 3)
    
    return surf

def main():
    pg.init()
    
    sprite_dir = 'resources/sprites/player'
    os.makedirs(sprite_dir, exist_ok=True)
    
    states = ['idle', 'walk', 'run', 'shoot']
    for state in states:
        surf = create_soldier_sprite(state, state)
        path = os.path.join(sprite_dir, f'{state}.png')
        pg.image.save(surf, path)
        print(f'Created {path}')
    
    pg.quit()
    print('High-quality soldier sprites generated!')

if __name__ == '__main__':
    main()



"""
Weapon system with multiple weapons and switching.
"""
import pygame as pg
from collections import deque
from settings import *


class WeaponManager:
    def __init__(self, game):
        self.game = game
        self.weapons = {
            1: Pistol(game),
            2: Shotgun(game),
            3: Rifle(game)
        }
        self.current_weapon_id = 2  # Start with shotgun
        self.current_weapon = self.weapons[self.current_weapon_id]
    
    def switch_weapon(self, weapon_id):
        if weapon_id in self.weapons:
            self.current_weapon_id = weapon_id
            self.current_weapon = self.weapons[weapon_id]
    
    def update(self):
        self.current_weapon.update()
    
    def draw(self):
        self.current_weapon.draw()


class WeaponBase:
    def __init__(self, game, path, scale, animation_time, damage, ammo_per_shot):
        self.game = game
        self.path = path
        self.scale = scale
        self.animation_time = animation_time
        self.damage = damage
        self.ammo_per_shot = ammo_per_shot
        
        self.image = pg.image.load(path).convert_alpha()
        self.images = deque([pg.transform.smoothscale(self.image, (self.image.get_width() * scale, 
                                                                     self.image.get_height() * scale))])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False
    
    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
    
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)
    
    def update(self):
        self.check_animation_time()
        self.animate_shot()
    
    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True
    
    @property
    def reload_progress(self):
        if not self.reloading or self.num_images <= 1:
            return 0.0
        return min(1.0, self.frame_counter / (self.num_images - 1))


class Pistol(WeaponBase):
    def __init__(self, game):
        super().__init__(game, 'resources/sprites/weapon/shotgun/0.png', 0.3, 60, 25, 1)
        self.images = deque([pg.transform.smoothscale(self.image, 
                            (self.image.get_width() * self.scale, self.image.get_height() * self.scale))])
        self.num_images = 1
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height() + 50)


class Shotgun(WeaponBase):
    def __init__(self, game):
        super().__init__(game, 'resources/sprites/weapon/shotgun/0.png', 0.4, 90, 50, 1)
        self.images = deque([pg.transform.smoothscale(img, (self.image.get_width() * self.scale, 
                            self.image.get_height() * self.scale)) for img in self.get_images()])
        self.num_images = len(self.images)
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
    
    def get_images(self):
        images = []
        for i in range(20):
            try:
                img = pg.image.load(f'resources/sprites/weapon/shotgun/{i}.png').convert_alpha()
                images.append(img)
            except:
                break
        return images if images else [self.image]


class Rifle(WeaponBase):
    def __init__(self, game):
        super().__init__(game, 'resources/sprites/weapon/shotgun/0.png', 0.35, 50, 35, 1)
        self.images = deque([pg.transform.smoothscale(self.image, 
                            (self.image.get_width() * self.scale, self.image.get_height() * self.scale))])
        self.num_images = 1
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height() + 20)

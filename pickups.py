"""
Pickups system for health and ammo.
"""
import pygame as pg
from settings import *
import math


class Pickup:
    def __init__(self, game, pos, pickup_type):
        self.game = game
        self.x, self.y = pos
        self.type = pickup_type  # 'health' or 'ammo'
        self.collected = False
        self.size = 0.3
        self.animation_time = 200
        self.animation_time_prev = pg.time.get_ticks()
        self.angle = 0
        
        if self.type == 'health':
            self.value = 25
            self.color = (255, 50, 50)
        else:  # ammo
            self.value = 20
            self.color = (255, 200, 50)
    
    def check_pickup(self):
        if self.collected:
            return
        
        player = self.game.player
        dx = self.x - player.x
        dy = self.y - player.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < 0.6:  # Pickup range
            self.collected = True
            if self.type == 'health':
                player.health = min(PLAYER_MAX_HEALTH, player.health + self.value)
                self.game.sound.npc_pain.play()  # Reuse sound
            else:  # ammo
                player.ammo = min(player.max_ammo, player.ammo + self.value)
                self.game.sound.shotgun.play()  # Reuse sound
    
    def update(self):
        self.check_pickup()
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.angle += 0.2
    
    def get_sprite_projection(self):
        if self.collected:
            return None
        
        dx = self.x - self.game.player.x
        dy = self.y - self.game.player.y
        
        theta = math.atan2(dy, dx)
        delta = theta - self.game.player.angle
        
        if (dx > 0 and self.game.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau
        
        delta_rays = delta / DELTA_ANGLE
        screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        
        dist = math.sqrt(dx * dx + dy * dy)
        if -5 <= delta_rays <= NUM_RAYS + 5 and dist > 0.5:
            proj_height = min(int(SCREEN_DIST / dist * self.size * 200), 2 * HEIGHT)
            half_proj_height = proj_height // 2
            
            # Create simple colored square as pickup sprite
            surface = pg.Surface((proj_height, proj_height), pg.SRCALPHA)
            pg.draw.circle(surface, self.color, (half_proj_height, half_proj_height), half_proj_height)
            pg.draw.circle(surface, (255, 255, 255), (half_proj_height, half_proj_height), half_proj_height // 2)
            
            return (dist, surface, (screen_x - half_proj_height, HALF_HEIGHT - half_proj_height))
        return None


class PickupHandler:
    def __init__(self, game):
        self.game = game
        self.pickups = []
        self.spawn_pickups()
    
    def spawn_pickups(self):
        # Health packs
        health_positions = [(3.5, 3.5), (8.5, 8.5), (12.5, 3.5), (3.5, 15.5), (14.5, 20.5)]
        for pos in health_positions:
            self.pickups.append(Pickup(self.game, pos, 'health'))
        
        # Ammo crates
        ammo_positions = [(5.5, 5.5), (10.5, 10.5), (7.5, 15.5), (12.5, 18.5)]
        for pos in ammo_positions:
            self.pickups.append(Pickup(self.game, pos, 'ammo'))
    
    def update(self):
        for pickup in self.pickups:
            pickup.update()
    
    def get_sprites_to_render(self):
        sprites = []
        for pickup in self.pickups:
            if not pickup.collected:
                sprite_proj = pickup.get_sprite_projection()
                if sprite_proj:
                    sprites.append(sprite_proj)
        return sprites

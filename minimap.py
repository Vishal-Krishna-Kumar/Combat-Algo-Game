"""
Minimap system to show player position and enemies.
"""
import pygame as pg
from settings import *
import math


class Minimap:
    def __init__(self, game):
        self.game = game
        self.size = 220
        self.scale = 12
        self.position = (WIDTH - self.size - 10, 10)
        self.bg_color = (20, 20, 20, 220)
        self.wall_color = (80, 80, 80)
        self.player_color = (0, 255, 0)
        self.enemy_color = (255, 0, 0)
        self.surface = pg.Surface((self.size, self.size), pg.SRCALPHA)
    
    def draw(self):
        self.surface.fill(self.bg_color)
        
        # Draw walls
        for (x, y) in self.game.map.world_map:
            map_x = int((x - self.game.player.x + self.size // self.scale // 2) * self.scale)
            map_y = int((y - self.game.player.y + self.size // self.scale // 2) * self.scale)
            if 0 <= map_x < self.size and 0 <= map_y < self.size:
                pg.draw.rect(self.surface, self.wall_color, (map_x, map_y, self.scale, self.scale))
        
        # Draw enemies ONLY (not decorative sprites)
        for npc in self.game.object_handler.npc_list:
            if npc.alive:
                map_x = int((npc.x - self.game.player.x + self.size // self.scale // 2) * self.scale)
                map_y = int((npc.y - self.game.player.y + self.size // self.scale // 2) * self.scale)
                if 0 <= map_x < self.size and 0 <= map_y < self.size:
                    # Draw larger red dot for enemies
                    pg.draw.circle(self.surface, self.enemy_color, (map_x, map_y), 5)
                    # Add red outline for visibility
                    pg.draw.circle(self.surface, (255, 100, 100), (map_x, map_y), 5, 1)
        
        # Draw player (center) - larger and more visible
        player_x = self.size // 2
        player_y = self.size // 2
        # Draw white outline first
        pg.draw.circle(self.surface, (255, 255, 255), (player_x, player_y), 8, 2)
        # Draw green player dot
        pg.draw.circle(self.surface, self.player_color, (player_x, player_y), 7)
        
        # Draw player direction line - thicker and brighter
        dir_len = 20
        end_x = player_x + int(math.cos(self.game.player.angle) * dir_len)
        end_y = player_y + int(math.sin(self.game.player.angle) * dir_len)
        pg.draw.line(self.surface, (255, 255, 255), (player_x, player_y), (end_x, end_y), 3)
        
        # Border
        pg.draw.rect(self.surface, (200, 200, 200), (0, 0, self.size, self.size), 2)
        
        self.game.screen.blit(self.surface, self.position)

import pygame as pg
from settings import *


class UIButton:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), text_color=(255, 255, 255)):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False
        self.font = pg.font.SysFont('consolas', 16)

    def draw(self, surface):
        color = (150, 150, 150) if self.hovered else self.color
        pg.draw.rect(surface, color, self.rect)
        pg.draw.rect(surface, (200, 200, 200), self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        self.ui_font = pg.font.SysFont('consolas', 26)
        self.shake_intensity = 0  # Screen shake effect
        
        # Player sprites for TPS
        self.player_sprites = {}
        try:
            self.player_sprites['idle'] = self.get_texture('resources/sprites/player/idle.png', (96, 96))
            self.player_sprites['walk'] = self.get_texture('resources/sprites/player/walk.png', (96, 96))
            self.player_sprites['run'] = self.get_texture('resources/sprites/player/run.png', (96, 96))
            self.player_sprites['shoot'] = self.get_texture('resources/sprites/player/shoot.png', (96, 96))
        except:
            self.player_sprites = {}
        
        # FPS/TPS Toggle Button
        self.tps_button = UIButton(WIDTH - 140, HEIGHT - 50, 130, 40, 'FPS/TPS')

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_crosshair()
        self.draw_reload_indicator()
        self.draw_damage_indicators()


    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))
        
        # Ammo display
        ammo_font = pg.font.SysFont('consolas', 36, bold=True)
        ammo_text = ammo_font.render(f'AMMO: {self.game.player.ammo}', True, (255, 200, 50))
        self.screen.blit(ammo_text, (WIDTH - 220, 10))
        
        # Kills counter
        kills_text = ammo_font.render(f'KILLS: {self.game.player.kills}', True, (255, 100, 100))
        self.screen.blit(kills_text, (WIDTH - 220, 55))
        
        # Stamina bar
        self.draw_stamina_bar()
        
        # Weapon ammo count for current weapon
        # self.draw_weapon_ammo()

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))
        self.shake_intensity = 8  # Trigger screen shake

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    def draw_crosshair(self):
        cx, cy = HALF_WIDTH, HALF_HEIGHT
        size = CROSSHAIR_SIZE
        thickness = CROSSHAIR_THICKNESS
        color = CROSSHAIR_COLOR
        pg.draw.line(self.screen, color, (cx - size, cy), (cx + size, cy), thickness)
        pg.draw.line(self.screen, color, (cx, cy - size), (cx, cy + size), thickness)

    def draw_reload_indicator(self):
        weapon = self.game.weapon
        if not weapon.reloading:
            return
        bar_w, bar_h = RELOAD_BAR_SIZE
        x = HALF_WIDTH - bar_w // 2
        y = HEIGHT - bar_h - 24
        pg.draw.rect(self.screen, RELOAD_BAR_BG_COLOR, (x, y, bar_w, bar_h))
        progress = weapon.reload_progress
        pg.draw.rect(self.screen, RELOAD_BAR_COLOR, (x, y, int(bar_w * progress), bar_h))
        if self.ui_font:
            label = self.ui_font.render('RELOADING', True, RELOAD_BAR_COLOR)
            self.screen.blit(label, (x, y - label.get_height() - 6))
    
    def draw_damage_indicators(self):
        """Draw red arrows showing damage direction."""
        for angle, _ in self.game.player.damage_indicators:
            # Calculate arrow position on screen edge
            relative_angle = angle - self.game.player.angle
            arrow_dist = 150
            arrow_x = HALF_WIDTH + int(math.cos(relative_angle) * arrow_dist)
            arrow_y = HALF_HEIGHT + int(math.sin(relative_angle) * arrow_dist)
            
            # Draw red arrow
            arrow_size = 20
            end_x = arrow_x + int(math.cos(relative_angle) * arrow_size)
            end_y = arrow_y + int(math.sin(relative_angle) * arrow_size)
            pg.draw.line(self.screen, (255, 0, 0), (arrow_x, arrow_y), (end_x, end_y), 4)
            
            # Arrow head
            left_angle = relative_angle + 2.8
            right_angle = relative_angle - 2.8
            pg.draw.line(self.screen, (255, 0, 0), (end_x, end_y),
                        (end_x + int(math.cos(left_angle) * 10), end_y + int(math.sin(left_angle) * 10)), 4)
            pg.draw.line(self.screen, (255, 0, 0), (end_x, end_y),
                        (end_x + int(math.cos(right_angle) * 10), end_y + int(math.sin(right_angle) * 10)), 4)
    
    def draw_weapon_ammo(self):
        """Show ammo count for current weapon."""
        ammo_font = pg.font.SysFont('consolas', 24, bold=True)
        ammo_per_mag = self.game.weapon_manager.current_weapon.ammo_per_mag
        ammo_text = ammo_font.render(f'{self.game.player.ammo}/{ammo_per_mag}', True, (150, 200, 255))
        self.screen.blit(ammo_text, (HALF_WIDTH - ammo_text.get_width() // 2, HEIGHT - 90))
    
    def draw_stamina_bar(self):
        """Draw stamina/sprint bar on left side."""
        stamina_pct = self.game.player.stamina / STAMINA_MAX
        bar_width = 200
        bar_height = 15
        x, y = 10, HEIGHT - 50
        
        # Background
        pg.draw.rect(self.screen, (50, 50, 50), (x, y, bar_width, bar_height))
        
        # Stamina color: green when full, yellow when medium, red when low
        if stamina_pct > 0.5:
            color = (100, 255, 100)
        elif stamina_pct > 0.2:
            color = (255, 255, 100)
        else:
            color = (255, 100, 100)
        
        # Fill bar
        pg.draw.rect(self.screen, color, (x, y, int(bar_width * stamina_pct), bar_height))
        
        # Border
        pg.draw.rect(self.screen, (200, 200, 200), (x, y, bar_width, bar_height), 2)
        
        # Label
        label_font = pg.font.SysFont('consolas', 14)
        label = label_font.render('STAMINA', True, (200, 200, 200))
        self.screen.blit(label, (x, y - 20))

    def draw_tps_avatar(self):
        """Draw player avatar from behind in TPS mode (clean, simple)."""
        player = self.game.player
        weapon = self.game.weapon
        
        # Only show in TPS mode
        if not player.is_tps:
            return
        
        # Select sprite based on state
        if weapon.reloading:
            sprite_key = 'shoot'
        elif player.is_sprinting:
            sprite_key = 'run'
        elif pg.key.get_pressed()[pg.K_w] or pg.key.get_pressed()[pg.K_UP] or \
             pg.key.get_pressed()[pg.K_s] or pg.key.get_pressed()[pg.K_DOWN]:
            sprite_key = 'walk'
        else:
            sprite_key = 'idle'
        
        if sprite_key not in self.player_sprites:
            return
            
        sprite = self.player_sprites[sprite_key]
        sprite_scale = 3.5
        scaled_sprite = pg.transform.scale(sprite, 
                                           (int(sprite.get_width() * sprite_scale), 
                                            int(sprite.get_height() * sprite_scale)))
        
        # Position at bottom-center
        avatar_x = WIDTH // 2 - scaled_sprite.get_width() // 2
        avatar_y = HEIGHT - scaled_sprite.get_height() - 5
        
        # Draw character only - clean view
        self.screen.blit(scaled_sprite, (avatar_x, avatar_y))
        
        # Simple health display at bottom-left (away from character)
        hp_font = pg.font.SysFont('consolas', 18)
        hp_text = hp_font.render(f'HP: {player.health}  Stamina: {int(player.stamina)}', 
                                 True, (255, 100, 100))
        self.screen.blit(hp_text, (10, HEIGHT - 35))

    def draw_ui_buttons(self):
        """Draw FPS/TPS toggle button."""
        mouse_pos = pg.mouse.get_pos()
        self.tps_button.update(mouse_pos)
        self.tps_button.draw(self.screen)

    def draw_mode_indicator(self):
        """Show current mode in corner."""
        if self.game.player.is_tps:
            mode_font = pg.font.SysFont('consolas', 18)
            mode_surf = mode_font.render('MODE: TPS', True, (100, 200, 255))
            self.screen.blit(mode_surf, (10, 10))

    def draw_v_key_hint(self):
        """Show V key hint for toggling FPS/TPS."""
        if not self.game.player.is_tps:
            hint_font = pg.font.SysFont('consolas', 16)
            hint_text = hint_font.render('Press V to toggle FPS/TPS', True, (150, 150, 150))
            self.screen.blit(hint_text, (10, HEIGHT - 35))

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }

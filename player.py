from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()
        # diagonal movement correction
        self.diag_move_corr = 1 / math.sqrt(2)
        self.stamina = STAMINA_MAX
        self.is_sprinting = False
        self.is_crouching = False
        self.ammo = 75  # Increased from 50
        self.max_ammo = 150  # Increased from 100
        self.kills = 0
        self.damage_indicators = []  # List of (angle, time)
        self.melee_cooldown = 0
        self.melee_damage = 75

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        # Add damage indicator from attacking NPC
        for npc in self.game.object_handler.npc_list:
            if npc.alive and npc.attack_dist > 0:
                dx = npc.x - self.x
                dy = npc.y - self.y
                angle = math.atan2(dy, dx)
                self.damage_indicators.append((angle, pg.time.get_ticks()))
                break
        self.check_game_over()

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading and self.ammo > 0:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True
                self.ammo -= 1
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if not self.shot and not self.game.weapon.reloading and self.ammo > 0:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True
                self.ammo -= 1
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        crouch = keys[pg.K_LCTRL] or keys[pg.K_RCTRL]
        sprint_input = (keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]) and not crouch and self.stamina > 1
        num_key_pressed = -1
        if keys[pg.K_w] or keys[pg.K_UP]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        speed_factor = 1.0
        if crouch:
            speed_factor *= PLAYER_CROUCH_MULT
            self.is_crouching = True
        else:
            self.is_crouching = False

        if sprint_input and num_key_pressed >= 0:
            speed_factor *= PLAYER_SPRINT_MULT
            self.is_sprinting = True
        else:
            self.is_sprinting = False

        if speed_factor != 1.0:
            dx *= speed_factor
            dy *= speed_factor

        # diag move correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        collider_scale = PLAYER_CROUCH_COLLIDER_SCALE if self.is_crouching else 1.0
        self.check_wall_collision(dx, dy, collider_scale)
        self.update_stamina(self.is_sprinting and num_key_pressed >= 0)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy, collider_scale=1.0):
        scale = (PLAYER_SIZE_SCALE * collider_scale) / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update_stamina(self, sprinting):
        if sprinting:
            self.stamina = max(0, self.stamina - STAMINA_DRAIN_RATE * self.game.delta_time)
        else:
            self.stamina = min(STAMINA_MAX, self.stamina + STAMINA_RECOVER_RATE * self.game.delta_time)
    
    def melee_attack(self):
        if self.melee_cooldown > 0:
            return
        self.melee_cooldown = 500  # 500ms cooldown
        self.game.sound.shotgun.play()  # Reuse sound
        
        # Check for nearby enemies
        for npc in self.game.object_handler.npc_list:
            if npc.alive:
                dx = npc.x - self.x
                dy = npc.y - self.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < 1.5:  # Melee range
                    npc.health -= self.melee_damage
                    npc.pain = True
                    self.game.sound.npc_pain.play()
                    npc.check_health()

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()
        if self.melee_cooldown > 0:
            self.melee_cooldown -= self.game.delta_time
        # Update damage indicators
        current_time = pg.time.get_ticks()
        self.damage_indicators = [(angle, time) for angle, time in self.damage_indicators 
                                  if current_time - time < 1000]

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
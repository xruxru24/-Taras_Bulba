from random import choice
import pygame
import expansion
import Engine


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (84, 116))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = 0.05
        self.max_speed = 0.6
        self.friction = 0.1
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.hp = 100
        self.dash_distance = 150
        self.dash_cooldown_time = 2
        self.dash_cooldown = 0
        self.is_dashing = False
        self.weapon = weapon

    def run(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_speed -= self.acceleration
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_speed += self.acceleration
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_speed -= self.acceleration
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_speed += self.acceleration
        if keys[pygame.K_LEFT]:
            Engine.eng.damage_collides(self.weapon, 'left', self, creepe_group)
        elif keys[pygame.K_RIGHT]:
            Engine.eng.damage_collides(self.weapon, 'right', self, creepe_group)
        elif keys[pygame.K_UP]:
            Engine.eng.damage_collides(self.weapon, 'up', self, creepe_group)
        elif keys[pygame.K_DOWN]:
            Engine.eng.damage_collides(self.weapon, 'down', self, creepe_group)

        self.x_speed = max(-self.max_speed, min(self.x_speed, self.max_speed))
        self.y_speed = max(-self.max_speed, min(self.y_speed, self.max_speed))

        if not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.x_speed *= self.friction
        if not (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.y_speed *= self.friction

        if keys[pygame.K_SPACE] and self.dash_cooldown <= 0 and not self.is_dashing:
            self.is_dashing = True
            self.dash_cooldown = self.dash_cooldown_time
            if self.x_speed > 0:
                self.pos_x += self.dash_distance
            elif self.x_speed < 0:
                self.pos_x -= self.dash_distance
            elif self.y_speed > 0:
                self.pos_y += self.dash_distance
            elif self.y_speed < 0:
                self.pos_y -= self.dash_distance
            else:
                self.pos_x += self.dash_distance

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1 / expansion.FPS
        if self.is_dashing:
            self.is_dashing = False

        self.pos_x += self.x_speed
        self.pos_y += self.y_speed

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        self.rect.clamp_ip(expansion.SCREEN.get_rect())
        self.weapon.move(*self.get_position())

    def get_position(self):
        return self.rect.centerx, self.rect.centery


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, speed, acceleration, friction, hp, weapon):
        super().__init__(creepe_group, all_sprites)
        self.weapon = weapon
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = acceleration
        self.max_speed = speed
        self.friction = friction
        self.player = None
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.hp = hp

    def set_player(self, player):
        self.player = player

    def update(self):
        if self.player:
            player_x, player_y = self.player.get_position()
            dx = player_x - self.rect.centerx
            dy = player_y - self.rect.centery

            self.move_logic(dx, dy)

            self.x_speed = max(-self.max_speed, min(self.x_speed, self.max_speed))
            self.y_speed = max(-self.max_speed, min(self.y_speed, self.max_speed))

            self.pos_x += self.x_speed
            self.pos_y += self.y_speed

            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)
            self.rect.clamp_ip(expansion.SCREEN.get_rect())

    def move_logic(self, dx, dy):
        if dx > 0:
            self.x_speed += self.acceleration
        if dx < 0:
            self.x_speed -= self.acceleration
        if dy > 0:
            self.y_speed += self.acceleration
        if dy < 0:
            self.y_speed -= self.acceleration


class SwordMan(Enemy):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(pos_x, pos_y, sword_man, 0.6, 0.005, 0.8, 100, weapon)


class Archer(Enemy):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(pos_x, pos_y, sword_man, 0.3, 0.005, 0.8, 1, weapon)

    def move_logic(self, dx, dy):
        screen_rect = expansion.SCREEN.get_rect()

        if abs(dx) > 500:
            if dx > 0:
                self.x_speed += self.acceleration
            if dx < 0:
                self.x_speed -= self.acceleration
        elif 500 > abs(dx) > 0:
            if dx > 0:
                self.x_speed -= self.acceleration
            if dx < 0:
                self.x_speed += self.acceleration
        if abs(dy) > 500:
            if dy > 0:
                self.y_speed += self.acceleration
            if dy < 0:
                self.y_speed -= self.acceleration
        elif 500 > abs(dy) > 0:
            if dy > 0:
                self.y_speed -= self.acceleration
            if dy < 0:
                self.y_speed += self.acceleration

        if self.rect.left < screen_rect.left:
            self.x_speed = abs(self.x_speed)
            self.pos_x = screen_rect.left
        elif self.rect.right > screen_rect.right:
            self.x_speed = -abs(self.x_speed)
            self.pos_x = screen_rect.right - self.rect.width
        if self.rect.top < screen_rect.top:
            self.y_speed = abs(self.y_speed)
            self.pos_y = screen_rect.top
        elif self.rect.bottom > screen_rect.bottom:
            self.y_speed = -abs(self.y_speed)
            self.pos_y = screen_rect.bottom - self.rect.height

class PigMan(Enemy):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(pos_x, pos_y, pig_man, 0.4, 0.001, 0.8, 12000, weapon)


class Boss(Enemy):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(pos_x, pos_y, pig_man, 0.4, 0.001, 0.8, 12000, weapon)
        self.teleport_cooldown = 0
        self.teleport_cooldown_time = 3
        self.is_teleporting = False

    def update(self):
        super().update()
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1 / expansion.FPS
        self.teleport()

    def teleport(self):
        if self.teleport_cooldown <= 0 and not self.is_teleporting:
            self.is_teleporting = True
            self.teleport_cooldown = self.teleport_cooldown_time
            direction = choice(['up', 'down', 'left', 'right'])

            teleport_distance = 150

            new_x = self.pos_x
            new_y = self.pos_y

            if direction == 'up':
                new_y -= teleport_distance
            elif direction == 'down':
                new_y += teleport_distance
            elif direction == 'left':
                new_x -= teleport_distance
            elif direction == 'right':
                new_x += teleport_distance

            screen_rect = expansion.SCREEN.get_rect()

            new_x = max(screen_rect.left, min(new_x, screen_rect.right - self.rect.width))
            new_y = max(screen_rect.top, min(new_y, screen_rect.bottom - self.rect.height))

            self.pos_x = new_x
            self.pos_y = new_y

            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)
        if self.is_teleporting:
            self.is_teleporting = False



player_image = expansion.load_image('taras.png', -1)
sword_man = expansion.load_image('swordsman.png', -1)
pig_man = expansion.load_image('pigman.png', -1)
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
creepe_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
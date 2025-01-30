from random import choice

import pygame

from Engine import eng


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
        self.money = 0
        self.dash_distance = 150
        self.dash_cooldown_time = 2
        self.dash_cooldown = 0
        self.is_dashing = False
        self.weapon = weapon
        self.last_button = None

    def run(self, keys, mb_down):
        '''
        Метод реализует движение игрока
        '''
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_speed -= self.acceleration
            self.last_button = pygame.K_LEFT
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_speed += self.acceleration
            self.last_button = pygame.K_RIGHT
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_speed -= self.acceleration
            self.last_button = pygame.K_UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_speed += self.acceleration
            self.last_button = pygame.K_DOWN
        if self.last_button == pygame.K_LEFT and mb_down:
            eng.damage_collides(self.weapon, 'left', self, creepe_group, False, False, self)
        elif self.last_button == pygame.K_RIGHT and mb_down:
            eng.damage_collides(self.weapon, 'right', self, creepe_group, False, False, self)
        elif self.last_button == pygame.K_UP and mb_down:
            eng.damage_collides(self.weapon, 'up', self, creepe_group, False, False, self)
        elif self.last_button == pygame.K_DOWN and mb_down:
            eng.damage_collides(self.weapon, 'down', self, creepe_group, False, False, self)

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
                if self.pos_x + self.dash_distance >= 1750:
                    self.pos_x = 1750
                else:
                    self.pos_x += self.dash_distance
            elif self.x_speed < 0:
                if self.pos_x - self.dash_distance <= 0:
                    self.pos_x = 40
                else:
                    self.pos_x -= self.dash_distance
            elif self.y_speed > 0:
                if self.pos_y + self.dash_distance >= 900:
                    self.pos_y = 900
                else:
                    self.pos_y += self.dash_distance
            elif self.y_speed < 0:
                if self.pos_y - self.dash_distance <= 0:
                    self.pos_y = 40
                else:
                    self.pos_y -= self.dash_distance
            else:
                if self.pos_x - self.dash_distance <= 0:
                    self.pos_x = 30
                else:
                    self.pos_x -= self.dash_distance

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1 / FPS
        if self.is_dashing:
            self.is_dashing = False

        self.pos_x += self.x_speed
        self.pos_y += self.y_speed

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        self.rect.clamp_ip(SCREEN.get_rect())
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
        '''
        Отслеживание игрока крипами
        '''
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
            self.rect.clamp_ip(SCREEN.get_rect())
            self.weapon.move(self.rect.x, self.rect.y)

    def move_logic(self, dx, dy):
        '''
        Метод реализующий атаки крипов
        '''
        if dx > 30:
            self.x_speed += self.acceleration
        if dx < -30:
            self.x_speed -= self.acceleration
        if dy > 30:
            self.y_speed += self.acceleration
        if dy < -30:
            self.y_speed -= self.acceleration

        attack_range = 25

        if not hasattr(self, 'attacked'):
            self.attacked = False

        if abs(dx) > attack_range or abs(dy) > attack_range:
            if not self.attacked and not self.weapon.reloads:
                if abs(dx) > abs(dy):
                    if dx > attack_range:
                        eng.damage_collides(self.weapon, 'right', self, player_group, False, False, self.player)
                    elif dx < -attack_range:
                        eng.damage_collides(self.weapon, 'left', self, player_group, False, False, self.player)
                else:
                    if dy > attack_range:
                        eng.damage_collides(self.weapon, 'down', self, player_group, False, False, self.player)
                    elif dy < -attack_range:
                        eng.damage_collides(self.weapon, 'up', self, player_group, False, False, self.player)
                self.weapon.reloads = True
                self.attacked = True
        else:
            self.attacked = False


class SwordMan(Enemy):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(pos_x, pos_y, sword_man, 0.4, 0.005, 0.8, 100, weapon)


class Archer(Enemy):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(pos_x, pos_y, archer, 0.3, 0.005, 0.8, 1, weapon)

    def move_logic(self, dx, dy):
        screen_rect = SCREEN.get_rect()

        if abs(dx) > 300:
            if dx > 0:
                self.x_speed += self.acceleration
            if dx < 0:
                self.x_speed -= self.acceleration
        elif 500 > abs(dx) > 0:
            if dx > 0:
                self.x_speed -= self.acceleration
            if dx < 0:
                self.x_speed += self.acceleration
        if abs(dy) > 300:
            if dy > 0:
                self.y_speed += self.acceleration
            if dy < 0:
                self.y_speed -= self.acceleration
        elif 300 > abs(dy) > 0:
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

        attack_range = 300
        from Weapons import Arrow

        if abs(dx) > attack_range or abs(dy) > attack_range:
            if not self.weapon.reloads:
                b_x, b_y = int(self.pos_x), int(self.pos_y)
                p_x, p_y = self.player.get_position()
                Arrow(b_x, b_y, p_x, p_y, self.player)
                self.weapon.reloads = True


class General(Enemy):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(pos_x, pos_y, gener, 0.4, 0.001, 0.8, 400, weapon)
        self.teleport_cooldown = 0
        self.teleport_cooldown_time = 3
        self.is_teleporting = False

    from expansion import FPS, SCREEN

    def update(self):
        super().update()
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1 / FPS
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
            screen_rect = SCREEN.get_rect()
            new_x = max(screen_rect.left, min(new_x, screen_rect.right - self.rect.width))
            new_y = max(screen_rect.top, min(new_y, screen_rect.bottom - self.rect.height))
            self.pos_x = new_x
            self.pos_y = new_y
            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)
        if self.is_teleporting:
            self.is_teleporting = False


class Andrey(Enemy):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(pos_x, pos_y, andr, 0.4, 0.001, 0.8, 1500, weapon)
        self.rage_cooldown = 6000
        self.rage_duration = 1800
        self.rage_flag = False

    def move_logic(self, dx, dy):
        if dx > 30:
            self.x_speed += self.acceleration
        if dx < -30:
            self.x_speed -= self.acceleration
        if dy > 30:
            self.y_speed += self.acceleration
        if dy < -30:
            self.y_speed -= self.acceleration

        attack_range = 50

        if not hasattr(self, 'attacked'):
            self.attacked = False

        if abs(dx) > attack_range or abs(dy) > attack_range:
            if not self.attacked and not self.weapon.reloads:
                if abs(dx) > abs(dy):
                    if dx > attack_range:
                        eng.damage_collides(self.weapon, 'right', self, player_group, False, False, self.player)
                    elif dx < -attack_range:
                        eng.damage_collides(self.weapon, 'left', self, player_group, False, False, self.player)
                else:
                    if dy > attack_range:
                        eng.damage_collides(self.weapon, 'down', self, player_group, False, False, self.player)
                    elif dy < -attack_range:
                        eng.damage_collides(self.weapon, 'up', self, player_group, False, False, self.player)
                self.weapon.reloads = True
                self.attacked = True
        else:
            self.attacked = False

    def rage(self):
        self.x_speed *= 2
        self.y_speed *= 2
        self.acceleration *= 2
        self.max_speed *= 2
        self.friction *= 2
        self.attacked *= 2
        self.rage_flag = True
        self.rage_duration = 3000
        print(1)

    def unrage(self):
        self.x_speed /= 2
        self.y_speed /= 2
        self.acceleration /= 2
        self.max_speed /= 2
        self.friction /= 2
        self.attacked /= 2
        self.rage_flag = False
        self.rage_cooldown = 6000
        print(2)


class PigMan(Enemy):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(pos_x, pos_y, pig_man, 0.1, 0.001, 0.8, 3000, weapon)

    def move_logic(self, dx, dy):
        if dx > 30:
            self.x_speed += self.acceleration
        if dx < -30:
            self.x_speed -= self.acceleration
        if dy > 30:
            self.y_speed += self.acceleration
        if dy < -30:
            self.y_speed -= self.acceleration

        attack_range = 50

        if not hasattr(self, 'attacked'):
            self.attacked = False

        if abs(dx) > attack_range or abs(dy) > attack_range:
            if not self.attacked and not self.weapon.reloads:
                if abs(dx) > abs(dy):
                    if dx > attack_range:
                        eng.damage_collides(self.weapon, 'right', self, player_group, False, False, self.player)
                    elif dx < -attack_range:
                        eng.damage_collides(self.weapon, 'left', self, player_group, False, False, self.player)
                else:
                    if dy > attack_range:
                        eng.damage_collides(self.weapon, 'down', self, player_group, False, False, self.player)
                    elif dy < -attack_range:
                        eng.damage_collides(self.weapon, 'up', self, player_group, False, False, self.player)
                self.weapon.reloads = True
                self.attacked = True
        else:
            self.attacked = False


from expansion import FPS, SCREEN, load_image

player_image = load_image('taras.png', -1)
sword_man = load_image('swordsman.png')
archer = load_image('Archer.png')
gener = pygame.transform.scale(load_image('General.png'), (160, 305))
andr = load_image('Andrey.png')
pig_man = pygame.transform.scale(load_image('pigman.png', -1), (200, 200))
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
creepe_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()

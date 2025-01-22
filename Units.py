import sys
import os
import pygame
import expansion



class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(expansion.player_group, expansion.all_sprites)
        self.image = pygame.transform.scale(expansion.player_image, (84, 116))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = 0.1
        self.max_speed = 1
        self.friction = 0.9

    def run(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_speed -= self.acceleration
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_speed += self.acceleration
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_speed -= self.acceleration
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_speed += self.acceleration

        self.x_speed = max(-self.max_speed, min(self.x_speed, self.max_speed))
        self.y_speed = max(-self.max_speed, min(self.y_speed, self.max_speed))

        if not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.x_speed *= self.friction
        if not (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.y_speed *= self.friction

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.rect.clamp_ip(expansion.SCREEN.get_rect())

    def get_position(self):
        return self.rect.centerx, self.rect.centery


class SwordMan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(expansion.creepe_group, expansion.all_sprites)
        self.image = expansion.sword_man
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = 0.01
        self.max_speed = 1
        self.friction = 0.9
        self.player = None

    def set_player(self, player):
        self.player = player

    def update(self):
        if self.player:
            player_x, player_y = self.player.get_position()
            dx = player_x - self.rect.centerx
            dy = player_y - self.rect.centery
            if dx > 0:
                self.x_speed += self.acceleration
            if dx < 0:
                self.x_speed -= self.acceleration
            if dy > 0:
                self.y_speed += self.acceleration
            if dy < 0:
                self.y_speed -= self.acceleration
            self.x_speed = max(-self.max_speed, min(self.x_speed, self.max_speed))
            self.y_speed = max(-self.max_speed, min(self.y_speed, self.max_speed))
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed
            self.rect.clamp_ip(expansion.SCREEN.get_rect())

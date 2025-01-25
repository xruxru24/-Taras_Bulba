import pygame
import time
import expansion
from expansion import load_image


class Weapon(pygame.sprite.Sprite):
    def __init__(self, image, koeff_x, koeff_y):
        super().__init__(expansion.weapon_group, expansion.all_sprites)

        self.image = image
        self.rect = self.image.get_rect()
        self.damage = 0
        self.attack_distance = 0
        self.reload = 0

        self.koeff_x, self.koeff_y = koeff_x, koeff_y

    def move(self, player_x, player_y):
        self.rect.move(player_x - self.rect.x - self.koeff_x, player_y - self.rect.y - self.koeff_y)


class CavalrySword(Weapon):
    def __init__(self):
        self.image = pygame.transform.scale(expansion.load_image('CavalrySword.png'), (200, 200))

        self.damage = 25
        self.attack_distance = 60
        self.reload = 0.5

        self.koeff_y = 45
        self.koeff_x = 10
        super().__init__(self.image, self.koeff_x, self.koeff_y)


class Saber(Weapon):
    def __init__(self):
        self.image = pygame.transform.scale(expansion.load_image('Saber.png'), (150, 150))

        self.damage = 40
        self.attack_distance = 60
        self.reload = 0.7

        self.koeff_y = 45
        self.koeff_x = 10
        super().__init__(self.image, self.koeff_x, self.koeff_y)


class Dagger(Weapon):
    def __init__(self):
        self.image = pygame.transform.scale(expansion.load_image('Dagger.png'), (50, 50))

        self.damage = 20
        self.attack_distance = 30
        self.reload = 0.3

        self.koeff_y = 45
        self.koeff_x = 10
        super().__init__(self.image, self.koeff_x, self.koeff_y)


class Bow(Weapon):
    def __init__(self):
        self.image = pygame.transform.scale(expansion.load_image('Bow.png'), (150, 150))
        self.reload = 4

        self.koeff_y = 45
        self.koeff_x = 10
        super().__init__(self.image, self.koeff_x, self.koeff_y)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, bow_x, bow_y, player_x, player_y):
        super().__init__(expansion.weapon_group, expansion.all_sprites)

        self.image = pygame.transform.scale(expansion.load_image('Arrow.png'), (150, 150))
        self.rect = self.image.get_rect()
        self.damage = 100
        self.attack_distance = 540

        self.player_x, self.player_y = player_x, player_y
        self.rect.move_ip(bow_x, bow_y)


    def move(self, player_x, player_y):
        coeff_x = player_x // (player_y - self.rect.x)
        coeff_y = player_y // (player_y - self.rect.y)
        while self.rect.x != self.player_x and self.rect.y != self.player_y:
            time.sleep(0.01)
            self.rect.x -= coeff_x
            self.rect.y -= coeff_y
            self.rect.move_ip(self.rect.x, self.rect.y)

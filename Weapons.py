import pygame

from Units import weapon_group, all_sprites, arrow_group, creepe_group
from expansion import load_image


class Weapon(pygame.sprite.Sprite):
    def __init__(self, image, koeff_x, koeff_y, damage, attack_distance, reload):
        super().__init__(weapon_group, all_sprites)

        self.image = image
        self.rect = self.image.get_rect()
        self.damage = damage
        self.attack_distance = attack_distance
        self.reload = reload
        self.reloads = False
        self.cooldown = self.reload * 600

        self.koeff_x, self.koeff_y = koeff_x, koeff_y

    def move(self, player_x, player_y):
        self.rect.move_ip(player_x - self.rect.x - self.koeff_x, player_y - self.rect.y - self.koeff_y)


class CavalrySword(Weapon):
    def __init__(self):
        self.image = pygame.transform.scale(load_image('CavalrySword.png'), (100, 100))
        super().__init__(self.image, -5, 50, 25, 60, 1)


class Saber(Weapon):
    def __init__(self):
        self.image = pygame.transform.scale(load_image('Saber.png'), (150, 150))
        super().__init__(self.image, 10, 75, 40, 60, 1.3)


class Dagger(Weapon):
    def __init__(self):
        self.image = pygame.transform.scale(load_image('Dagger.png'), (50, 50))
        super().__init__(self.image, -10, 10, 20, 30, 0.5)


class Bow(Weapon):
    def __init__(self):
        self.image = pygame.transform.scale(load_image('Bow.png'), (125, 125))
        super().__init__(self.image, 25, 40, 0, 0, 4)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, bow_x, bow_y, player_x, player_y):
        super().__init__(arrow_group, all_sprites)

        from Engine import eng

        self.image = pygame.transform.scale(load_image('Arrow.png'), (150, 150))
        self.rect = self.image.get_rect()
        self.damage = 100
        self.attack_distance = 540
        self.bow_x = bow_x
        self.bow_y = bow_y
        self.x_speed = 0.4
        self.y_speed = 0.4

        self.player_x, self.player_y = player_x, player_y
        self.rect.move_ip(bow_x, bow_y)


    def update(self):

        self.bow_x += self.x_speed
        self.bow_y += self.y_speed

        from expansion import SCREEN

        self.rect.x = int(self.bow_x)
        self.rect.y = int(self.bow_y)
        self.rect.clamp_ip(SCREEN.get_rect())
        eng.damage_collides(Arrow, None, None, None, True)

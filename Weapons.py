import pygame

import expansion
from Units import weapon_group, all_sprites, arrow_group
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
    def __init__(self, bow_x, bow_y, player_x, player_y):
        super().__init__(arrow_group, all_sprites)

        self.image = pygame.transform.scale(load_image('Arrow.png'), (75, 75))
        self.rect = self.image.get_rect()
        self.damage = 100
        self.attack_distance = 540
        self.bow_x = bow_x
        self.bow_y = bow_y
        self.x_speed = 1
        self.y_speed = 1

        self.player_x, self.player_y = player_x, player_y
        self.rect.move_ip(bow_x, bow_y)


    def update(self):

        if self.bow_x + self.x_speed > expansion.WIDTH or self.bow_y + self.y_speed > expansion.HEIGHT:
            self.kill()

        else:
            if self.bow_x < self.player_x:
                self.bow_x += self.x_speed
            else:
                self.bow_x -= self.x_speed
            if self.bow_y < self.player_y:
                self.bow_y += self.y_speed
            else:
                self.bow_y -= self.y_speed

            from Engine import eng

            self.rect.move_ip(int(self.bow_x), int(self.bow_y))
            eng.damage_collides(self, None, None, None, True, False)

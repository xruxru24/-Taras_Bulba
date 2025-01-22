import pygame

from expansion import load_image


class Weapon:
    def __init__(self, image):
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.damage = 0
        self.attack_distance = 0
        self.reload = 0

    def move(self, player_x, player_y):
        self.rect.move(abs(player_x - self.rect.x), abs(player_y - self.rect.y))


class CavalrySword(Weapon):
    def __init__(self):
        self.damage = 25
        self.attack_distance = 60
        self.reload = 0.5
        super().__init__()


class Saber(Weapon):
    def __init__(self):
        self.damage = 40
        self.attack_distance = 60
        self.reload = 0.7
        super().__init__()


class Dagger(Weapon):
    def __init__(self):
        self.damage = 20
        self.attack_distance = 30
        self.reload = 0.3
        super().__init__()


class Bow(Weapon):
    def __init__(self):
        self.damage = 100
        self.attack_distance = 540
        self.reload = 4
        super().__init__()

import pygame

class Weapon:
    def __init__(self):
        self.damage = 0
        self.attack_distance = 0
        self.reload = 0

    def attack(self, unit_list):
        for i in unit_list:
            if i.rect.y == self.rect.y:
                if abs(self.rect.x - i.rect.x) <= self.attack_distance:
                    ''' ЛОГИКА НАНЕСЕНИЯ УРОНА '''
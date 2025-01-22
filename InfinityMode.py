import pygame, os, sys
from random import choices
from Units import Player, SwordMan, Archer
import expansion

class sale_spot:
    def __init__(self):
        self.items = {
            ''' РАЗНЫЕ ВЕЩИ, ДОБАВЛЮ КОГДА ДОДЕЛАЮ КЛАССЫ ОРУЖИЙ '''
        }
        self.assortment = {'''СПИСОК ВЕЩЕЙ КОТОРЫЕ СЕЙЧАС НАХОДЯТСЯ В МАГАЗИНЕ'''}

    def buy(self, elem, money, player_money):
        if player_money < money:
            return 'Недостаточно средств!'
        else:
            '''Логика списывания средств со счета персонажа'''
            self.assortment.pop(elem)
            if not self.assortment.items():
                self.update_inventory()
            return 'Удачно'

    def update_inventory(self):
        self.assortment.clear()
        for v, k in choices(self.items.items(), 3):
            self.assortment.append[v] = k


def infinity_game():
    run = True

    field_sprite = pygame.sprite.Group()
    field = pygame.sprite.Sprite()
    field.image = pygame.transform.scale(expansion.load_image('field.png'), (1920, 1080))
    field.rect = field.image.get_rect()
    field_sprite.add(field)

    sale_point_sprite = pygame.sprite.Group()
    sale_point = pygame.sprite.Sprite()
    sale_point.image = pygame.transform.scale(expansion.load_image('sale_point.png'), (400, 200))
    sale_point.rect = sale_point.image.get_rect().move(1000, 300)
    sale_point_sprite.add(sale_point)

    SALE_SPOT = sale_spot()
    player = Player(50, 50)
    swordman = Archer(300, 300)
    swordman.set_player(player)
    c = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        player.run(keys)
        expansion.player_group.update()
        expansion.all_sprites.update()
        field_sprite.draw(expansion.SCREEN)
        sale_point_sprite.draw(expansion.SCREEN)
        expansion.player_group.draw(expansion.SCREEN)
        expansion.creepe_group.draw(expansion.SCREEN)

        pygame.display.flip()

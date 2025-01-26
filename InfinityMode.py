import pygame, os, sys
from random import choices

from Units import creepe_group
from expansion import load_image, SCREEN, switching_waves
import Weapons
import Units

player = Units.Player(50, 50, Weapons.Saber())
font = pygame.font.SysFont('Comic Sans MS', 40)

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
    field.image = pygame.transform.scale(load_image('field.png'), (1920, 1080))
    field.rect = field.image.get_rect()
    field_sprite.add(field)

    sale_point_sprite = pygame.sprite.Group()
    sale_point = pygame.sprite.Sprite()
    sale_point.image = pygame.transform.scale(load_image('sale_point.png'), (400, 200))
    sale_point.rect = sale_point.image.get_rect().move(1000, 300)
    sale_point_sprite.add(sale_point)

    SALE_SPOT = sale_spot()
    switching_waves(1, 3)
    cur_wave = 0
    c = 0
    FLAG_WAVE_TIME = 6000
    wave_image = load_image('waves_1.png')

    while run:
        mb_down = False
        if FLAG_WAVE_TIME == 0:
            FLAG_WAVE_TIME = 6000
            cur_wave += 1
            switching_waves(cur_wave, 3)

        if len(creepe_group) == 0:
            SCREEN.blit(wave_image, (760, 200))
            num = font.render(str(cur_wave), False, '#880015')
            SCREEN.blit(num, (840, 220))
            pygame.display.flip()
            FLAG_WAVE_TIME -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mb_down = True

        keys = pygame.key.get_pressed()
        player.run(keys, mb_down)
        Units.player_group.update()
        Units.all_sprites.update()

        Units.weapon_group.update()
        field_sprite.draw(SCREEN)

        sale_point_sprite.draw(SCREEN)
        Units.player_group.draw(SCREEN)
        Units.creepe_group.draw(SCREEN)
        Units.weapon_group.draw(SCREEN)

        pygame.display.flip()

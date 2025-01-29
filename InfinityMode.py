import pygame, os, sys

import expansion
from Units import arrow_group
from Weapons import Dagger, Saber, CavalrySword, Arrow
from expansion import load_image, SCREEN, switching_waves
import Weapons
import Units

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 40)

class SaleSpot:
    def __init__(self):
        self.items = {Dagger: 15, Saber: 30, CavalrySword: 45}
        self.flag = False


    def update(self):
        '''
        Отрисовка лавки с оружием
        '''
        SCREEN.blit(load_image('sale_spot.png'), (550, 400))

    def buy(self, x, y):
        '''
        Логика покупок
        '''
        click_data = {(range(500, 722), range(575, 767)): CavalrySword,
            (range(723, 996), range(575, 767)): Dagger,
            (range(1000, 1200), range(575, 767)): Saber}

        s = 1000

        for i in click_data.keys():
            if x in i[0] and y in i[1]:
                if player.money <= self.items[click_data[i]]:
                    n = font.render('Недостаточно средств!', False, 'black')
                    while s != 0:
                        SCREEN.blit(n, (675, 400))
                        pygame.display.flip()
                        s -= 1
                else:
                    player.weapon.kill()
                    player.weapon = click_data[i]()
                    player.money -= self.items[click_data[i]]


def infinity_game():
    global player
    '''
    Метод реализации бесконечного режима
    '''
    run = True
    expansion.clear_groups(False)
    player = Units.Player(50, 50, Weapons.Saber())

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

    SALE_SPOT = SaleSpot()
    switching_waves(1, 3, player)
    cur_wave = 1
    FLAG_WAVE_TIME = 6000
    wave_image = load_image('waves_1.png')
    K_e_counter = 0

    while run:
        mb_down = False
        if FLAG_WAVE_TIME == 0:
            FLAG_WAVE_TIME = 6000
            cur_wave += 1
            switching_waves(cur_wave, 3, player)

        if player.weapon.reloads:
            if player.weapon.cooldown - 1 == 0:
                player.weapon.reloads = False
                player.weapon.cooldown = player.weapon.reload * 600
            player.weapon.cooldown -= 1

        for i in Units.weapon_group:
            if i.reloads:
                if i.cooldown - 1 == 0:
                    i.reloads = False
                    i.cooldown = i.reload * 600
                i.cooldown -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not SALE_SPOT.flag:
                if player.weapon.reloads:
                    mb_down = False
                else:
                    player.weapon.reloads = True
                    mb_down = True
            elif event.type == pygame.MOUSEBUTTONDOWN and SALE_SPOT.flag:
                SALE_SPOT.buy(*event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e \
                    and player.get_position()[0] in range(800, 1200) \
                    and player.get_position()[1] not in range(100, 500) and K_e_counter % 2 == 0:
                K_e_counter += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and K_e_counter % 2 != 0:
                K_e_counter += 1

        keys = pygame.key.get_pressed()
        player.run(keys, mb_down)

        Units.player_group.update()
        Units.all_sprites.update()
        Units.weapon_group.update()
        field_sprite.draw(SCREEN)

        Units.arrow_group.draw(SCREEN)
        Units.arrow_group.update()

        sale_point_sprite.draw(SCREEN)
        Units.player_group.draw(SCREEN)
        Units.creepe_group.draw(SCREEN)
        Units.weapon_group.draw(SCREEN)

        if len(Units.creepe_group) == 0:
            SCREEN.blit(wave_image, (760, 200))
            num = font.render(str(cur_wave), False, '#880015')
            SCREEN.blit(num, (940, 220))
            FLAG_WAVE_TIME -= 1

        hp = font.render(f'Health: {player.hp}', False, 'Red')
        SCREEN.blit(hp, (0, 950))

        cash = font.render(f'Money: {player.money}', False, 'Black')
        SCREEN.blit(cash, (0, 1000))

        fst = 400
        for i in ['Press to move: WASD', 'Press to attack: LMB', 'Press to dash: Space', 'Press to buy: E']:
            o = font.render(i, False, 'Black')
            fst += 100
            SCREEN.blit(o, (0, fst))


        if K_e_counter % 2 != 0 and FLAG_WAVE_TIME != 6000:
            SALE_SPOT.update()
            SALE_SPOT.flag = True
        elif K_e_counter % 2 == 0 or FLAG_WAVE_TIME == 6000:
            SALE_SPOT.flag = False
        elif K_e_counter % 2 != 0 and FLAG_WAVE_TIME == 6000:
            K_e_counter += 1

        if player.weapon.reloads:
            cooldown = font.render('Can not do it now!', False, 'Black')
            SCREEN.blit(cooldown, (1600, 900))

        pygame.display.flip()
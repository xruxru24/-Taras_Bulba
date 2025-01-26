import pygame, os, sys

from Units import creepe_group
from Weapons import Dagger, Saber, CavalrySword
from expansion import load_image, SCREEN, switching_waves
import Weapons
import Units

pygame.font.init()
player = Units.Player(50, 50, Weapons.Dagger())
font = pygame.font.SysFont('Comic Sans MS', 40)

class SaleSpot:
    def __init__(self):
        self.items = {Dagger: 15, Saber: 30, CavalrySword: 45}
        self.flag = False


    def update(self):
        SCREEN.blit(load_image('sale_spot.png'), (550, 400))

    def buy(self, x, y):
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

    SALE_SPOT = SaleSpot()
    switching_waves(1, 3)
    cur_wave = 1
    c = 0
    FLAG_WAVE_TIME = 6000
    wave_image = load_image('waves_1.png')
    K_e_counter = 0


    while run:
        mb_down = False
        if FLAG_WAVE_TIME == 0:
            FLAG_WAVE_TIME = 6000
            cur_wave += 1
            switching_waves(cur_wave, 3)

        if len(creepe_group) == 0:
            SCREEN.blit(wave_image, (760, 200))
            num = font.render(str(cur_wave), False, '#880015')
            SCREEN.blit(num, (940, 220))
            pygame.display.flip()
            FLAG_WAVE_TIME -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not SALE_SPOT.flag:
                mb_down = True
            elif event.type == pygame.MOUSEBUTTONDOWN and SALE_SPOT.flag:
                SALE_SPOT.buy(*event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and FLAG_WAVE_TIME != 6000 \
                and player.get_position()[0] in range(1000, 1200) and player.get_position()[1] in range(0, 500):
                K_e_counter += 1

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

        if K_e_counter % 2 != 0 and FLAG_WAVE_TIME != 6000:
            SALE_SPOT.update()
            SALE_SPOT.flag = True
        elif K_e_counter % 2 == 0 or FLAG_WAVE_TIME == 6000:
            SALE_SPOT.flag = False
        elif K_e_counter % 2 != 0 and FLAG_WAVE_TIME == 6000:
            K_e_counter += 1

        pygame.display.flip()

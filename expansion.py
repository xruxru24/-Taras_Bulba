import time

import pygame, os, sys
from random import randint, choice

SIZE = WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()
FPS = 60
wave = 1

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 40)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def switching_waves(cur_wave, creepe):

    from Units import creepe_group, SwordMan, Archer
    from Weapons import Saber, CavalrySword, Dagger, Bow
    from InfinityMode import player

    creepe = creepe * cur_wave

    for i in range(creepe):
        ch = randint(0, 1)
        if not ch:
            Sw_man = SwordMan(randint(100, WIDTH - 100), randint(100, HEIGHT - 100),
                                      choice([Dagger, Saber, CavalrySword])())
            Sw_man.set_player(player)
            creepe_group.add(Sw_man)
        else:
            Arc = Archer(randint(100, WIDTH - 100), randint(100, HEIGHT - 100), Bow())
            Arc.set_player(player)
            creepe_group.add(Arc)
    creepe_group.draw(SCREEN)
    creepe_group.update()
    pygame.display.flip()

def clear_groups(company):
    from Units import creepe_group, weapon_group, arrow_group, player_group

    for i in creepe_group:
        i.kill()

    for i in arrow_group:
        i.kill()
    if company:
        for i in player_group:
            i.kill()

        for i in weapon_group:
            i.kill()
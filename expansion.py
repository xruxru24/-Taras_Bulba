import pygame, os, sys
from random import randint, choice

SIZE = WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()
FPS = 500


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


def switching_waves(cur_wave, creepe, player):
    '''
    Функция для переключения волн в бесконечном режиме и спавна соотвествующего кол-ва крипов на карте.
    '''
    from Units import creepe_group, SwordMan, Archer
    from Weapons import Saber, CavalrySword, Dagger, Bow

    # подсчет крипов
    creepe = creepe * cur_wave

    for i in range(creepe):
        # логика создания крипов
        ch = randint(0, 1)
        if not ch:
            weap = choice([Dagger, Saber, CavalrySword])

            if weap is Dagger:
                koeff_x, koeff_y = -75, -50
            elif weap is Saber:
                koeff_x, koeff_y = -50, 10
            else:
                koeff_x, koeff_y = -75, 10

            sw_man = SwordMan(randint(100, WIDTH - 100), randint(100, HEIGHT - 100), weap(koeff_y, koeff_x))
            sw_man.set_player(player)
            creepe_group.add(sw_man)
        else:
            arc = Archer(randint(100, WIDTH - 100), randint(100, HEIGHT - 100), Bow(-25, -40))
            arc.set_player(player)
            creepe_group.add(arc)
    if cur_wave != 1:
        player.hp += 25


def clear_groups(company):
    '''
    Очистка всех групп спрайтов
    '''
    from Units import creepe_group, weapon_group, arrow_group, player_group

    for i in creepe_group:
        i.kill()

    for i in arrow_group:
        i.kill()

    for i in weapon_group:
        i.kill()

    if company:
        for i in player_group:
            i.kill()

import pygame, os, sys
from random import randint

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


wave_image = load_image('waves_1.png')


def switching_waves(cur_wave, creepe):
    creepe = creepe * cur_wave + 3
    SCREEN.blit(wave_image, (760, 200))
    num = font.render(str(cur_wave), False, '#880015')
    SCREEN.blit(num, (840, 220))
    for i in range(creepe):
        creepe_group.add(Units.SwordMan(randint(100, WIDTH - 100), randint(1620, 1920)))
import pygame, os, sys

SIZE = WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()
FPS = 10

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

player_image = load_image('taras.png', -1)
sword_man = load_image('swordsman.png', -1)
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
creepe_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
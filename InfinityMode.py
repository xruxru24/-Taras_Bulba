import pygame, os, sys

size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60


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


def infinity_game():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            """
            
            ЛОГИКА ВЗАИМОДЕЙСТВИЯ С ПЕРСОНАЖЕМ
            
            """
        field_sprite.draw(screen)
        sale_point_sprite.draw(screen)
        pygame.display.flip()

infinity_game()
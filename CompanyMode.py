import pygame, os, sys
from expansion import SCREEN


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


image_1 = load_image("company_mode_menu.png")


def company_game():

    from main_menu import start_menu

    click_data = {(range(140, 610), range(145, 900)): print('Свинья'),
        (range(720, 1200), range(145, 900)): print('Войцех'),
        (range(1290, 1745), range(145, 900)): print('Андрий'),
        (range(1655, 1890), range(20, 95)): start_menu}
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in click_data.keys():
                    if event.pos[0] in i[0] and event.pos[1] in i[1]:
                        click_data[i]
        SCREEN.fill('black')
        SCREEN.blit(image_1, (0, 0))
        pygame.display.flip()


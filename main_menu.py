import pygame
import os
import sys

# from InfinityMode import infinity_game

pygame.init()
clock = pygame.time.Clock()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Engine:
    def draw_map_and_units(self, all_sprites):
        for unit in all_sprites:
            if isinstance(unit, Player):
                self.pos_data_player = {}
            elif isinstance(unit, SwordMan):
                self.pos_data_swordman = {}
            image = self.pos_data_player[(unit.pos, unit.weapon)]
            image = load_image(image)
            screen.blit(image, unit.coords)

    def music(self, song):
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)


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


def company_game():
    pass

def statictics():
    pass


def exit_game():
    sys.exit()


image = load_image("startmenu.png")


def start_menu():
    '''
    Функция для реализации стартового меню и его кнопок.
    '''
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_data = {(range(15, 435), range(345, 480)): infinity_game,
                              (range(1650, 1920), range(895, 1025)): exit_game,
                              (range(15, 435), range(175, 315)): company_game,
                              (range(15, 435), range(525, 655)): statictics}
                for i in click_data.keys():
                    if event.pos[0] in i[0] and event.pos[1] in i[1]:
                        click_data[i]()
        screen.fill('black')
        screen.blit(image, (0, 0))
        pygame.display.flip()
        clock.tick(60)


start_menu()

pygame.quit()

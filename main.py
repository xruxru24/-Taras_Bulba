import pygame
import os
import sys

pygame.init()
clock = pygame.time.Clock()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)


class Engine:
    def draw_map_and_units(self, all_sprites):
        pass


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


image = load_image("startmenu.png")


def start_menu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and int(event.pos[0]) in range(17, 434) and \
                    int(event.pos[1]) in range(344, 480):
                pass
        screen.fill('black')
        screen.blit(image, (0, 0))
        pygame.display.flip()
        clock.tick(60)


start_menu()

pygame.quit()


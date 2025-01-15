import pygame
import os
import sys

pygame.init()
clock = pygame.time.Clock()
size = width, height = 800, 600
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
image1 = pygame.transform.scale(image, (800, 600))


def start_menu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.pos.x in range(?, ?) and event.pos.y in range(?, ?):
                pass
        screen.fill('black')
        screen.blit(image1, (0, 0))
        pygame.display.flip()
        clock.tick(60)


start_menu()

pygame.quit()

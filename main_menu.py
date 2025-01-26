import pygame
import sys
from expansion import load_image, SCREEN, CLOCK
import csv

image = load_image("startmenu.png")


def company_game():
    pass


def exit_game():
    sys.exit()


def start_menu():
    '''
    Функция для реализации стартового меню и его кнопок.
    '''
    run = True
    c = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                from InfinityMode import infinity_game
                from Engine import eng, statictics

                click_data = {(range(15, 435), range(345, 480)): (
                    infinity_game, eng.music(('song_1.mp3', 'song_2.mp3'))),
                    (range(1650, 1920), range(895, 1025)): (exit_game, eng.music(('song_1.mp3', 'song_2.mp3'))),
                    (range(15, 435), range(175, 315)): (company_game, eng.music(('song_1.mp3', 'song_2.mp3'))),
                    (range(15, 435), range(525, 655)): (statictics, eng.music(('song_1.mp3', 'song_2.mp3')))}
                for i in click_data.keys():
                    if event.pos[0] in i[0] and event.pos[1] in i[1]:
                        for func in click_data[i]:
                            if func:
                                func()
        SCREEN.fill('black')
        SCREEN.blit(image, (0, 0))
        pygame.display.flip()
        CLOCK.tick(10)


start_menu()

pygame.quit()

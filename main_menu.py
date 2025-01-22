import pygame
import sys
import Units
import InfinityMode
import expansion
from expansion import SCREEN

pygame.mixer.init()


class Engine:
    def __init__(self):
        self.kills = 0
        self.damage = 0

    def music(self, songs):
        for i in songs:
            pygame.mixer.music.load(i)
            pygame.mixer.music.queue(i)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.6)

    def damage_collides(self, weapon, dir, who, creeps):
        data_player_dir = {'up': (0, -weapon.raduis), 'down': (0, weapon.raduis),
                           'left': (-weapon.raduis, 0), 'right': (weapon.raduis, 0)}
        divs = data_player_dir[dir]
        hitbox_weapon = pygame.Rect(who.coords[0] + divs[0], who.coords[1] + divs[1], weapon.raduis, weapon.raduis)
        for unit in creeps:
            if hitbox_weapon.colliderect(unit.rect):
                if unit.health - weapon.damage <= 0:
                    unit.health = 0
                    creeps.pop(unit)
                    if isinstance(unit, Units.Player):
                        end_game()
                    else:
                        self.kills += 1
                        self.damage += unit.health
                else:
                    unit.health -= weapon.damage
                    self.damage += weapon.damage


def company_game():
    pass


def statictics():
    pass


def exit_game():
    sys.exit()


def end_game():
    pass


image = expansion.load_image("startmenu.png")
eng = Engine()


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
                click_data = {(range(15, 435), range(345, 480)): (InfinityMode.infinity_game, eng.music(('song_2.mp3', 'song_1.mp3'))),
                              (range(1650, 1920), range(895, 1025)): exit_game,
                              (range(15, 435), range(175, 315)): company_game,
                              (range(15, 435), range(525, 655)): statictics}
                for i in click_data.keys():
                    if event.pos[0] in i[0] and event.pos[1] in i[1]:
                        for j in range(len(i)):
                            click_data[i][j]()
        expansion.SCREEN.fill('black')
        expansion.SCREEN.blit(image, (0, 0))
        pygame.display.flip()
        expansion.CLOCK.tick(60)


start_menu()

pygame.quit()

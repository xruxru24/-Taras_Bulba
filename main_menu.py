import pygame
import sys
import Units
import InfinityMode
import expansion
import csv
from expansion import SCREEN

pygame.mixer.init()
image = expansion.load_image("startmenu.png")
image1 = expansion.load_image("statsmenu.png")


class Engine:
    def __init__(self):
        self.kills = 0
        self.damage = 0
        self.deaths = 0
        self.hits = 0

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
                        self.deaths += 1
                        end_game()
                    else:
                        self.kills += 1
                        self.damage += unit.health
                else:
                    unit.health -= weapon.damage
                    self.damage += weapon.damage
                self.hits += 1
        self.update_stats()

    def update_stats(self):
        with open('stats.csv', mode='wt') as file:
            data = [self.damage, self.kills, self.deaths, self.hits]
            data1 = ['Damage', 'Kills', 'Deaths', 'Hits']
            temp = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(data)):
                temp.writerow([data1[i], data[i]])


eng = Engine()
font = pygame.font.SysFont(None, 50)


def company_game():
    pass


def statictics():
    data_coords = {'Deaths': (100, 200),
                   'Kills': (80, 300),
                   'Hits': (70, 400),
                   'Damage': (100, 500)}
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and \
                    event.pos[0] in range(400, 500) and event.pos[1] in range(450, 500):
                start_menu()
                run = False
        expansion.SCREEN.blit(image1, (400, 300))
        with open('stats.csv', mode='rt') as file:
            data = list(csv.reader(file, delimiter=';', quotechar='"'))
            for stat in data:
                num = font.render(str(stat[0]), False, 'red')
                expansion.SCREEN.blit(num, (data_coords[stat[0]]))
        pygame.display.flip()


def exit_game():
    sys.exit()


def end_game():
    pass


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
                click_data = {(range(15, 435), range(345, 480)): (
                InfinityMode.infinity_game, eng.music(('song_2.mp3', 'song_1.mp3'))),
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
        expansion.CLOCK.tick(10)


start_menu()

pygame.quit()

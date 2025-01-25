import pygame
import sys
import Units
import InfinityMode
import expansion
import csv
from expansion import SCREEN

pygame.mixer.init()
pygame.font.init()
image = expansion.load_image("startmenu.png")
image1 = expansion.load_image("stats.png")


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
                        statictics('end_game')
                    else:
                        self.kills += 1
                        self.damage += unit.health
                else:
                    unit.health -= weapon.damage
                    self.damage += weapon.damage
                self.hits += 1
        self.update_stats('all_time')
        self.update_stats('one_game')

    def update_stats(self, param):
        data_files = {'all_time': 'stats.csv',
                      'one_game': 'stats_one_game.csv'}
        with open(data_files[param], mode='wt') as file:
            temp = csv.reader(file, delimiter=';', quotechar='"')
            temp = sorted(temp, key=lambda x: int(x[1]))
            data = [self.damage, self.kills, self.deaths, self.hits]
            for row in range(len(temp)):
                temp[row][1] += data[row]
            writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(temp)):
                writer.writerow(temp[i])


eng = Engine()
font = pygame.font.SysFont('Comic Sans MS', 27)


def company_game():
    pass


def statictics(param=None):
    data_coords = {'Deaths': (680, 370),
                   'Kills': (685, 430),
                   'Hits': (700, 485),
                   'Damage': (650, 580)}
    data_files = {None: 'stats.csv',
                  'end_game': 'stats_one_game.csv'}
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and \
                    event.pos[0] in range(855, 980) and event.pos[1] in range(620, 685):
                start_menu()
                run = False
        expansion.SCREEN.blit(image1, (400, 300))
        with open(data_files[param], mode='rt') as file:
            data = list(csv.reader(file, delimiter=';', quotechar='"'))
            for stat in data:
                num = font.render(str(stat[1]), False, '#880015')
                expansion.SCREEN.blit(num, (data_coords[stat[0]]))
        pygame.display.flip()


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
                click_data = {(range(15, 435), range(345, 480)): (
                    InfinityMode.infinity_game, eng.music(('song_2.mp3', 'song_1.mp3'))),
                    (range(1650, 1920), range(895, 1025)): (exit_game, eng.music(('song_2.mp3', 'song_1.mp3'))),
                    (range(15, 435), range(175, 315)): (company_game, eng.music(('song_2.mp3', 'song_1.mp3'))),
                    (range(15, 435), range(525, 655)): (statictics, eng.music(('song_2.mp3', 'song_1.mp3')))}
                for i in click_data.keys():
                    if event.pos[0] in i[0] and event.pos[1] in i[1]:
                        for func in click_data[i]:
                            func()
        expansion.SCREEN.fill('black')
        expansion.SCREEN.blit(image, (0, 0))
        pygame.display.flip()
        expansion.CLOCK.tick(10)


start_menu()

pygame.quit()

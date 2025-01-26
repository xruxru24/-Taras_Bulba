import time

import pygame
import csv
import pygame.font

pygame.mixer.init()
pygame.font.init()

import expansion

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
        pygame.mixer.music.set_volume(0)

    def damage_collides(self, weapon, dir, who, creeps):
        data_player_dir = {'up': (-(weapon.attack_distance // 4), -weapon.attack_distance),
                           'down': (-(weapon.attack_distance // 4), 116),
                           'left': (-weapon.attack_distance, -(weapon.attack_distance // 4)),
                           'right': (84, -(weapon.attack_distance // 4))}

        from Units import Player, creepe_group, player_group

        divs = data_player_dir[dir]
        hitbox_weapon = pygame.Rect(who.pos_x + divs[0], who.pos_y + divs[1], weapon.attack_distance, weapon.attack_distance)
        for unit in creeps:
            if hitbox_weapon.colliderect(unit.rect):
                if unit.hp - weapon.damage <= 0:
                    unit.hp = 0
                    unit.weapon.kill()
                    unit.kill()
                    if isinstance(unit, Player):
                        self.deaths += 1
                        player_group.pop(unit)
                        statictics('end_game')
                    else:
                        self.kills += 1
                        self.hits += 1
                        self.damage += unit.hp
                else:
                    unit.hp -= weapon.damage
                    self.damage += weapon.damage
                    self.hits += 1
        self.update_stats('all_time')
        self.update_stats('one_game')

    def update_stats(self, param):
        data_files = {'all_time': 'stats.csv',
                      'one_game': 'stats_one_game.csv'}
        with open(data_files[param], mode='rt') as file:
            temp = csv.reader(file, delimiter=';', quotechar='"')
            for index, row in enumerate(temp):
                print(row)
            temp = sorted(temp, key=lambda x: int(x[1]))
            data = [self.damage, self.kills, self.deaths, self.hits]
            for row in range(len(temp)):
                temp[row][1] += data[row]
            writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(temp)):
                writer.writerow(temp[i])


font = pygame.font.SysFont('Comic Sans MS', 27)
eng = Engine()


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
                run = False
        expansion.SCREEN.blit(image1, (400, 300))
        with open(data_files[param], mode='rt') as file:
            data = list(csv.reader(file, delimiter=';', quotechar='"'))
            for stat in data:
                num = font.render(str(stat[1]), False, '#880015')
                expansion.SCREEN.blit(num, (data_coords[stat[0]]))
        pygame.display.flip()

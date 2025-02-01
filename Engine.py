import pygame
import csv
import pygame.font
import expansion

pygame.mixer.init()
pygame.font.init()

# подгрузка спрайтов
image1 = expansion.load_image("stats.png")
slashes_images = [pygame.transform.scale(expansion.load_image('slash_down.png'), (200, 140)),
                  pygame.transform.scale(expansion.load_image('slash_up.png'), (200, 140)),
                  pygame.transform.scale(expansion.load_image('slash_right.png'), (140, 200)),
                  pygame.transform.scale(expansion.load_image('slash_left.png'), (140, 200))]


class Engine:
    def music(self, songs):
        '''
        Метод для запуска музыки
        '''
        for i in songs:
            pygame.mixer.music.load(i)
            pygame.mixer.music.queue(i)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0)

    def damage_collides(self, weapon, dir, who, creeps, arrow_or_not, miss, player):
        '''
        Метод, реализующий: отрисовку удара, нанесение урона от всех оружий и от всех игровых персонажей,
        а также вызывает метод обновления статистики.
        '''
        from Units import Player

        # параметры статистики(урон, убийства, попадания, смерти)
        damage, kills, hits, deaths = 0, 0, 0, 0

        if arrow_or_not:
            if weapon.rect.colliderect(player.rect):
                player.weapon.kill()
                player.kill()
                deaths += 1

                self.update_stats('all_time', damage, deaths, hits, kills)
                self.update_stats('one_game', damage, deaths, hits, kills)

                statictics('end_game')
            if weapon.rect.x >= 1910 or weapon.rect.y >= 1070 or weapon.rect.x <= 0 or weapon.rect.y <= 0:
                weapon.kill()
            return
        else:
            data_player_dir = {'up': (-(weapon.attack_distance // 4), -weapon.attack_distance, slashes_images[1]),
                               'down': (-(weapon.attack_distance // 4), 116, slashes_images[0]),
                               'left': (-weapon.attack_distance, -(weapon.attack_distance // 4), slashes_images[3]),
                               'right': (84, -(weapon.attack_distance // 4), slashes_images[2])}
            # по ключу направления удара из словаря data_player_dir выбирается
            # смещение координат для определения хитбокса атаки
            divs = data_player_dir[dir][:2]
            # создается хитбокс атаки
            hitbox_weapon = pygame.Rect(who.pos_x + divs[0], who.pos_y + divs[1],
                                        weapon.attack_distance * 2, weapon.attack_distance * 2)

            # отрисовка атаки(блеск меча)
            FLAG_SLASH_TIME = 35
            while FLAG_SLASH_TIME != 0:
                expansion.SCREEN.blit(data_player_dir[dir][-1], (who.pos_x + divs[0], who.pos_y + divs[1] - 10))
                pygame.display.flip()
                FLAG_SLASH_TIME -= 1

            # логика проверки попадания и нанесения урона
            for unit in creeps:
                if hitbox_weapon.colliderect(unit.rect):
                    if unit.hp - weapon.damage <= 0:
                        unit.weapon.kill()
                        unit.kill()
                        if isinstance(unit, Player):
                            unit.weapon.kill()
                            unit.kill()
                            deaths += 1
                            self.update_stats('all_time', damage, deaths, hits, kills)
                            self.update_stats('one_game', damage, deaths, hits, kills)
                            statictics('end_game')
                        else:
                            kills += 1
                            hits += 1
                            damage += unit.hp
                            player.money += 10
                            if not isinstance(unit, Player):
                                kills += 1
                                hits += 1
                                damage += unit.hp
                    else:
                        unit.hp -= weapon.damage
                        if not isinstance(unit, Player):
                            damage += weapon.damage
                            hits += 1


    def update_stats(self, param, damage, deaths, hits, kills):
        '''
        Метод получает на вход параметр(от него зависит в какой файл записывается статистика),
        а дальше передаются сами параметры статистики.
        Метод обновляет статистику.
        '''
        # словарь для выбора нужного файла взависимости от параметра param
        data_files = {'all_time': 'stats.csv',
                      'one_game': 'stats_one_game.csv'}
        with open(data_files[param], mode='rt') as file:
            temp = list(csv.reader(file, delimiter=';', quotechar='"'))
            data = [damage, kills, deaths, hits]
            temp = [value for value in temp if value]

            # обновление параметров статистики
            for row in range(len(temp)):
                temp[row][1] = str(int(temp[row][1]) + data[row])
        with open(data_files[param], mode='wt') as file:
            writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            # запись обновлений
            for row in temp:
                writer.writerow(row)


# создание шрифта
font = pygame.font.SysFont('Comic Sans MS', 27)

eng = Engine()


def statictics(param=None):
    '''
    Функция реализует и общую статистику(статистику за все время), и финальное меню(статистику одного боя),
    поэтому принимает параметр по которому определяет какую статистику нужно вывести на экран.
    '''
    # словарь для определения координат, где нужно вывести соотвествующие ключам параметры статистики.
    data_coords = {'Deaths': (680, 370),
                   'Kills': (685, 430),
                   'Hits': (700, 485),
                   'Damage': (650, 580)}
    # словарь для определения файла, с которым нужно работать
    data_files = {None: 'stats.csv',
                  'end_game': 'stats_one_game.csv'}
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                clear_stats(data)
            # реализация кнопки выхода
            elif event.type == pygame.MOUSEBUTTONDOWN and \
                    event.pos[0] in range(855, 980) and event.pos[1] in range(620, 685):
                run = False
                # очистка статистики одного боя
                clear_stats(data)
                from main_menu import start_menu
                start_menu()
        expansion.SCREEN.blit(image1, (400, 300))
        with open(data_files[param], mode='rt', encoding='utf-8') as file:
            data = list(csv.reader(file, delimiter=';', quotechar='"'))
            data = [value for value in data if value]

            # отрисовка параметров статистики(урона, убийств и т.д.)
            for stat in data:
                num = font.render(str(stat[1]), False, '#880015')
                expansion.SCREEN.blit(num, (data_coords[stat[0]]))
        pygame.display.flip()
        if param is not None:
            with open(data_files[param], mode='wt') as file:
                writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                for row in range(len(data)):
                    if data[row][0] == "Deaths":
                        data[row][1] = '1'
                    else:
                        data[row][1] = '0'
                writer.writerows(data)


def clear_stats(params):
    '''
    Функция реализующий очистику статистики одного боя.
    '''
    with open('stats_one_game.csv', mode='wt') as file:
        writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        for row in range(len(params)):
            if params[row][0] == "Deaths":
                params[row][-1] = '1'
            else:
                params[row][-1] = '0'
        writer.writerows(params)

from dataclasses import field

import pygame, os, sys
from expansion import SCREEN, clear_groups
from Units import Player, weapon_group, player_group, all_sprites, arrow_group, creepe_group
from Weapons import Saber

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 40)

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


def company_game_menu():

    from main_menu import start_menu

    click_data = {(range(140, 610), range(145, 900)): 'Свиноподобный',
        (range(720, 1200), range(145, 900)): 'Войцех',
        (range(1290, 1745), range(145, 900)): 'Андрий',
        (range(1655, 1890), range(20, 95)): None}
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in click_data.keys():
                    if event.pos[0] in i[0] and event.pos[1] in i[1]:
                        if isinstance(click_data[i], str):
                            company_game(click_data[i])
                        else:
                            start_menu()
        SCREEN.fill('black')
        SCREEN.blit(image_1, (0, 0))
        pygame.display.flip()


def company_game(boss):
    clear_groups(True)

    boss_locations = {'Свиноподобный': 'company_mode_1st_boss.png',
                     'Войцех': 'company_mode_2nd_boss.png',
                     'Андрий': 'company_mode_3rd_boss.png'}
    boss_location = load_image(boss_locations[boss])
    field_sprite = pygame.sprite.Group()
    field = pygame.sprite.Sprite()
    field.image = pygame.transform.scale(boss_location, (1920, 1080))
    field.rect = field.image.get_rect()
    player = Player(50, 50, Saber())
    field_sprite.add(field)

    run = True
    while run:
        mb_down = False
        if player.weapon.reloads:
            if player.weapon.cooldown - 1 == 0:
                player.weapon.reloads = False
                player.weapon.cooldown = player.weapon.reload * 600
            player.weapon.cooldown -= 1

        for i in weapon_group:
            if i.reloads:
                if i.cooldown - 1 == 0:
                    i.reloads = False
                    i.cooldown = i.reload * 600
                i.cooldown -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.weapon.reloads:
                    mb_down = False
                else:
                    player.weapon.reloads = True
                    mb_down = True

        keys = pygame.key.get_pressed()
        player.run(keys, mb_down)
        player_group.update()
        all_sprites.update()

        weapon_group.update()
        arrow_group.update()
        field_sprite.draw(SCREEN)

        player_group.draw(SCREEN)
        creepe_group.draw(SCREEN)
        weapon_group.draw(SCREEN)

        hp = font.render(f'Health: {player.hp}', False, 'Red')
        SCREEN.blit(hp, (0, 950))

        if player.weapon.reloads:
            cooldown = font.render('Can not do it now!', False, 'Black')
            SCREEN.blit(cooldown, (1600, 900))

        pygame.display.flip()
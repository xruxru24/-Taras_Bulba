import sys
import os
import pygame

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


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


player_image = load_image('taras.png', True)
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = 0.3
        self.max_speed = 2
        self.friction = 0.9

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x_speed -= self.acceleration
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x_speed += self.acceleration
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.y_speed -= self.acceleration
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.y_speed += self.acceleration

            self.x_speed = max(-self.max_speed, min(self.x_speed, self.max_speed))
            self.y_speed = max(-self.max_speed, min(self.y_speed, self.max_speed))

            if not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                self.x_speed *= self.friction
            if not (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
                self.y_speed *= self.friction

            self.rect.x += self.x_speed
            self.rect.y += self.y_speed
            self.rect.clamp_ip(screen.get_rect())

            screen.fill('white')
            player_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


player = Player(50, 50)
player.run()
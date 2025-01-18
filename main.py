import sys
import os
import pygame

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f"Cannot load image: {fullname}")
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


player_image = load_image('taras.png', -1)
sword_man = load_image('swordsman.png', -1)
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
creepe_group = pygame.sprite.Group()


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

    def run(self, keys):
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

    def get_position(self):
        return self.rect.centerx, self.rect.centery


class SwordMan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(creepe_group, all_sprites)
        self.image = sword_man
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = 0.2
        self.max_speed = 1
        self.friction = 0.9
        self.player = None

    def set_player(self, player):
        self.player = player

    def update(self):
        if self.player:
            player_x, player_y = self.player.get_position()
            dx = player_x - self.rect.centerx
            dy = player_y - self.rect.centery
            if dx > 0:
                self.x_speed += self.acceleration
            if dx < 0:
                self.x_speed -= self.acceleration
            if dy > 0:
                self.y_speed += self.acceleration
            if dy < 0:
                self.y_speed -= self.acceleration
            self.x_speed = max(-self.max_speed, min(self.x_speed, self.max_speed))
            self.y_speed = max(-self.max_speed, min(self.y_speed, self.max_speed))
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed
            self.rect.clamp_ip(screen.get_rect())


player = Player(50, 50)
swordman = SwordMan(300, 300)
swordman.set_player(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False

    keys = pygame.key.get_pressed()
    player.run(keys)
    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
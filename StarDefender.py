import pygame
import sys
import os
import random

pygame.init()
SIZE = WIDTH, HEIGHT = 600, 800
FPS = 130

STEP = 8
STEPOFSHOT = 7
STARSSTEP = 1

# радиус круга
RAD = 25

shotss = []
enemyshots = []
end_text = []

# ширина spaceship
WIDTH_OF_SPACESHIP = 120

# начальное положение spaceship
x, y = WIDTH // 2 - WIDTH_OF_SPACESHIP // 2, 600

end = False

nnn = 0

rise = 0

clock = pygame.time.Clock()

GRAVITY = 0.2

TILE_HEIGHT = HEIGHT // 10

level_number = None


def load_image(file, colorkey=None):
    fullname = os.path.join('data', file)
    if not os.path.isfile(fullname):
        print(f'{file} не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


# враги основа
class Enemy(pygame.sprite.Sprite):
    def __init__(self, y, x):
        super().__init__(enemies)
        self.health = 2
        self.image = pygame.transform.scale(load_image("33.png"), (WIDTH // 7, HEIGHT // 7))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 300
        # отсчет перед стрельбой
        self.n = 0
        self.rect.y = y
        self.rect.x = x
        # ценность, количество очков, которое дает
        self.value = 1

    def update(self):
        global rise
        for i in shotss:
            if pygame.sprite.collide_mask(self, i):
                self.health -= 1
                i.kill()
                del shotss[shotss.index(i)]
                rise += 1
        if pygame.sprite.collide_mask(self, spaceship):
            spaceship.kill()
            spaceship.health -= 1
        if self.health == 0:
            self.kill()

        self.rect.y += STARSSTEP


# враги тип 1
class EnemyT1(Enemy):
    def update(self):
        super(EnemyT1, self).update()
        self.n += 1
        if self.n == FPS * random.randint(8, 20):
            self.n = 0
        if self.rect.y < HEIGHT:
            self.rect.y += STARSSTEP
        else:
            self.kill()


class Myspaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image =  self.image = pygame.transform.scale(load_image("gg.png"), (WIDTH // 4, HEIGHT // 4))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.health = 1

    def updateleft(self, STEP):
        # движение влево
        if self.rect.x > -20:
            self.rect = self.rect.move(-STEP, 0)

    def updateright(self, STEP):
        # движение вправо
        if self.rect.x < WIDTH - WIDTH_OF_SPACESHIP + 10:
            self.rect = self.rect.move(STEP, 0)

    def update(self):
        for i in enemyshots:
            if pygame.sprite.collide_mask(self, i):
                self.health -= 1
                i.kill()
        if end_text:
            if pygame.sprite.collide_mask(self, end_text[0]):
                pass


class Shott(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(shots)
        self.image = load_image("strike.png")
        self.rect = self.image.get_rect()
        self.mask_of_shot = pygame.mask.from_surface(self.image)
        self.rect.x = x + WIDTH_OF_SPACESHIP // 2 - RAD // 4
        self.rect.y = y + WIDTH_OF_SPACESHIP // 2 - RAD // 2

    def update(self):
        if self.rect.y > 0:
            self.rect.y -= STEPOFSHOT
        else:
            self.kill()


class Star(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__(stars)
        r = random.randint(0, 2)
        self.image = pygame.Surface((r * 2, r * 2),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color((150, 150, 150)),
                           (r, r), r)
        self.rect = pygame.Rect(random.randint(0, WIDTH), y, 2 * r, 2 * r)

    def update(self):
        if self.rect.y < HEIGHT:
            self.rect.y += STARSSTEP
        else:
            self.kill()


class EndText(pygame.sprite.Sprite):
    def __init__(self, y, x):
        super().__init__(textt)
        self.image = load_image('endtext.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.y += STARSSTEP
        if pygame.sprite.collide_mask(self, spaceship):
            if level_number == 3:
                end_screen((500, 500), 500, 500)
            elif level_number == 2 or level_number == 1:
                space_map((500, 500), 500, 500)


# проигрыш
def losing():
    global rise
    global nnn
    with open('data\\' + 'nnn.txt', 'wt') as f:
        print(f.write(str(nnn + rise)))
    screen.fill('black')
    pygame.display.set_mode((500, 500))
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('gameover.png'), (500, 500))
    for i in range(4000):
        screen.fill(pygame.Color('white'),
                    (random.random() * 500,
                     random.random() * 500, 1, 1))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                space_map((500, 500), 500, 500)
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        clock.tick(50)


def terminate():
    pygame.quit()
    sys.exit()


screen = pygame.display.set_mode(SIZE)

all_sprites = pygame.sprite.Group()
stars = pygame.sprite.Group()
shots = pygame.sprite.Group()
enemies = pygame.sprite.Group()
textt = pygame.sprite.Group()
spaceship = Myspaceship(x, y)


# 2
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.transform.scale(load_image('gem.png'), (WIDTH // 20, HEIGHT // 20))]
    for scale in (15, 17, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        screen_rect = (0, 0, WIDTH, HEIGHT)
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    global end, shots, enemies, textt, all_sprites
    all_sprites = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    textt = pygame.sprite.Group()
    level.reverse()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                EnemyT1(-y * TILE_HEIGHT, x * WIDTH // len(level[y]))
            elif level[y][x] == '-':
                EndText(-y * TILE_HEIGHT, x * WIDTH // len(level[y]))
                end = True


def start_screen(size, width, height):
    pygame.display.set_mode(size)
    pygame.display.set_caption('Star Defender')
    screen.fill((0, 0, 0))
    pygame.display.set_icon(load_image('icon.png'))
    fon = pygame.transform.scale(load_image('bg.jpg'), size)
    title_text = pygame.transform.scale(load_image('title.png'), (width, height // 2))
    start_text = pygame.transform.scale(load_image('start_text.png'), (width // 2, height // 4))
    screen.blit(fon, (0, 0))
    screen.blit(title_text, (10, 0))
    screen.blit(start_text, (125, 215))
    for i in range(4000):
        screen.fill(pygame.Color('white'),
                    (random.random() * width,
                     random.random() * height, 1, 1))
    font = pygame.font.SysFont('bandal', 50)
    text_start = font.render("START", True, 'blue')
    text_title = font.render('STAR DEFENDER', True, (255, 255, 255))
    text_x = width // 2 - text_start.get_width() // 2
    text_y = height // 2 - text_start.get_height() // 2
    text_w = text_start.get_width()
    text_h = text_start.get_height()
    button_rect = pygame.draw.rect(screen, (0, 142, 204), (text_x - 10, text_y - 10,
                                                           text_w + 20, text_h + 20), 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and (
                    text_x - 10 <= pygame.mouse.get_pos()[0] <= text_x - 10 + text_w + 20) \
                    and (text_y - 10 <= pygame.mouse.get_pos()[1] <= text_y - 10 + text_h + 20):
                space_map((500, 500), 500, 500)
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(size, width, height):
    pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('winscreen.jpg'), size)
    win_text = pygame.transform.scale(load_image('wintext.png'), (width, height // 2))
    chest = pygame.transform.scale(load_image('chest.png'), (width // 2, height // 2), )
    screen.blit(fon, (0, 0))
    screen.blit(win_text, (-8, 0))
    screen.blit(chest, (80, 270))
    for i in range(4000):
        screen.fill(pygame.Color('white'),
                    (random.random() * width,
                     random.random() * height, 1, 1))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen((500, 500), 500, 500)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # создаём частицы по щелчку мыши
                create_particles(pygame.mouse.get_pos())
        all_sprites.update()
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        screen.blit(win_text, (-8, 0))
        screen.blit(chest, (80, 270))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)


def space_map(size, width, height):
    global level_number
    space_running = True
    text1 = pygame.transform.scale(load_image('1.png'), (width // 2, height // 4))
    text2 = pygame.transform.scale(load_image('2.png'), (width // 2, height // 4))
    text3 = pygame.transform.scale(load_image('3.png'), (width // 2, height // 4))
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('space.jpg'), size)
    screen.blit(fon, (0, 0))
    screen.blit(text1, (-65, 335))
    screen.blit(text2, (0, 100))
    screen.blit(text3, (245, 320))
    levelone_rect = pygame.draw.rect(screen, (0, 142, 204), (45, 350,
                                                             35, 50), 2)
    leveltwo_rect = pygame.draw.rect(screen, (0, 142, 204), (100, 100,
                                                             55, 70), 2)
    levelboss_rect = pygame.draw.rect(screen, (0, 142, 204), (310, 280,
                                                              120, 155), 2)
    for i in range(4000):
        screen.fill(pygame.Color('white'),
                    (random.random() * width,
                     random.random() * height, 1, 1))
    while space_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # 1-й уровень
            elif event.type == pygame.MOUSEBUTTONDOWN and (45 <= pygame.mouse.get_pos()[0] <= 45 + 35) \
                    and (350 <= pygame.mouse.get_pos()[1] <= 350 + 50):
                pygame.display.set_mode(SIZE)
                level_number = 1
                generate_level(load_level('level.txt'))
                space_running = False
            # 2-й уровень
            elif event.type == pygame.MOUSEBUTTONDOWN and (100 <= pygame.mouse.get_pos()[0] <= 100 + 55) \
                    and (100 <= pygame.mouse.get_pos()[1] <= 100 + 70):
                pygame.display.set_mode(SIZE)
                level_number = 2
                generate_level(load_level('level2.txt'))
                space_running = False
            # 3-й уровень
            elif event.type == pygame.MOUSEBUTTONDOWN and (310 <= pygame.mouse.get_pos()[0] <= 310 + 120) \
                    and (280 <= pygame.mouse.get_pos()[1] <= 280 + 155):
                generate_level(load_level('level3.txt'))
                pygame.display.set_mode(SIZE)
                level_number = 3
                space_running = False
        pygame.display.flip()
        clock.tick(FPS)
    main()


def main():
    global nnn
    global end
    global spaceship
    spaceship = Myspaceship(x, y)
    running = True
    screen.fill('black')
    all_sprites.draw(screen)
    global rise
    rise = 0
    # rise - кол-во очков за игру
    # nnn - кол-во очков всего
    with open('data\\' + 'nnn.txt', 'rt') as f:
        nnn = int(f.read())
    print(nnn)

    for i in range(HEIGHT):
        Star(i)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if pygame.key.get_pressed()[pygame.K_d] or event.type == pygame.K_d:
                spaceship.updateright(STEP)
                # двигается вправо
            if pygame.key.get_pressed()[pygame.K_a] or event.type == pygame.K_a:
                spaceship.updateleft(STEP)
                # двигается влево
            if event.type == pygame.MOUSEBUTTONDOWN:
                shotss.append(Shott(spaceship.rect.x, spaceship.rect.y))
        Star(0)
        screen.fill('black')
        stars.update()
        stars.draw(screen)
        textt.update()
        textt.draw(screen)
        shots.update()
        shots.draw(screen)
        spaceship.update()
        all_sprites.draw(screen)
        enemies.update()
        enemies.draw(screen)
        clock.tick(FPS)
        if end:
            textt.update()
            textt.draw(screen)
        pygame.display.flip()
        if spaceship.health < 1:
            losing()
    pygame.quit()


start_screen((500, 500), 500, 500)

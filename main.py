import pygame
import sys
import random


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Добро пожаловать в игру!", "",
                  "Правило только одно: ВЫЖИВАЙ ПО МАКСИМУМУ",
                  "Победителей тут нет, только рекордстмены"]

    fon = pygame.image.load('data/img/fon.jpg').convert()
    fon = pygame.transform.scale(fon, (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# Класс игрока
class Player(pygame.sprite.Sprite):
    player_image = pygame.transform.scale(pygame.image.load('data/img/player.png').convert_alpha(), (40, 30))
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = Player.player_image
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = width / 2 - self.rect.width // 2
        self.rect.y = 370
        self.step = 0

    def update(self):
        self.step = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.step = -5
        if keys[pygame.K_RIGHT]:
            self.step = 5
        self.rect.x += self.step
        if self.rect.x + self.rect.width > width:
            self.rect.right = width
        if self.rect.x < 0:
            self.rect.x = 0

    def gun(self):
        fire = Fire(self.rect.center, self.rect.top)


# Класс пули
class Fire(pygame.sprite.Sprite):
    fire_image = pygame.transform.scale(pygame.image.load('data/img/fire.png').convert_alpha(), (20, 10))
    def __init__(self, x, y):
        super().__init__(bullets_group, all_sprites)
        self.image = Fire.fire_image
        self.image = self.image.convert_alpha()
        self.speed_bullet = -10
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.center = x

    def update(self):
        self.rect.y += self.speed_bullet
        # если он заходит за верхнюю часть экрана, исчезает
        if self.rect.bottom < 0:
            self.kill()


# Класс дома(участка)
class House(pygame.sprite.Sprite):
    image = pygame.image.load('data/img/houae.png').convert_alpha()
    def __init__(self):
        super().__init__(house_group, all_sprites)
        self.image = House.image
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (800, 200))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


#  Класс зомби
class Zombie(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('data/img/zombie.jpg').convert_alpha(), (30,30))
    def __init__(self, x, y):
        super().__init__(zombie_group, all_sprites)
        self.image = Zombie.image
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if not pygame.sprite.collide_mask(self, house):
            self.rect = self.rect.move(0, 1)
        else:
            self.kill()


#  завершение игры
def game_over():
    img = pygame.image.load('data/img/gameover.jpg').convert()
    record_time = read_record_time()
    record_zombi = read_record_zombi()
    font_game_over = pygame.font.Font(None, 50)
    img = pygame.transform.scale(img, (400, 200))
    screen.blit(img, (150, 150))
    text_counter1 = font_game_over.render(f'Количетсво прожитого времени: {record_time}',
                                          True, (255, 255, 255))
    text_counter2 = font_game_over.render(f'Количество убитых зомби: {record_zombi}',
                                          True, (255, 255, 255))
    screen.blit(text_counter1, (150, 315))
    screen.blit(text_counter2, (150, 350))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


# функция возвращает число - рекордный счет времени, записанный в файле
def read_record_time():
    with open('data/record_seconds.txt') as f:
        return f.readline()


# перезаписываем рекорд времени, если счет больше
def write_record_time(r):
    with open('data/record_seconds.txt', 'w') as f:
        f.write(str(r))

# функция возвращает число - рекордный счет убитых зомби, записанный в файле
def read_record_zombi():
    with open('data/record_zombi.txt') as f:
        return f.readline()


# перезаписываем рекорд убитых зомби, если счет больше
def write_record_zombi(r):
    with open('data/record_zombi.txt', 'w') as f:
        f.write(str(r))



start_screen()
pygame.mixer.music.load("data/sound/fon.mp3")
volume = 0.2
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

fon = pygame.image.load('data/img/grass.png').convert()
pygame.display.set_caption('Нашествие зомби')
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
house_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()

house = House()
player = Player()

timer = 50
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 7000)

timer_game = 0
timer_game_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_game_event, 1000)

count_game = 0
font = pygame.font.Font(None, 70)
running = True
sound = True
paused = False
while running:
    record = read_record_zombi()
    screen.blit(fon, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_m:
                sound = not sound
                if sound:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_KP_MINUS:
                volume -= 0.1
                pygame.mixer.music.set_volume(volume)
            if event.key == pygame.K_KP_PLUS:
                volume += 0.1
                pygame.mixer.music.set_volume(volume)
        if event.type == timer_event:
            timer -= 1
            x = random.randint(0, 750)
            y = random.randint(-10, 0)
            zombiecoor = Zombie(x, y)
        if event.type == timer_game_event:
            timer_game += 1
            if count_game > int(record):
                write_record_zombi(count_game)
            if  timer_game > int(record):
                write_record_time(timer_game)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.gun()

    #  спрайты
    house_group.draw(screen)
    zombie_group.draw(screen)
    player_group.draw(screen)
    bullets_group.draw(screen)
    zombie_group.update()
    player_group.update()
    bullets_group.update()

    #  конфликт пули и зомби
    conflict1 = pygame.sprite.groupcollide(zombie_group, bullets_group, True, True)
    if conflict1:
        count_game += 1
    text = font.render(f'таймер: {str(timer_game)}   счет: {str(count_game)}', True, ('red'))
    screen.blit(text, (25, 400))
    text2 = font.render(f'рекорд: {str(record)}', True, ('yellow'))
    screen.blit(text2, (500, 400))

    #  конфликт игрока и зомби
    conflict2 = pygame.sprite.spritecollide(player, zombie_group, True)
    if conflict2:
        if count_game > int(record):
            write_record_zombi(count_game)
        if timer_game > int(record):
            write_record_time(timer_game)
        game_over()

    #  конфликт дома и зомби
    conflict3 = pygame.sprite.spritecollide(house, zombie_group, True)
    if conflict3:
        if count_game > int(record):
            write_record_zombi(count_game)
        if timer_game > int(record):
            write_record_time(timer_game)
        game_over()

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
